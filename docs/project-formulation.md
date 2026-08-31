# Project Formulation

Fill this before opening the first implementation issue. Delete examples that do
not fit the project rather than preserving unused process.

## Mission

- Project name: `v9fs-agent-team`
- Observable outcome: `Land proof-carrying v9fs kernel and harness slices that may change v9fs/linux, v9fs/test, or both, with linux remaining a rebase-clean mirror and regression evidence coming from the test harness`
- GitHub repository: `v9fs/agent-team`
- Default branch: `main`
- First vertical scenario: `Map the t0011 allsquash / t0013 ACL tip residuals (v9fs/test#28) to a pinned evidence boundary across diod, v9fs, and the harness so a later slice can land a fix plus a non-XFAIL assertion`

## Authority

- Default level: `A2`
- Agents may: read named evidence; create scoped issues, branches, commits, and
  draft PRs; run approved verification; update active-slice evidence.
- Human gate: merge, release, deployment, production mutation, external
  communication, destructive history change, secret handling, or wider scope.
- Exceptions: agents must not merge into `v9fs/linux`; must not add `.github`
  or other non-upstream files to `v9fs/linux`; kernel and harness merges stay
  human-gated even when this forge's process PR could be A2.

Authority levels:

| Level | Agent authority | Typical use |
| --- | --- | --- |
| A0 | Read and report only | sensitive discovery or audit |
| A1 | Create plans and draft issues | early formulation |
| A2 | Create branches, commits, draft PRs, and verification evidence | default engineering work |
| A3 | Mark ready and merge after independent approval and green gates | trusted low/medium-risk project |
| A4 | Release, deploy, or mutate external systems | explicit project-specific authority only |

## Evidence

- Source of truth: `v9fs/linux and v9fs/test (commits, issues, Actions artifacts, wiki)`
- Versioning rule: `pin product-repo commit SHAs, issue numbers, and Actions run IDs; pin this forge by merge commit on main`
- Evidence-map owner: `orchestrator`
- Evidence-map path: `docs/ledgers/evidence-map.md`
- Independent reference required for equality claims: `yes — harness result vs pinned kernel/diod/server behavior, not vs an expected constant copied into the test`

## Slicing

- Semantic unit: `one observable 9P/v9fs behavior (kernel path, harness assertion, or both)`
- Target size: `one implementer and one reviewer; write scope names linux, test, or both`
- Planned backlog horizon: `3`
- Parallelism rule: disjoint issues and disjoint write scopes across product
  repos, not only this forge
- Integration rule: predecessor must be landed unless the plan names a stable
  interface and an explicit merge order. A cross-cut slice that writes both
  product repos names linux vs test merge order.

## Proof

- Enabled levels: `mapped, static, unit, contract, integration, operational`
- Required shared gates:
  - this forge: `scripts/check-scaffold.sh`
  - product slices: the named `v9fs/test` workflow, suite, or artifact
- Required negative evidence: `FAIL or XFAIL with the wrong kernel, server, or mount option; do not treat a skipped suite as proof`
- Performance claim rule: generated, versioned measurement artifact required
- Proof-ledger owner: `CI/proof owner`

## Review

- Creator and reviewer must be distinct: `yes`
- Required approval count: `1`
- Blocking comment classes: `blocker`, decision-critical `question`
- Unresolved blocker policy: PR remains draft or changes-requested
- Human reviewer requirement: `always for v9fs/linux; risk-based for v9fs/test and this forge`
- Review authority in this edition: labels `review:*` and a review-note comment
- Native GitHub reviews / CODEOWNERS / rulesets: deferred (see `docs/HOST.md`)

## GitHub

- Milestone model: `M0 - Bootstrap, then outcome phases for mapped residuals, nightly regression, and later feature work`
- Branch pattern: `kind/<issue-number>-<short-scope>`
- Required label families: `kind`, `area`, `proof`, `status`, `review`
- Label separator: `:` (GitLab origin used `::`; keep family tokens stable)
- Optional label families: `risk`
- Area values: `linux`, `test`, `cross-cut`
- Issue/PR workflow authority: GitHub issues in `v9fs/agent-team`
- Host CLI: `gh`
- Detailed audit location: checked-in report or CI artifact, linked once
- Host edition and deferred B/C work: `docs/HOST.md`
- Org project boards: human product trackers only; not workflow authority

## Cadence

- Methodology review: every `5` landed slices or milestone close
- Early review: `2` repeated blocker/proof/infrastructure failures
- Cleanup consideration: every `10` landed slices when concrete debt exists
- Maximum operating-method changes per normal review: `1`

## Audit and Cost

- PR-local agent report: `off`
- Human steering capture: `concise GitHub comment`
- Context-boundary capture: `off`
- Token/cost accounting: `off`
- Measurement question: `not enabled until a slice fails because session cost or context loss blocked closeout`

## First Three Slices

| Rank | Issue | Outcome | Evidence boundary | Proof promotion | Predecessor | Unblocks |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [#1](https://github.com/v9fs/agent-team/issues/1) | Pin t0011/t0013 as two independent claims | E0003–E0006; run 32929975795 | Unmapped → Mapped | — | Two implementation slices |
| 2 | (open after #1 lands) | t0011: squashuser vs ownership assertion | E0005/E0006 t0011 only | Mapped → Integration | 1 | Drop matching XFAIL rows |
| 3 | (open after #1 lands) | t0013: ACL xattr / `TMPFS_XATTR` vs 9p path | E0003/E0005 t0013 only | Mapped → Integration | 1 | Drop matching XFAIL rows |

Execute only the first slice before deciding whether more process, telemetry, or
parallelism is justified.
