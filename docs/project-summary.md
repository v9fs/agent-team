---
title: "v9fs: Separating Regression Mapping from Filesystem Fixes"
date: "19 October 2026"
abstract: >
  The v9fs coordination forge maps kernel, server and harness behavior before changing product code. A retained diod run had zero unexpected failures while still containing known failures and skipped tests. We explain that distinction, the pinned ownership and ACL residuals, and the evidence required for a product fix.
---

**Status:** Draft; independent report review pending.
**Distribution:** Public.
**Snapshot:** default branch [3e753717e728](https://github.com/v9fs/agent-team/commit/3e753717e728d44cf9d5a4fff088f2b5fcfca63f); clean product sources,
report-only working-tree edits. Measurements are historical, with dates and
conditions retained below.

# A known failure is not a fixed filesystem

Linux 9P filesystem testing spans a kernel client, a userspace server, mount
options and a guest harness. A failure attributed to the wrong layer can lead
to an unnecessary kernel change or a new expected-failure row that hides a
regression. The v9fs agent-team forge coordinates small changes across
`v9fs/linux` and `v9fs/test`, with product evidence coming from the named harness
rather than this forge's structure checks [1].

The default branch maps t0011 allsquash ownership and t0013 ACL/xattr behavior
at Mapped/Static proof levels. It records no integrated kernel fix.

# Architecture and current artifacts

The kernel mirror retains upstream shape, the test repository owns the guest
harness, and this forge holds pins, plans and patches. Acceptance must identify
actual product commits and harness observations.

The t0011 plan identifies a harness/server option mismatch: the runner's
ownership assertion needs diod's explicit `--squashuser` selection. Its patch
and proof row remain Static in this snapshot. Integration requires the actual
harness test to pass after the matching expected-failure rows are removed.
The t0013 ACL path is a separate claim and cannot be closed by that change [2].

# Historical regression observations

The retained September 1, 2026 record cites `v9fs/test` run 33511542559 at harness
revision `e896a9b2db1e`, building diod `de51d1ee1bd5`. The guest/server context
was arm64/arm64; the record does not specify the physical CPU model or RAM.
These are one recorded suite execution's counts, not averages, performance
measurements or a fresh check of today's upstream state [3,4].

| Suite summary field | Recorded count |
| --- | ---: |
| Total | 122 |
| Pass | 98 |
| Skip | 6 |
| Fail | 16 |
| Error | 2 |

The evaluator separately reported **unexpected: 0** with 16 FAIL lines and 16
XFAIL rows. That result means the observed failures matched the allow-list;
it does not mean the filesystem passed every test. The record attributes the
remaining FAIL/ERROR strings to t0011/t0013. Skipped assertions establish no
behavior. The selected subset excludes several diod tests, including the
t0001 case relevant to one upstream issue [3].

The historical issue inventory contains 14 open items: 11 issues and three
pull requests. None required a new machine-parsed failure line for that
captured subset. Search/listing discrepancies prompted enumeration by issue
number; that is a lesson about inventory completeness, not a current count of
upstream work [4]. The harness used floating `DIOD_REF=master`, so later runs
can build different bytes without a harness change.

An all-known-fail result detects newly unexpected failures while preserving
known defects and coverage gaps. Product proof must replace a specific XFAIL
with an actual passing assertion.

At this report's October 19 inventory, separate draft proposals describe Rust
9P mapping, a read-only virtio implementation and harness/Actions work (PRs
10–14). Those unmerged branches are not included in this default-branch result
set. Their review and product receipts require a later report refresh; draft
titles alone do not establish Rust port acceptance [5].

# Limits and next boundary

The snapshot establishes no current upstream currency, kernel fix, Rust
equivalence, performance or operational qualification. No remote harness or
current upstream issue enumeration was repeated for this report.

Next, pin kernel/server/harness revisions, reproduce the expected failure on
the predecessor or wrong option, and require PASS on the corrected candidate
with its XFAIL removed. Keep t0011/t0013 separate and retain human kernel merge
authority.

# References

1. [Project formulation and repository boundaries](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/project-formulation.md).
2. [Proof ledger](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/ledgers/proof-ledger.md) and
   [t0011 slice plan](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/plans/5-t0011-squashuser.md).
3. [Historical diod coverage report](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/reports/diod-upstream-known-fail.md).
4. [Pinned inventory ledger](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/ledgers/diod-upstream.md),
   [issue snapshot](https://github.com/v9fs/agent-team/blob/3e753717e728d44cf9d5a4fff088f2b5fcfca63f/docs/ledgers/diod-upstream-open-issues.json) and
   [original harness run](https://github.com/v9fs/test/actions/runs/33511542559).
5. [Open Rust/harness proposal PR 14](https://github.com/v9fs/agent-team/pull/14)
   and its dependency chain; state inspected 2026-10-19.
