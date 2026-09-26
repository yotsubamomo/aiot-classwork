"""Static guards for the Forecast chart's range band and weekly extremes
(WI-UI-POLISH-1 B5 / B6).

Offline and browser-free, like ``test_fence_frontend.py``: they read the frontend
source text. They lock:

* B5 — the MinT–MaxT band is one polygon built from the same series values the
  lines use (MaxT left to right, then MinT right to left), drawn under the lines,
  never taking the pointer, with no paint-server / url() reference;
* B6 — exactly two marks, the week's highest MaxT and lowest MinT, chosen by the
  same rule as the Weekly summary (first strict extreme); the summary rule itself
  is unchanged; their value uses the table's number format; no other point is
  labelled;
* the lines stay straight polylines, and the per-date hit targets are still drawn
  last (on top), so hover and the tooltip are not taken over by the new marks.
"""

from __future__ import annotations

from pathlib import Path

from tests.test_map_frontend import _function_body, _strip_comments

_STATIC = Path(__file__).resolve().parent.parent / "static"
_JS = (_STATIC / "app.js").read_text(encoding="utf-8")
_CSS = (_STATIC / "styles.css").read_text(encoding="utf-8")


def _body(name: str) -> str:
    return _strip_comments(_function_body(_JS, name))


def test_range_band_is_one_polygon_from_the_series_under_the_lines() -> None:
    band = _body("rangeBand")
    assert 'svgEl("polygon", { class: "chart__band"' in band
    assert "yAt(r.maxt)" in band and "yAt(r.mint)" in band and ".reverse()" in band
    assert "url(" not in band and "Gradient" not in band
    chart = _body("renderChart")
    i_band = chart.index("rangeBand(series, xAt, yAt)")
    assert i_band < chart.index('polyline(series, "maxt"') and i_band < chart.index('polyline(series, "mint"')
    assert ".chart__band, .chart__extreme { pointer-events: none; }" in _CSS


def test_extremes_follow_the_weekly_summary_rule() -> None:
    summary = _body("renderSummary")
    # the Weekly summary rule is unchanged: the first strict extreme
    assert "var minRow = series[0];" in summary and "var maxRow = series[0];" in summary
    assert "if (r.mint < minRow.mint) minRow = r;" in summary
    assert "if (r.maxt > maxRow.maxt) maxRow = r;" in summary
    chart = _body("renderChart")
    assert "var minI = 0;" in chart and "var maxI = 0;" in chart
    assert "if (r.mint < series[minI].mint) minI = i;" in chart
    assert "if (r.maxt > series[maxI].maxt) maxI = i;" in chart
    assert chart.count("extremeMark(") == 2
    assert '"maxt", series[maxI].maxt' in chart and '"mint", series[minI].mint' in chart


def test_only_the_two_extremes_carry_a_value_label() -> None:
    mark = _body("extremeMark")
    assert mark.count('svgEl("text"') == 1
    assert 'label.textContent = formatTemp(value) + "°";' in mark, "same number format as the table / summary"
    assert 'svgEl("text"' not in _body("dot"), "no per-point value labels"
    chart = _body("renderChart")
    # renderChart itself still creates only the axis texts: y ticks, y title, x ticks, x title
    assert chart.count('svgEl("text"') == 4 and "chart__extreme-label" not in chart


def test_lines_stay_straight_and_hit_targets_stay_on_top() -> None:
    line = _body("polyline")
    assert 'svgEl("polyline"' in line and "path" not in line
    chart = _body("renderChart")
    last_mark = max(chart.index("rangeBand("), chart.rindex("extremeMark("))
    assert chart.index('class: "chart__hit"') > last_mark
    assert 'hit.addEventListener("mouseenter"' in chart and 'hit.addEventListener("mousemove"' in chart
