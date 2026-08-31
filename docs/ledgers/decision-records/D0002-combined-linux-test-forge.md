# Decision Record

- ID: D0002
- Date: 2026-08-31
- Status: Accepted
- Decision: One combined GitHub a-team repository coordinates `v9fs/linux` and
  `v9fs/test`. Do not overlay the scaffold onto either product repo, and do
  not split into per-repo agent teams.

## Context

v9fs maintainer work already cuts across two public trees. `v9fs/linux` is a
torvalds/linux mirror that must stay rebase-clean, so it cannot grow `.github`
workflows or a-team templates. `v9fs/test` already owns cron-sync, Image
publish, harness CI, and wiki reporting. Kernel fixes are not done until a
harness assertion exists; harness work is not done until it is pinned to a
linux ref. Two agent-team backlogs would split that loop.

## Options

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Combined forge (`v9fs/agent-team`) | One proof-carrying backlog; area labels for linux/test/cross-cut; linux stays mirror-only | Work-slice issues live here, product PRs live elsewhere; agents must name write scope across repos |
| B. Overlay scaffold onto `v9fs/test` | Fewer repositories | Mixes process contracts with harness CI; linux-only slices have no natural home; does not help linux issues |
| C. Separate a-team repos per product tree | Appears to match repo boundaries | Every realistic fix becomes two slices; duplicate labels/milestones; linux still cannot host the scaffold |
| D. GitHub Projects only (no scaffold repo) | Reuses org boards #2/#4/#5 | Boards are not proof-carrying; HOST.md treats Projects as non-authority; no work-slice template or ledgers |

## Outcome

A won. The semantic unit is one observable 9P/v9fs behavior, not one git
repository. Org boards stay as human product trackers. This repository is
workflow authority for agent slices.

## Verification

```bash
scripts/check-scaffold.sh
git diff --check
```

Discriminating observation: `AGENTS.md` and `docs/project-formulation.md` name
both product repos, forbid `.github` on linux, and set area values to
`linux` / `test` / `cross-cut`. A linux-only or test-only scaffold would not
need that split.

## Revisit When

- A linux-only stream of work has no harness consequence for several landed
  slices.
- `v9fs/test` process files start colliding with harness CI ownership.
- Dual-host (GitLab) coordination is required; then follow `docs/HOST.md`
  Option B rather than splitting linux vs test.
