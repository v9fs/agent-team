# Decision Log

| ID | Date | Status | Decision | Evidence | Consequence | Revisit trigger | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D0001 | 2026-08-30 | Accepted | Ship a GitHub edition (Option A): swap host surfaces, keep process identical | E0001, E0002, `docs/HOST.md` | GitLab templates/CI removed from tree; recover from `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | Need both hosts (B) or native GitHub review enforcement (C); see `docs/ledgers/decision-records/D0001-github-edition.md` |  |
| D0002 | 2026-08-31 | Accepted | Combined a-team forge for `v9fs/linux` and `v9fs/test`; do not overlay product repos or split teams | E0003, E0004, linux-mirror CI contract | Work slices live here; product PRs land in linux and/or test; area labels `linux`/`test`/`cross-cut` | Linux-only stream with no harness consequence, or test process colliding with harness CI; see `docs/ledgers/decision-records/D0002-combined-linux-test-forge.md` |  |

Use `docs/templates/decision-record.md` for a decision that needs alternatives
and detailed rationale.
