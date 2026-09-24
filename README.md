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
