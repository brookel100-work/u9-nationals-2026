# SA U9 Nationals 2026 Team Hub — v4

Mobile-first Progressive Web App for the South Australia U9 Inline Hockey team at the 2026 Australian National Championships.

## v4 additions
- Automatic schedule progression: games move from Upcoming to Past based on Queensland time.
- Home always shows the next relevant confirmed game.
- Results-ready data model: enter scores in `app-data.js` and the app automatically shows SA's record, goals for/against and final score cards.
- HockeySyte results/statistics link included as the official source; the supplied link currently points to the organiser-provided superseason page and may be updated for 2026.
- Official Nationals YouTube channel added for streams/video.
- Team contact card added with Brooke (Team Manager), Rohan (Coach) and direct U9 Messenger group link.
- Official Nationals Facebook feed attempt retained with a direct-page fallback.

## Updating results
In `app-data.js`, each round-robin game has `homeScore` and `awayScore`. Replace `null` with the final scores, e.g.:

```js
{ home: "QLD", away: "SA", homeScore: 2, awayScore: 4 }
```

The app will automatically calculate the team record and goals for/against.

## Finals
Finals remain conditional until SA's pathway is known. Set the applicable final game's `confirmed` value to `true` when known so it can become the Home screen's next game after round robin.

## Privacy
This public app contains no parent phone numbers, payment status or private Team Manager notes.
