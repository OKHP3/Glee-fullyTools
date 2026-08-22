---
name: GitHub reconciliation limits
description: Replit connector and Git transport constraints encountered when reconciling a public GitHub repository.
---

For a public GitHub repository, fetch the live branch with credential helpers disabled into a temporary ref before comparing local history. Treat the live GitHub branch—not a stale local tracking ref—as authoritative.

**Why:** The Replit GitHub connector can read and create individual Git blobs, but its Git Database tree operation is unavailable and its Contents write path can be blocked by the connector proxy. The proxy can also truncate large request bodies while returning a misleading success response. Git transport with a valid PAT remains the reliable path for publishing a complete tree.

**How to apply:** Verify blob SHAs and never advance a branch after a size-mismatched API response. Use recovery refs before rebasing or pruning. After reconciliation, a clean local `main` that is ahead of verified `origin/main` is ready for a normal fast-forward push; force-push is unnecessary unless the remote moves independently.