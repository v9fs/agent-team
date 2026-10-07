# Decision Log

| ID | Date | Status | Decision | Evidence | Consequence | Revisit trigger | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D0001 | 2026-08-30 | Accepted | Ship a GitHub edition (Option A): swap host surfaces, keep process identical | E0001, E0002, `docs/HOST.md` | GitLab templates/CI removed from tree; recover from `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | Need both hosts (B) or native GitHub review enforcement (C); see `docs/ledgers/decision-records/D0001-github-edition.md` |  |
| D0002 | 2026-08-31 | Accepted | Combined a-team forge for `v9fs/linux` and `v9fs/test`; do not overlay product repos or split teams | E0003, E0004, linux-mirror CI contract | Work slices live here; product PRs land in linux and/or test; area labels `linux`/`test`/`cross-cut` | Linux-only stream with no harness consequence, or test process colliding with harness CI; see `docs/ledgers/decision-records/D0002-combined-linux-test-forge.md` |  |
| D0003 | 2026-10-07 | Proposed | Rust port of fs/9p + net/9p: incremental leaf-first in `net/9p` behind Kconfig with C retained; upstream-first abstractions; transports and VFS gated on upstream | E0009, E0010, `docs/reports/rust-port-inventory.md` | No out-of-tree abstractions on the `v9fs/linux` mirror; first code slice is R1 `p9dirent_read` after harness Rust Image (R-H) | Human rejects/amends; upstream Rust VFS/netfs/virtio/socket abstractions merge; net/9p maintainers reject Rust; see `docs/ledgers/decision-records/D0003-rust-port-strategy.md` |  |

Use `docs/templates/decision-record.md` for a decision that needs alternatives
and detailed rationale.
