# Report: diod currency and known-fail coverage

Human appendix for the diod-upstream inventory. Live claim:
`docs/ledgers/diod-upstream.md`.

## What we checked

1. Is `v9fs/test` diod-regression on a reasonably current chaos/diod?
2. Are outstanding chaos/diod issues visible to the harness known-fail list?

## Currency

`scripts/v9fs-prepare-diod-regression` clones `https://github.com/chaos/diod`
at `DIOD_REF=master` (depth 1) and builds it. Harness CI run
[33511542559](https://github.com/v9fs/test/actions/runs/33511542559)
(2026-09-01) produced `diod-build-de51d1e-mount-helper-v12`.

That SHA is chaos/diod HEAD:

- `de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106` 2026-06-23 "Merge pull request #173 from erentar/fix-gcc15"
- No newer commits on `master` as of 2026-09-01
- Tag `v1.1.0` is 2025-11-02; `master` is ahead of the tag
- Fork `v9fs/diod` (2022) is not used

There is nothing to bump. The remaining gap is that `master` is floating: a
later chaos/diod push would change CI without a harness pin.

`diod-9p2000.L` installs distro `apt` diod. That suite is **not** in Harness CI
(`ci.yml` matrix is smoke/fsx/postmark/dbench/diod-regression/qemu-9p2000.L).

## Known-fail vs upstream issues

`diod/xfail.txt` is a machine-parsed allow-list of FAIL/ERROR strings from the
guest `make check` subset. Comments are ignored.

On run 33511542559:

- `# TOTAL: 122` `# PASS: 98` `# SKIP: 6` `# FAIL: 16` `# ERROR: 2`
- `diod-regression-eval: unexpected: 0` (16 FAIL lines, 16 XFAIL rows)
- All FAIL/ERROR strings are t0011 allsquash or t0013 ACL (`v9fs/test#28`)
- t0010 including flock steps 21–24 PASS; t0012 PASS (xattr SKIP); t0020/t0021 PASS

GitHub `issues?state=open` and issue search for chaos/diod return only the
three open PRs (#31, #91, #165). Numbered GET of 1–173 finds 11 additional
open issues. The inventory uses the numbered set (14 items). None of those 14
are `xfail-fail-line`. Highest-risk misses if we had trusted search: #163
(getlock/sqlite) and #164 (32-bit readdir loop).

## Product patch (not landed)

`docs/patches/v9fs-test-diod-upstream/` is a comment-only update for
`v9fs/test`. This agent cannot push that repo. Do not add FAIL rows.

## Commands

```bash
scripts/check-diod-upstream-inventory.sh
scripts/check-scaffold.sh
```
