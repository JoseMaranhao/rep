# Apartment Condition Report

Create a reviewable, evidence-preserving move-in condition report from apartment photos. It can read photos from a local folder or a Google Drive folder, copy the original evidence into the report, and—only when explicitly requested—use a vision model to propose clearly visible issues such as paint scuffs, dirty surfaces, stains, cracks, or damaged fixtures.

> **Use this as an organizing aid, not as legal advice or a professional inspection.** Review every finding against the original photo, keep originals and metadata unchanged, and share the final report with your landlord according to your lease and local rules.

## Privacy-first workflow

1. Put copies of the move-in photos in a dedicated Google Drive folder (or download them locally from Google Photos). Google Drive is used because the tool accepts a shareable folder ID and supports file download through its API.
2. Run **evidence-only mode** first. It creates a PDF report and an `evidence/` folder without sending photos to any AI provider.
3. Inspect the output. If you choose AI analysis, understand that each photo is sent to the configured model provider; do not use it for photos containing information you should not disclose.
4. Manually confirm, correct, or remove every proposed finding. Email or otherwise deliver the confirmed report promptly and keep delivery evidence.

For detailed installation, Google Drive setup, review steps, and troubleshooting, see [the usage guide](docs/USAGE.md).

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Evidence-only: no photo leaves your computer.
python -m apartment_condition_report.cli --folder /path/to/apartment-photos --output condition-report

# Optional AI-assisted review. This sends photos to your configured OpenAI account.
export OPENAI_API_KEY='...'
python -m apartment_condition_report.cli --folder /path/to/apartment-photos --output condition-report --analyze
```

Open `condition-report/report.pdf`, review its photo appendix, and manually verify the original files in `condition-report/evidence/`.

## Google Drive folder input

1. In Google Cloud, create an OAuth **Desktop app** client with the Google Drive API enabled, then download its client-secrets JSON. Do not commit it.
2. Copy the Drive folder ID from `https://drive.google.com/drive/folders/<FOLDER_ID>`.
3. Run the command below. Your browser will open so you can authorize read-only access; the tool does not upload or change Drive files.

```bash
python -m apartment_condition_report.cli \
  --drive-folder-id '<FOLDER_ID>' \
  --google-client-secrets /secure/path/client_secret.json \
  --output condition-report \
  --analyze
```

The tool recursively downloads supported image files to `condition-report/.downloads/`, embeds a working copy of every photo in the PDF appendix when its format is supported, and places copies in `condition-report/evidence/`. Keep both the Drive originals and the generated PDF/evidence folder.

## What AI analysis does—and does not—do

The optional model prompt is intentionally conservative: it requests only clearly visible conditions and excludes guesses about cause, age, responsibility, hidden damage, repair costs, people, and personal information. The report records the source filename/Drive ID with each candidate finding. A model can still miss or misdescribe conditions, so human verification is required.

## Development

```bash
python -m unittest discover -s tests -v
./scripts/check-doc-links.sh
```
