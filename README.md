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
# AI Project Portfolio

A lightweight operating system for a personal GitHub account that is expected to grow from experiments into maintained products.

## Start here

1. Keep this repository as your **portfolio hub**: it explains what you are building and how you work.
2. Create each new project from the [project setup checklist](docs/project-setup-checklist.md).
3. Use the [project brief](docs/project-brief-template.md) before writing code; it prevents a prototype from becoming an undocumented commitment.
4. Capture ideas as GitHub issues using the included templates, then promote only the strongest ideas to repositories.

## Repository map

Use a small number of predictable repository types rather than one repository per thought.

| Prefix | Purpose | Lifecycle | Example |
| --- | --- | --- | --- |
| `lab-` | Time-boxed learning or technical experiments | Archive, promote, or delete quickly | `lab-rag-evaluation` |
| `proto-` | Product prototypes validated with real users or workflows | Promote or archive after a decision | `proto-meeting-copilot` |
| `tool-` | Small, durable utilities used in daily work | Maintain while it saves time | `tool-invoice-triage` |
| `product-` | A committed product with users, releases, and support expectations | Actively maintained | `product-client-portal` |
| `lib-` | Shared package, SDK, prompt, or reusable component | Versioned and documented | `lib-ai-workflows` |
| `infra-` | Shared deployment, data, or operational configuration | Restricted and carefully reviewed | `infra-home-lab` |

Use lowercase kebab-case names. State the owner, intended user, and status in every repository README.

## Suggested account structure

- **Personal account:** public learning, experiments, portfolio pieces, and small personal tools.
- **GitHub organization:** client work, collaborators, products with billing, secrets, or production infrastructure. Create one when you need team permissions or a project is no longer purely personal.
- **One repository per deployable product or independently useful tool.** Keep a prototype with its product only while they share a release cycle; otherwise separate them.
- **Private by default** for client-sensitive, credential-adjacent, or commercially exploratory work. Make a repository public deliberately after removing secrets and documenting setup.

## Workflow

```text
idea issue → short brief → lab/prototype → decision → tool/product/archive
```

Each project should have a visible status: `idea`, `active`, `maintenance`, `paused`, or `archived`. Review `lab-` and `proto-` repositories monthly. Archive projects that have not earned the cost of maintenance; preserve a short explanation in their README.

## Minimum standard for every active repository

- A README with purpose, audience, status, local setup, and deployment location.
- An explicit license (for public code) and a `.gitignore` appropriate to the language.
- A `.env.example`; never commit real credentials or production exports.
- An issue tracker with `bug`, `feature`, `idea`, `security`, and `maintenance` labels.
- A pull-request checklist and a basic automated check before merging.
- A decision log for meaningful product, model, vendor, privacy, and architecture decisions.

See [the complete setup checklist](docs/project-setup-checklist.md) and [the project brief template](docs/project-brief-template.md).

## AI-specific guardrails

- Treat prompts, evaluation cases, and model configuration as source code: version them, review changes, and keep representative test cases.
- Keep user data, API keys, and model-provider credentials out of Git. Use a secret manager or repository secrets for deployment.
- Write down where data is sent, retained, and who may access it before testing with real data.
- Add a small evaluation set before relying on an AI workflow in daily work; record known failure modes and a human fallback.
- Prefer a simple, observable workflow over autonomous behavior. Log inputs/outputs safely and add cost limits.

## Portfolio index

Add active projects below as they are created.

| Repository | Type | Status | One-line purpose | Next review |
| --- | --- | --- | --- | --- |
| _Add a repository_ | `lab` / `proto` / `tool` / `product` / `lib` / `infra` | `idea` | _What it does_ | YYYY-MM |
