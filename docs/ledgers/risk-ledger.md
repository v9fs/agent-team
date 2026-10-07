# Risk Ledger

| ID | Risk | Trigger | Impact | Mitigation | Owner | State | Closure evidence | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R0001 | GitHub labels from one family stack instead of replacing | Issue or PR carries two `status:*`, `proof:*`, or `review:*` values | Workflow state is ambiguous; closeout lies | Agents replace family values; HOST.md forbids exclusivity bots in this edition | Orchestrator | Open | Option C exclusivity helper after the named trigger, or zero collisions across five landed slices |  |
| R0002 | GitHub-native enforcement lands inside an unrelated slice | CODEOWNERS, YAML issue forms, rulesets, or native reviews become process authority without a B/C issue | Dual-host split (B) requires ripping host policy out of the process core | HOST.md non-claims; D0001 revisit triggers | Orchestrator | Open | B or C opened as its own methodology/scaffold issue, or explicit keep after review |  |
| R0003 | Floating `DIOD_REF=master` changes diod-regression without a harness pin | chaos/diod `master` moves, or a new open issue FAILS the TESTS= subset | Silent XFAIL drift or an unexpected FAIL attributed to v9fs | Inventory in `docs/ledgers/diod-upstream.md`; comment-only product patch; optional SHA pin | CI/proof owner | Open | Product PR pins SHA or inventory re-run when HEAD or open issue count changes | [#3](https://github.com/v9fs/agent-team/pull/3) / [#4](https://github.com/v9fs/agent-team/issues/4) |
| R0004 | Rust port work carries out-of-tree kernel abstractions on `v9fs/linux` | A Rust slice needs a VFS/netfs/virtio/socket abstraction not in mainline | Mirror stops being rebase-clean; v9fs owns kernel-wide APIs without their maintainers | D0003 gates R5/R6 on upstream merges; inventory rerun per tag | Orchestrator | Open | D0003 accepted with gates, or rejected | D0003 |
| R0005 | Rust slices collide with another slice holding the linux Image config | R-H starts while #6 may change the Image config (`TMPFS_XATTR`) | Two slices write the same Image config surface | Sequence R-H after #6 frees that scope | Orchestrator | Open | #6 landed or explicitly confirms no Image change | [#6](https://github.com/v9fs/agent-team/issues/6) |

Do not use this as a generic concern list. Each open risk needs a trigger,
mitigation owner, and evidence that would close or downgrade it.
