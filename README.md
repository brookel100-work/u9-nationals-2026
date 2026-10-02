V36 hotfix: fixed invalid app-data JavaScript that could prevent Home from rendering; aligned cache-busting to V36.

V28 — manual update through 30 September 2026.

Home: embedded official U9 competition page below Quick Access.
Schedule & Results: upcoming, completed and finals cards first; embedded official SA team page below finals; embedded U9 season statistics page below that (choose Stats → goalies on HockeySyte).
Team: individual player profile links only; no manual stat lines.
TAS 7–5 SA has been added. The official TAS game link is the supplied pregame URL and may redirect after publication.
The embedded goalie view opens the official U9 season page because a verified direct goalie-tab URL was not supplied.
Automatic sync remains disabled.


## V31 Photos
Adds a Photos tab linked to the shared SA U9 Nationals Google Drive folder, with a compact multi-column photo-wall treatment of the live embedded Drive grid and a direct folder button for family uploads (subject to Google Drive sharing permissions).


V31 removes the oversized single-column mobile presentation by rendering the live Google Drive grid in a compact wall. Google Drive still controls the embedded file UI; the app does not expose or store photo metadata itself.

## V32 photo wall
The Photos page now renders a native masonry collage with no filenames. A GitHub Action reads the public shared Google Drive folder every 5 minutes and updates `photo-data.js`. Families still upload through the existing “Open & add photos” button. The repository must allow GitHub Actions write access for automatic commits.
