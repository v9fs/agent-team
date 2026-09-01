# Work Slice Plan

## Summary

- Slice: Pin chaos/diod HEAD used by `v9fs/test` diod-regression and classify
  every open chaos/diod issue/PR against the harness known-fail list
- Human outcome: an engineer can see that our diod is current `master` HEAD
  and that outstanding diod bugs are either already outside XFAIL FAIL lines
  or explicitly not exercised
- Evidence version: chaos/diod `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106`
  (2026-06-23, still HEAD 2026-09-01); harness
  `e896a9b2db1e87dfeaaa1bb0208568469c8172c3`; Actions
  [33511542559](https://github.com/v9fs/test/actions/runs/33511542559)
- Target component/API/artifact: this forge's diod-upstream ledger + inventory
  checker; proposed comment patch for `v9fs/test` `diod/xfail.txt`
- GitHub milestone: M0 - Bootstrap (parallel to #1; does not implement t0011/t0013)
- GitHub issue: not created (token cannot POST issues); this PR is the slice
- GitHub PR: this branch
- Branch: `cursor/diod-upstream-known-fail-c9a7`
- Authority level/exceptions: A2; no merge to `v9fs/linux`; no write to
  `v9fs/test` (no push); do not edit files owned by PR #2
- Owner: evidence mapper / implementer (this slice)
- Independent reviewer: distinct from creator
- Date: 2026-09-01

## Scope

- In scope: pin diod SHA vs floating `master`; enumerate all 14 open
  chaos/diod issues/PRs; classify each vs `diod/xfail.txt` and the harness
  `TESTS=` subset; add an offline inventory checker; ship a comment-only
  product patch for later landing
- Explicit non-claims: no chaos/diod, kernel, or harness behavior change; no
  new XFAIL FAIL rows; t0011/t0013 remain `v9fs/test#28` (PR #2); Debian
  packaged diod is not in the CI matrix; `diod-9p2000.L` not claimed
- Required dependencies: public chaos/diod + v9fs/test; run 33511542559 logs
- Deferred dependencies: product PR on `v9fs/test`; copy E0007/P0003 into
  main ledgers after PR #2 lands; optional `DIOD_REF` SHA pin

## Backlog Context

| Rank | GitHub issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 1 | agent-team#1 / PR #2 | Map t0011 vs t0013 | Unmapped → Mapped | M0 first vertical | Do not implement |
| parallel | this PR | diod HEAD + upstream issues vs XFAIL | Mapped + Static | User request; disjoint from #1 files | Stop if an open diod issue actually FAILS the subset and is missing from xfail |
| later | v9fs/test product PR | Comment inventory in `diod/xfail.txt` | Static on test repo | Needs test-repo write | Do not add FAIL rows |

## Evidence Map

| Source/spec/runtime/data | Version | Purpose | Constraint | Target |
| --- | --- | --- | --- | --- |
| chaos/diod `master` | `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` | Server + sharness source | Floating `DIOD_REF=master` | E0007 |
| Open chaos/diod issues/PRs | 14 items, numbered GET 1–173 | Outstanding upstream | Search/list APIs omit non-PR issues | E0007 |
| v9fs/test xfail + subset | `e896a9b2`; run 33511542559 | Known-fail machine list | Eval ignores `#` comments | E0008 |

## Design

- Public interface: `docs/ledgers/diod-upstream.md` + JSON snapshot + checker
- Ownership/state boundaries: do not touch PR #2 paths; do not push `v9fs/test`
- Invariants: FAIL-line snapshot matches current `xfail.txt` parsed rows; every
  open issue ID is named in the ledger
- Failure and rollback handling: inventory is documentation; eval behavior unchanged
- Compatibility/migration behavior: comment-only product patch is additive
- Observability: checker fails if an open ID is dropped from the ledger

## Proof Plan

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Static | `scripts/check-scaffold.sh` | Scaffold still valid |
| Static | `scripts/check-diod-upstream-inventory.sh` | All 14 IDs present; none marked `xfail-fail-line`; FAIL snapshot has 16 t0011/t0013 rows only |
| Mapped | `docs/ledgers/diod-upstream.md` | Another agent can restate currency + dispositions without chat |
| Integration | not in this slice | Product landing on v9fs/test later |

Plausible wrong mechanism and the observation that rejects it:

> The inventory would fail if we treated GitHub search (3 open PRs) as the
> full outstanding set, because numbered GET finds 11 more open issues
> including #163 and #164. It would also fail if we added those issues as
> XFAIL FAIL lines: run 33511542559 has `unexpected: 0` with only t0011/t0013
> strings, and t0010 flock steps 21–24 PASS.

## Team Orchestration

| Role | Agent/thread | GitHub issue | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | ericvh | this PR | both product repos | workflow state | keep disjoint from PR #2 | first/last |
| Evidence mapper | this slice | this PR | chaos/diod, v9fs/test, CI | this forge diod-upstream files | inventory + checker | before product PR |
| Implementer | this slice | this PR | | this forge only | commit + verification | |
| Independent reviewer | distinct | this PR | full PR | review note only | decision/findings | after coherent PR |
| CI/proof owner | v9fs/test | run 33511542559 | pipeline | none this slice | `unexpected: 0` | already landed |
| State closer | after review | this PR | GitHub + records | state rows | landed reconciliation | last |

## Exit Criteria

- [x] Evidence, authority, dependencies, and write scopes are explicit.
- [x] Target behavior and non-claims are bounded.
- [x] Proof rejects search-only enumeration and synthetic XFAIL rows.
- [ ] Required review and approval are complete.
- [x] Follow-ups have bounded dispositions (product comment PR; ledger merge after #1).
- [ ] GitHub and durable evidence agree after landing.
