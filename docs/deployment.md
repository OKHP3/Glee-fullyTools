# Glee-fully Tools deployment contract

This repository is the source of truth for the public site at
[glee-fully.tools](https://glee-fully.tools).

## Publishing source

- **Source branch:** `main`
- **Current Pages mode:** GitHub-managed legacy branch publishing from the `main` root
- **Current handoff:** external to the visible repository workflows; the existing Pages build history is the active deployment mechanism
- **Repository-owned workflow:** prepared as `.github/workflows/deploy-pages.yml` in the deployment plan, but not installed because the available GitHub connection cannot create commits that add workflow files (`CreateCommitOnBranch` is permission-restricted)
- **Migration prerequisite:** a repository owner must enable workflow-file write access for the deployment connection, add the prepared workflow, and change the Pages source from legacy branch publishing to GitHub Actions

The managed handoff must remain in place until that prerequisite is completed. Removing or changing it before then would stop publication. This limitation is intentional and reviewable here rather than being mistaken for a source-controlled deploy.

## Artifact and paths

The published artifact is the repository root. It contains the root `index.html`, `assets/`, each public route directory, generated data files, and the committed `CNAME`. There is no bundler, framework build, or alternate output directory.

The site is served at the domain root. Existing root-relative links, asset references, and direct route directories (`/about/`, `/legal/`, and toolbox routes) are preserved exactly as authored. No base-path prefix or HTML rewrite is applied.

## Custom domain

`CNAME` is committed at the artifact root and must contain exactly:

`glee-fully.tools`

GitHub Pages custom-domain and HTTPS settings remain attached to `glee-fully.tools`. The CNAME must not be replaced with a preview or repository URL.

## Release guardrails

Run `node .agents/skills/publishing-trigger-check/audit-sites.mjs --strict --json` from the audit repository before release. A successful managed Pages run is currently required while the external handoff remains. The repository validation workflows continue to protect HTML, links, responsive layout, and sparkle behavior. Visual content, navigation, and brand tokens are not changed by this handoff.
