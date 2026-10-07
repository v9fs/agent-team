# Reports

Use this directory only when detailed evidence would make the human GitHub
surface harder to read.

- `agent-loops/`: optional PR-local agent, steering, context-boundary, or cost
  reports tied to a named measurement question.
- `methodology/`: evidence matrices and appendices for operating-method reviews.
- `diod-upstream-known-fail.md`: chaos/diod HEAD pin and open-issue vs XFAIL classification.
- `rust-port-inventory.md` (JSON via `--json`, gitignored): generated fs/9p + net/9p kernel surface vs
  existing Rust abstractions (`scripts/rust-port-inventory.py`; D0003).

Do not store credentials, tokens, cookies, secret-bearing session URLs, or raw
reasoning. Prefer compact, reproducible evidence and link it once from GitHub.
