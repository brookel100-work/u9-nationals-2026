# SA U9 Inline Nationals 2026 — Team Hub V18

## V12 schedule update — 18 September 2026
- Updated to official Nationals Draw v2.8.
- Four confirmed SA U9 round-robin games remain unchanged.
- Updated conditional U9 finals pathway, including Game 125: 3rd vs Winner Game 113.
- Conditional finals are clearly labelled and do not automatically become the Next Game.
- Schedule version/date updated to v2.8 / 18 September 2026.
- Info → Documents now opens the packaged Nationals Draw v2.8.
- PWA cache bumped to V17.
- Existing V11 roster, jersey graphics, artwork, announcements, checklist and links retained.

Upload/replace the full contents of this folder in the GitHub Pages repository, then commit.

## V17 team artwork update — 19 September 2026
- Corrected red/gold U9 Representative Team artwork included and displayed on the Team page.
- Rylee Ruwette spelling is correct.
- Roster includes Jasiah Mumford, Coach Rohan Grantham and Manager Brooke Lodge.
- Updated artwork is included in the PWA cache.


## V17 updates
- Replaced the in-app Checklist tab with a detailed mobile-first Rules & Regs guide.
- Added verified junior protective-equipment requirements from the ILHA January 2021 rulebook.
- Kept the existing Nationals Info banner unchanged.
- Simplified Team to the official roster artwork plus a clean team/staff list; removed duplicate player cards and unreliable jersey-number graphics.
- Preserved schedule v2.8 and conditional finals behaviour.
- Cache/version bumped to V17.


## V17
- Added approved Rules & Regs banner artwork.
- Added visible Rules & Regs Quick Access icon.
- No team jersey numbers changed in this build because final confirmed numbers have not been supplied.


## V18 — 21 September 2026
- Replaced the previous forms/SIA announcement with the Nationals Week packing reminder.
- Reminder covers SA playing uniform, SA polo, playing gear, skates and stick/s.
- Points families to the existing Rules & Regs section for game-day information.
- PWA cache/assets bumped to V18.
- No schedule, team, jersey-number, banner or Rules & Regs content changed in this build.


## V20 — Live Nationals stats + game-day update
- Updated HockeySyte throughout the app to the live 2026 Nationals season page (season 1130).
- Promoted live results/stats in Home Quick Access, Schedule & Results and Info.
- Updated the Home announcement for Nationals being underway and the Monday 9:15am U9 opener / 8:15am arrival.
- Retained the current NTC venue/game-day Rules & Regs from V19, including 3-minute warm-up, SA polos, team entry/holding area, bag storage, white stick tape and red-line handshakes.
- No roster, jersey-number, draw or artwork changes in this build.

## V22 — automatic HockeySyte sync — 28 September 2026
- Added a GitHub Actions sync that runs every 5 minutes and can also be run manually.
- Uses a headless Chromium browser on GitHub's runner to read the public HockeySyte Nationals pages, so the phone/browser does not need cross-origin access to HockeySyte.
- Updates `live-data.json` only when all five U9 standings teams can be parsed safely; otherwise the app keeps its last-known-good data.
- Home and Schedule now load `live-data.json` on launch and merge official scores/standings into the existing app.
- SA round-robin results are mapped into the existing schedule so Latest SA Result, record, GF/GA and completed-game cards update automatically.
- No API key is embedded in the public site.

### One-time GitHub step
Upload/replace the repository with this V22 pack and make sure GitHub Actions are enabled for the repository. Then open **Actions → Sync HockeySyte Nationals data → Run workflow** once to verify the first live refresh. After that, the scheduled job runs automatically.
