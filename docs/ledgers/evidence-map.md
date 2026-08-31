# Evidence Map

| ID | Domain | Evidence source | Version/commit/hash/date | Relevant boundary | Constraints/dependencies | Audit state | GitHub issue | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E0001 | Host edition | This repository's GitLab-origin scaffold | `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | `.gitlab/`, `.gitlab-ci.yml`, GitLab nouns in contracts | GitHub edition must keep process identical so Options B/C remain file splits | Mapped |  | Keep GitLab tree recoverable from this commit; do not mix hosts in-tree |
| E0002 | Host edition | `docs/HOST.md` | working tree | GitHub surface map, non-claims, B/C triggers | Do not start B or C inside an unrelated product slice | Designed |  | Revisit B/C only on named triggers |
| E0003 | v9fs kernel | https://github.com/v9fs/linux | tag `v7.2` = `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (2026-08-16) | Kernel in Image `kernel-v7.2` / floating `kernel-latest` | Mirror-only: no `.github` / CI in-tree; Image config enables `TMPFS_POSIX_ACL` but not `TMPFS_XATTR` | Mapped | #1 | Implementation slices must re-pin if Image moves off v7.2 |
| E0004 | v9fs harness | https://github.com/v9fs/test | run SHA `94b2182f54b30a073d893990db8f64e69f0d911a`; XFAIL list same on main `cce752431c359134fad9b0ae628bc9ecfefdc179` | `diod/xfail.txt`, mount-helper-v12, Harness CI | All regression CI lives here; docker `ghcr.io/v9fs/docker:latest` is floating | Mapped | #1 | Keep XFAIL until a slice removes rows with PASS |
| E0005 | Tip residuals | https://github.com/v9fs/test/issues/28 | Actions [32929975795](https://github.com/v9fs/test/actions/runs/32929975795) 2026-08-26; eval `unexpected: 0` | t0011 uid 65534 vs test `id -u`; t0013 `Txattrwalk` EOPNOTSUPP 95 | Two independent claims; XFAIL is not integration proof | Mapped | #1 | Open separate implementation slices after #1 lands |
| E0006 | diod | https://github.com/chaos/diod | `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` (`master` 2026-06-23; still HEAD 2026-08-31) | t0011 `--allsquash` (default squashuser nobody); t0013 `setfacl` on export | Prepare clones `--depth 1` `DIOD_REF=master`; pin SHA in later slices | Mapped | #1 | Do not treat floating `master` as a pin in implementation PRs |

Status vocabulary: `Unmapped`, `Mapped`, `Designed`, `Blocked`, `Superseded`.
