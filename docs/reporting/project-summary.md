# Maintained Project Summary

People evaluating a project need its system context, design, evidence, and
remaining limits in one readable artifact. Produce `docs/project-summary.md`
and `docs/project-summary.pdf` as the stable entry point for that audience.
The report explains the underlying project; agent roles, labels, workflow
ledgers, and session history belong in supporting material unless the operating
method is itself the project's subject.

## Refresh Contract

- Create a bootstrap snapshot, then refresh when the architecture, scope,
  measured results, or limitations change, at milestone closeout, and before
  handing the report to another reader. Ordinary changes that leave the report
  accurate do not require a rewrite.
- Read the current formulation, relevant source, evidence map, proof ledger,
  experiment log, and raw result artifacts. Record the source revision and
  whether relevant uncommitted changes were included. A previous PDF or issue
  description alone is insufficient evidence of the current project state.
- On adoption, preserve an existing report's authors, classification, content,
  and working export path. Merge this contract into the project's instructions
  and closeout workflow within the authorized scope. Do not replace AGENTS.md.
  Copy the packaged renderer and template only where they do not collide.
- The state closer owns the refresh decision; the independent reviewer checks
  important claims against their sources as part of the existing review gate.
- Rebuild after the last source edit. Commit source, PDF, receipt, and any
  authored figures together within project authority. The receipt's Git head
  records build context; it is not proof that every source was clean or current.

## Content

Aim for a concise 2-4 page technical report, expanding only when the evidence
requires it. Define unfamiliar terms. Follow the repository's writing guide
when available: concrete system pressure, mechanisms, tradeoffs, and practical
consequences. Use institutional "we" for shared work and preserve known authors;
do not infer authorship or affiliations from repository ownership.

1. **Title, abstract, and status:** explain the project and strongest supported
   finding in plain language. Include the report date, source revision, and
   distribution classification visibly in the body.
2. **Problem and context:** deployment pressure, intended users, constraints,
   and the baseline or existing approach.
3. **Design and implementation:** components, interfaces, data/control flow,
   implemented behavior, and proposed work. Add a system diagram when useful.
4. **Evaluation and measured results:** the question, method, measurements,
   interpretation, and what the evidence permits us to conclude.
5. **Limitations and next step:** unresolved gaps, failed or negative results,
   known tradeoffs, and the next discriminating experiment or integration.
6. **References:** human-readable, versioned sources and reproduction links.
   Include required evidence here, rather than only in a stripped Related or
   Source Notes section.

Each quantitative result must name units, workload/dataset and version,
hardware/software configuration, measurement date, sample/run count and
aggregation, baseline when applicable, and an exact raw artifact or command
reference. State missing fields as unknown and narrow the claim. Cite input
values and formula for derived comparisons. Do not invent sample counts,
variance, significance, speedups, coverage, or measurements from tests.
Separate measured observations, source-reported results, estimates, targets,
and proposed evaluations. Label fixture/synthetic evidence and avoid extending
it to native hardware, production, or representative performance.

If no measured results exist, say **"No measured results are available yet."**
Explain what is implemented and verified, what remains unverified, and the
evaluation plan. Compilation and scaffold checks are validation, not workload
performance. At bootstrap the mission describes intent, not delivered behavior.

## Build and Review

The generator installs `scripts/render-project-summary.py` and
`docs/reporting/usenix-summary.typst` alongside this contract. From the project
root run:

```bash
python3 scripts/render-project-summary.py
pdftoppm -scale-to 1500 -png docs/project-summary.pdf /tmp/project-summary
```

The renderer requires Python 3, Pandoc, and Typst. It uses a local template
without network packages and writes the PDF only after successful compilation.
Keep images and other report dependencies inside the project; pass additional
Pandoc options by adapting the project's renderer when needed. Do not silently
fall back to a different layout or install missing tools.

Use US letter, two columns, a 7 by 9 inch text area, and 10 point Times or a
similar serif on 12 point leading, following the
[USENIX author template guidance](https://www.usenix.org/conferences/author-resources/paper-templates).
This is a project report; do not imply conference submission, acceptance, or
peer review. Keep export-tool details out of the PDF body.

Inspect every rendered page for clipping, broken figures, overlapping tables,
unreadable columns, missing glyphs, and awkward page breaks. Extract text to
check that key claims, visible classification, limitations, and references
survive export. Check the receipt's source and PDF hashes after the final edit;
review changed evidence inputs explicitly, because hashes alone cannot assess
claim freshness. Link the PDF and source near the top of the project README.

If tools, evidence, or QA are incomplete, preserve the source and last good
PDF, name the blocker, and mark the PDF stale or unverified in the README and
handoff. Do not present an old PDF as updated. Keep bootstrap success, PDF
compilation, claim review, visual QA, CI, and remote publication distinct.

## Distribution

Inherit the most restrictive applicable source/project classification and
display it in the report. A more readable format does not broaden its audience.
Keep credentials, raw private session paths, personal data, and inaccessible
links out of a shareable report. Creating it in an authorized repository does
not authorize email, external distribution, publication, or a visibility change.
Offer a separately reviewed audience-specific version if necessary.
