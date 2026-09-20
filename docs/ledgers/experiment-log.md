# Experiment Log

| ID | Date | Hypothesis | Method | Result | Artifact | Decision/claim affected | Rerun trigger | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X0001 | 2026-09-01 | GitHub issue list/search for chaos/diod returns the full outstanding set | `issues?state=open`, `search/issues?q=repo:chaos/diod+is:open`, then GET issues 1–173 | Search `is:pr is:open` shows 3 PRs only; numbered GET found 14 open items (11 issues + 3 PRs). Highest-risk misses: #163, #164, #166. A PAT `issues?state=open` list can also return the 14; do not treat PR-only search as complete. | `docs/ledgers/diod-upstream-open-issues.json` | P0003 inventory must not trust search completeness | chaos/diod `open_issues_count` changes or HEAD moves | [#3](https://github.com/v9fs/agent-team/pull/3) / [#4](https://github.com/v9fs/agent-team/issues/4) |

Record rejected ideas and failed experiments when they prevent a later agent
from repeating the same work without new evidence.
