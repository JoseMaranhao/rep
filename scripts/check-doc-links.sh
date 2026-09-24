#!/usr/bin/env bash
set -euo pipefail

# Verifies relative Markdown links used by this portfolio template.
while IFS= read -r -d '' file; do
  while IFS= read -r target; do
    target=${target%%#*}
    [[ -z "$target" || "$target" == http* || "$target" == mailto:* ]] && continue
    [[ -e "$(dirname "$file")/$target" ]] || {
      echo "Broken link in $file: $target" >&2
      exit 1
    }
  done < <(sed -nE 's/.*\]\(([^ )]+).*/\1/p' "$file")
done < <(find . -name '*.md' -not -path './.git/*' -print0)

echo "Markdown relative links are valid."
