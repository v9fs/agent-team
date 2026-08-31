# v9fs Agent Team

> Generated as an A-Team project from `ericvh/github-agentic-team-template`.
> The `template` remote preserves the source scaffold; `origin` is
> `git@github.com:v9fs/agent-team.git`.

Linux 9P/v9fs work already splits across two public trees: `v9fs/linux` is a
rebase-clean mainline mirror, and `v9fs/test` owns sync, Image publish, harness
CI, and the wiki status table. Putting an agent-team scaffold into either
product repo would either fight upstream rebases or mix process contracts with
harness CI. This repository is the combined coordination forge: one
proof-carrying backlog for issue fixes and later development that may land in
linux, test, or both.

## Three-repo split

| Repo | Role | Hosts a-team scaffold? |
| --- | --- | --- |
| [`v9fs/linux`](https://github.com/v9fs/linux) | Kernel source mirror. Product PRs for v9fs. No `.github`. | No |
| [`v9fs/test`](https://github.com/v9fs/test) | Sync, kernel Image publish, regression suites, wiki, artifacts | No |
| **`v9fs/agent-team` (this)** | Work-slice issues, evidence, proof, independent review, methodology | Yes |

Existing org boards ([roadmap](https://github.com/orgs/v9fs/projects/2),
[Test Infrastructure](https://github.com/orgs/v9fs/projects/4),
[Edgentic](https://github.com/orgs/v9fs/projects/5)) remain human product
trackers. They are not workflow authority. Issues and PRs in this repository
are.

A slice names `area:linux`, `area:test`, or `area:cross-cut`. Implementation
PRs land in the product repo(s) named by the write scope. This repo's own PRs
are process, evidence, and skills unless a slice explicitly says otherwise.

## Core Model

```text
Done = implemented
   AND proven
   AND independently reviewed
   AND integrated
   AND durable state synchronized
```

The team has six responsibilities:

1. The orchestrator owns backlog order, authority, and integration.
2. The evidence mapper pins sources and defines the proof plan.
3. Each implementer owns one issue and one disjoint write scope.
4. An independent reviewer tests the claim and highest-risk boundary.
5. The CI/proof owner keeps verification executable and separates
   infrastructure failures from product failures.
6. The state closer reconciles GitHub and checked-in evidence after landing.

One agent may hold several responsibilities across a project, but a slice's
creator and independent reviewer must be distinct.

## Start here

1. Read [AGENTS.md](AGENTS.md) and [docs/project-formulation.md](docs/project-formulation.md).
2. Use [docs/ledgers/decision-records/D0002-combined-linux-test-forge.md](docs/ledgers/decision-records/D0002-combined-linux-test-forge.md) for the combined-repo rule.
3. Run `scripts/check-scaffold.sh`.
4. Open work from the `Work Slice` issue template. Do not start implementation
   until evidence is pinned.
5. Land product changes in `v9fs/linux` and/or `v9fs/test`. Close the slice here
   only after proof, independent review, and durable state match.

## Repository Surfaces

| Surface | Purpose |
| --- | --- |
| `AGENTS.md` | Repository-wide mission, authority, roles, proof, and closeout contract |
| `.github/` | Human-first issue and pull-request templates, plus Actions |
| `docs/HOST.md` | GitHub edition mapping and deferred host follow-ups |
| `docs/HUMAN_SURFACE.md` | Separates engineering narrative from audit telemetry |
| `docs/WORKFLOW.md` | GitHub lifecycle, labels, milestones, and team orchestration |
| `docs/PROOF_MODEL.md` | Project proof ladder and discriminating evidence rules |
| `docs/ledgers/` | Evidence that cannot be reconstructed reliably from GitHub |
| `docs/templates/` | Detailed plans, reviews, and decision records |
| `skills/` | Narrow project-local agent workflows |
| `scripts/check-scaffold.sh` | Deterministic scaffold validation |

## Default GitHub Labels

```text
kind:<feature|bug|migration|experiment|cleanup|methodology|scaffold>
area:<linux|test|cross-cut>
proof:<none|mapped|static|unit|contract|integration|operational>
status:<planned|active|blocked|review|ready|landed>
review:<needs-independent|changes-requested|approved>
risk:<project-specific-risk>
```

GitHub labels are flat. Replace a family value rather than stacking siblings.
Do not add exclusivity automation in this edition.

## Default Cadence

- Keep a dependency-ordered horizon of three to five planned issues.
- Review methodology after five landed slices or at milestone close.
- Trigger early review after two repeated blocker or proof-failure families.
- Consider a behavior-preserving cleanup after ten landed slices when the code
  shows concrete structural debt.

These are starting values. Change them to fit project risk and cycle time.

## Validation

```bash
scripts/check-scaffold.sh
git diff --check
```

Product proof for a kernel or harness slice is the named `v9fs/test` workflow,
wiki table, or artifact — not this repository's scaffold job.

## Provenance

This GitHub edition preserves the operating pattern of the GitLab agentic team
template at commit `2b581184d08daed1d0f0b9611fbafbaa0f24e278`.
That scaffold generalizes the pattern observed in the internal `gem5-rs` project
at commit `adf246c7055fab821dde166ba23a5cd0161e12b3`. It deliberately does not
copy the project's approximately-1,000-line audit budget, full telemetry
machinery, or port-specific parity vocabulary as universal requirements.
