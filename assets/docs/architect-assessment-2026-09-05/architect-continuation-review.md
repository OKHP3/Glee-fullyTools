# Architect review of the remaining-program submission

Review date: September 5, 2026. Status: **Review in progress; one QA correction returned to the PM.**

## Submission and scope

The implementation PM submitted source commit `6f5d4d5c472c4e2bc66bf1a29e58464e692463a8` and evidence commit `b15257b6d6177b7d900a5eacd27187903f6a2567` on `codex/assessment-corrections-20260905`, at `C:/Users/jamie/.codex/worktrees/73b4/glee-fullytools`. The clean branch preserves the earlier corrective commits and PR #22; it is four commits ahead of the recorded main baseline `9b4ade05`.

The submission implements the remaining authorized local corrections and supplies prototypes and policy proposals for decisions outside that implementation scope. Its assignment register accounts for A01-A20, R01-R16, D01-D09 and G01-G08. Completing a proposal is not implementing that proposal, and neither constitutes release or live acceptance.

## Review findings

**AR01, P2: correct the reusable layout-shift measurement before full measurement acceptance.** `scripts/tests/test-experience-performance.cjs` adds every non-input layout-shift value to a field named `cls`. Current CLS is the largest session-window score, using the one-second gap and five-second window boundaries, rather than the total of all observation-window shifts. Multiple separated bursts can therefore be overstated. This is a test-instrumentation defect, not an established production regression. The raw outlier and single-shift results are not thereby disproved.

The PM has been directed to delegate the smallest correction, add synthetic burst/boundary/input-exclusion tests, preserve original reports, inspect timestamped evidence for any changed interpretation, label legacy totals where recomputation is impossible, and run one focused smoke. Broad browser sampling and production modifications are not needed for this correction. Definition: [Chrome's CLS guidance](https://web.dev/articles/cls).

No other actionable introduced production defect was identified in this review. The Architect inspected content/schema changes, significant-date evidence, governance and proposals. A separate read-only Assessment PM reviewed modal opener capture and timer cancellation, fragment focus/history/reduced motion, dark-theme selector precedence, responsive homepage image sizes, and reserved search space. That review found no introduced production blocker.

## Fresh Architect verification

| Evidence | Result |
| --- | --- |
| Unit discovery | 54 tests: 53 pass, one Windows symlink-creation skip |
| Internal links and sitemap | 63 pages; 2,719 internal links; zero broken links or style issues; 60 sitemap URLs. External links counted only |
| Generated search | Current, 60 entries |
| Cross-engine browser journeys | 13 Chromium and 13 WebKit checks pass on HEAD `b15257b6`; actual committed search JSON served, external requests and SW blocked in this fixture |
| Packaged artifact and final tar | Verified against source `6f5d4d5c`: 711 files, 63 HTML pages, 208,684,194 bytes; required hidden public files retained |
| Git preservation | Earlier accepted commits remain ancestors; clean implementation branch; whitespace check passes |

Fresh browser evidence is `C:/Users/jamie/.codex/visualizations/2026/09/05/01a07280-c6e5-7d70-8aa1-feba93994a47/architect-continuation-browser.json`. The PM's separate full 504/504 Chromium sweep, 13 rendered checks, seven packaged service-worker checks, before/after defect reproductions, date ledger and source fingerprints were reviewed as PM evidence; they are not mislabeled as new Architect runs.

## Assessment of deliverables

Content corrections replace unsupported application/pricing/screenshot assertions with canonical WebPage identities across 42 details. The catalog's 1 live, 24 beta and 17 unavailable states remain unchanged. The Showcase and public instructions better distinguish intended uses from verified external behavior. All 38 advisories have individual dispositions; the broken `#why` route is repaired. Removing unsupported assertions does not verify any external GPT.

The sitemap retains 60 URLs with 57 supported modification dates and three optional omissions. The ledger distinguishes substantive content/schema changes from cache-token maintenance and cites inspected historical diffs. The old feed remains an acknowledged limitation with a concrete maintenance proposal. It has not been silently regenerated or accepted as current.

The representative catalog prototype supplies a homepage, branch/task/status discovery and a concise detail pattern. The Architect inspected its desktop and mobile dark captures and source inventory. This establishes delivery of a reviewable design option, not production-rollout approval or proven user-task improvement. Broader adoption should use the proposed representative task study and brand/interaction review.

Platform materials provide actionable source/target promotion rules, dependency/runtime candidates, hosting options, observed-versus-desired review settings, and a local PR draft. Candidate versions and historical observations require revalidation at adoption. No sibling promotion, dependency change, hosting change, review-setting change, external PR or deployment has occurred.

## Open limits and approval boundary

Python browser CI, actual GitHub transfer, publication and live checks remain open. Installed Firefox fails before website navigation; WebKit native next-link Tab, actual browser zoom, human assistive technology, loaded Google Fonts, provider settings and field outcomes remain unverified. The lab's retained homepage shift outlier remains unattributed after six nonreproducing observations; there is no basis to erase it or claim zero homepage layout shift.

Production changes can be considered separately from the measurement correction, but full local submission acceptance is held until AR01 is reviewed. Final owner/release approval, proposal adoption and deployed-site acceptance remain distinct decisions after this local review.
