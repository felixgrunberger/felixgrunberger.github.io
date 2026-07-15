# QA report — refined light portfolio

## Changes verified

- Every page background is full-bleed: Quarto page wrappers, hero, content sections and footer span the complete viewport width.
- The desktop hero fills the visible viewport below the pinned header; tablet and mobile use natural content height.
- The palette is now neutral navy, slate and muted steel blue, with no saturated turquoise or mint panels.
- The workflow remains interactive by hover, click, keyboard and automatic cycling.
- Active workflow states stay fully inside their row boxes: no translation, rotation or scaling can push icons or labels outside.
- The active row uses an internal left accent and bottom progress line; response text cross-fades without changing the box dimensions.
- Header spacing, horizontal overflow and workflow bounds were checked at 1536, 1280, 1024, 390 and 360 px.

## Automated results

- Source QA: passed.
- Horizontal overflow: 0 px at all tested sizes.
- Hero background: exactly viewport width at all tested sizes.
- Workflow markers and active-state animation: within row and panel bounds at all tested sizes.
- Pinned header does not overlap the hero.

The project remains neutrally positioned as a scientific portfolio and contains no explicit job-search language.
