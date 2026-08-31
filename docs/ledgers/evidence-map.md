# Evidence Map

| ID | Domain | Evidence source | Version/commit/hash/date | Relevant boundary | Constraints/dependencies | Audit state | GitHub issue | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E0001 | Host edition | This repository's GitLab-origin scaffold | `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | `.gitlab/`, `.gitlab-ci.yml`, GitLab nouns in contracts | GitHub edition must keep process identical so Options B/C remain file splits | Mapped |  | Keep GitLab tree recoverable from this commit; do not mix hosts in-tree |
| E0002 | Host edition | `docs/HOST.md` | working tree | GitHub surface map, non-claims, B/C triggers | Do not start B or C inside an unrelated product slice | Designed |  | Revisit B/C only on named triggers |
| E0003 | v9fs kernel | https://github.com/v9fs/linux | pin SHA per slice | Kernel v9fs paths; issues as product tracker | Mirror-only: no `.github` / CI in-tree; rebases on torvalds/linux | Mapped |  | Pin commit and issue for the active slice |
| E0004 | v9fs harness | https://github.com/v9fs/test | pin SHA and Actions run per slice | Sync, Image publish, suites, wiki, JSON/diff artifacts | All regression CI lives here; linux is checkout source | Mapped |  | Pin workflow, suite, and artifact for the claim |
| E0005 | Tip residuals | https://github.com/v9fs/test/issues/28 | open issue; pin run/log in bootstrap | t0011 allsquash ownership; t0013 POSIX ACL xattrs on guest `/tmp` | May be diod, v9fs, or harness expectation; currently XFAIL | Unmapped | bootstrap issue | Pin kernel/diod/harness versions and discriminating FAIL |

Status vocabulary: `Unmapped`, `Mapped`, `Designed`, `Blocked`, `Superseded`.
