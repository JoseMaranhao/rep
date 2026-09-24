from __future__ import annotations

import hashlib
from pathlib import Path

from .models import Photo

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def local_photos(folder: Path) -> list[Photo]:
    """Return image files recursively and deterministically from a local folder."""
    if not folder.is_dir():
        raise ValueError(f"Not a readable folder: {folder}")
    return [Photo(path=p, source=str(p), evidence_filename=f"{hashlib.sha256(str(p).encode()).hexdigest()[:12]}_{p.name}") for p in sorted(folder.rglob("*")) if p.suffix.lower() in IMAGE_EXTENSIONS]


def drive_photos(folder_id: str, destination: Path, credentials_file: Path) -> list[Photo]:
    """Download images below a Google Drive folder using an installed-app OAuth flow."""
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), scopes)
    credentials = flow.run_local_server(port=0)
    service = build("drive", "v3", credentials=credentials)
    destination.mkdir(parents=True, exist_ok=True)
    photos: list[Photo] = []
    queue = [folder_id]
    while queue:
        parent_id = queue.pop(0)
        page_token = None
        while True:
            response = service.files().list(
                q=f"'{parent_id}' in parents and trashed = false",
                fields="nextPageToken, files(id,name,mimeType,createdTime)",
                pageToken=page_token,
                pageSize=1000,
            ).execute()
            for item in response.get("files", []):
                if item["mimeType"] == "application/vnd.google-apps.folder":
                    queue.append(item["id"])
                elif item["mimeType"].startswith("image/"):
                    safe_name = f"{item['id']}_{Path(item['name']).name}"
                    target = destination / safe_name
                    request = service.files().get_media(fileId=item["id"])
                    with target.open("wb") as output:
                        downloader = MediaIoBaseDownload(output, request)
                        done = False
                        while not done:
                            _, done = downloader.next_chunk()
                    photos.append(Photo(path=target, source=f"Google Drive: {item['name']} ({item['id']})", evidence_filename=safe_name))
            page_token = response.get("nextPageToken")
            if not page_token:
                break
    return photos
