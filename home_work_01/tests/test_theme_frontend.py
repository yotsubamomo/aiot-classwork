"""Static guards for the page's light / dark switch (WI-UI-THEME-1).

Offline and browser-free: they read the frontend source text. They lock:

* the forced-dark token block (``:root[data-theme="dark"]``) carries exactly the
  same declarations as the system-dark block, so the two themes cannot drift;
* ``theme.js`` is loaded in <head> before the stylesheets (a saved choice applies
  before the first paint), stores only ``dark`` / ``light`` in localStorage inside
  try / catch, makes no request, and reports the state with ``aria-pressed``;
* the switch is a real button after the mode switch in the DOM, so the mode switch
  stays the first Tab stop (AC-V2-01's keyboard check is unchanged), with a
  visible "Dark mode" label and a >= 44 x 44 target;
* the Taiwan Map card keeps its own dark tokens (P-1): the switch changes the page
  tokens only.
"""

from __future__ import annotations

import re
from pathlib import Path

_STATIC = Path(__file__).resolve().parent.parent / "static"
_CSS = (_STATIC / "styles.css").read_text(encoding="utf-8")
_HTML = (_STATIC / "index.html").read_text(encoding="utf-8")
_THEME = (_STATIC / "theme.js").read_text(encoding="utf-8")


def _decls(block: str) -> list[str]:
    return sorted(line.strip() for line in block.strip().splitlines() if line.strip())


def test_forced_dark_tokens_equal_the_system_dark_tokens() -> None:
    system = re.search(r'@media \(prefers-color-scheme: dark\) \{\n  :root:not\(\[data-theme="light"\]\) \{\n(.*?)\n  \}\n\}',
                       _CSS, re.S)
    forced = re.search(r'\n:root\[data-theme="dark"\] \{\n(.*?)\n\}', _CSS, re.S)
    assert system and forced
    assert _decls(system.group(1)) == _decls(forced.group(1))
    assert "color-scheme: dark;" in forced.group(1)


def test_theme_script_runs_in_head_before_the_stylesheets() -> None:
    head = _HTML[:_HTML.index("</head>")]
    assert '<script src="/static/theme.js"></script>' in head
    assert head.index("/static/theme.js") < head.index('href="/static/styles.css"')


def test_theme_script_stores_only_the_choice_and_makes_no_request() -> None:
    assert 'var KEY = "hw01-theme";' in _THEME
    assert 'value === "dark" || value === "light" ? value : null' in _THEME
    assert _THEME.count("try {") == 2 and _THEME.count("catch (e)") == 2, "storage access is guarded"
    assert 'root.setAttribute("data-theme", next);' in _THEME
    assert 'button.setAttribute("aria-pressed"' in _THEME
    for banned in ("fetch(", "XMLHttpRequest", "http://", "https://", "sendBeacon", "document.cookie"):
        assert banned not in _THEME, banned


def test_switch_is_a_labelled_button_after_the_mode_switch() -> None:
    body = _HTML[_HTML.index("<body>"):]
    assert re.search(r'<button type="button" id="theme-toggle" class="theme-toggle" aria-pressed="false">', body)
    assert '<span class="theme-toggle__label">Dark mode</span>' in body
    # the mode switch is still the first focusable control of the page
    first = re.search(r"<(button|select|a|input)\b[^>]*>", body)
    assert first and 'id="mode-now"' in first.group(0)
    assert body.index('id="mode-forecast"') < body.index('id="theme-toggle"') < body.index('id="map-frame"')
    rule = _CSS[_CSS.index(".theme-toggle {"):]
    rule = rule[:rule.index("}")]
    assert "min-height: 44px;" in rule and "min-width: 44px;" in rule


def test_map_card_keeps_its_own_dark_tokens() -> None:
    card = _CSS[_CSS.index("\n.map-card {\n  --surface:"):]
    card = card[:card.index("}")]
    for token in ("--surface: #1c2738;", "--text: var(--map-text);", "--heading: var(--map-heading);"):
        assert token in card
