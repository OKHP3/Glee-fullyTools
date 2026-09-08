# FoundRy accessibility QA

## Scope

Focused browser coverage for `foundry/index.html`: page landmarks and heading structure, visible CTA names, keyboard operation of the FAQ disclosures, focus visibility, and horizontal overflow at 320px and 390px widths. This is not a replacement for the site's full validation or viewport suites.

## Evidence

- Source SHA: `0277324983f6db4248245fa319674b18b1878bd6`
- Runner: [`scripts/tests/foundry-accessibility-qa.mjs`](../../scripts/tests/foundry-accessibility-qa.mjs)
- Fixture: loopback HTTP server on an ephemeral port, with third-party requests and service workers blocked. The production HTML is not rewritten on disk.
- Browser driver result on 2026-09-07: **NOT RUN**. The bundled workspace runtime
  provided Playwright without an installation, but this sandbox rejected the
  ephemeral loopback listener with `EPERM` before browser assertions could run.
  A `NOT RUN` result exits with status 2, so automation cannot treat it as a pass.
- Human screen-reader testing: **NOT RUN**.

## Coverage implemented

When an installed Chromium Playwright driver is available, the runner asserts:

1. The intended page title, one `h1`, and `header`, `main`, `nav`, and `footer` landmarks.
2. Heading levels do not skip forward by more than one level.
3. The four visible `.hero-actions` links have non-empty, expected accessible names.
4. A FAQ `summary` receives focus, opens with Enter, and closes with Space.
5. Every link, button, and FAQ summary exposes a non-zero visible focus indicator.
6. The document does not exceed the viewport width at 320px or 390px, and no page errors occur.

## Findings and limitations

No rendered defect is claimed because the sandbox prevented the local-only
fixture server from starting. The runner deliberately reports that environment
boundary as `NOT RUN` rather than weakening or skipping an assertion. A later
assigned run should use an environment that permits loopback binding and record
concrete reproduction evidence for any failure. Run it with the bundled Node
runtime and its already-installed Playwright package when available; do not
install dependencies. Screen-reader semantics and
announcements remain unverified by this automated check.
