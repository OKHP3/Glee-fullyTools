# FoundRy accessibility QA

## Scope

Focused browser coverage for `foundry/index.html`: page landmarks and heading structure, visible CTA names, keyboard operation of the FAQ disclosures, focus visibility, and horizontal overflow at 320px and 390px widths. This is not a replacement for the site's full validation or viewport suites.

## Evidence

- Site and stylesheet baseline: `89d5bef70e959065a9bc195481d6b755013b173e`.
  Each runner report records the tested checkout SHA.
- Tested runner revision: `9c47937a0ca1616de95440dc3813fd99be24f2f3`, run on
  2026-09-08 at 14:00 UTC: 12 PASS, 0 FAIL, 0 NOT RUN. This revision includes
  the corrected keyboard traversal and waits for stylesheet loading; the
  subsequent documentation-only commit records that result.
- Runner: [`scripts/tests/foundry-accessibility-qa.mjs`](../../scripts/tests/foundry-accessibility-qa.mjs)
- Fixture: loopback HTTP server on an ephemeral port, with third-party requests and service workers blocked. The production HTML is not rewritten on disk.
- Browser driver result on 2026-09-08: **PASS**. The bundled workspace runtime
  ran Chromium without an installation. The focused check passes at both narrow
  widths after using real keyboard Tab navigation; the mobile menu is opened
  before its links are checked, and the intentionally off-screen skip link is
  checked separately as the first keyboard target.
- Human screen-reader testing: **NOT RUN**.

## Coverage implemented

When an installed Chromium Playwright driver is available, the runner asserts:

1. The intended page title, one `h1`, and `header`, `main`, `nav`, and `footer` landmarks.
2. Heading levels do not skip forward by more than one level.
3. The four visible `.hero-actions` links have non-empty, expected accessible names.
4. A FAQ `summary` receives focus, opens with Enter, and closes with Space.
5. A complete keyboard cycle reaches every eligible link, button, and FAQ summary
   in both closed-menu and open-menu states, with a non-zero focus indicator.
   Inert, disabled, and collapsed controls are excluded by their current state.
   The skip link is the initial target and appears inside the viewport after its
   transition. Escape closes the menu and returns focus to its toggle.
6. The document does not exceed the viewport width at 320px or 390px, and no page errors occur.

## Findings and limitations

The earlier failure at 320px and 390px for the “WHY GLEE‑FULLY” navigation link
was a test-detector issue: programmatic focus included controls in the closed,
off-canvas mobile navigation and did not establish keyboard `:focus-visible`
state. The corrected runner uses keyboard navigation and passes without a
production CSS change. Both widths pass all 12 checks, covering 39 controls with
the menu closed and 50 with it open. A browser-only negative control removes
the skip link outline and shadow, verifies that the detector rejects it, then
restores its original style. The fixture resets scroll restoration for a
deterministic initial visit; this does not test every restored-scroll scenario.

The page and relationship unit tests (W01/W04) now run in Site Validation CI.
This focused browser runner remains a separate installed-driver check.

If the bundled runtime is unavailable, the runner reports `NOT RUN` rather than
weakening or skipping an assertion. Run it with the bundled Node runtime and its
already-installed Playwright package when available; do not install dependencies.
Screen-reader semantics and announcements remain unverified by this automated
check.
