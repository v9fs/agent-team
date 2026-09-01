# diod upstream vs known-fail

Disjoint ledger for the diod-currency / known-fail inventory (this slice).
Do not edit `evidence-map.md` or `proof-ledger.md` here: PR
[#2](https://github.com/v9fs/agent-team/pull/2) owns E0003–E0006 on
`scaffold/1-map-tip-xfails`. After that lands, copy E0007 / P0003 into the
main tables.

## Evidence

| ID | Domain | Evidence source | Version | Relevant boundary | Constraints | Audit state | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E0007 | diod upstream | https://github.com/chaos/diod | HEAD `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` (2026-06-23, still HEAD 2026-09-01) | Open issues/PRs vs `v9fs/test` `diod/xfail.txt` and harness subset | GitHub list/search omits non-PR issues; enumerate by number. Harness clones `DIOD_REF=master` `--depth 1`. | Mapped | Re-pin when HEAD moves or `open_items` change |
| E0008 | harness known-fail | https://github.com/v9fs/test `diod/xfail.txt` + run [33511542559](https://github.com/v9fs/test/actions/runs/33511542559) | harness `e896a9b2db1e87dfeaaa1bb0208568469c8172c3`; eval `unexpected: 0` (16/16) | TESTS= t0010 t0011 t0012 t0013 t0020 t0021 | XFAIL rows are t0011/t0013 (`v9fs/test#28`), not chaos/diod issues. Comments in `xfail.txt` are ignored by eval. | Mapped | Land comment inventory on `v9fs/test` when that write scope is free |

## Proof

| ID | Claim | Evidence | Level | Exact proof | Non-claims | Next gap |
| --- | --- | --- | --- | --- | --- | --- |
| P0003 | diod-regression already builds chaos/diod HEAD; every open chaos/diod issue/PR is classified against the harness known-fail surface; none currently require a new machine-parsed XFAIL FAIL line | E0007, E0008 | Mapped + Static | `scripts/check-diod-upstream-inventory.sh`; run 33511542559 `unexpected: 0` | No diod or kernel fix; no new FAIL rows; Debian `apt` diod (`diod-9p2000.L`) is not in CI; floating `DIOD_REF=master` is not a SHA pin | Product PR on `v9fs/test` to copy comments into `diod/xfail.txt`; optional `DIOD_REF` SHA pin |

## Currency (2026-09-01)

- chaos/diod last push: 2026-06-23 (~70 days). Nothing newer to bump.
- Latest tag: `v1.1.0` (2025-11-02). `master` is ahead (gcc 15 fix #173).
- Harness CI built `/workspaces/tmp/diod-build-de51d1e-mount-helper-v12` on run 33511542559.
- Unused fork `v9fs/diod` last push 2022-12-04. Not used by prepare.

`scripts/v9fs-prepare-diod-regression` clones `https://github.com/chaos/diod`
`DIOD_REF=master`. That is current, but it is a floating ref, not a recorded SHA.

## Known-fail surface

`v9fs-diod-regression-eval` treats `diod/xfail.txt` as the set of allowed
FAIL/ERROR strings. Comments (`#`) are dropped. Adding synthetic FAIL rows for
issues that do not fail the subset would hide a real regression or never match.

Harness `TESTS=` subset (from `scripts/v9fs-build-initrd`):

```text
t0010-v9fs-runasuser.t
t0011-v9fs-allsquash.t
t0012-v9fs-multiuser.t
t0013-v9fs-acl.t
t0020-dbench.t
t0021-postmark.t
```

t0001–t0006, t0022–t0025, t1000 are **not** run. Current XFAIL FAIL lines are
only t0011 allsquash and t0013 ACL (`v9fs/test#28`).

## Disposition vocabulary

| Token | Meaning |
| --- | --- |
| `xfail-fail-line` | Produces a FAIL/ERROR string in the subset that belongs in `xfail.txt` |
| `subset-pass` | Exercised by the subset and PASSed on the pinned run |
| `not-in-subset` | diod has a test, harness `TESTS=` does not run it |
| `not-exercised-arch` | Needs a 32-bit server or mixed-arch errno; CI is arm64/arm64 |
| `coverage-gap` | Real report, no matching subset assertion |
| `operational` | Perf/leak/throughput; no FAIL assertion |
| `feature` / `feature-stale-pr` | Enhancement or unmerged PR, not a current FAIL |

Zero open items are `xfail-fail-line`.

## Open chaos/diod items (14)

| ID | Kind | Title | Disposition | Why the harness known-fail list does not grow |
| --- | --- | --- | --- | --- |
| [31](https://github.com/chaos/diod/pull/31) | PR | use read() for sequential reads on fd | feature-stale-pr | 2016 pread-vs-read workaround for special files. No subset FAIL. |
| [35](https://github.com/chaos/diod/issues/35) | issue | RLERROR doesn't work across architectures | not-exercised-arch | Guest and diod are both arm64. t0013 EOPNOTSUPP 95 is same-arch (`v9fs/test#28`), not this bug. |
| [53](https://github.com/chaos/diod/issues/53) | issue | Very slow over SSH port forwarding | operational | Suite uses unix sockets in-guest, not SSH. |
| [59](https://github.com/chaos/diod/issues/59) | issue | Performance bottleneck for large files | operational | No throughput gate in diod-regression. |
| [90](https://github.com/chaos/diod/issues/90) | issue | Support OFD locks? | feature | Protocol/feature request. t0010 flock PASSed (steps 21–24) on run 33511542559. |
| [91](https://github.com/chaos/diod/pull/91) | PR | Implement locking with OFD locks | feature-stale-pr | Unmerged 2022. Same as #90. |
| [138](https://github.com/chaos/diod/issues/138) | issue | add tests for Tremove/Trename | coverage-gap | Kernel prefers Tunlinkat/Trenameat. Missing diod tests, not a harness FAIL. |
| [140](https://github.com/chaos/diod/issues/140) | issue | Performance factors / low throughput | operational | No perf assertion. |
| [148](https://github.com/chaos/diod/issues/148) | issue | vsock support | feature | Harness uses virtio-9p hostshare + unix diod. |
| [162](https://github.com/chaos/diod/issues/162) | issue | possible memory leak | operational | No RSS measurement. |
| [163](https://github.com/chaos/diod/issues/163) | issue | diod_getlock EINVAL (sqlite) | coverage-gap | t0010 flock PASSed; sqlite `getlock` is a different path, not in `TESTS=`. Do not XFAIL flock. |
| [164](https://github.com/chaos/diod/issues/164) | issue | diod server: infinite loop | not-exercised-arch | 32-bit `long` truncates readdir `d_off`. CI server is arm64. |
| [165](https://github.com/chaos/diod/pull/165) | PR | WIP fix readdir on 32-bit server | not-exercised-arch | Proposed fix for #164; unmerged. Not a 64-bit FAIL. |
| [166](https://github.com/chaos/diod/issues/166) | issue | t0001 nobody exec from source tree | not-in-subset | t0001 is not in harness `TESTS=`. |

Pinned snapshot: `docs/ledgers/diod-upstream-open-issues.json`.
FAIL-line snapshot: `docs/ledgers/diod-xfail-snapshot.txt`.

## Product follow-up (v9fs/test)

This forge cannot push `v9fs/test`. Ready copy is
`docs/patches/v9fs-test-diod-upstream/`. Land comments only; do not add FAIL
rows. Optional later: pin `DIOD_REF` to `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106`
instead of floating `master`.
