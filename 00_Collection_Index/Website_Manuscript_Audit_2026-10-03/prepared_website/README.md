# B-Theory website

Local Astro draft of the B-Theory research site. The October 2026 draft makes **B = Being + Becoming** explicit and organizes the work around representation, observation, structure, and change.

## Develop

```powershell
npm install
npm run dev
```

Run `npm run check` and `npm run build` before publishing. If the local sandbox prevents Astro from writing telemetry configuration, set `ASTRO_TELEMETRY_DISABLED=1` for that command.

Project copy and research status live in `src/content/projects/`; the research map, MIND guide, and paper guide are in `src/pages/`. Shared layout and styles live in `src/layouts/` and `src/styles/`. Original image assets and fonts are stored locally in `public/assets/`.

The existing project slugs remain in place. New routes are `/research-map/`, `/the-mind/`, `/papers/`, and the added project pages. Five manuscript reading copies are bundled in `public/manuscripts/`, all credited to Brian Theory. Three use reading copy 2 for author or metadata corrections; the two unchanged PDFs remain copy 1. Superseded files are preserved in `manuscript-history/reading-copy-1/`. Structured Boolean Factorization remains index-only pending an integrated manuscript with a named author. Site release numbers remain separate from internal manuscript versions. See [MANUSCRIPT_READING_COPIES.md](MANUSCRIPT_READING_COPIES.md) for the selected files and hashes. Shop, Help, and Legal still point to the current live site. See [RESEARCH_MAP_DRAFT.md](RESEARCH_MAP_DRAFT.md) for the editorial map and review points.

The 3 October review pass is recorded in [REVIEW_PANEL_2026-10-03.md](REVIEW_PANEL_2026-10-03.md). The research-contact link uses `Brian@B-Theory.com`, which is listed in Brian's public B-Theory résumé and was confirmed by Brian for this draft.
