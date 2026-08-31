# v9fs Agent Team Guide

## Mission

Land proof-carrying v9fs kernel and harness slices — issue fixes and later
feature work — that may change `v9fs/linux`, `v9fs/test`, or both. Linux stays
a rebase-clean mainline mirror with no CI surface. Regression evidence comes
from the test harness (Actions, wiki table, JSON/diff artifacts). Authoritative
evidence begins at `v9fs/linux` and `v9fs/test` (commits, issues, and Actions
artifacts).

GitHub repository: `v9fs/agent-team`.

## Agent Fast Path

1. Inspect `pwd` and `git status --short --branch`.
2. Read this guide, the active GitHub issue, and the narrowest project skill.
3. Read `docs/HUMAN_SURFACE.md`, `docs/WORKFLOW.md`, `docs/HOST.md`, and the
   relevant evidence, proof, decision, experiment, and risk rows.
4. Confirm authority, issue ownership, predecessor state, write scope, evidence
   version, current proof level, target proof level, and independent reviewer.
5. Work on one semantic slice. Preserve unrelated work and do not widen scope
   silently.
6. Run the narrowest discriminating proof, then the required shared gates.
7. Obtain independent review before ready or merge state.
8. After landing, reconcile GitHub and durable project evidence before starting
   the next dependent issue.

## Authority Contract

Default authority level: `A2`.

Agents may:

- read the repository and evidence sources named by the active issue;
- create scoped issues, branches, commits, and draft pull requests;
- run project-approved verification;
- update project-local evidence and workflow artifacts for the active slice.

Human approval is required for:

- merging unless the project formulation explicitly grants `A3`;
- releases, deployments, production writes, or external communication;
- destructive history changes, secret handling, or materially wider scope.
- merging patches into `v9fs/linux`;
- writing `.github` or any non-upstream file into `v9fs/linux`.

A request to finish or continue does not imply broader authority.

## Human Surface Contract

GitHub is the durable coordination surface. Issues and pull requests lead with:

1. the human goal and why it is next;
2. the versioned evidence anchor;
3. the component or behavior changed;
4. the proof promotion and exact result;
5. the highest-risk review focus;
6. behavior explicitly outside the claim.

Agent ids, transcripts, session paths, token tables, raw runner logs, and long
evidence appendices belong in checked-in reports or job artifacts. Link them
once from the pull request when they answer a real audit question.

## Team Contract

- The **orchestrator** owns dependency order, authority, issue assignment,
  branch/PR integration, and conflict resolution.
- The **evidence mapper** pins sources, constraints, prior behavior, risks, and
  the proof plan before implementation.
- An **implementer** owns one GitHub issue and one disjoint write scope.
- The **independent reviewer** is distinct from the creator and reviews the
  stated claim, highest-risk boundary, and proof sufficiency.
- The **CI/proof owner** keeps verification executable and distinguishes
  infrastructure failure from product failure.
- The **state closer** reconciles landed code, issue/PR state, evidence, proof,
  decisions, experiments, risks, and bounded follow-ups.

Parallel agents must own disjoint issues and disjoint write scopes. If two
implementers need the same file, the orchestrator must sequence them or land an
interface split first.

Write scope is a product-repo path set, not only a path in this forge. Two
active slices must not both write `v9fs/linux` or both write the same
`v9fs/test` harness surface.

## Backlog Contract

GitHub is the backlog. Maintain a short dependency-ordered horizon configured in
`docs/project-formulation.md`. Each active or planned slice names:

- predecessor and what it unblocks;
- dependency and proof boundary;
- parallel lane and integration order;
- next issue;
- owner and write scope.

Do not use private chat plans as the only backlog. Do not manufacture speculative
issues merely to satisfy the horizon.

Public `v9fs/linux` and `v9fs/test` issues remain product trackers and evidence
sources. They are not a second agent backlog. Link them from the work slice.

## Slice Contract

Each non-trivial issue represents one proof-carrying semantic slice:

```text
one dependency boundary
+ one coherent behavior change
+ one observable proof promotion
+ one independent review
+ one synchronized closeout
```

A slice is correctly sized when one implementer can explain its behavioral
contract, one reviewer can inspect its highest risk, and one proof suite can
demonstrate the claim without implying broader behavior.

## Evidence and Proof Contract

- Pin evidence by commit, version, timestamp, dataset hash, or captured runtime
  artifact before claiming coverage.
- Separate evidence coverage from behavioral proof.
- Compilation is static evidence, not runtime proof.
- Derive equality or success from observed implementation behavior and an
  independently obtained reference; do not emit expected constants as if they
  were measurements.
- Name a discriminating observation that would fail for a copied constant,
  stale owner, clone, wrong order, silent fallback, widened parser, partial
  migration, or synthetic success path.
- Widened input/state surfaces require source-backed positive semantics plus
  negative rejection or failure evidence.
- Performance and operational claims require generated measurement artifacts.
- Record skipped checks and the reason.

Use the proof ladder in `docs/PROOF_MODEL.md` and the exact project selection in
`docs/project-formulation.md`.

Kernel Image build success is static. A named harness suite in `v9fs/test` is
integration. Relative comparison against the prior newest v6+ tag is
operational and only when the slice claims it.

## Review Contract

No self-approval. Review comments classify landing impact:

- `blocker:` must change before merge because correctness, safety,
  compatibility, data loss, security, rollback, or proof is at risk;
- `question:` context required before deciding;
- `suggestion:` useful non-blocking improvement;
- `nit:` optional local polish;
- `praise:` a specific engineering choice worth retaining.

Every blocker needs a concrete landing path. The creator responds with changed
code or evidence. An actionable suggestion is implemented, linked to a GitHub
issue with an exact reconsideration trigger, or explicitly declined/superseded.
The pull request remains draft or `review:changes-requested` while blockers or
decision-critical questions remain unresolved.

## GitHub Contract

- Milestones are outcome phases with explicit exit evidence.
- Use the label families defined in `docs/WORKFLOW.md`.
- Create issues and PRs from the templates under `.github/`.
- Branches use `<kind>/<issue-number>-<short-scope>`.
- Comments are sparse: planning change, proof update, independent review,
  creator response, human steering that changes the contract, and final
  closeout.
- The GitHub issue/PR state is authoritative for workflow state. Checked-in
  ledgers preserve domain evidence and must not silently contradict GitHub.
- Host-specific paths, CLI, and deferred dual-host or GitHub-native work live
  in `docs/HOST.md`. Do not add host enforcement in an unrelated slice.
- Product PRs live in `v9fs/linux` and/or `v9fs/test`. Link them from the slice
  issue in this repository.

## Methodology Contract

Use `skills/agent-team-methodology-review/SKILL.md` after the configured landed
slice count, at milestone close, or early when the same blocker, proof failure,
state drift, human-surface failure, or manual recovery repeats.

A methodology review answers each question from named evidence and chooses
`keep`, `delete`, `automate`, or `change`. Normally make zero or one operating
method change. Prefer deleting or automating friction over adding prose.

Every methodology gap must identify the surface that failed: this guide, a
skill, script, template, CI job, GitHub convention, or ledger.

## Closeout Contract

Before final reporting, name:

- exact verification commands and results;
- issue/PR state and independent review decision;
- evidence and proof movement;
- decisions, experiments, risks, and follow-ups updated;
- methodology trigger status;
- the next dependency-ordered GitHub issue.

The next agent must be able to resume from GitHub and checked-in evidence without
reconstructing the previous session from chat.
