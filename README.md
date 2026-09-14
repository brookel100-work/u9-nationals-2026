# SA U9 Inline Nationals 2026 — Team Hub v6

Mobile-first PWA for the South Australia U9 Inline Hockey team at the 2026 Australian National Championships.

## v6 changes

- New approved SA U9 Home hero artwork with Nationals branding, dates and venue
- New Schedule & Results banner
- New Nationals Checklist banner
- Corrected embedded Nationals Facebook page: `61592878025737`
- Quick Access simplified: Team and Checklist removed from Home shortcuts
- Schedule renamed and rebuilt as **Schedule & Results**
- Game results appear on the same fixture cards when scores are entered in `app-data.js`
- Completed games without a score show an official HockeySyte result link
- Restored important Info links
- Added downloadable official 2026 Championship Rules PDF
- Added downloadable full Nationals Draw v2.6 workbook
- External links open in a new tab/window
- U9 Messenger group remains available for team contact
- Service worker cache bumped to v6 and remains network-first

## Updating results

Open `app-data.js` and add the official score to the relevant game, for example:

```js
homeScore: 3,
awayScore: 2
```

The app automatically updates the game card plus SA's W-L-D record, Goals For and Goals Against.

## Official results integration

HockeySyte remains the official source. Automatic live syncing is not enabled yet because the 2026 Nationals public results endpoint has not been confirmed. Once the organisers update/publish the 2026 Nationals HockeySyte competition, the app is ready for that integration to be tested.

## Privacy

Do not add private parent contacts, payment status, medical information or internal Team Manager notes to this public repository.
