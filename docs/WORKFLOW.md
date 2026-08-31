# GitHub Workflow

GitHub is the workflow authority. Checked-in artifacts preserve evidence and
decisions that should survive issue/PR closure. Host-specific paths and
deferred follow-ups are in `docs/HOST.md`.

## Milestones

Milestones are outcome phases with exit evidence, not calendar buckets.

| Milestone | Purpose | Exit evidence |
| --- | --- | --- |
| M0 - Bootstrap | Prove the team can execute and review one slice | scaffold validator and first landed PR |
| M1 - First Vertical Behavior | Establish one end-to-end route | contract or Golden proof |
| M2 - Capability Expansion | Reuse the vertical route for adjacent behaviors | integration evidence |
| M3 - Hardening | Close failure, migration, security, and operational boundaries | operational evidence |

Replace these phases when the project has a better outcome model.

## Labels

Use orthogonal labels. The family token is unchanged from the GitLab origin;
only the separator is `:` instead of `::`.

| Family | Examples | Meaning |
| --- | --- | --- |
| `kind:*` | `feature`, `bug`, `migration`, `experiment`, `cleanup`, `methodology`, `scaffold` | work type |
| `area:*` | `linux`, `test`, `cross-cut` | kernel tree, harness/CI, or both |
| `proof:*` | `none`, `mapped`, `static`, `unit`, `contract`, `integration`, `operational` | current proof level |
| `status:*` | `planned`, `active`, `blocked`, `review`, `ready`, `landed` | workflow state |
| `review:*` | `needs-independent`, `changes-requested`, `approved` | independent review state |
| `risk:*` | project-specific risk | material risk requiring filtering |

Avoid labels that duplicate assignees, milestones, or issue state. Replace a
family value on an issue or PR; do not leave two values from the same family.

## Work-Slice State Machine

```text
Planned -> Evidence Mapped -> Active -> Independent Review -> Ready -> Landed
                          \-> Blocked --------------------/
```

Only proof and review evidence advance the state. Agent confidence does not.

## Backlog and Team Orchestration

Maintain the configured dependency-ordered issue horizon. Each issue names
predecessor, unblocks, dependency/proof boundary, parallel lane, integration
order, owner, write scope, and next issue.

Before implementation:

1. Evidence mapper pins the evidence and fills the proof plan.
2. Orchestrator confirms predecessor state, authority, issue ownership, and
   write-scope separation.
3. Implementer creates `<kind>/<issue-number>-<short-scope>`.
4. Reviewer identity or independent agent role is selected before ready state.
5. CI/proof owner confirms the named verification can run.

Parallel agents work only on disjoint GitHub issues, disjoint paths, independent
review, CI diagnosis, or evidence generation. The orchestrator owns merge order.

## Issue Flow

Use `.github/ISSUE_TEMPLATE/work-slice.md`.

Before coding, the issue must include:

- evidence version and relevant source/spec/runtime/data boundary;
- target component and behavioral contract;
- current/target proof levels and exact proof;
- highest-risk review focus and plausible false positive;
- explicit non-claims;
- backlog and ownership context.

Long orchestration belongs in `docs/templates/work-slice-plan.md`.

## Branch and Pull Request Flow

Open a draft PR after the first coherent commit using
`.github/PULL_REQUEST_TEMPLATE.md`.

The creator owns implementation and evidence updates. The independent reviewer
uses `docs/templates/review-note.md` as a PR comment. Apply:

- `review:needs-independent` until a review exists;
- `review:changes-requested` while blockers remain;
- `review:approved` only after creator responses and corrected evidence.

Do not self-approve. Native GitHub review states are optional extra signal in
this edition; labels and the review note remain the process authority.

## CI and Proof Ownership

Expose proof layers rather than hiding them behind one opaque job:

```text
validate-scaffold
format-lint-build
focused-unit-contract
integration
evidence-artifact-check
```

Add a job only when the project formulation states the claim it supports.
Missing workers, flaky infrastructure, and timeouts are not product success.
Repeated manual CI recovery should become a tested helper or be removed.

## Closeout

Before merge or final handoff:

- issue and PR have milestone, orthogonal labels, and current state;
- human summary, evidence version, proof result, review focus, and non-claims are
  current;
- exact commands and results are recorded;
- independent review and creator responses are complete;
- actionable follow-ups have bounded dispositions;
- evidence, proof, decisions, experiments, and risks are updated as applicable;
- methodology trigger status and next issue are named.

After merge, the state closer performs one landed-state reconciliation before a
dependent issue starts.

## Methodology and Cleanup

Use `.github/ISSUE_TEMPLATE/methodology-review.md` and
`skills/agent-team-methodology-review/SKILL.md` at the configured cadence.

The review normally changes zero or one operating surface. It may delete or
shorten process, automate repeated work, repair a proof rule, adjust a template
or label, or select behavior-preserving cleanup. Cleanup does not advance the
feature proof claim it restructures.
