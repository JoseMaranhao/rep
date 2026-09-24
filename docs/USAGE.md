# Using Apartment Condition Report

This guide explains how to install, run, review, and keep the output from the apartment condition reporting tool.

## What the tool produces

Each run writes the following into the output directory (by default, `condition-report/`):

```text
condition-report/
├── report.pdf        # The report to review and share after you verify it
└── evidence/         # Byte-for-byte copies of the input photos
```

The PDF contains a summary, any optional AI-proposed findings, and a photo appendix. The `evidence/` directory preserves the original files used for the report. Keep this directory with the PDF; do not edit the originals after creating your report.

## 1. Prepare photos

Create one folder containing only the apartment move-in photos.

- If photos are in **Google Photos**, download copies to your computer or add/export copies to a dedicated **Google Drive** folder first.
- Take or retain wide shots of each room plus close-ups of paint marks, dirt, stains, damage, fixtures, floors, windows, cabinets, and appliances.
- Do not rename or edit the original source photos after they are taken. The tool makes copies, but the originals and their original metadata are the strongest evidence.
- Exclude photos containing documents, people, account details, or other sensitive information before using optional AI analysis.

Supported file extensions are `.jpg`, `.jpeg`, `.png`, `.webp`, and `.heic`. A PDF photo preview may be unavailable for some formats; the original file is still retained in `evidence/`.

## 2. Install

The tool requires Python 3.11 or later.

```bash
cd /path/to/this/repository
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Run the module commands below directly from this repository. To install the optional short commands, run `pip install -e .` after installing the requirements.

## 3. Use the local browser interface (recommended)

Start the interface after installation:

```bash
python -m apartment_condition_report.web
```

Keep that terminal running, then open `http://127.0.0.1:8765` in a browser on the **same computer**. A `127.0.0.1` address is local to the computer where the command runs; it will not work when opened from GitHub, ChatGPT, or another device.

If you installed the project with `pip install -e .`, the equivalent command is `apartment-condition-report-web`. Choose a local folder (or drag photos), set a report title, and choose whether to enable AI suggestions. The downloaded ZIP contains `report.pdf` and the `evidence/` directory. The server binds only to `127.0.0.1`, so it is not accessible to other devices on your network.

## 4. Create an evidence-only report from the command line

This mode does **not** send photos to an AI provider. It creates a PDF with all input photos in the appendix but does not automatically label conditions.

```bash
python -m apartment_condition_report.cli \
  --folder /path/to/apartment-photos \
  --output condition-report \
  --title "Move-in condition report — 123 Example Street"
```

Open `condition-report/report.pdf`, check that every photo appears in the appendix, then inspect the original files under `condition-report/evidence/`.

## 5. Optionally ask AI to propose conditions from the command line

Only use this mode after deciding that sending the selected photos to your configured OpenAI account is appropriate. The model is asked to identify only clearly visible items such as paint scuffs, dirty surfaces, stains, cracks, chips, water damage, or damaged fixtures.

```bash
export OPENAI_API_KEY='your-key'
# Optional: choose a vision-capable model.
export OPENAI_VISION_MODEL='gpt-4.1-mini'

python -m apartment_condition_report.cli \
  --folder /path/to/apartment-photos \
  --output condition-report \
  --title "Move-in condition report — 123 Example Street" \
  --analyze
```

The AI output is only a list of proposed findings. It cannot determine when damage occurred, who is responsible, repair cost, or hidden conditions. Carefully verify every item against the original image and remove or correct anything inaccurate before sharing the report.

## 6. Use a Google Drive folder instead of a local folder

The tool reads Google Drive, not Google Photos directly. To use it:

1. Put copies of the desired Google Photos images into a dedicated Drive folder.
2. In Google Cloud, enable the Google Drive API.
3. Create an OAuth **Desktop app** client and download the client-secrets JSON to a secure local location. Never commit this file.
4. Copy the folder ID from the Drive URL: `https://drive.google.com/drive/folders/<FOLDER_ID>`.
5. Run:

```bash
python -m apartment_condition_report.cli \
  --drive-folder-id '<FOLDER_ID>' \
  --google-client-secrets /secure/path/client_secret.json \
  --output condition-report \
  --title "Move-in condition report — 123 Example Street"
```

A browser window opens on the first run so that you can grant read-only Drive access. The tool recursively downloads image files to `condition-report/.downloads/`, copies them to `condition-report/evidence/`, and does not modify Drive files. Add `--analyze` only if you also want the optional AI review.

## 7. Review and deliver the report

Before sending anything to a landlord:

1. Open the PDF and compare each listed finding with the original evidence file.
2. Add or correct room/location descriptions so they are precise and factual.
3. Ensure the photo appendix covers every relevant condition and that filenames are readable.
4. Keep the generated PDF, its `evidence/` folder, the original source photos, and any source metadata.
5. Send the reviewed PDF according to the move-in inspection process in your lease. Retain the sent email/message and any acknowledgement.

This tool is an evidence-organizing aid, not legal advice or a professional inspection. Local tenant-landlord rules and your lease determine what evidence and notice are required.

## Command reference

```text
python -m apartment_condition_report.cli \
  (--folder PATH | --drive-folder-id ID) \
  [--google-client-secrets PATH] \
  [--output PATH] \
  [--title TEXT] \
  [--analyze]
```

| Option | Required | Meaning |
| --- | --- | --- |
| `--folder PATH` | One source option | Local folder to search recursively for supported photos. |
| `--drive-folder-id ID` | One source option | Google Drive folder ID to search recursively. |
| `--google-client-secrets PATH` | With Drive | OAuth desktop-client JSON used for read-only Google Drive access. |
| `--output PATH` | No | Output directory; defaults to `condition-report`. |
| `--title TEXT` | No | Title printed at the top of the PDF. |
| `--analyze` | No | Sends each selected photo to the configured vision model for optional proposed findings. |

Run `python -m apartment_condition_report.cli --help` to display the command-line help.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `No supported images found.` | Confirm the selected folder contains supported image files, not only videos or unsupported formats. |
| Drive authorization fails | Confirm the Drive API is enabled, the OAuth file is a Desktop app client, and you selected the account that can access the folder. |
| PDF preview missing for a photo | Open the corresponding original in `evidence/`; that file is retained even when a PDF preview is unavailable. |
| `No module named ...` or PDF dependency error | Activate the virtual environment and run `pip install -r requirements.txt`. |
| AI analysis fails | Confirm `OPENAI_API_KEY` is set, your account can use the chosen model, and the photo is not too large for the API request. |
