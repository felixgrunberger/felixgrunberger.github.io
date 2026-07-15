# Felix Grünberger — Quarto scientific portfolio

A responsive, light editorial portfolio designed to present molecular biology, sequencing, analytical workflows and data analysis as one connected scientific profile.

## Run locally

```bash
quarto preview
```

## Build

```bash
quarto render
```

The rendered site is written to `docs/`.

## Validate

```bash
bash test-site.sh
```

The validation checks required files, rendered pages, metadata, DOI links, unresolved QMD links and horizontal overflow at desktop, tablet and mobile widths. Chromium and Python are needed for the optional browser checks.

## Design notes

- Fully light visual system, including the interactive workflow panel.
- Neutral scientific positioning: no job-search language or "open to work" cues.
- Responsive layouts for desktop, tablet and mobile.
- Interactive workflow supports hover, touch, keyboard navigation and reduced-motion preferences.
- No external font, icon or JavaScript dependencies.

## Before publishing

1. Run `quarto render` and `bash test-site.sh`.
2. Confirm all publication links.
3. Confirm LinkedIn, ORCID and Google Scholar URLs.
4. Commit source files and the rendered `docs/` folder.
5. Configure GitHub Pages to publish from `docs/` on the main branch.
