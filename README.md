# SA U9 Inline Nationals 2026 — Team Hub v7

Version 7 adds the requested team-manager dashboard refinements:

- Restored a prominent dynamic **Countdown to Nationals** on Home.
- Restored the official **SA U9 representative team roster artwork** on the Team page.
- Rebuilt the Home **Quick Access** cards with consistent custom SVG icons instead of mixed emoji/text symbols.
- Added a **Team Announcements** system with priority levels (Info / Reminder / Important), author and update date.
- Added **Share to U9 Messenger**: on supported phones this opens the native share sheet; fallback copies the announcement and opens the U9 Messenger group.
- Announcements automatically disappear from Home when none are marked active in `app-data.js`.
- Kept the dynamic Schedule & Results, Facebook feed, HockeySyte, YouTube, Info links, checklist and external-link new-tab behaviour.
- Cache bumped to **v7** to force the new interface/assets to deploy over older PWA versions.

## Updating announcements
Edit the `announcements` array in `app-data.js`.
Set `active: false` to hide an announcement without deleting it.

## Privacy
Do not add private parent phone numbers, payment status, medical information, or internal Team Manager notes to this public GitHub repository.
