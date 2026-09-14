# SA U9 Inline Nationals 2026 — Team Hub v5

This is the clean V5 rebuild for GitHub Pages.

## What changed
- Uses only the approved V5 production artwork extracted from the approved design board
- New Home hero: `assets/sa-u9-home-hero.png`
- New Team header: `assets/sa-u9-team-header.png`
- New Nationals header: `assets/nationals-2026-header.png`
- New app icons from the approved SA puck design
- No legacy training artwork or older screenshot-based assets
- Official Nationals Facebook feed embed attempt plus fallback link
- Automatic date-aware next-game/upcoming/past-game behaviour
- Results/stats section ready for HockeySyte data/manual score entry
- Official YouTube channel link
- U9 Messenger group contact section
- Cache version bumped to `sa-u9-nationals-v5` and network-first updates to avoid stale app builds

## Updating scores
In `app-data.js`, add `homeScore` and `awayScore` to a completed round-robin game. The app automatically updates the W-L-D record and goals for/against.

## Privacy
Do not place parent phone numbers, payment status, medical information, or private manager notes in this public repository.
