# Glee-fully Tools deployment contract

This repository is the source of truth for the public site at
[glee-fully.tools](https://glee-fully.tools).

## Publishing source

- **Source branch:** `main`
- **Current Pages mode:** GitHub Actions deployment
- **Repository-owned workflow:** `.github/workflows/pages.yml`
- **Release flow:** the workflow validates the exact `main` commit, builds a static Pages artifact, and deploys that artifact to GitHub Pages.

GitHub Pages is the sole public publishing target. Replit’s local preview workflow is for development only and does not publish the site.

## Artifact and paths

The published artifact is the repository root. It contains the root `index.html`, `assets/`, each public route directory, generated data files, and the committed `CNAME`. There is no bundler, framework build, or alternate output directory.

The site is served at the domain root. Existing root-relative links, asset references, and direct route directories (`/about/`, `/legal/`, and toolbox routes) are preserved exactly as authored. No base-path prefix or HTML rewrite is applied.

## Custom domain

`CNAME` is committed at the artifact root and must contain exactly:

`glee-fully.tools`

GitHub Pages custom-domain and HTTPS settings remain attached to `glee-fully.tools`. The CNAME must not be replaced with a preview or repository URL.

## Release guardrails

Run `node .agents/skills/publishing-trigger-check/audit-sites.mjs --strict --json` from the audit repository before release. A successful managed Pages run is currently required while the external handoff remains. The repository validation workflows continue to protect HTML, links, responsive layout, and sparkle behavior. Visual content, navigation, and brand tokens are not changed by this handoff.
