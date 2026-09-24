# New repository setup checklist

Use this checklist after creating a repository from the naming scheme in the root README.

## Before the first commit

- [ ] Choose a descriptive prefix and kebab-case repository name.
- [ ] Write `README.md` with purpose, audience, status, setup, and a screenshot/demo when applicable.
- [ ] Add `docs/project-brief.md` from the [brief template](project-brief-template.md).
- [ ] Add a license for public repositories; confirm the license supports your intended use of dependencies and models.
- [ ] Add `.gitignore`, `.env.example`, and a dependency lockfile where the ecosystem supports one.
- [ ] Confirm no secrets, real customer data, or generated private artifacts are in Git history.

## GitHub configuration

- [ ] Set repository visibility deliberately and add a concise description and topics.
- [ ] Enable issue tracking and add labels: `bug`, `feature`, `idea`, `security`, `maintenance`, `good first issue`.
- [ ] Use the included issue forms and pull-request template (copy `.github` from this repository).
- [ ] Protect the default branch once the repository is active: require pull requests and passing checks.
- [ ] Enable Dependabot/security alerts when the repository has dependencies.
- [ ] Add collaborators through an organization and least-privilege teams when the project has more than one person.

## Before first real user or production data

- [ ] Document data flow, retention, and access controls.
- [ ] Store production secrets in the deployment platform or GitHub Actions secrets, not in files.
- [ ] Add a health check, error reporting, and a way to disable risky AI actions.
- [ ] Add a small regression/evaluation set and a manual review path.
- [ ] Record hosting, domain, backups, owner, and monthly cost in the README or decision log.

## Monthly review

- [ ] Review open issues, costs, credentials, dependencies, and automation failures.
- [ ] Decide whether each lab/prototype should be promoted, paused, or archived.
- [ ] Archive completed experiments with a final README note and links to any successor repository.
