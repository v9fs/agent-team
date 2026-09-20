# Risk Ledger

| ID | Risk | Trigger | Impact | Mitigation | Owner | State | Closure evidence | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R0001 | GitHub labels from one family stack instead of replacing | Issue or PR carries two `status:*`, `proof:*`, or `review:*` values | Workflow state is ambiguous; closeout lies | Agents replace family values; HOST.md forbids exclusivity bots in this edition | Orchestrator | Open | Option C exclusivity helper after the named trigger, or zero collisions across five landed slices |  |
| R0002 | GitHub-native enforcement lands inside an unrelated slice | CODEOWNERS, YAML issue forms, rulesets, or native reviews become process authority without a B/C issue | Dual-host split (B) requires ripping host policy out of the process core | HOST.md non-claims; D0001 revisit triggers | Orchestrator | Open | B or C opened as its own methodology/scaffold issue, or explicit keep after review |  |
| R0003 | Floating `DIOD_REF=master` changes diod-regression without a harness pin | chaos/diod `master` moves, or a new open issue FAILS the TESTS= subset | Silent XFAIL drift or an unexpected FAIL attributed to v9fs | Inventory in `docs/ledgers/diod-upstream.md`; comment-only product patch; optional SHA pin | CI/proof owner | Open | Product PR pins SHA or inventory re-run when HEAD or open issue count changes | [#3](https://github.com/v9fs/agent-team/pull/3) / [#4](https://github.com/v9fs/agent-team/issues/4) |

Do not use this as a generic concern list. Each open risk needs a trigger,
mitigation owner, and evidence that would close or downgrade it.
