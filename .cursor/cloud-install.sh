#!/usr/bin/env bash
# Checkout the product repos next to this forge. Blobless so the linux mirror
# stays usable without downloading every historical blob up front.
set -euo pipefail
root="${HOME}/src/v9fs"
mkdir -p "$root"
sync_repo() {
  local dest="$1" url="$2" branch="$3"
  if [ ! -d "$dest/.git" ]; then
    git clone --filter=blob:none --branch "$branch" "$url" "$dest"
  fi
  git -C "$dest" fetch --prune origin "$branch"
  if git -C "$dest" diff --quiet && git -C "$dest" diff --cached --quiet; then
    git -C "$dest" checkout -B "$branch" "origin/$branch"
  fi
}
sync_repo "$root/linux" https://github.com/v9fs/linux.git upstream
sync_repo "$root/test" https://github.com/v9fs/test.git main
