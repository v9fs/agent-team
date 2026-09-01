#!/usr/bin/env bash
set -euo pipefail

# Offline check that the diod-upstream inventory names every pinned open
# chaos/diod issue/PR, that none are classified as machine-parsed XFAIL FAIL
# lines, and that the xfail snapshot is only t0011/t0013 strings.
#
# The proof would fail if the catalog omitted an open ID from
# diod-upstream-open-issues.json, or if it claimed those IDs were already
# xfail-fail-line while the FAIL snapshot contains only v9fs/test#28 rows.

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

json="docs/ledgers/diod-upstream-open-issues.json"
ledger="docs/ledgers/diod-upstream.md"
patch="docs/patches/v9fs-test-diod-upstream/xfail.txt"
snapshot="docs/ledgers/diod-xfail-snapshot.txt"

failures=0

need() {
  local path="$1"
  if [[ ! -s "$path" ]]; then
    echo "missing or empty: $path" >&2
    failures=$((failures + 1))
    return 1
  fi
}

need "$json" || true
need "$ledger" || true
need "$patch" || true
need "$snapshot" || true
if (( failures > 0 )); then
  echo "diod-upstream inventory check failed: $failures problem(s)" >&2
  exit 1
fi

python3 - "$json" "$ledger" "$patch" "$snapshot" <<'PY'
import json, re, sys
from pathlib import Path

json_path, ledger_path, patch_path, snapshot_path = sys.argv[1:]
data = json.loads(Path(json_path).read_text())
ledger = Path(ledger_path).read_text()
patch = Path(patch_path).read_text()
snapshot = Path(snapshot_path).read_text()
errors = []

items = data.get("open_items") or []
if len(items) < 14:
    errors.append(f"expected at least 14 open_items, got {len(items)}")

numbers = []
for item in items:
    n = item.get("number")
    disp = item.get("disposition")
    numbers.append(n)
    if disp == "xfail-fail-line":
        errors.append(
            f"chaos/diod#{n} marked xfail-fail-line; subset FAIL lines are "
            "t0011/t0013 only (v9fs/test#28)"
        )
    token = f"chaos/diod#{n}"
    alt = f"[{n}]("
    if token not in ledger and alt not in ledger:
        errors.append(f"{ledger_path} does not name chaos/diod#{n}")
    if f"#{n}" not in patch:
        errors.append(f"{patch_path} comments do not name #{n}")

if len(numbers) != len(set(numbers)):
    errors.append("duplicate issue numbers in snapshot JSON")

fail_lines = []
for line in snapshot.splitlines():
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    fail_lines.append(s)

if len(fail_lines) != 16:
    errors.append(f"xfail snapshot should have 16 FAIL lines, got {len(fail_lines)}")

for line in fail_lines:
    if not (line.startswith("t0011-") or line.startswith("t0013-")):
        errors.append(f"xfail snapshot has non-t0011/t0013 FAIL line: {line}")

# Patch must not introduce new machine-parsed FAIL rows.
def parsed_fail_rows(text: str) -> list[str]:
    rows = []
    for line in text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if not s or s.startswith("#"):
            continue
        rows.append(s)
    return rows

snap_rows = parsed_fail_rows(snapshot)
patch_rows = parsed_fail_rows(patch)
if patch_rows != snap_rows:
    errors.append(
        "product patch FAIL rows differ from snapshot; comments-only patch required"
    )

# Discriminating negative: GitHub search-only set is not sufficient.
search_only = {31, 91, 165}
pinned = set(numbers)
if not (pinned - search_only):
    errors.append("snapshot contains only search-visible PRs; numbered issues missing")
for must in (163, 164, 166):
    if must not in pinned:
        errors.append(f"required coverage-gap/arch issue #{must} missing from snapshot")

expected_head = "de51d1ee1bd5ccf1d8c16b96227c8bb03ec50106"
if data.get("diod_head") != expected_head:
    errors.append(f"diod_head is {data.get('diod_head')}, expected {expected_head}")
if expected_head[:12] not in ledger:
    errors.append("ledger does not pin diod HEAD SHA")

if errors:
    print("diod-upstream inventory check failed:", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    sys.exit(1)

print(
    f"diod-upstream inventory check passed: {len(items)} open items, "
    f"{len(fail_lines)} XFAIL FAIL lines, diod {expected_head[:12]}"
)
PY
