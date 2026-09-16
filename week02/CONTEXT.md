# Personal Site

This context defines the small set of user-facing concepts used by Momo's personal site.

## Language

**Display name**:
The public name shown on the site; its value is `Momo`.
_Avoid_: Full name, username

**Current time**:
The current wall-clock date and time in the `Asia/Taipei` time zone.
_Avoid_: Browser local time, device time

**Time format**:
The clock notation selected by the visitor: 24-hour time by default, or 12-hour time with an explicit AM/PM marker.
_Avoid_: Time zone, locale

**Visual theme**:
The site's presentation selected from `Aurora`, `Minimal`, and `Sunset`. A visual theme changes only color, background, lighting, and related visual treatment; it never changes layout, information architecture, or features.
_Avoid_: Layout variant, page variant

**Saved preference**:
A visitor choice that remains selected across visits. Only the visual theme and time format are saved preferences.
_Avoid_: Session state, focus mode state

**Focus mode**:
A temporary view containing only the display name, current time, date, and an explicit exit control. It always starts inactive on a new visit and can be exited with the Escape key.
_Avoid_: Zen mode, saved mode

**Copied time**:
A complete text representation containing the display name, Taipei date, current time in the selected format, and `Asia/Taipei (UTC+8)` time-zone identity.
_Avoid_: Time only, device time
