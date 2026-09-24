/* Taiwan Weather Forecast — dashboard frontend (Issues #23 UI/UX + #24 map,
 * reworked in #28).
 *
 * All data comes from THIS application's own JSON API under the "/api/" prefix
 * (R-DS-5, R-SHR-5, AC-04(b)); the browser never calls CWA and holds no key.
 * The page bootstraps from /api/health, populates "Select Region" from
 * /api/regions, and for the selected Region draws a MaxT / MinT seven-day line
 * chart (hand-drawn inline SVG, no chart library) with a legend, axis labels and
 * an interactive hover tooltip, a Date / MinT / MaxT table whose seven rows equal
 * data.db, and a weekly summary (lowest MinT / highest MaxT) derived in the
 * browser from the same /api/ series — no new business logic (INV-2, AC-04(b)).
 *
 * "Select Date" (the seven Forecast Days from /api/days, default first) lives in
 * the Taiwan Map's floating info panel (#28). The Taiwan Map is drawn with
 * vendored Leaflet on a vendored VECTOR basemap (window.TAIWAN_BASEMAP, a
 * same-origin <script>, no fetch, no tiles), so it makes no external request and
 * needs no key (R-EN-6). Its six Region markers are temperature "pills" whose
 * TEXT (the day's derivedMapTemperature to one decimal) and COLOUR (the day's
 * colourBand) come straight from /api/days/<date>; the frontend re-derives
 * nothing and re-bands nothing (H-3 single-sourced, R-SHR-4). oneDp/toFixed(1) is
 * display formatting only.
 *
 * State mapping is DR-19 (decision-20260924-dashboard-state-mapping):
 *   - loading : a request is in flight (page-level for /api/health -> /api/regions;
 *               inline in the chart card for a per-Region /series request, and
 *               inline in the map card for the /api/days requests);
 *   - error   : a request FAILED — a network failure, an unparseable response, OR
 *               ANY non-2xx (503 missing/empty/incomplete, 500/502/504, 404). The
 *               server's `error` message is surfaced so those causes stay distinct.
 *               A snapshot-unavailable 503 is ALWAYS error, never empty;
 *   - empty   : a request SUCCEEDED (2xx) but there is nothing to render —
 *               /api/regions with an empty list (page-level), /series with an empty
 *               series (inline in the chart card), or /api/days[/<date>] with no
 *               days/values (inline in the map card) — always a message, never a
 *               blank card.
 * The map-card inline status overlays ONLY the map, never the info panel, so
 * "Select Date" stays visible and operable — the user can switch to a working day
 * to recover from an inline error/empty (DR-19, #28 P-7b).
 */
"use strict";

(function () {
  var els = {};
  var chartState = null;   // geometry + series for the hover tooltip
  var currentSeries = null; // last-rendered series, for responsive re-draw
  var resizeTimer = null;

  // --- Taiwan Map (R-EN-3..R-EN-7) -------------------------------------------
  // The six Region names in the canonical order (matches /api/regions and the
  // shared module's R-SHR-2(b)); used to iterate markers deterministically.
  var REGION_ORDER = [
    "北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區",
  ];

  // Project-defined representative points [lat, lng] for each Region marker
  // (R-EN-4: coordinates are HOW; README notes they are project-defined, not a CWA
  // authority). 北部 / 東北部 are nudged apart (vs. #24's 25.03,121.50 /
  // 24.72,121.74) so the two pills never overlap at the 375px initial zoom. Each
  // point lies within a member county of its Region. fitBounds over these keeps
  // the map centred on Taiwan with all six markers visible (R-EN-4).
  var REGION_POINTS = {
    "北部地區": [25.12, 121.38],
    "中部地區": [24.15, 120.68],
    "南部地區": [22.85, 120.35],
    "東北部地區": [24.66, 121.80],
    "東部地區": [23.98, 121.55],
    "東南部地區": [22.80, 121.10],
  };

  // Colour per Derived Map Temperature band. The band comes straight from the
  // /api/days/<date> endpoint (R-SHR-4 / DR-4 owns the derivation and banding in
  // the shared module); the frontend re-derives nothing (H-3 single-sourced) and
  // only maps the band NAME to a fill colour. The legend swatches are painted from
  // this same map so the legend always matches the pills (R-EN-5, AC-17). The four
  // tokens are the blue / green / yellow / red family named by R-SHR-4.
  var BAND_COLOURS = {
    blue: "#2b6cb0",
    green: "#2f855a",
    yellow: "#d69e2e",
    red: "#c53030",
  };
  // Pill text colour per band: the yellow band uses dark text for contrast, the
  // rest use white (both meet WCAG AA against their band fill — see worklog V-2).
  var BAND_TEXT = {
    blue: "#ffffff",
    green: "#ffffff",
    yellow: "#1a2230",
    red: "#ffffff",
  };

  var map = null;          // the Leaflet map, created once (when the map has size)
  var markers = {};        // Region name -> L.marker (pill divIcon)
  var mapReqSeq = 0;       // latest /api/days/<date> request wins (out-of-order)
  var selectedRegion = "北部地區"; // the Region shown in the info panel's selected block
  var latestDay = null;    // {date, byRegion} for the day currently rendered/pending
  var mapInitScheduled = false;

  document.addEventListener("DOMContentLoaded", function () {
    els.pageError = document.getElementById("page-error");
    els.pageErrorText = document.getElementById("page-error-text");
    els.pageLoading = document.getElementById("page-loading");
    els.pageEmpty = document.getElementById("page-empty");
    els.pageEmptyText = document.getElementById("page-empty-text");
    els.dashboard = document.getElementById("dashboard");
    els.regionSelect = document.getElementById("region-select");
    els.ingestionTime = document.getElementById("ingestion-time");
    els.summary = document.getElementById("summary");
    els.summaryMinValue = document.getElementById("summary-min-value");
    els.summaryMinDay = document.getElementById("summary-min-day");
    els.summaryMaxValue = document.getElementById("summary-max-value");
    els.summaryMaxDay = document.getElementById("summary-max-day");
    els.panel = document.getElementById("region-panel");
    els.panelHeading = document.getElementById("panel-heading");
    els.chartStatus = document.getElementById("chart-status");
    els.chart = document.getElementById("chart");
    els.chartTooltip = document.getElementById("chart-tooltip");
    els.tableBody = document.getElementById("table-body");
    // Select Date + Taiwan Map info panel (#28).
    els.dateSelect = document.getElementById("date-select");
    els.mapCaption = document.getElementById("map-caption");
    els.mapStatus = document.getElementById("map-status");
    els.mapFrame = document.getElementById("map-frame");
    els.mapForecastDay = document.getElementById("map-forecast-day");
    els.tileMaxValue = document.getElementById("tile-max-value");
    els.tileMaxRegion = document.getElementById("tile-max-region");
    els.tileMinValue = document.getElementById("tile-min-value");
    els.tileMinRegion = document.getElementById("tile-min-region");
    els.selRegion = document.getElementById("sel-region");
    els.selDate = document.getElementById("sel-date");
    els.selMin = document.getElementById("sel-min");
    els.selMax = document.getElementById("sel-max");
    els.selDerived = document.getElementById("sel-derived");

    els.regionSelect.addEventListener("change", function () {
      loadRegion(els.regionSelect.value);
    });
    els.dateSelect.addEventListener("change", function () {
      loadDay(els.dateSelect.value);
    });

    // Redraw the chart at the new width on resize (the SVG is drawn at the
    // container's own pixel width so its labels stay legible) and drop any open
    // tooltip so its pixel maths never goes stale. Also keep Leaflet in sync.
    window.addEventListener("resize", function () {
      hideTooltip();
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (currentSeries) renderChart(currentSeries);
        // Re-fit the map: the panel/legend layout (floating vs stacked) and the
        // reserved padding change with width, so the six markers must be re-fitted
        // to stay clear of the panels at the new width (#28 F-1). Only resize
        // re-fits — a Select Date change never does (P-12).
        if (map) fitToMarkers();
      }, 150);
    });

    // Colour the legend swatches up front so they show the four band colours even
    // before the first day loads / in the loading/empty/error states (#28 F-6).
    colourLegend();

    bootstrap();
  });

  // --- top-level page states -------------------------------------------------

  function showLoading() {
    els.pageLoading.hidden = false;
    els.pageError.hidden = true;
    els.pageEmpty.hidden = true;
    els.dashboard.hidden = true;
  }
  function showError(message) {
    els.pageErrorText.textContent = message;
    els.pageError.hidden = false;
    els.pageLoading.hidden = true;
    els.pageEmpty.hidden = true;
    els.dashboard.hidden = true;
  }
  function showEmpty(message) {
    els.pageEmptyText.textContent = message;
    els.pageEmpty.hidden = false;
    els.pageLoading.hidden = true;
    els.pageError.hidden = true;
    els.dashboard.hidden = true;
  }
  function showDashboard() {
    els.dashboard.hidden = false;
    els.pageLoading.hidden = true;
    els.pageError.hidden = true;
    els.pageEmpty.hidden = true;
  }

  // --- bootstrap: health -> regions -> first region --------------------------

  function bootstrap() {
    showLoading();
    fetchJson("/api/health")
      .then(function (res) {
        if (failed(res)) {
          // Any non-2xx (503 missing/empty/incomplete, 5xx, 404) or an
          // unparseable body is an error (DR-19); surface the server's message so
          // the cause stays visible.
          showError(reasonMessage(res.body));
          return;
        }
        showIngestionTime(res.body.ingestion_time);
        return loadRegions();
      })
      .catch(function () {
        showError(
          "Cannot reach the forecast service. Please check that the server is running and try again."
        );
      });
  }

  function loadRegions() {
    return fetchJson("/api/regions").then(function (res) {
      if (failed(res)) {
        showError(reasonMessage(res.body)); // failed request -> error (DR-19)
        return;
      }
      var regions = (res.body && res.body.regions) || [];
      if (!regions.length) {
        // Succeeded (2xx) but nothing to show -> empty (DR-19).
        showEmpty("No Regions are available in this snapshot.");
        return;
      }
      populateRegions(regions);
      showDashboard();
      // Default to the first Region, but honour a ?region= deep link when it
      // names one of the six Regions (shareable per-Region URL).
      var wanted = new URLSearchParams(window.location.search).get("region");
      var initial = regions.indexOf(wanted) >= 0 ? wanted : regions[0];
      els.regionSelect.value = initial;
      loadRegion(initial);
      // Select Date + Taiwan Map load independently of the selected Region.
      loadDays();
    });
  }

  function populateRegions(regions) {
    els.regionSelect.innerHTML = "";
    regions.forEach(function (name) {
      var opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      els.regionSelect.appendChild(opt);
    });
  }

  // --- a selected Region: series -> chart + table + summary ------------------

  function loadRegion(region) {
    // Reveal the panel and set the heading up front so that EVERY outcome —
    // success, a 404/503 from /series, or a network error — renders inside a
    // visible panel (finding F-1 of #20, R-DS-6), and show an inline loading
    // state while the request is in flight (DR-19 per-Region loading).
    els.panel.hidden = false;
    els.panelHeading.textContent = "Temperature Forecast – " + region;
    setChartStatus("Loading " + region + "…", "loading");
    fetchJson("/api/regions/" + encodeURIComponent(region) + "/series")
      .then(function (res) {
        if (failed(res)) {
          // Failed request (404 / 503 / 5xx / unparseable) -> inline error (DR-19).
          els.summary.hidden = true;
          setChartStatus(
            res.status === 404
              ? "That Region is not available in this snapshot."
              : reasonMessage(res.body),
            "error"
          );
          return;
        }
        var series = (res.body && res.body.series) || [];
        if (!series.length) {
          // Succeeded but nothing to render -> inline empty, not a blank card.
          els.summary.hidden = true;
          setChartStatus("No forecast data for this Region yet.", "empty");
          return;
        }
        hideChartStatus();
        renderSummary(series);
        renderChart(series);
        renderTable(series);
      })
      .catch(function () {
        els.summary.hidden = true;
        setChartStatus(
          "Cannot load this Region right now. Please try again.",
          "error"
        );
      });
  }

  // --- Select Date + Taiwan Map (R-EN-3..R-EN-7) -----------------------------
  // Independent of the selected Region. /api/days fills Select Date (seven days,
  // ascending, default first); /api/days/<date> gives the six Regions' values for
  // the chosen day, each already carrying the Derived Map Temperature and its
  // colour band from the shared module — the frontend re-derives nothing.

  function loadDays() {
    setMapStatus("Loading the map…", "loading");
    return fetchJson("/api/days")
      .then(function (res) {
        if (failed(res)) {
          // No days to list: the map card shows an inline error; Select Date has
          // nothing to offer so it is disabled (DR-19, P-7b).
          setDateSelectEnabled(false);
          setMapStatus(reasonMessage(res.body), "error");
          return;
        }
        var days = (res.body && res.body.days) || [];
        if (!days.length) {
          setDateSelectEnabled(false);
          setMapStatus("No Forecast Days are available in this snapshot.", "empty");
          return;
        }
        populateDates(days);
        setDateSelectEnabled(true);
        var first = days[0];              // ascending; default the first day (R-EN-3)
        els.dateSelect.value = first;
        loadDay(first);
      })
      .catch(function () {
        setDateSelectEnabled(false);
        setMapStatus(
          "Cannot load the map right now. Please try again.",
          "error"
        );
      });
  }

  function populateDates(days) {
    els.dateSelect.innerHTML = "";
    days.forEach(function (date) {
      var opt = document.createElement("option");
      opt.value = date;
      opt.textContent = date;
      els.dateSelect.appendChild(opt);
    });
  }

  function setDateSelectEnabled(enabled) {
    if (els.dateSelect) els.dateSelect.disabled = !enabled;
  }

  function loadDay(date) {
    // Tag this request; if the user picks another date before it resolves, a
    // later request bumps mapReqSeq and this (stale/out-of-order) response is
    // ignored so it cannot overwrite the current day's pills/panel (#24 F-3).
    var seq = ++mapReqSeq;
    els.mapCaption.textContent = "Showing " + date;
    setMapStatus("Loading " + date + "…", "loading");
    return fetchJson("/api/days/" + encodeURIComponent(date))
      .then(function (res) {
        if (seq !== mapReqSeq) return; // superseded by a newer Select Date request
        if (failed(res)) {
          // 404 / 503 / 5xx / unparseable -> inline error (DR-19 per-Region rule).
          // The info panel (with Select Date) stays visible so the user can pick
          // another day and recover (P-7b).
          setMapStatus(
            res.status === 404
              ? "That date is not available in this snapshot."
              : reasonMessage(res.body),
            "error"
          );
          return;
        }
        var values = (res.body && res.body.values) || [];
        if (!values.length) {
          // Succeeded but nothing to render -> inline empty (DR-19).
          setMapStatus("No values are available for this date yet.", "empty");
          return;
        }
        hideMapStatus();
        applyDay(date, values);
      })
      .catch(function () {
        if (seq !== mapReqSeq) return; // superseded; do not clobber the current day
        setMapStatus(
          "Cannot load this date right now. Please try again.",
          "error"
        );
      });
  }

  // Render `date`'s six values: recolour/relabel the pills, refresh their
  // tooltips, and update the info panel (day tiles + selected-Region block).
  // Called only on a successful 2xx with values. The map view is NOT reset when
  // Select Date changes — only the pills/tooltips/panel update (AC-18, P-12).
  function applyDay(date, values) {
    var byRegion = {};
    values.forEach(function (v) { byRegion[v.regionName] = v; });
    latestDay = { date: date, byRegion: byRegion };

    // Bring up the map when its container actually has a non-zero size (init
    // hardening, P-12) — then render this day onto the pills.
    ensureMapSized(function () {
      if (!initMap()) {
        setMapStatus("The map library is unavailable.", "error");
        return;
      }
      renderDay(latestDay.date, latestDay.byRegion);
    });
  }

  function renderDay(date, byRegion) {
    els.mapForecastDay.textContent = date;

    // Day summary tiles: front-end max/min over the six endpoint values for the
    // day (same pattern as the weekly summary — no new business logic, R-EN-1(3),
    // R-SHR-1, INV-1). We compare the endpoint's own mint/maxt; nothing is derived.
    var hi = null, lo = null;
    REGION_ORDER.forEach(function (region) {
      var v = byRegion[region];
      if (!v) return;
      if (hi === null || v.maxt > hi.maxt) hi = v;
      if (lo === null || v.mint < lo.mint) lo = v;
    });
    if (hi) { els.tileMaxValue.textContent = oneDp(hi.maxt); els.tileMaxRegion.textContent = hi.regionName; }
    if (lo) { els.tileMinValue.textContent = oneDp(lo.mint); els.tileMinRegion.textContent = lo.regionName; }

    // Pills: TEXT = endpoint derivedMapTemperature (1dp display), COLOUR = endpoint
    // colourBand. No re-derivation, no re-banding (H-3, R-SHR-4).
    REGION_ORDER.forEach(function (region) {
      var marker = markers[region];
      var v = byRegion[region];
      if (!marker || !v) return;
      paintPill(marker, region, date, v);
      marker._dayInfo = { region: region, date: date, value: v };
    });

    highlightSelected();
    updateSelectedBlock(date, byRegion);
  }

  // Update one marker's pill element (text/colour/aria) and its hover tooltip.
  function paintPill(marker, region, date, v) {
    var el = marker.getElement();
    if (!el) return;
    var band = v.colourBand;
    var pill = el.querySelector(".pill");
    if (pill) {
      pill.textContent = oneDp(v.derivedMapTemperature) + "°";
      pill.className = "pill pill--" + band;
      pill.style.background = BAND_COLOURS[band] || "#888888";
      pill.style.color = BAND_TEXT[band] || "#ffffff";
      pill.setAttribute(
        "aria-label",
        region + " " + date +
        " Min " + oneDp(v.mint) + "°C" +
        " Max " + oneDp(v.maxt) + "°C" +
        " derived " + oneDp(v.derivedMapTemperature) + "°C"
      );
    }
    bindOrUpdateTip(marker, tooltipHtml(region, date, v));
  }

  // Pick a tooltip direction that keeps the WHOLE tooltip inside the Leaflet
  // container: a marker near the top of the view opens its tooltip downward,
  // everything else upward (V-3, so the north pill's tooltip is never clipped at
  // the top edge — closes #24 N-1 without over-compressing the markers at 375px).
  function tipDir(marker) {
    if (!map) return "top";
    var y = map.latLngToContainerPoint(marker.getLatLng()).y;
    return y < 118 ? "bottom" : "top";
  }

  function bindOrUpdateTip(marker, html) {
    var dir = tipDir(marker);
    if (marker.getTooltip() && marker._tipDir === dir) {
      marker.setTooltipContent(html); // refresh an already-open tooltip in place
      return;
    }
    if (marker.getTooltip()) marker.unbindTooltip();
    marker._tipDir = dir;
    marker.bindTooltip(html, {
      direction: dir,
      offset: dir === "bottom" ? [0, 20] : [0, -20],
      opacity: 1,
      className: "map-tip",
    });
  }

  function tooltipHtml(region, date, v) {
    return (
      '<b class="map-tip__region">' + escapeHtml(region) + "</b>" +
      '<span class="map-tip__row">Date ' + escapeHtml(date) + "</span>" +
      '<span class="map-tip__row">Min ' + escapeHtml(oneDp(v.mint)) +
      "°C · Max " + escapeHtml(oneDp(v.maxt)) + "°C</span>" +
      '<span class="map-tip__row">Derived ' + escapeHtml(oneDp(v.derivedMapTemperature)) +
      '°C <span class="map-tip__note">(derived)</span></span>'
    );
  }

  // The selected-Region block (Region, Date, Min, Max, Derived map temperature).
  // Updates when a pill is clicked and on every Select Date change (F-1 / AC-18).
  function updateSelectedBlock(date, byRegion) {
    var v = byRegion[selectedRegion];
    if (!v) return;
    els.selRegion.textContent = selectedRegion;
    els.selDate.textContent = date;
    els.selMin.textContent = oneDp(v.mint) + " °C";
    els.selMax.textContent = oneDp(v.maxt) + " °C";
    els.selDerived.textContent = oneDp(v.derivedMapTemperature);
  }

  function highlightSelected() {
    REGION_ORDER.forEach(function (region) {
      var marker = markers[region];
      if (!marker) return;
      var el = marker.getElement();
      if (el) el.classList.toggle("is-active", region === selectedRegion);
    });
  }

  // Defer the callback until the map container reports a non-zero box, so Leaflet
  // never initialises on a 0x0 element (which makes fitBounds compute an invalid
  // zoom and the markers collapse to "Invalid LatLng (NaN, NaN)"). ResizeObserver
  // fires when the container is laid out (e.g. the tab was hidden at load), and
  // visibilitychange covers a background tab (P-12, init hardening).
  function ensureMapSized(cb) {
    var container = els.mapFrame ? document.getElementById("map") : null;
    function sized() {
      return container && container.clientWidth > 0 && container.clientHeight > 0;
    }
    if (sized()) { cb(); return; }
    if (mapInitScheduled) return; // already waiting; latestDay carries the newest day
    mapInitScheduled = true;
    var done = false;
    function fire() {
      if (done || !sized()) return;
      done = true;
      cb();
    }
    if (typeof ResizeObserver !== "undefined" && container) {
      var ro = new ResizeObserver(function () {
        if (sized()) { ro.disconnect(); fire(); }
      });
      ro.observe(container);
    }
    document.addEventListener("visibilitychange", function onVis() {
      if (!document.hidden && sized()) {
        document.removeEventListener("visibilitychange", onVis);
        fire();
      }
    });
  }

  // Create the Leaflet map once: the vendored vector basemap (surrounding
  // coastlines under the Taiwan county polygons) and six pill markers, then fit
  // the view to the markers ONCE (R-EN-4). Returns false if Leaflet is
  // unavailable. Assumes the container already has a non-zero size (ensureMapSized).
  function initMap() {
    if (map) return true;
    if (typeof L === "undefined") return false;

    var basemap = window.TAIWAN_BASEMAP || {};

    map = L.map("map", {
      zoomControl: false,          // added at top-right below (R-EN-4, "zoomable")
      scrollWheelZoom: true,
      attributionControl: true,
      center: [23.75, 121.0],
      zoom: 7,
    });
    L.control.zoom({ position: "topright" }).addTo(map);
    map.attributionControl.setPrefix(false);
    // Short on-map attribution so the control stays a small bottom-right corner and
    // never overlaps a pill's tap target at 375px (#28 F-4); the full source and
    // licence text is in the README (P-2a).
    map.attributionControl.addAttribution("Natural Earth · 內政部 open data");

    // Surrounding coastline first (behind), then the Taiwan county polygons on
    // top. Both are non-interactive backdrops (no county-level data semantics).
    if (basemap.context) {
      L.geoJSON(basemap.context, {
        style: { color: "#2b3648", weight: 0.8, fillColor: "#1a2331", fillOpacity: 1 },
        interactive: false,
      }).addTo(map);
    }
    if (basemap.taiwan) {
      L.geoJSON(basemap.taiwan, {
        style: { color: "#44577a", weight: 0.9, fillColor: "#25324a", fillOpacity: 1 },
        interactive: false,
      }).addTo(map);
    }

    REGION_ORDER.forEach(function (region) {
      var latlng = REGION_POINTS[region];
      var icon = L.divIcon({
        className: "pill-icon",
        html:
          '<span class="pill" tabindex="0" role="button" aria-label="' +
          escapeHtml(region) + '">–</span>' +
          '<span class="rlabel">' + escapeHtml(region) + "</span>",
        iconSize: [104, 52],
        iconAnchor: [52, 16],
      });
      // keyboard:false so the marker's icon box is NOT a second tab stop — only
      // the inner .pill is focusable (its own tabindex/role/keydown), which
      // removes the nested-button that ignored Enter (#28 F-8).
      var marker = L.marker(latlng, { icon: icon, keyboard: false, title: region });
      marker.on("add", function () {
        var el = marker.getElement();
        if (!el) return;
        var pill = el.querySelector(".pill");
        function select() { selectedRegion = region; onSelect(); }
        // The click listens on the pill (the only interactive element now, F-4);
        // it still bubbles, so Leaflet's own marker handling is unaffected.
        (pill || el).addEventListener("click", select);
        if (pill) {
          pill.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
              e.preventDefault();
              select();
            }
          });
        }
      });
      marker.addTo(map);
      markers[region] = marker;
    });

    // On any move (zoom, or a resize re-fit) the markers shift relative to the
    // edges, so refresh the zoom-label class and re-pick each tooltip's direction
    // to keep it unclipped (V-3).
    map.on("moveend", refreshMapChrome);

    // Now that the container is laid out, recompute size and fit to the markers.
    // fitToMarkers() is the ONLY fitBounds call site — reused at init and on
    // resize, never on a Select Date change (the view must not reset, P-12).
    fitToMarkers();
    refreshMapChrome();
    colourLegend();
    return true;
  }

  // Hide the Region labels when zoomed far out (the name is still in the tooltip,
  // panel and aria-label) and re-pick every open tooltip's direction.
  function refreshMapChrome() {
    if (!map) return;
    var mapEl = document.getElementById("map");
    if (mapEl) mapEl.classList.toggle("map--labels-hidden", map.getZoom() < 8);
    REGION_ORDER.forEach(function (region) {
      var m = markers[region];
      if (m && m._dayInfo) {
        bindOrUpdateTip(m, tooltipHtml(region, m._dayInfo.date, m._dayInfo.value));
      }
    });
  }

  // Fit the view to the six markers. Padding depends on the layout: when the info
  // panel and legend FLOAT over the map (>= 1180px), reserve their footprint (left
  // for the top-left panel, right for the bottom-right legend) so no marker or its
  // tooltip sits under them (P-7c, #28 F-1/F-2/F-3); below 1180px the panels are
  // stacked OUTSIDE the map (CSS), so modest padding keeps the six pills separated
  // and their tooltips inside the frame (V-3, V-4). Tooltip clipping at the top
  // edge is handled per-marker by tipDir(). Called at init and on resize only.
  function fitToMarkers() {
    if (!map) return;
    var points = REGION_ORDER.map(function (r) { return REGION_POINTS[r]; });
    map.invalidateSize();
    var floating = window.innerWidth >= 1180;
    var pad = floating
      ? { tl: [392, 64], br: [300, 56] }
      : { tl: [26, 52], br: [26, 44] };
    map.fitBounds(points, {
      paddingTopLeft: pad.tl,
      paddingBottomRight: pad.br,
      maxZoom: 8,
    });
  }

  // A pill was clicked/activated: reflect the selection in the panel and pills.
  function onSelect() {
    highlightSelected();
    if (latestDay) updateSelectedBlock(latestDay.date, latestDay.byRegion);
  }

  // Paint the legend swatches from the same band->colour map the pills use, so
  // the legend always matches the pill colours (R-EN-5, AC-17).
  function colourLegend() {
    var swatches = document.querySelectorAll(".band-swatch");
    Array.prototype.forEach.call(swatches, function (el) {
      var band = el.getAttribute("data-band");
      if (BAND_COLOURS[band]) el.style.background = BAND_COLOURS[band];
    });
  }

  // Inline status inside the Taiwan Map card. `kind` is "loading" | "error" |
  // "empty". The status overlays ONLY the map frame — the info panel (with Select
  // Date) stays visible and operable so the user can switch to a working day
  // (DR-19, P-7b). The map is hidden while a status shows so a stale map is never
  // left behind an error message; it keeps its layout box (visibility, not
  // display) so ResizeObserver still sees a non-zero size.
  function setMapStatus(message, kind) {
    if (!els.mapStatus) return;
    els.mapStatus.textContent = message;
    els.mapStatus.className = "map-status state--inline state--inline-" + kind;
    els.mapStatus.setAttribute("role", kind === "error" ? "alert" : "status");
    els.mapStatus.hidden = false;
    if (els.mapFrame) els.mapFrame.classList.add("map-frame--status");
  }

  function hideMapStatus() {
    if (!els.mapStatus) return;
    els.mapStatus.hidden = true;
    els.mapStatus.textContent = "";
    if (els.mapFrame) els.mapFrame.classList.remove("map-frame--status");
  }

  function oneDp(v) {
    var n = Number(v);
    return isNaN(n) ? String(v) : n.toFixed(1);
  }

  // --- weekly summary (R-EN-1 item 3): lowest MinT / highest MaxT ------------
  // Pure aggregation of the /api/ series already fetched — no business logic.

  function renderSummary(series) {
    if (!series.length) {
      els.summary.hidden = true;
      return;
    }
    var minRow = series[0];
    var maxRow = series[0];
    series.forEach(function (r) {
      if (r.mint < minRow.mint) minRow = r;
      if (r.maxt > maxRow.maxt) maxRow = r;
    });
    els.summaryMinValue.textContent = formatTemp(minRow.mint);
    els.summaryMinDay.textContent = "on " + minRow.dataDate;
    els.summaryMaxValue.textContent = formatTemp(maxRow.maxt);
    els.summaryMaxDay.textContent = "on " + maxRow.dataDate;
    els.summary.hidden = false;
  }

  function renderTable(series) {
    els.tableBody.innerHTML = "";
    series.forEach(function (row) {
      var tr = document.createElement("tr");
      tr.appendChild(cell(row.dataDate));
      tr.appendChild(cell(formatTemp(row.mint)));
      tr.appendChild(cell(formatTemp(row.maxt)));
      els.tableBody.appendChild(tr);
    });
  }

  function cell(text) {
    var td = document.createElement("td");
    td.textContent = text;
    return td;
  }

  // --- inline-SVG line chart (MaxT red, MinT blue) with hover tooltip --------

  function renderChart(series) {
    // Draw the SVG at the container's own pixel width so the render scale stays
    // ~1 and the axis labels keep their real size at 375px too. The chart is
    // re-drawn on resize. A taller box on narrow screens keeps it readable.
    var cw = els.chart.clientWidth;
    var W = Math.max(300, Math.round(cw || 700));
    var H = cw && cw < 520 ? 300 : Math.round(W * 0.46);
    var m = { top: 18, right: 18, bottom: 46, left: 46 };
    var innerW = W - m.left - m.right;
    var innerH = H - m.top - m.bottom;

    els.chart.innerHTML = "";
    hideTooltip();
    chartState = null;
    currentSeries = series;
    if (!series.length) {
      return;
    }

    var mins = series.map(function (r) { return r.mint; });
    var maxs = series.map(function (r) { return r.maxt; });
    var lo = Math.min.apply(null, mins);
    var hi = Math.max.apply(null, maxs);
    var pad = (hi - lo) * 0.15 || 1;
    lo = Math.floor(lo - pad);
    hi = Math.ceil(hi + pad);

    var n = series.length;
    var xAt = function (i) {
      return m.left + (n === 1 ? innerW / 2 : (innerW * i) / (n - 1));
    };
    var yAt = function (v) {
      return m.top + innerH - (innerH * (v - lo)) / (hi - lo || 1);
    };

    var svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, role: "img" });

    // Y gridlines + tick labels.
    var ticks = yTicks(lo, hi);
    ticks.forEach(function (t) {
      var y = yAt(t);
      svg.appendChild(svgEl("line", {
        class: "chart__grid", x1: m.left, y1: y, x2: m.left + innerW, y2: y,
      }));
      var label = svgEl("text", {
        class: "chart__tick-label", x: m.left - 8, y: y + 4, "text-anchor": "end",
      });
      label.textContent = String(t);
      svg.appendChild(label);
    });

    // Axes.
    svg.appendChild(svgEl("line", {
      class: "chart__axis", x1: m.left, y1: m.top, x2: m.left, y2: m.top + innerH,
    }));
    svg.appendChild(svgEl("line", {
      class: "chart__axis",
      x1: m.left, y1: m.top + innerH, x2: m.left + innerW, y2: m.top + innerH,
    }));

    // Y axis title.
    var yTitle = svgEl("text", {
      class: "chart__axis-label", x: 14, y: m.top + innerH / 2,
      "text-anchor": "middle",
      transform: "rotate(-90 14 " + (m.top + innerH / 2) + ")",
    });
    yTitle.textContent = "Temperature (°C)";
    svg.appendChild(yTitle);

    // X tick labels (dates, MM-DD to stay legible) + X axis title.
    series.forEach(function (r, i) {
      var label = svgEl("text", {
        class: "chart__tick-label", x: xAt(i), y: m.top + innerH + 18,
        "text-anchor": "middle",
      });
      label.textContent = shortDate(r.dataDate);
      svg.appendChild(label);
    });
    var xTitle = svgEl("text", {
      class: "chart__axis-label",
      x: m.left + innerW / 2, y: H - 6, "text-anchor": "middle",
    });
    xTitle.textContent = "Date";
    svg.appendChild(xTitle);

    // Hover guide line (hidden until hover).
    var guide = svgEl("line", { class: "chart__guide", y1: m.top, y2: m.top + innerH });
    guide.setAttribute("visibility", "hidden");
    svg.appendChild(guide);

    // Lines.
    svg.appendChild(polyline(series, "maxt", xAt, yAt));
    svg.appendChild(polyline(series, "mint", xAt, yAt));

    // Dots, each carrying a native <title> as a no-JS tooltip fallback.
    var maxtDots = [];
    var mintDots = [];
    series.forEach(function (r, i) {
      var d1 = dot(xAt(i), yAt(r.maxt), "maxt", r.dataDate, r.maxt, "MaxT");
      var d2 = dot(xAt(i), yAt(r.mint), "mint", r.dataDate, r.mint, "MinT");
      maxtDots.push(d1);
      mintDots.push(d2);
      svg.appendChild(d1);
      svg.appendChild(d2);
    });

    // Full-height transparent hit targets, one per date, drive the rich tooltip.
    // Each carries its own <title> so the values remain reachable natively even
    // though the hit rect sits above the dots (F-1 fallback).
    var half = n === 1 ? innerW / 2 : innerW / (n - 1) / 2;
    series.forEach(function (r, i) {
      var x0 = xAt(i) - half;
      var w = half * 2;
      if (i === 0) { x0 = m.left; }
      if (i === n - 1) { w = m.left + innerW - x0; }
      var hit = svgEl("rect", {
        class: "chart__hit", x: x0, y: m.top, width: Math.max(w, 1), height: innerH,
      });
      var hitTitle = svgEl("title", {});
      hitTitle.textContent =
        r.dataDate + " — MaxT " + formatTemp(r.maxt) + "°C, MinT " +
        formatTemp(r.mint) + "°C";
      hit.appendChild(hitTitle);
      hit.addEventListener("mouseenter", function () { showTooltip(i); });
      hit.addEventListener("mousemove", function () { showTooltip(i); });
      svg.appendChild(hit);
    });

    els.chart.addEventListener("mouseleave", hideTooltip);

    els.chart.appendChild(svg);
    chartState = {
      svg: svg, W: W, H: H, series: series, xAt: xAt, yAt: yAt,
      guide: guide, maxtDots: maxtDots, mintDots: mintDots,
    };
  }

  function polyline(series, key, xAt, yAt) {
    var pts = series.map(function (r, i) {
      return xAt(i) + "," + yAt(r[key]);
    }).join(" ");
    return svgEl("polyline", {
      class: "chart__line chart__line--" + key,
      points: pts, fill: "none", "stroke-width": 2,
    });
  }

  function dot(x, y, key, date, value, label) {
    var c = svgEl("circle", {
      class: "chart__dot chart__dot--" + key, cx: x, cy: y, r: 3.5,
    });
    var title = svgEl("title", {});
    title.textContent = label + " " + date + ": " + formatTemp(value) + "°C";
    c.appendChild(title);
    return c;
  }

  // --- interactive hover tooltip ---------------------------------------------
  // Positioned in JS and clamped inside the chart box so the WHOLE tooltip (Date,
  // MaxT, MinT) is visible for every date at every width — it flips below the
  // point when placing it above would clip the top edge, and never overhangs the
  // first/last date (F-1). The canvas has overflow:visible and the SVG is drawn
  // at container width, so there is no clipping and no inner scrollbar on hover.

  function showTooltip(i) {
    if (!chartState) return;
    var s = chartState;
    var row = s.series[i];
    if (!row) return;

    clearActiveDots();
    if (s.maxtDots[i]) s.maxtDots[i].classList.add("chart__dot--active");
    if (s.mintDots[i]) s.mintDots[i].classList.add("chart__dot--active");

    var gx = s.xAt(i);
    s.guide.setAttribute("x1", gx);
    s.guide.setAttribute("x2", gx);
    s.guide.setAttribute("visibility", "visible");

    els.chartTooltip.innerHTML =
      '<div class="chart-tooltip__date">' + escapeHtml(row.dataDate) + "</div>" +
      '<div class="chart-tooltip__row"><span class="chart-tooltip__dot chart-tooltip__dot--maxt"></span>MaxT ' +
      escapeHtml(formatTemp(row.maxt)) + "°C</div>" +
      '<div class="chart-tooltip__row"><span class="chart-tooltip__dot chart-tooltip__dot--mint"></span>MinT ' +
      escapeHtml(formatTemp(row.mint)) + "°C</div>";
    els.chartTooltip.hidden = false; // must be laid out before measuring

    // Convert SVG viewBox coords to canvas pixels (scale ~1 by construction).
    var scale = (s.svg.clientWidth || s.W) / s.W;
    var canvasW = s.svg.clientWidth || s.W * scale;
    var canvasH = s.svg.clientHeight || s.H * scale;
    var tipW = els.chartTooltip.offsetWidth;
    var tipH = els.chartTooltip.offsetHeight;
    var GAP = 10;

    var pointX = s.xAt(i) * scale;
    var maxtY = s.yAt(row.maxt) * scale;
    var mintY = s.yAt(row.mint) * scale;

    // Horizontal: centre on the point, clamp inside the box.
    var left = clamp(pointX - tipW / 2, 0, Math.max(0, canvasW - tipW));
    // Vertical: prefer above the MaxT dot; if that clips the top, drop below MinT.
    var top = maxtY - tipH - GAP;
    if (top < 0) top = mintY + GAP;
    top = clamp(top, 0, Math.max(0, canvasH - tipH));

    els.chartTooltip.style.left = left + "px";
    els.chartTooltip.style.top = top + "px";
  }

  function hideTooltip() {
    if (els.chartTooltip) els.chartTooltip.hidden = true;
    clearActiveDots();
    if (chartState && chartState.guide) {
      chartState.guide.setAttribute("visibility", "hidden");
    }
  }

  function clearActiveDots() {
    if (!chartState) return;
    chartState.maxtDots.concat(chartState.mintDots).forEach(function (d) {
      d.classList.remove("chart__dot--active");
    });
  }

  function yTicks(lo, hi) {
    var out = [];
    var step = Math.max(1, Math.round((hi - lo) / 5));
    for (var v = lo; v <= hi; v += step) {
      out.push(v);
    }
    return out;
  }

  // --- small helpers ---------------------------------------------------------

  function fetchJson(url) {
    // Read the body as text and parse it explicitly so a 2xx response whose body
    // is not valid JSON is reported as a PARSE FAILURE, not as empty content
    // (DR-19 §4.1): an unparseable response is an ERROR. `parseError` lets every
    // caller treat that case as a failed request via `failed()`.
    return fetch(url, { headers: { Accept: "application/json" } }).then(
      function (response) {
        return response.text().then(function (text) {
          var body = {};
          var parseError = false;
          if (text) {
            try {
              body = JSON.parse(text);
            } catch (e) {
              parseError = true;
            }
          } else {
            parseError = true; // an empty body is not a parseable JSON response
          }
          return {
            ok: response.ok,
            status: response.status,
            body: body,
            parseError: parseError,
          };
        });
      }
    );
  }

  // A request FAILED when the HTTP status is non-2xx OR the body could not be
  // parsed as JSON (DR-19: both are errors, never empty). Callers use this so the
  // one-line rule "empty only for succeeded-but-nothing-to-show" holds.
  function failed(res) {
    return !res.ok || res.parseError;
  }

  function reasonMessage(body) {
    if (body && body.error) {
      return body.error;
    }
    return "The forecast data is currently unavailable.";
  }

  // Inline (per-Region) status inside the chart card. `kind` is one of
  // "loading" | "error" | "empty" and picks a visually distinct style (DR-19).
  function setChartStatus(message, kind) {
    els.chartStatus.textContent = message;
    els.chartStatus.className = "state state--inline state--inline-" + kind;
    els.chartStatus.setAttribute("role", kind === "error" ? "alert" : "status");
    els.chartStatus.hidden = false;
    els.chart.innerHTML = "";
    els.tableBody.innerHTML = "";
    hideTooltip();
    chartState = null;
    currentSeries = null;
  }
  function hideChartStatus() {
    els.chartStatus.hidden = true;
    els.chartStatus.textContent = "";
  }

  function showIngestionTime(value) {
    els.ingestionTime.textContent =
      "Last updated (data fetched from CWA): " + (value || "unknown");
  }

  function formatTemp(v) {
    // Show the stored REAL value as-is: JavaScript renders 31.0 as "31" and 24.8
    // as "24.8", which matches the Grading App's default formatting (observation
    // O-2). Non-numbers fall back to their string form.
    return String(v);
  }

  function shortDate(d) {
    return typeof d === "string" && d.length >= 10 ? d.slice(5) : d;
  }

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(v, hi));
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function svgEl(name, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.keys(attrs || {}).forEach(function (k) {
      el.setAttribute(k, attrs[k]);
    });
    return el;
  }
})();
