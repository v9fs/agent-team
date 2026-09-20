# Work Slice Plan

## Summary

- Slice: Make t0013 POSIX ACL a non-XFAIL by enabling Image `TMPFS_XATTR` **and**
  mounting a native guest tmpfs on `/tmp` (hostshare `/tmp` is 9p-backed)
- Human outcome: t0013 PASSes under guest-direct diod-regression; matching
  `diod/xfail.txt` rows are gone; no loopback/ext4 trash mount
- Evidence version: mapping run 32929975795; Integration runs 35528986660 /
  35529647361 (t0013 17/17); Image publish 35525453812; product main `25d3eea`
- Target component/API/artifact: `v9fs/test` publish.yml + `v9fs-build-initrd` +
  `diod/xfail.txt` (not chaos/diod, not linux tree files)
- GitHub milestone: M0 - Bootstrap
- GitHub issue: https://github.com/v9fs/agent-team/issues/6
- GitHub PR: https://github.com/v9fs/agent-team/pull/9
- Product PR: https://github.com/v9fs/test/pull/32 (TMPFS_XATTR Image, merged) +
  https://github.com/v9fs/test/pull/33 (guest `/tmp` tmpfs + XFAIL drop, merged `25d3eea`)
- Branch: `bug/6-t0013-tmpfs-xattr`
- Authority level/exceptions: A2; no merge to `v9fs/linux`; no `.github` on linux
- Owner: implementer (this slice)
- Independent reviewer: distinct from implementer (**still required**)
- Date: 2026-09-20

## Scope

- In scope (landed product path):
  1. Discriminator: in-guest `setfacl` on a **local** `/tmp` file (hard gate in
     diod-regression init).
  2. Image: `-e TMPFS_XATTR` (+ `TMPFS_POSIX_ACL`) in publish; republish.
  3. Guest: native tmpfs mount on `/tmp` inside diod-regression chroot (decisive
     after Image alone still failed on 9p-backed `/tmp`).
  4. Drop t0013 rows from `diod/xfail.txt` after PASS.
- Explicit non-claims: t0011 squashuser; loopback/ext4 trash mount; chaos/diod
  source; `v9fs/linux` in-tree files; Debian apt diod
- Required dependencies: mapping #1 / PR #2; product tracker v9fs/test#28;
  harness write scope free of [#5](https://github.com/v9fs/agent-team/issues/5)
  / [v9fs/test#31](https://github.com/v9fs/test/pull/31) for `diod/xfail.txt`
- Deferred dependencies: none once Image + PASS land

## Backlog Context

| Rank | GitHub issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 2 | [#5](https://github.com/v9fs/agent-team/issues/5) | t0011 PASS without XFAIL | Mapped → Integration on t0011 only | Independent of ACL | Product CI green; independent review |
| 3 | [#6](https://github.com/v9fs/agent-team/issues/6) | t0013 PASS without XFAIL | Mapped → Integration on t0013 only | After #5 frees `diod/xfail.txt` | Stop if local `/tmp` setfacl PASSes (not export-fs) |

## Evidence Map

| Source/spec/runtime/data | Version | Purpose | Constraint | Target |
| --- | --- | --- | --- | --- |
| Mapping diagnosis | E0003/E0005; run 32929975795 | `Txattrwalk` EOPNOTSUPP 95; publish lacks explicit `TMPFS_XATTR` | Do not treat missing create as the bug | E0005 |
| test#31 diod log | run 35522122683 | `Rxattrcreate` + 44-byte `Twrite` succeed; `Tclunk` ecode 95; walks stay 95 | Creates issued; persist fails on export | E0005 |
| Kconfig | `fs/Kconfig` TMPFS_* | `TMPFS_POSIX_ACL` **selects** `TMPFS_XATTR` | Explicit `-e TMPFS_XATTR` still required for proof clarity and trusted/security namespaces (t0012 SKIPs) | E0003 |
| Publish workflow | `linux-kernel-publish.yml` | `-e TMPFS_POSIX_ACL` today; no `-e TMPFS_XATTR` | Image rebuild required; harness CI alone is insufficient | E0004 |
| t0012 SKIP | same guest | `missing XATTR` on local trash probe | Same root cause as t0013 FAIL (no XATTR prereq on t0013) | E0005 |

## Design

- Public interface: unchanged 9p/diod; guest `/tmp` tmpfs gains xattr+ACL
- Ownership/state boundaries: t0013 only; do not mix with t0011 prepare stamp
- Invariants: linux mirror-only (config only via publish in `v9fs/test`); no
  loop device; no ext4 image in tmpfs
- Failure and rollback handling: keep t0013 XFAIL until PASS; if discriminator
  is local PASS, do not flip TMPFS flags as the claimed fix
- Compatibility/migration behavior: republish `kernel-latest` (and matching
  versioned tag if that is the floating tip) after workflow lands
- Observability: local `/tmp` discriminator log; Image `.config` / `/proc/config.gz`
  shows `CONFIG_TMPFS_XATTR=y` and `CONFIG_TMPFS_POSIX_ACL=y`; t0013 PASS

## Proof Plan

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Static | `grep TMPFS_XATTR` in `linux-kernel-publish.yml`; forge `scripts/check-scaffold.sh` | Explicit `-e TMPFS_XATTR`; scaffold valid |
| Mapped | This plan + E0003/E0005 | Export-fs vs 9p path is an explicit choice |
| Unit | not claimed | |
| Contract/Golden | not claimed | |
| Integration | Harness CI diod-regression on [test#33](https://github.com/v9fs/test/pull/33) after Image #32 | Local `/tmp` setfacl PASS; t0013 17/17 PASS; t0013 XFAIL removed; t0011 still XFAIL |
| Operational | not claimed | |

Plausible wrong mechanism and the observation that rejects it:

> The proof would fail if the implementation used a 9p/diod xattr fix while guest
> tmpfs still lacked xattrs (or the reverse) because in-guest `setfacl` on local
> `/tmp` (not 9p) would still be EOPNOTSUPP versus PASS, and `Tclunk`/walk would
> still return 95 even though `Txattrcreate` + `Twrite` already succeeded.

Note: `TMPFS_POSIX_ACL` already `select TMPFS_XATTR`. If the live Image still
lacks xattrs, verify `TMPFS`/`TMPFS_POSIX_ACL` actually survived `olddefconfig`
before claiming “select alone was enough.” Explicit `-e TMPFS_XATTR` remains in
scope either way.

## Team Orchestration

| Role | Agent/thread | GitHub issue | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | ericvh | #6 | workflow | labels/milestone | sequence after #5 | first/last |
| Evidence mapper | #1 (landed) | #1 | ledgers | E0003–E0006 | mapping | done |
| Implementer | this slice | #6 | v9fs/test + this forge | publish.yml; xfail after PASS; this plan/ledger | product PR + draft forge PR | after #5 xfail free |
| Independent reviewer | distinct from implementer | #6 | full PRs | review note only | Mapped+Integration decision | after CI + new Image |
| CI/proof owner | v9fs/test publish + diod-regression | #6 | harness | none here | t0013 PASS on new Image | before ready |
| State closer | after review | #6 | GitHub + records | labels | landed reconciliation | last |

## Exit Criteria

- [x] Evidence, authority, dependencies, and write scopes are explicit.
- [x] Target behavior and non-claims are bounded (no loopback).
- [x] Local `/tmp` discriminator recorded before claiming the fix path.
- [x] Proof rejects the named plausible false positive (Image-only failed; guest tmpfs fixed).
- [ ] Required review and approval are complete (**distinct** independent review of this forge PR).
- [x] Follow-ups have bounded dispositions (t0011 → #5/#31).
- [x] Product GitHub and durable evidence agree after landing (`25d3eea`); forge closeout waits on review.
