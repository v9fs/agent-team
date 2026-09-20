# Work Slice Plan

## Summary

- Slice: Map t0011 allsquash and t0013 ACL tip residuals as two independent
  claims with pinned kernel, diod, and harness versions
- Human outcome: an implementer can start either residual without reconstructing
  this diagnosis from chat
- Evidence version: Harness CI run 32929975795; kernel Image `kernel-latest` =
  v7.2 (`8d3ae59288f1e7d58d76558a6ee96d533bc5019f`); diod
  `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106`; harness
  `94b2182f54b30a073d893990db8f64e69f0d911a`
- Target component/API/artifact: evidence map + proof plan (no product code)
- GitHub milestone: M0 - Bootstrap
- GitHub issue: https://github.com/v9fs/agent-team/issues/1 (closed)
- GitHub PR: https://github.com/v9fs/agent-team/pull/2 (merged)
- Branch: `scaffold/1-map-tip-xfails`
- Authority level/exceptions: A2; no merge to `v9fs/linux`; no `.github` on linux
- Owner: evidence mapper (this slice)
- Independent reviewer: distinct from mapper; review the split and pins
- Date: 2026-08-31

## Scope

- In scope: pin versions; separate t0011 vs t0013; name discriminating
  observations; record non-claims; name next implementation slices
- Explicit non-claims: no kernel, diod, or harness code change; XFAIL remaining
  is not integration proof; `ghcr.io/v9fs/docker:latest` is floating
- Required dependencies: run 32929975795 logs/artifacts already diagnosed in
  `01-projects/v9fs/diod-tip-xfails-allsquash-acl.md`
- Deferred dependencies: implementation PRs in `v9fs/test` and/or `chaos/diod`
  and/or `v9fs/linux` after this mapping lands

## Backlog Context

| Rank | GitHub issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 1 | agent-team#1 | Pins + two independent claims | Unmapped → Mapped | M0; current next-action | Do not implement |
| 2 | [#5](https://github.com/v9fs/agent-team/issues/5) | t0011 squashuser vs assertion | Mapped → Integration on t0011 only | Independent of ACL | Stop if `--squashuser` trial is not decisive |
| 3 | [#6](https://github.com/v9fs/agent-team/issues/6) | t0013 ACL xattr / TMPFS_XATTR | Mapped → Integration on t0013 only | Independent of squash | Stop if in-guest local `/tmp` setfacl is not EOPNOTSUPP and not PASS |

## Evidence Map

| Source/spec/runtime/data | Version | Purpose | Constraint | Target |
| --- | --- | --- | --- | --- |
| `v9fs/linux` tag `v7.2` | `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (2026-08-16, "Linux 7.2") | Kernel in Image `kernel-v7.2` / `kernel-latest` | Mirror-only; no `.github` | E0003 |
| `v9fs/test` release `kernel-latest` | notes: "currently v7.2 / kernel-v7.2"; published 2026-08-24 | Floating Image used by Harness CI on push | Later tip Images may differ | E0004 |
| `v9fs/test` harness at run | `94b2182f54b30a073d893990db8f64e69f0d911a` (PR #26) | XFAIL eval, mount helper v12, `diod/xfail.txt` | Main later moved to `cce75243` (docs #27 only) | E0004 |
| Actions run | [32929975795](https://github.com/v9fs/test/actions/runs/32929975795) 2026-08-26 | Discriminating logs: uid 65534 vs EOPNOTSUPP 95 | `unexpected: 0`; XFAIL not a harness regression | E0005 |
| `chaos/diod` | `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` (`master` since 2026-06-23; still HEAD 2026-08-31) | t0011/t0013 source; `--allsquash` default squashuser nobody | Prepare clones `--depth 1` `DIOD_REF=master` | E0006 |
| Publish config | `linux-kernel-publish.yml` at harness SHA | `TMPFS_POSIX_ACL` on; `TMPFS_XATTR` not set | Guest `/tmp` may lack ACL xattrs | E0004 |
| Product tracker | [v9fs/test#28](https://github.com/v9fs/test/issues/28) | Human issue for residuals | Keep XFAIL until implementation slices | E0005 |

## Design

- Public interface: none (ledger + issue contract)
- Ownership/state boundaries: two residuals, two later write scopes
- Invariants: linux stays mirror-only; all CI stays in `v9fs/test`
- Failure and rollback handling: leave `diod/xfail.txt` until a slice removes rows with a PASS
- Compatibility/migration behavior: n/a
- Observability: named Actions run + diod logs in `diod-regression-logs`

## Proof Plan

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Static | `scripts/check-scaffold.sh` | Scaffold still valid after ledger edit |
| Mapped | This plan + E0003–E0006 pins | Another agent can restate both claims from git |
| Unit | not in this slice | |
| Contract/Golden | not in this slice | |
| Integration | later: named t0011 or t0013 without XFAIL | PASS for that test only |
| Operational | not claimed | |

Plausible wrong mechanism and the observation that rejects it:

> The mapping would fail if t0011 and t0013 were one harness bug, because the
> same run shows squash working (export uid 65534) while ACL walks return
> EOPNOTSUPP 95 with no `Txattrcreate`. A squashuser-only change cannot make
> t0013 PASS.

t0011 later discriminator: `--squashuser=$(id -un)` makes `exp/` ownership
match `id -u`; asserting 65534 would also pass if the test is what is wrong.
"v9fs dropped squash" is rejected by `Rgetattr uid 65534` and green t0012.

t0013 later discriminator: in-guest `setfacl` on a local `/tmp` file (not 9p).
EOPNOTSUPP ⇒ export fs / `TMPFS_XATTR`. PASS on local `/tmp` ⇒ 9p/diod xattr
path. "posixacl mount option not parsed" is rejected because `-o posixacl`
mounts and the client issues `Txattrwalk`.

## Team Orchestration

| Role | Agent/thread | GitHub issue | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | ericvh | #1 | both product repos | workflow state | ordered integration | first/last |
| Evidence mapper | this slice | #1 | linux/test/diod/CI | this forge ledgers | evidence/proof map | before code |
| Implementer | none yet | #1 | | none (no product code) | mapping only | |
| Independent reviewer | distinct | #1 | full PR | review note only | decision/findings | after mapping PR |
| CI/proof owner | v9fs/test | #1 | pipeline/proof | none this slice | run 32929975795 | already landed |
| State closer | after review | #1 | GitHub + records | state rows | landed reconciliation | last |

## Exit Criteria

- [x] Evidence, authority, dependencies, and write scopes are explicit.
- [x] Target behavior and non-claims are bounded.
- [x] Proof rejects the named plausible false positive (one-bug mapping).
- [x] Required review and approval are complete.
- [x] Follow-ups have bounded dispositions ([#5](https://github.com/v9fs/agent-team/issues/5), [#6](https://github.com/v9fs/agent-team/issues/6)).
- [x] GitHub and durable evidence agree after landing.
