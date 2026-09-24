from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import analyze_photo
from .render import build_report
from .sources import drive_photos, local_photos


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an evidence-preserving apartment condition report.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--folder", type=Path, help="Local folder containing apartment photos.")
    source.add_argument("--drive-folder-id", help="Google Drive folder ID (the text after /folders/ in its URL).")
    parser.add_argument("--google-client-secrets", type=Path, help="OAuth desktop client JSON; required with --drive-folder-id.")
    parser.add_argument("--output", type=Path, default=Path("condition-report"))
    parser.add_argument("--title", default="Apartment move-in condition report")
    parser.add_argument("--analyze", action="store_true", help="Call the configured vision model. Without it, create an evidence-only report.")
    args = parser.parse_args()
    if args.drive_folder_id:
        if not args.google_client_secrets:
            parser.error("--google-client-secrets is required with --drive-folder-id")
        photos = drive_photos(args.drive_folder_id, args.output / ".downloads", args.google_client_secrets)
    else:
        photos = local_photos(args.folder)
    if not photos:
        parser.error("No supported images found.")
    findings = [finding for photo in photos for finding in (analyze_photo(photo) if args.analyze else [])]
    report = build_report(args.title, findings, len(photos), args.output, photos)
    print(f"Wrote {report} and {args.output / 'evidence'}. Review the PDF and original evidence manually before sending it to your landlord.")


if __name__ == "__main__":
    main()
