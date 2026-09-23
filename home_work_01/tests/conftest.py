"""Shared pytest fixtures and fixture-mutation helpers.

The whole suite is offline: it reads only the committed JSON fixture, never the
network and never ``.env`` (R-TC-5). Negative-case inputs are derived from the
positive fixture by the mutators below (DR-10).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "F-D0047-091_sample.json"

TEMPERATURE_ELEMENTS = ("最高溫度", "最低溫度")


@pytest.fixture
def sample_response() -> dict:
    """A fresh deep copy of the real F-D0047-091 fixture for each test."""
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


# --- mutators (return a new mutated copy; never touch the input) ----------------


def _counties(data: dict) -> list[dict]:
    return data["records"]["Locations"][0]["Location"]


def _temp_elements(county: dict) -> list[dict]:
    return [
        e
        for e in county["WeatherElement"]
        if e.get("ElementName") in TEMPERATURE_ELEMENTS
    ]


def remove_county(data: dict, name: str) -> dict:
    """AC-09(1): drop a member county entirely."""
    out = copy.deepcopy(data)
    block = out["records"]["Locations"][0]
    block["Location"] = [c for c in block["Location"] if c["LocationName"] != name]
    return out


def remove_half_day(data: dict, name: str, date: str, hour: int) -> dict:
    """AC-09(2): drop one 12-hour period for one county-day."""
    out = copy.deepcopy(data)
    prefix = f"{date}T{hour:02d}"
    for county in _counties(out):
        if county["LocationName"] != name:
            continue
        for element in _temp_elements(county):
            element["Time"] = [
                t for t in element["Time"] if not t["StartTime"].startswith(prefix)
            ]
    return out


def corrupt_value(
    data: dict, name: str, date: str, hour: int, bad_value: str = "-"
) -> dict:
    """AC-09(3): replace one county-day value with an invalid token."""
    out = copy.deepcopy(data)
    prefix = f"{date}T{hour:02d}"
    for county in _counties(out):
        if county["LocationName"] != name:
            continue
        for element in _temp_elements(county):
            field = (
                "MinTemperature"
                if element["ElementName"] == "最低溫度"
                else "MaxTemperature"
            )
            for t in element["Time"]:
                if t["StartTime"].startswith(prefix):
                    t["ElementValue"][0][field] = bad_value
    return out


def remove_day(data: dict, date: str) -> dict:
    """AC-09(4): drop a whole Forecast Day so only six complete days remain."""
    out = copy.deepcopy(data)
    for county in _counties(out):
        for element in _temp_elements(county):
            element["Time"] = [
                t for t in element["Time"] if t["StartTime"][:10] != date
            ]
    return out


def shift_day(data: dict, old_date: str, new_date: str) -> dict:
    """AC-09(5): relabel a day's periods to open a gap (non-consecutive week)."""
    out = copy.deepcopy(data)
    for county in _counties(out):
        for element in _temp_elements(county):
            for t in element["Time"]:
                if t["StartTime"][:10] == old_date:
                    t["StartTime"] = t["StartTime"].replace(old_date, new_date, 1)
    return out
