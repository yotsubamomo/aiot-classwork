"""Representative station per county (Issue #36; SPEC-V2 R-V2-DD-2, R-V2-DD-3,
AC-V2-11).

Fully offline: every case starts from the committed sanitised real sample
``fixtures/O-A0001-001_sample.json`` (Issue #35) and derives its counter-examples
from it. The expected station ids below were computed by hand from that sample
with the README rule ("Representative station rule"): candidates = the county's
valid stations inside the map range; the preferred station if it is a candidate,
else the smallest ``stationId`` in character-code order; none -> no marker.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import observation as obs
import representative as rep
from server import create_app

UNIT_DIR = Path(__file__).resolve().parent.parent
SAMPLE_PATH = Path(__file__).parent / "fixtures" / "O-A0001-001_sample.json"
README = UNIT_DIR / "README.md"
SPEC_V2 = UNIT_DIR / "doc" / "spec" / "SPEC-V2.md"
TAIPEI = timezone(timedelta(hours=8))
T0 = datetime(2026, 9, 26, 0, 10, 5, tzinfo=TAIPEI)

# Hand-computed from the sample: in the unmodified sample every county's
# preferred station is valid and inside the map range, so it is chosen.
EXPECTED_SAMPLE = {
    "臺北市": "466920",  # 臺北
    "新竹市": "C0D660",  # 新竹市東區
    "嘉義縣": "C0M680",  # 太保
    "高雄市": "467441",  # 高雄
    "連江縣": "467990",  # 馬祖
}

# Hand-computed fallbacks after the preferred station is made invalid: the
# smallest stationId among the remaining valid in-range stations of the county.
EXPECTED_FALLBACK = {
    "臺北市": "466910",  # 鞍部 ("466910" < "466930" < "A0A010" ...)
    "南投縣": "42HA10",  # 萬大發電廠 ("42HA10" < "467550" ...)
    "嘉義縣": "467530",  # 阿里山
    # 高雄市: "468100" 東沙島 (lon 116.73) is outside the map range, so the
    # next smallest id is chosen.
    "高雄市": "72V140",  # 高改旗南分場
}


@pytest.fixture
def sample() -> dict:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def raw_stations(payload: dict) -> list[dict]:
    return payload["records"]["Station"]


def normalised(payload: dict) -> list[dict]:
    return obs.normalize(payload).stations


def county_of(stations: list[dict]) -> dict[str, str]:
    return {s["stationId"]: s["countyName"] for s in stations}


def invalidate(payload: dict, station_id: str) -> None:
    """Give the raw record the -99 air-temperature sentinel (-> invalid station)."""
    for record in raw_stations(payload):
        if record["StationId"] == station_id:
            record["WeatherElement"]["AirTemperature"] = "-99"
            return
    raise AssertionError(f"{station_id} not in sample")


# --- the rule on the real sample ------------------------------------------------


def test_at_most_one_valid_representative_per_county(sample) -> None:
    stations = normalised(sample)
    chosen = rep.select_representatives(stations)
    counties = county_of(stations)
    assert all(sid in counties for sid in chosen), "a representative is not a valid station"
    chosen_counties = [counties[sid] for sid in chosen]
    assert len(chosen_counties) == len(set(chosen_counties)), "two markers for one county"
    # all 22 counties have valid in-range stations in the sample
    assert set(chosen_counties) == obs.COUNTIES
    # ordered by the fixed county order
    assert chosen_counties == [c for c in rep.COUNTY_ORDER if c in set(chosen_counties)]


def test_hand_computed_representatives_on_the_sample(sample) -> None:
    stations = normalised(sample)
    counties = county_of(stations)
    chosen = {counties[sid]: sid for sid in rep.select_representatives(stations)}
    for county, expected in EXPECTED_SAMPLE.items():
        assert chosen[county] == expected, county
    # with the unmodified sample every county gets its preferred station
    assert chosen == dict(rep.PREFERRED_STATION)


def test_selection_is_deterministic(sample) -> None:
    stations = normalised(sample)
    first = rep.select_representatives(stations)
    assert rep.select_representatives(stations) == first
    # independent of the order the stations arrive in
    assert rep.select_representatives(list(reversed(stations))) == first
    assert rep.select_representatives(sorted(stations, key=lambda s: s["stationName"] or "")) == first


def test_fallback_when_preferred_stations_are_invalid(sample) -> None:
    """AC-V2-11: >= 3 counties' chosen stations made invalid -> each falls back to
    another valid station of the same county; every other county is unchanged."""
    before_stations = normalised(sample)
    before = {county_of(before_stations)[s]: s for s in rep.select_representatives(before_stations)}
    for county in EXPECTED_FALLBACK:
        invalidate(sample, rep.PREFERRED_STATION[county])
    after_stations = normalised(sample)
    after = {county_of(after_stations)[s]: s for s in rep.select_representatives(after_stations)}
    for county, expected in EXPECTED_FALLBACK.items():
        assert after[county] == expected, county
        assert after[county] != rep.PREFERRED_STATION[county]
        assert county_of(after_stations)[after[county]] == county
    for county in set(before) - set(EXPECTED_FALLBACK):
        assert after[county] == before[county], county


def test_fallback_never_uses_a_station_outside_the_map_range(sample) -> None:
    invalidate(sample, rep.PREFERRED_STATION["高雄市"])
    stations = normalised(sample)
    by_id = {s["stationId"]: s for s in stations}
    assert "468100" in by_id and not rep.in_map_range(by_id["468100"])  # 東沙島 is valid
    for sid in rep.select_representatives(stations):
        assert rep.in_map_range(by_id[sid]), sid


def test_county_with_no_valid_station_has_no_representative(sample) -> None:
    for record in raw_stations(sample):
        if record["GeoInfo"]["CountyName"] == "連江縣":
            record["WeatherElement"]["AirTemperature"] = "X"
    stations = normalised(sample)
    chosen_counties = {county_of(stations)[s] for s in rep.select_representatives(stations)}
    assert "連江縣" not in chosen_counties
    assert chosen_counties == obs.COUNTIES - {"連江縣"}


def test_rule_ignores_unknown_counties_and_missing_ids() -> None:
    stations = [
        {"stationId": "B", "countyName": "臺北市", "latitude": 25.0, "longitude": 121.5},
        {"stationId": "A", "countyName": "臺北市", "latitude": 25.0, "longitude": 121.5},
        {"stationId": "Z", "countyName": "東京都", "latitude": 25.0, "longitude": 121.5},
        {"stationId": "", "countyName": "臺中市", "latitude": 24.1, "longitude": 120.7},
        {"stationId": "Q", "countyName": "臺中市", "latitude": None, "longitude": 120.7},
    ]
    assert rep.select_representatives(stations, preferred={}) == ["A"]
    assert rep.select_representatives(stations, preferred={"臺北市": "B"}) == ["B"]
    assert rep.select_representatives(stations, preferred={"臺北市": "missing"}) == ["A"]


# --- static preference data (HOW data, R-V2-DD-3(f)) ----------------------------


def test_preference_data_covers_exactly_the_22_counties() -> None:
    assert set(rep.COUNTY_ORDER) == obs.COUNTIES
    assert len(rep.COUNTY_ORDER) == 22
    assert set(rep.PREFERRED_STATION) == obs.COUNTIES
    assert all(isinstance(v, str) and v for v in rep.PREFERRED_STATION.values())


def test_preferred_stations_are_valid_in_range_and_in_their_county_in_the_sample(sample) -> None:
    by_id = {s["stationId"]: s for s in normalised(sample)}
    for county, sid in rep.PREFERRED_STATION.items():
        assert sid in by_id, f"{county}: preferred {sid} not valid in the sample"
        assert by_id[sid]["countyName"] == county
        assert rep.in_map_range(by_id[sid])


def test_readme_and_spec_do_not_enumerate_the_preference_ids() -> None:
    """AC-V2-11: neither the Spec nor the README carries a list of the 22
    StationIds as a contract. The README may use a few ids in worked examples."""
    ids = set(rep.PREFERRED_STATION.values())
    for path, limit in ((README, 4), (SPEC_V2, 0)):
        text = path.read_text(encoding="utf-8")
        found = {i for i in ids if re.search(r"(?<![0-9A-Za-z])" + re.escape(i) + r"(?![0-9A-Za-z])", text)}
        assert len(found) <= limit, f"{path.name} enumerates preference ids: {sorted(found)}"


# --- the /api/ response ---------------------------------------------------------


def test_api_success_body_lists_the_representatives(sample) -> None:
    payload = json.dumps(sample, ensure_ascii=False).encode("utf-8")

    class Upstream:
        def __call__(self, url, headers=None, params=None, timeout=None):
            class R:
                status_code = 200
                content = payload

                def close(self):
                    pass
            return R()

    service = obs.LatestObservationService(
        env={"CWA_API_KEY": "SENTINEL-not-a-key"}, clock=lambda: T0, http_get=Upstream()
    )
    client = create_app(observation_service=service).test_client()
    body = client.get("/api/observations/latest").get_json()
    stations = body["stations"]
    assert body["representativeStationIds"] == rep.select_representatives(stations)
    assert len(body["representativeStationIds"]) == 22
    ids = {s["stationId"] for s in stations}
    assert set(body["representativeStationIds"]) <= ids
