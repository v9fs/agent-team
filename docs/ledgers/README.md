# Durable Project Evidence

GitHub is authoritative for live workflow state. These records preserve domain
evidence that cannot be reconstructed reliably from issues, pull requests, or
the code alone.

Keep only the records that answer a real project question:

| Record | Question answered |
| --- | --- |
| `evidence-map.md` | Which versioned sources, requirements, runtime captures, or data constrain the work? |
| `proof-ledger.md` | What bounded claims exist, what proves them, and what gap is next? |
| `decision-log.md` | Why was a durable design choice made, and when should it reopen? |
| `decision-records/` | Long-form alternatives and rationale for selected decisions |
| `experiment-log.md` | Which hypothesis was tested, what happened, and when should it rerun? |
| `risk-ledger.md` | Which trigger could harm the project, and what evidence closes it? |
| `methodology-ledger.md` | Which operating-method review occurred, what changed, and what triggers the next one? |
| `diod-upstream.md` | Is harness diod current, and are open chaos/diod issues classified against `diod/xfail.txt`? |

Do not duplicate assignees, issue state, PR state, or labels without an explicit
synchronization reason and authority rule.
