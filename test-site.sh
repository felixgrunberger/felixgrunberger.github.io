#!/usr/bin/env bash
set -euo pipefail

if ! command -v quarto >/dev/null 2>&1; then
  echo "ERROR: Quarto is not available in PATH. Install Quarto, then run this script again."
  exit 1
fi

python scripts/source_qa.py

rm -rf docs
quarto render

required=(
  docs/index.html
  docs/expertise.html
  docs/work.html
  docs/publications.html
  docs/about.html
  docs/404.html
  docs/images/favicon.svg
  docs/images/project-longread.svg
  docs/images/project-multiomics.svg
  docs/images/project-quality.svg
  docs/images/project-digital.svg
  docs/images/project-assay.svg
  docs/images/social-preview.png
  docs/site.js
  docs/robots.txt
  docs/.nojekyll
)

for file in "${required[@]}"; do
  [[ -f "$file" ]] || { echo "ERROR: Missing $file"; exit 1; }
done

if grep -RqiE 'href="[^"]+\.qmd' docs/*.html; then
  echo "ERROR: An unresolved .qmd link was found in rendered HTML."
  exit 1
fi

if grep -Rqi "open to work\|open to new opportunities\|job search" docs/*.html; then
  echo "ERROR: Explicit job-search language was found."
  exit 1
fi

doi_count=$(grep -o "https://doi.org/" docs/publications.html | wc -l | tr -d ' ')
if [[ "$doi_count" -lt 17 ]]; then
  echo "ERROR: Expected at least 17 DOI links, found $doi_count."
  exit 1
fi

for page in docs/index.html docs/expertise.html docs/work.html docs/publications.html docs/about.html; do
  grep -qi '<meta name="description"' "$page" || { echo "ERROR: Missing description meta tag in $page"; exit 1; }
done

if command -v python >/dev/null 2>&1 && python -c 'import playwright' >/dev/null 2>&1; then
  python scripts/browser_qa.py docs
else
  echo "INFO: Browser QA skipped because Python or Playwright is unavailable."
fi

echo "SUCCESS: The Quarto website rendered and validated correctly."
