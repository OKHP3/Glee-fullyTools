# ADR-0007: Canonical OKHP3 Static-Site Stack

## Status

Proposed

## Date

2026-09-13

## Context

Three OKHP3 sites (glee-fully.tools, askjamie.bot, overkillhill.com) were built
in parallel during August and early September 2026, primarily through ChatGPT
with some Replit. Three independent audits were run on 2026-09-09 under an
identical evidence schema, in three isolated sessions with no cross-visibility.

The audits found no runtime defects. All fifteen top-ranked defects across the
three reports were documentation and governance drift. The sites work.

They also found twenty contradictions, distributed 7 / 6 / 7. That uniformity is
the finding. A per-repository problem clusters in one repository. A rate holding
across three independently written codebases indicates a shared origin.

Two pieces of direct evidence confirm the shared origin:

- `generate-illustrations.py` exists in `scripts/archive/` in both
  overkillhill.com and glee-fully.tools at exactly 176,744 bytes.
- All three repositories contain a root `skills/` directory holding exactly one
  skill, `okhp3-skill-promotion`, byte-identical to its `.agents/skills/`
  counterpart, while 55 to 66 sibling skills have no mirror.

These repositories were cloned from a common pattern, and the pattern carries
its defects forward. Repairing one repository does not repair the other two.

The audits also measured toolchain divergence that nothing in the three sites
requires: three dev-server invocations for one job, two browser-automation
libraries where one suffices, three Node versions (one of which conflicts with
itself between CI and local config), and two deploy-action majors.

## Decision Drivers

- **Must be checkable, not just written** — AGENTS.md already drifted from
  `viewport-qa.yml`. An unenforced standard becomes another contradiction.
- **Must not need the toolchain it checks** — the conformance check has to run
  in a fresh clone, before `npm ci`.
- **Must preserve legitimate per-site difference** — overkillhill.com has a real
  content pipeline; flattening it would destroy working capability.
- **Should reduce authority surfaces** — two overlapping instruction files is
  how a contradiction is born and then never noticed.
- **Should prefer deletion over documentation** — 142 retired scripts across
  three repos are already preserved by git history.

## Considered Options

### Option A: Converge on this repository's shape (chosen)

- **Pros**: Most of these values are already this repository's values. It
  carries six ADRs, a dependency policy, a CI action-version policy, a lifecycle
  document, pinned Node, and the newer deploy action.
- **Cons**: Two sibling repositories absorb the migration cost.

### Option B: Clean each site independently

- **Pros**: No cross-repository coordination.
- **Cons**: Performs the same seven fixes three times and leaves the pattern
  intact, so a fourth repository inherits all of it.

### Option C: Adopt askjamie.bot as the reference

- **Pros**: Strongest verification evidence of the three; the only audit that
  executed its own gates.
- **Cons**: Carries a Node 24-versus-20 self-conflict and 124 MB of committed
  release artifact.

### Option D: Copy the standard into each repository as prose

- **Cons**: Reproduces the original failure. Three copies of a standard drift
  into three standards.

## Decision

Adopt a single canonical stack across the three sites, with this repository as
the reference implementation, enforced by `scripts/check-stack-conformance.py`
in CI.

| Layer | Standard |
|---|---|
| Node | 22.19.0, pinned in `.node-version` and `package.json` `engines` |
| Browser automation | Playwright, exact pin `1.60.0`. Puppeteer removed |
| Lighthouse | Exact pin `13.4.1` |
| Python QA | `requirements-qa.txt` pinning `beautifulsoup4==4.15.0` and `playwright==1.60.0`; `Pillow==12.3.0` only where an image pipeline exists |
| Dev server | `scripts/serve-site.py`, identical filename in every repository |
| Deploy | `actions/deploy-pages@v5` |
| Skill store | `.agents/skills/` only. Root `skills/` does not exist |
| Agent instructions | `AGENTS.md` canonical; `CLAUDE.md` a pointer under 512 bytes; `replit.md` does not exist |
| Retired scripts | Deleted. Git history is the archive |
| Generated output | `.gitignore` covers `__pycache__/` and `*.pyc` always, and `assets/audit/` or `dist-pages/` where those directories exist |

Exact version pins follow `docs/dependency-policy.md` rather than caret ranges.

The build step stays site-specific and is explicitly out of scope. This ADR
standardizes the QA, deployment, and governance layers only.

Documented exceptions live in `.stack-conformance.json` at the repository root
and are always reported by the checker, never hidden.

## Consequences

### Positive

- One toolchain to learn, upgrade, and patch instead of three.
- A new OKHP3 site starts from a pattern with these defects already removed.
- Dependency upgrades become one decision applied three times.
- Each repository keeps one authority file, removing the most productive source
  of contradictions the audits found.
- Repository size drops materially in the sibling repositories.

### Negative

- overkillhill.com downgrades Playwright from 1.62.1 to 1.60.0, a deliberate
  step backward for consistency.
- Deleting `replit.md` risks losing operating knowledge not present in
  `AGENTS.md`.
- `check-stack-conformance.py` is new code in three repositories, and new code
  is new maintenance.

### Mitigations

- The Playwright downgrade is validated by running the affected tests before
  and after, not assumed safe.
- `replit.md` is diffed against `AGENTS.md` and anything unique merged before
  deletion; it is never deleted first.
- The checker is standard library only and has no dependencies to maintain.
- `--fix` repairs only mechanical items. It untracks files with
  `git rm -r --cached` and never deletes from disk, so every repair is
  reversible.
