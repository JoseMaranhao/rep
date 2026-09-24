"""Local-only browser interface for creating apartment condition report archives."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default
from typing import Any
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .models import Photo
from .render import build_report
from .sources import IMAGE_EXTENSIONS

STATIC_DIR = Path(__file__).with_name("static")
MAX_UPLOAD_BYTES = 300 * 1024 * 1024


def _safe_filename(filename: str, index: int) -> str:
    """Return a collision-safe filename without trusting client-side paths."""
    original = Path(filename).name or f"photo-{index}.jpg"
    digest = hashlib.sha256(f"{index}:{original}".encode()).hexdigest()[:12]
    return f"{digest}_{original}"


@dataclass(frozen=True)
class Upload:
    filename: str
    content: bytes


def _parse_multipart(content_type: str, body: bytes) -> tuple[str, bool, list[Upload]]:
    """Parse browser multipart form data without third-party web dependencies."""
    message = BytesParser(policy=default).parsebytes(f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode() + body)
    title = ""
    analyze = False
    uploads = []
    for part in message.iter_parts():
        if part.get_content_disposition() != "form-data":
            continue
        field = part.get_param("name", header="content-disposition")
        content = part.get_payload(decode=True) or b""
        if field == "title":
            title = content.decode("utf-8", errors="replace")
        elif field == "analyze":
            analyze = content.decode("utf-8", errors="replace") == "true"
        elif field == "photos":
            filename = part.get_filename()
            if filename:
                uploads.append(Upload(filename, content))
    return title, analyze, uploads


def _write_archive(title: str, uploads: list[Upload], analyze: bool) -> bytes:
    """Create a zipped PDF report and evidence folder from browser uploads."""
    with tempfile.TemporaryDirectory(prefix="apartment-report-") as temporary_directory:
        root = Path(temporary_directory)
        uploads_dir = root / "uploads"
        uploads_dir.mkdir()
        photos: list[Photo] = []
        for index, item in enumerate(uploads, start=1):
            if not item.filename:
                continue
            original_name = Path(item.filename).name
            if Path(original_name).suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            evidence_filename = _safe_filename(original_name, index)
            target = uploads_dir / evidence_filename
            target.write_bytes(item.content)
            photos.append(Photo(path=target, source=f"Uploaded file: {original_name}", evidence_filename=evidence_filename))
        if not photos:
            raise ValueError("Upload at least one supported image: JPG, JPEG, PNG, WEBP, or HEIC.")
        findings = []
        if analyze:
            from .analyze import analyze_photo
            findings = [finding for photo in photos for finding in analyze_photo(photo)]
        output = root / "condition-report"
        build_report(title or "Apartment move-in condition report", findings, len(photos), output, photos)
        archive_path = root / "apartment-condition-report.zip"
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in output.rglob("*"):
                if item.is_file():
                    archive.write(item, item.relative_to(output))
        return archive_path.read_bytes()


class AppHandler(BaseHTTPRequestHandler):
    server_version = "ApartmentConditionReport/0.1"

    def do_GET(self) -> None:  # noqa: N802
        route = urlparse(self.path).path
        pages = {"/": ("index.html", "text/html; charset=utf-8"), "/app.js": ("app.js", "text/javascript; charset=utf-8"), "/styles.css": ("styles.css", "text/css; charset=utf-8")}
        if route not in pages:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        filename, content_type = pages[route]
        content = (STATIC_DIR / filename).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/report":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > MAX_UPLOAD_BYTES:
            self._json_error("Upload must be between 1 byte and 300 MB.", HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return
        try:
            title, analyze, uploads = _parse_multipart(self.headers.get("Content-Type", ""), self.rfile.read(content_length))
            archive = _write_archive(title, uploads, analyze)
        except (RuntimeError, ValueError, ModuleNotFoundError) as exc:
            self._json_error(str(exc), HTTPStatus.BAD_REQUEST)
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", 'attachment; filename="apartment-condition-report.zip"')
        self.send_header("Content-Length", str(len(archive)))
        self.end_headers()
        self.wfile.write(archive)

    def _json_error(self, message: str, status: HTTPStatus) -> None:
        body = json.dumps({"error": message}).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Apartment Condition Report web interface.")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), AppHandler)
    print(f"Open http://127.0.0.1:{args.port} in your browser. Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
