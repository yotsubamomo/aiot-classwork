"""Representative station per county for the Now mode's Taiwan-wide view.

SPEC-V2 R-V2-DD-2 / R-V2-DD-3 (Issue #36). On the Taiwan-wide view the Now mode
shows **at most one marker per county**: the air temperature of one
*representative* valid station. The marker is a station value — never a county
value, average or aggregate (INV-V2-5, H-3).

The rule (documented in the README section "Representative station rule" so a
reader can recompute it by hand from a ``/api/observations/latest`` response):

1. **Candidates** of a county are the response's valid stations (every station
   in ``stations[]`` is valid, R-V2-OBS-2) whose ``countyName`` is that county
   and whose WGS84 position lies inside :data:`MAP_RANGE` (bounds inclusive).
   Stations outside that range — for example 高雄市's 東沙島 — are never
   representatives, because they are not placed on the Taiwan map.
2. If the county's **preferred station** (:data:`PREFERRED_STATION`, static
   project data) is a candidate, it is the representative.
3. Otherwise (**fallback**) the candidate with the smallest ``stationId`` in plain
   character-code order is the representative (``"466920" < "C0A980"``).
4. A county with no candidate has **no** representative (no marker; not a
   failure).

The selection depends only on the current valid stations and the static
preference data, so the same station set always gives the same result
(deterministic, R-V2-DD-3(a)(b)); a preferred station that is invalid this hour
falls back by rule 3 (R-V2-DD-3(c)).

:data:`PREFERRED_STATION` is **HOW data, not a contract** (R-V2-DD-3(f)): for each
county it names a lowland station in the county's seat or named after the
county or its seat —
the CWA manned weather station there when one exists (for example 臺北 for
臺北市), otherwise an automatic station in the seat's town (for example 太保
for 嘉義縣). The README describes this principle and works examples; it does not
enumerate the 22 identifiers.

This module is pure (standard library only, no I/O, no SQL, no HTTP client, no
key); :mod:`observation` calls it when it builds a success body.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

# The 22 counties in a fixed display order: the V1 Region order (R-DER-5 member
# counties, north → south → east) followed by the three outlying-island
# counties (R-V2-DD-1). The order only fixes the order of the returned list.
COUNTY_ORDER: tuple[str, ...] = (
    "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣",
    "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣",
    "臺南市", "高雄市", "屏東縣",
    "宜蘭縣",
    "花蓮縣",
    "臺東縣",
    "澎湖縣", "金門縣", "連江縣",
)

# The useful Taiwan map range (SPEC-V2 §5.3 instrument "E": main island and the
# main outlying islands incl. 金門, 連江, 澎湖, 蘭嶼, 綠島), bounds inclusive.
MAP_RANGE: Mapping[str, tuple[float, float]] = {
    "latitude": (21.2, 26.7),
    "longitude": (117.6, 122.9),
}

# Static preference data (HOW, not contract): county -> preferred StationId.
# Principle: a lowland station in the county's seat or named after the county
# or its seat; the CWA
# manned station when there is one, else an automatic station in the seat town.
PREFERRED_STATION: Mapping[str, str] = {
    "基隆市": "466940",  # 基隆 (manned)
    "臺北市": "466920",  # 臺北 (manned)
    "新北市": "466881",  # 新北, named after the county (manned)
    "桃園市": "C2C480",  # 桃園, 桃園區 (automatic)
    "新竹市": "C0D660",  # 新竹市東區 (automatic)
    "新竹縣": "467571",  # 新竹, 竹北市 (manned)
    "苗栗縣": "C0E750",  # 苗栗, 苗栗市 (automatic)
    "臺中市": "467490",  # 臺中 (manned)
    "彰化縣": "A0G720",  # 彰師大, 彰化市 (automatic)
    "南投縣": "C0I460",  # 南投, 南投市 (automatic)
    "雲林縣": "C0K400",  # 斗六, 斗六市 (automatic)
    "嘉義市": "467480",  # 嘉義 (manned)
    "嘉義縣": "C0M680",  # 太保, 太保市 (automatic)
    "臺南市": "467410",  # 臺南 (manned)
    "高雄市": "467441",  # 高雄 (manned)
    "屏東縣": "C2R170",  # 屏東, 屏東市 (automatic)
    "宜蘭縣": "467080",  # 宜蘭 (manned)
    "花蓮縣": "466990",  # 花蓮 (manned)
    "臺東縣": "467660",  # 臺東 (manned)
    "澎湖縣": "467350",  # 澎湖, 馬公市 (manned)
    "金門縣": "467110",  # 金門 (manned)
    "連江縣": "467990",  # 馬祖 (manned)
}


def in_map_range(station: Mapping[str, Any]) -> bool:
    """Whether a station's WGS84 position lies inside :data:`MAP_RANGE`."""
    lat = station.get("latitude")
    lon = station.get("longitude")
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False
    lat_lo, lat_hi = MAP_RANGE["latitude"]
    lon_lo, lon_hi = MAP_RANGE["longitude"]
    return lat_lo <= lat <= lat_hi and lon_lo <= lon <= lon_hi


def select_representatives(
    stations: Iterable[Mapping[str, Any]],
    preferred: Mapping[str, str] = PREFERRED_STATION,
) -> list[str]:
    """Return the representative ``stationId`` of each county that has one.

    ``stations`` are normalised **valid** stations (the success body's
    ``stations[]``). The result lists at most one id per county, in
    :data:`COUNTY_ORDER`; counties without a candidate are absent.
    """
    candidates: dict[str, list[str]] = {county: [] for county in COUNTY_ORDER}
    for station in stations:
        county = station.get("countyName")
        station_id = station.get("stationId")
        if county not in candidates or not isinstance(station_id, str) or not station_id:
            continue
        if in_map_range(station):
            candidates[county].append(station_id)

    chosen: list[str] = []
    for county in COUNTY_ORDER:
        ids = candidates[county]
        if not ids:
            continue  # rule 4: no candidate, no representative
        wanted = preferred.get(county)
        chosen.append(wanted if wanted in ids else min(ids))  # rules 2 and 3
    return chosen
