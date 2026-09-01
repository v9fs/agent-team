# Proposed v9fs/test patch: diod upstream vs known-fail

Copy `xfail.txt` over `diod/xfail.txt` on `v9fs/test`. Comments only; FAIL
rows are unchanged so `v9fs-diod-regression-eval` stays `unexpected: 0`.

Do not merge this from `v9fs/agent-team`. Open a product PR when that write
scope is free. Optional follow-up in the same product PR: set
`DIOD_REF=de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` in
`scripts/v9fs-prepare-diod-regression` instead of floating `master`.
