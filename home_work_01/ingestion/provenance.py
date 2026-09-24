"""Acquisition-time provenance for a saved raw JSON (DR-17).

The ingestion timestamp (`IngestionMetadata.ingestedAt`) means the **acquisition
time**: the local time the raw JSON was fetched from CWA, not the time the snapshot
rows were (re)built. Because the F-D0047-091 response carries no acquisition or
publish time (DR-17 E-5), the online run records that time in a small **provenance
sidecar** next to the saved raw JSON, and the offline rebuild reads it back instead
of reading the clock.

The sidecar:

* never alters the raw JSON (R-ING-4 / AC-25 keep the raw response byte-complete);
* stays in the unit directory next to the raw JSON;
* contains no key, ``Authorization`` header, or any request header (R-SEC-2 / H-1);
  it is a scan target for the secret checks.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import config
from .acquisition_time import validate_acquisition_time


class ProvenanceError(RuntimeError):
    """Missing or unreadable acquisition-time provenance for an offline rebuild.

    Raised so the offline path fails closed (non-zero exit, no database write)
    rather than inventing a timestamp (DR-17 §4.3).
    """


def provenance_path(raw_path: str | Path) -> Path:
    """The sidecar path for a raw JSON: ``X.json`` -> ``X.meta.json``."""
    return Path(raw_path).with_suffix(".meta.json")


def write_provenance(
    raw_path: str | Path,
    acquired_at: str,
    source_dataset_id: str = config.RESOURCE_ID,
) -> Path:
    """Write the provenance sidecar for a saved raw JSON and return its path."""
    path = provenance_path(raw_path)
    record = {
        "sourceDatasetId": source_dataset_id,
        "acquiredAt": acquired_at,
        "rawJson": Path(raw_path).name,
        "note": (
            "acquiredAt is the local time (ISO 8601 +08:00) this raw JSON was "
            "fetched from CWA, after the success/resource_id checks passed. Offline "
            "rebuilds reuse this value and do not update it. No credentials here."
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return path


def read_acquisition_time(raw_path: str | Path) -> str:
    """Return the acquisition time recorded for a saved raw JSON.

    Raises :class:`ProvenanceError` if the sidecar is missing, unreadable, or has no
    ``acquiredAt`` key (behaviour and messages unchanged — DR-22.3 AT-9). If the key
    is present, its value is validated against the exact acquisition-time format
    (DR-22.3 AT-1/AT-2): a non-string or malformed value is rejected — never coerced
    with ``str()`` — and raises :class:`~ingestion.acquisition_time.AcquisitionTimeError`
    naming the sidecar file, the ``acquiredAt`` field, and (for a non-string) the JSON
    type. Both errors let the offline path fail closed (non-zero exit, no database
    write) rather than record a malformed "last updated" value (DR-17 §4.3).
    """
    path = provenance_path(raw_path)
    if not path.is_file():
        raise ProvenanceError(
            f"no acquisition-time provenance found for {raw_path} "
            f"(expected {path.name}); provide one or pass --acquired-at"
        )
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ProvenanceError(
            f"provenance record {path.name} could not be read: {exc}"
        ) from exc
    if not isinstance(record, dict) or "acquiredAt" not in record:
        raise ProvenanceError(
            f"provenance record {path.name} has no 'acquiredAt' value"
        )
    return validate_acquisition_time(
        record["acquiredAt"],
        source=f"the {path.name} 'acquiredAt' field",
    )
