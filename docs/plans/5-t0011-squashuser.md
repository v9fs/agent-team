# Work Slice Plan

## Summary

- Slice: Make t0011 allsquash a non-XFAIL ownership assertion by passing
  `--squashuser=$(id -un)` in the `v9fs/test` diod prepare patch
- Human outcome: t0011 PASSes under guest-direct diod-regression; matching
  `diod/xfail.txt` rows are gone; t0013 is untouched
- Evidence version: mapping run 32929975795; kernel Image `kernel-latest` =
  v7.2 (`8d3ae59288f1e7d58d76558a6ee96d533bc5019f`); diod
  `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106`; harness after klog #30
- Target component/API/artifact: `v9fs/test` `scripts/v9fs-prepare-diod-regression`
  + `diod/xfail.txt` (not chaos/diod, not linux)
- GitHub milestone: M0 - Bootstrap
- GitHub issue: https://github.com/v9fs/agent-team/issues/5
- GitHub PR: https://github.com/v9fs/agent-team/pull/8
- Product PR: https://github.com/v9fs/test/pull/31 (`v9fs/test`)
- Branch: `bug/5-t0011-squashuser`
- Authority level/exceptions: A2; no merge to `v9fs/linux`; no `.github` on linux
- Owner: implementer (this slice)
- Independent reviewer: distinct from implementer
- Date: 2026-09-20

## Scope

- In scope: t0011 `--allsquash` plus `--squashuser=$(id -un)`; drop t0011 XFAIL
  rows when CI PASSes
- Explicit non-claims: t0013 ACL; kernel squash rewrite; chaos/diod source;
  Debian apt diod; `DIOD_REF` SHA pin (deferred)
- Required dependencies: mapping #1 / PR #2; product tracker v9fs/test#28
- Deferred dependencies: t0013 (#6); optional `DIOD_REF` SHA pin

## Backlog Context

| Rank | GitHub issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 2 | [#5](https://github.com/v9fs/agent-team/issues/5) | t0011 PASS without XFAIL | Mapped → Integration on t0011 only | Independent of ACL | Stop if `--squashuser` trial is not decisive (export still 65534 or t0012 fails) |
| 3 | [#6](https://github.com/v9fs/agent-team/issues/6) | t0013 ACL | Mapped → Integration on t0013 only | After t0011 write scope is free | Do not mix with this PR |

## Evidence Map

| Source/spec/runtime/data | Version | Purpose | Constraint | Target |
| --- | --- | --- | --- | --- |
| Mapping diagnosis | E0005/E0006; run 32929975795 | Squash works (`Rgetattr uid 65534`); test expects `$(id -u)` | Do not treat “v9fs dropped squash” as the fix | E0005 |
| `t0011-v9fs-allsquash.t` | chaos/diod `de51d1ee` | `--allsquash` without `--squashuser`; asserts exp/ == `id -u` | Later create/chmod steps also assume runner is squashuser | E0006 |
| Harness prepare | `v9fs-prepare-diod-regression` stamp `t0011-squashuser-v1` | Patch `--squashuser=$(id -un)` only | Do not change t0013 | E0004 |

## Design

- Public interface: unchanged diod CLI; harness injects squashuser
- Ownership/state boundaries: t0011 only; t0013 XFAIL rows stay
- Invariants: linux mirror-only; allsquash still squashes (t0012 remains green)
- Failure and rollback handling: restore t0011 XFAIL rows if diod-regression FAIL
- Compatibility/migration behavior: n/a
- Observability: diod-regression eval `unexpected: 0` with no t0011 FAIL lines

## Proof Plan

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Static | `grep -- '--squashuser=$(id -un)'` after prepare; `scripts/check-scaffold.sh` on forge | Patch present; scaffold valid |
| Mapped | This plan + E0005/E0006 | `--squashuser` vs assert-65534 is an explicit choice |
| Unit | not claimed | |
| Contract/Golden | not claimed | |
| Integration | Harness CI `diod-regression` on the product PR | t0011 PASS; no t0011 XFAIL rows; t0013 still XFAIL; t0012 still PASS |
| Operational | not claimed | |

Plausible wrong mechanism and the observation that rejects it:

> The proof would fail if the implementation used “v9fs dropped squash” as the
> fix because t0011 export `Rgetattr uid 65534` and green t0012 would not match
> that story, while `exp/` would still be 65534 unless `--squashuser=$(id -un)`
> or the assertion is changed. Changing the assertion *and* squashuser at once
> would lose the discriminator.

## Team Orchestration

| Role | Agent/thread | GitHub issue | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | ericvh | #5 | workflow | labels/milestone | sequence vs #6 | first/last |
| Evidence mapper | #1 (landed) | #1 | ledgers | E0003–E0006 | mapping | done |
| Implementer | this slice | #5 | v9fs/test + this forge | `v9fs/test` prepare/xfail; this plan/ledger | product PR + draft forge PR | |
| Independent reviewer | distinct from implementer | #5 | full PRs | review note only | Mapped+Integration decision | after CI |
| CI/proof owner | v9fs/test diod-regression | #5 | harness | none here | t0011 PASS | before ready |
| State closer | after review | #5 | GitHub + records | labels | landed reconciliation | last |

## Exit Criteria

- [ ] Evidence, authority, dependencies, and write scopes are explicit.
- [ ] Target behavior and non-claims are bounded.
- [ ] Proof rejects the named plausible false positive.
- [ ] Required review and approval are complete.
- [ ] Follow-ups have bounded dispositions.
- [ ] GitHub and durable evidence agree after landing.
