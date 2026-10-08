# Experiment Log

| ID | Date | Hypothesis | Method | Result | Artifact | Decision/claim affected | Rerun trigger | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X0001 | 2026-09-01 | GitHub issue list/search for chaos/diod returns the full outstanding set | `issues?state=open`, `search/issues?q=repo:chaos/diod+is:open`, then GET issues 1–173 | Search `is:pr is:open` shows 3 PRs only; numbered GET found 14 open items (11 issues + 3 PRs). Highest-risk misses: #163, #164, #166. A PAT `issues?state=open` list can also return the 14; do not treat PR-only search as complete. | `docs/ledgers/diod-upstream-open-issues.json` | P0003 inventory must not trust search completeness | chaos/diod `open_issues_count` changes or HEAD moves | [#3](https://github.com/v9fs/agent-team/pull/3) / [#4](https://github.com/v9fs/agent-team/issues/4) |
| X0002 | 2026-10-08 | KVM-accelerated QEMU is usable in the cloud VM for kernel smoke runs | `qemu-system-x86_64 -enable-kvm -cpu host` with `earlyprintk=serial` (after `chmod 666 /dev/kvm`) vs `-accel tcg` on the same bzImage/initramfs | KVM: zero bytes of serial output in 60 s and 900 s runs. TCG: full boot and smoke in ~95 s guest time. Also: `make olddefconfig` without `LLVM=1` silently drops `CONFIG_RUST` when `CONFIG_KASAN=y` | `docs/reports/r9fs-virtio-smoke.md` | P0006 (run under TCG) | Different VM image or nested-virt change | v9fs/agent-team PR (r9fs evidence) |

Record rejected ideas and failed experiments when they prevent a later agent
from repeating the same work without new evidence.
