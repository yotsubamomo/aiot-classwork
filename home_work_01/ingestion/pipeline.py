"""Pipeline / CLI wiring the fetch, derive and persist stages together.

Two entry paths:

* Online (default): read the key from ``.env``, fetch F-D0047-091 once, save the
  complete indented raw JSON, print a fetch summary, derive the 42 rows, print the
  preview, and persist the snapshot.
* Offline (``--from-json PATH``): load an already-saved raw JSON and run only
  derive -> persist. No network and no ``.env`` are touched, so tests, CI and
  offline rebuilds use this path (R-ING-5, R-TC-5).

Any FetchError or DeriveError is reported (without the key) and turned into a
non-zero exit code with no database write.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import config, provenance
from .derive import DeriveError, derive_snapshot
from .fetch import FetchError, fetch_raw, load_api_key
from .persist import persist_snapshot
from .provenance import ProvenanceError

TAIPEI_TZ = timezone(timedelta(hours=8))
DEFAULT_RAW_OUT = config.UNIT_DIR / "data" / "raw" / f"{config.RESOURCE_ID}.json"
DEFAULT_ENV = config.UNIT_DIR / ".env"


def ingestion_timestamp() -> str:
    """Current local time as an ISO 8601 string in +08:00.

    Read only on the online path, at fetch success, to record the acquisition
    time (DR-17). The offline path never reads the clock.
    """
    return datetime.now(TAIPEI_TZ).replace(microsecond=0).isoformat()


def summarize_response(data: dict) -> dict:
    """Compute a small fetch summary: county count, element names, period count."""
    counties = (((data.get("records") or {}).get("Locations") or [{}])[0]).get(
        "Location"
    ) or []
    element_names: list[str] = []
    period_count = 0
    if counties:
        first = counties[0]
        for element in first.get("WeatherElement", []) or []:
            name = element.get("ElementName")
            if name and name not in element_names:
                element_names.append(name)
            if name == config.ELEMENT_MAX:
                period_count = len(element.get("Time", []) or [])
    return {
        "county_count": len(counties),
        "element_names": element_names,
        "period_count": period_count,
    }


def print_fetch_summary(data: dict, *, stream=sys.stdout) -> None:
    """Print the acquisition summary for the 'observe JSON' grading item."""
    summary = summarize_response(data)
    print("Fetch summary (F-D0047-091):", file=stream)
    print(f"  counties: {summary['county_count']}", file=stream)
    print(
        f"  weather elements ({len(summary['element_names'])}): "
        f"{', '.join(summary['element_names'])}",
        file=stream,
    )
    print(
        f"  periods per temperature element: {summary['period_count']}",
        file=stream,
    )


def print_preview(rows: list[dict], *, stream=sys.stdout) -> None:
    """Print the full 42-row derived snapshot preview (DR-6 / R-DER-8)."""
    print("Derived Forecast Snapshot preview:", file=stream)
    print(
        f"  {'regionName':<10} {'dataDate':<12} {'mint':>6} {'maxt':>6}",
        file=stream,
    )
    for row in rows:
        print(
            f"  {row['regionName']:<10} {row['dataDate']:<12} "
            f"{row['mint']:>6} {row['maxt']:>6}",
            file=stream,
        )
    dates = sorted({row["dataDate"] for row in rows})
    regions = {row["regionName"] for row in rows}
    print(
        f"  rows: {len(rows)} | regions: {len(regions)} | "
        f"date range: {dates[0]} .. {dates[-1]}",
        file=stream,
    )


def save_raw_json(data: dict, raw_out: str | Path) -> Path:
    """Write the complete, indented raw JSON to a documented location (R-ING-4)."""
    path = Path(raw_out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return path


def run_online(
    *,
    env_path: str | Path = DEFAULT_ENV,
    raw_out: str | Path = DEFAULT_RAW_OUT,
    db_path: str | Path = config.DB_PATH,
) -> int:
    """Full online ingestion: fetch -> save (+ provenance) -> derive -> persist.

    The acquisition time is captured **once**, right after the fetch succeeds
    (DR-17 §4.2), and the same value is written both to the provenance sidecar and
    to ``IngestionMetadata.ingestedAt``. The persist clock is never read here.
    """
    api_key = load_api_key(env_path)
    data = fetch_raw(api_key)
    acquired_at = ingestion_timestamp()  # acquisition time = fetch-success time
    saved = save_raw_json(data, raw_out)
    prov = provenance.write_provenance(saved, acquired_at, config.RESOURCE_ID)
    print(f"Saved raw JSON to {saved}")
    print(f"Saved provenance to {prov} (acquired at {acquired_at})")
    print_fetch_summary(data)
    rows = derive_snapshot(data)
    print_preview(rows)
    count = persist_snapshot(rows, acquired_at, config.RESOURCE_ID, db_path)
    print(f"Persisted {count} rows to {db_path} (ingested at {acquired_at})")
    return 0


def run_offline(
    *,
    json_path: str | Path,
    db_path: str | Path = config.DB_PATH,
    acquired_at: str | None = None,
) -> int:
    """Offline ingestion from a saved raw JSON: derive -> persist (no network).

    The acquisition time is **not** taken from the clock (DR-17 §4.3): it comes
    from ``acquired_at`` when given, otherwise from the raw JSON's provenance
    sidecar. If neither is available the run fails closed (no database write).
    """
    if acquired_at is None:
        acquired_at = provenance.read_acquisition_time(json_path)
    try:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DeriveError(f"raw JSON not found: {json_path}") from exc
    except ValueError as exc:
        raise DeriveError(f"raw JSON is not valid JSON: {json_path}") from exc
    rows = derive_snapshot(data)
    print_preview(rows)
    count = persist_snapshot(rows, acquired_at, config.RESOURCE_ID, db_path)
    print(f"Persisted {count} rows to {db_path} (ingested at {acquired_at})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m ingestion",
        description=(
            "Ingest F-D0047-091 into data.db: fetch, derive the six-Region x "
            "seven-day snapshot, and persist it."
        ),
    )
    parser.add_argument(
        "--from-json",
        dest="from_json",
        metavar="PATH",
        help="offline mode: derive+persist from a saved raw JSON (no network, no .env)",
    )
    parser.add_argument(
        "--raw-out",
        dest="raw_out",
        default=str(DEFAULT_RAW_OUT),
        metavar="PATH",
        help="where to save the raw JSON in online mode",
    )
    parser.add_argument(
        "--env",
        dest="env_path",
        default=str(DEFAULT_ENV),
        metavar="PATH",
        help="path to the .env holding CWA_API_KEY (online mode)",
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        default=str(config.DB_PATH),
        metavar="PATH",
        help="SQLite database path to write",
    )
    parser.add_argument(
        "--acquired-at",
        dest="acquired_at",
        metavar="ISO8601",
        help=(
            "offline mode: the acquisition time to record (ISO 8601 +08:00). "
            "Overrides the provenance sidecar; required if no sidecar exists."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code (0 ok, non-zero on failure)."""
    args = build_parser().parse_args(argv)
    try:
        if args.from_json:
            return run_offline(
                json_path=args.from_json,
                db_path=args.db_path,
                acquired_at=args.acquired_at,
            )
        return run_online(
            env_path=args.env_path, raw_out=args.raw_out, db_path=args.db_path
        )
    except (FetchError, DeriveError, ProvenanceError) as exc:
        # Messages are constructed to never contain the key.
        print(f"Ingestion failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
