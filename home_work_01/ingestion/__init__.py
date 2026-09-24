"""Ingestion package for HW10 Taiwan Weather Forecast (home_work_01, Issue #18).

The package covers the three poster stages — fetch, parse/derive, database —
that turn one CWA ``F-D0047-091`` JSON response into the six-Region x seven-day
Forecast Snapshot persisted in ``data.db``.

Stage map (README documents the correspondence to the poster ``HW10_Weather/``):

* :mod:`ingestion.fetch`    — fetch stage: acquire the raw JSON with the user's key.
* :mod:`ingestion.derive`   — parse stage: pure functions, JSON object -> 42 rows.
* :mod:`ingestion.persist`  — database stage: whole-snapshot atomic replace into SQLite.
* :mod:`ingestion.pipeline` — CLI wiring fetch -> save -> derive -> persist (and an
  offline ``--from-json`` path that skips the network).

Only ``ingestion`` reads the CWA endpoint or the key; the presentation layers and
the shared query module (later tickets) never do.
"""
