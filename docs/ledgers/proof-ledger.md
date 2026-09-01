# Proof Ledger

| ID | Claim | Component/artifact | Evidence ids | Current level | Exact proof artifact or command | Explicit non-claims | GitHub issue/PR | Next gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0001 | Scaffold is a GitHub edition: required GitHub templates, Actions workflow, and host contracts exist; process remains 1:1 with the GitLab origin | `.github/`, `docs/HOST.md`, `scripts/check-scaffold.sh` | E0001, E0002 | Static | `scripts/check-scaffold.sh` and `git diff --check` | Dual-host adapters (B); GitHub-native review/CODEOWNERS/issue forms (C); live `gh` issue/PR loop against a remote |  | Contract/Golden: create issue+draft PR from templates on a GitHub remote |
| P0002 | t0011 allsquash and t0013 ACL tip residuals are two independent mapped claims with pinned kernel/diod/harness versions | `v9fs/test` harness; `chaos/diod`; v9fs Image v7.2 | E0003, E0004, E0005, E0006 | Mapped | `docs/plans/1-map-tip-xfails.md`; run 32929975795; `scripts/check-scaffold.sh` | No kernel or diod fix; XFAIL is not integration proof; docker latest is floating | #1 | Create two implementation slices after independent review lands |

Use the levels selected from `docs/PROOF_MODEL.md`. A higher level requires an
actual artifact, not only a planned test.
