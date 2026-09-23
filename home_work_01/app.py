"""Taiwan Weather Forecast — Streamlit Grading App (``app.py``).

Run locally from the unit directory with ``streamlit run app.py`` (Spec R-GA-1).
This is the genuine Streamlit application the teacher's documents name; it carries
the complete MVM behaviour and only the MVM behaviour — it has no Taiwan Map and
no ``Select Date`` control, and it depends on neither ``folium`` nor
``streamlit-folium`` (R-GA-9 / DR-11, INV-9).

Every piece of data comes through the shared :mod:`weather_query` module: this
file contains no SQL, imports no HTTP client, and references no CWA URL or API key
(R-GA-6 / R-SHR-5, high-risk H-1 static check). The page shows the title
``Taiwan Weather Forecast``, a ``Select Region`` dropdown of the six Regions in
the fixed order, and — for the selected Region — a ``MaxT`` / ``MinT`` line chart
over the seven Forecast Days plus a ``Date`` / ``MinT`` / ``MaxT`` table, together
with the snapshot's acquisition time (R-GA-2..R-GA-5, R-GA-8, DR-17). Missing or
empty databases show a clear message and an incomplete snapshot a warning, with no
unhandled exception (R-GA-7 / DR-9).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

import weather_query as wq

PAGE_TITLE = "Taiwan Weather Forecast"
SELECT_REGION_LABEL = "Select Region"

# Line colours: MaxT red, MinT blue (R-GA-4 SHOULD / DR-15).
CHART_MAXT_COLOR = "#d62728"
CHART_MINT_COLOR = "#1f77b4"

_MISSING_MESSAGE = (
    "The forecast database `data.db` was not found. Generate it by running the "
    "ingestion pipeline from the `home_work_01` directory: `python -m ingestion` "
    "(online) or `python -m ingestion --from-json data/raw/F-D0047-091.json` "
    "(offline rebuild)."
)
_EMPTY_MESSAGE = (
    "The forecast database `data.db` contains no snapshot yet. Run the ingestion "
    "pipeline (`python -m ingestion`) to populate it before opening this app."
)
_INCOMPLETE_MESSAGE = (
    "The forecast snapshot is incomplete — it is not the full six Regions x seven "
    "Forecast Days. Showing the data that is present; re-run ingestion "
    "(`python -m ingestion`) to refresh the snapshot."
)


def _render_ingestion_time(db_path: str | Path) -> None:
    """Show the snapshot's acquisition time exactly as stored (R-GA-8 / DR-17).

    The value is ``IngestionMetadata.ingestedAt`` — when the data was fetched
    from CWA — shown verbatim and labelled as such, never as a publish or render
    time.
    """
    timestamp = wq.last_ingestion_time(db_path)
    shown = timestamp if timestamp else "unknown"
    st.caption(f"Last updated (data fetched from CWA): {shown}")


def _render_region(region: str, db_path: str | Path) -> None:
    """Render the chart and table for one selected Region (R-GA-4, R-GA-5).

    Builds a ``MaxT`` / ``MinT`` line chart over the seven Forecast Days and a
    ``Date`` / ``MinT`` / ``MaxT`` table (seven rows, dataDate ascending) whose
    values equal ``data.db``. If the Region has no rows (only possible for an
    incomplete snapshot) an explicit message is shown instead of an error.
    """
    series = wq.region_series(region, db_path)
    if not series:
        st.info(f"No forecast data is available for {region}.")
        return

    dates = [row["dataDate"] for row in series]
    mint = [row["mint"] for row in series]
    maxt = [row["maxt"] for row in series]

    st.subheader(f"Temperature Forecast – {region}")

    chart_df = pd.DataFrame({"Date": dates, "MaxT": maxt, "MinT": mint})
    st.line_chart(
        chart_df,
        x="Date",
        y=["MaxT", "MinT"],
        x_label="Date",
        y_label="Temperature (°C)",
        color=[CHART_MAXT_COLOR, CHART_MINT_COLOR],
    )

    table_df = pd.DataFrame({"Date": dates, "MinT": mint, "MaxT": maxt})
    st.dataframe(table_df, hide_index=True)


def main(db_path: str | Path = wq.DEFAULT_DB_PATH) -> None:
    """Render the Grading App page (R-GA-1..R-GA-9).

    ``db_path`` defaults to the snapshot beside the shared module and is
    overridable so tests can point the app at alternative databases (AC-10).
    """
    st.title(PAGE_TITLE)

    status = wq.snapshot_status(db_path)
    if status is wq.SnapshotStatus.MISSING:
        st.error(_MISSING_MESSAGE)
        return
    if status is wq.SnapshotStatus.EMPTY:
        st.error(_EMPTY_MESSAGE)
        return
    if status is wq.SnapshotStatus.INCOMPLETE:
        st.warning(_INCOMPLETE_MESSAGE)

    _render_ingestion_time(db_path)

    regions = list(wq.region_list())
    region = st.selectbox(
        SELECT_REGION_LABEL, regions, index=0, key="select_region"
    )
    _render_region(region, db_path)


if __name__ == "__main__":
    # Streamlit (and AppTest.from_file) run this file with ``__name__`` set to
    # ``"__main__"``; ``import app`` does not, so tests can drive ``main`` against
    # alternative databases without the module auto-rendering the default one.
    main()
