/* Taiwan Weather Forecast — dashboard frontend (Issues #23 UI/UX + #24 map).
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
 * Issue #24 adds "Select Date" (the seven Forecast Days from /api/days, default
 * first) and a vendored-Leaflet Taiwan Map whose six Region markers are coloured
 * by the selected day's Derived Map Temperature band from /api/days/<date>. The
 * band and the derived value come straight from the shared module via the
 * endpoint; the frontend re-derives nothing (H-3 single-sourced, R-SHR-4). The
 * map uses a vendored Taiwan outline (a vector layer) and SVG circle markers, so
 * it makes no external tile/data request and needs no key (R-EN-6).
 *
 * State mapping is DR-19 (decision-20260924-dashboard-state-mapping):
 *   - loading : a request is in flight (page-level for /api/health -> /api/regions;
 *               inline in the chart card for a per-Region request);
 *   - error   : a request FAILED — a network failure, an unparseable response, OR
 *               ANY non-2xx (503 missing/empty/incomplete, 500/502/504, 404). The
 *               server's `error` message is surfaced so those causes stay distinct.
 *               A snapshot-unavailable 503 is ALWAYS error, never empty;
 *   - empty   : a request SUCCEEDED (2xx) but there is nothing to render —
 *               /api/regions with an empty list (page-level), or /series with an
 *               empty series (inline, shown as a message, never a blank card).
 * One-line rule: empty only for "succeeded but nothing to show"; every failed
 * request is error (R-DS-6, AC-10, R-EN-1 item 5).
 */
"use strict";

(function () {
  var els = {};
  var chartState = null;   // geometry + series for the hover tooltip
  var currentSeries = null; // last-rendered series, for responsive re-draw
  var resizeTimer = null;

  // --- Taiwan Map (Issue #24, R-EN-3..R-EN-7) --------------------------------
  // The six Region names in the canonical order (matches /api/regions and the
  // shared module's R-SHR-2(b)); used to iterate markers deterministically.
  var REGION_ORDER = [
    "北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區",
  ];

  // Project-defined representative points [lat, lng] for each Region marker
  // (DR-1: coordinates are HOW; README notes they are project-defined, not a CWA
  // authority). fitBounds over these keeps the map centred on Taiwan with all six
  // markers visible (R-EN-4).
  var REGION_POINTS = {
    "北部地區": [25.03, 121.50],
    "中部地區": [24.15, 120.68],
    "南部地區": [22.85, 120.35],
    "東北部地區": [24.72, 121.74],
    "東部地區": [23.98, 121.55],
    "東南部地區": [22.80, 121.10],
  };

  // Colour per Derived Map Temperature band. The band comes straight from the
  // /api/days/<date> endpoint (R-SHR-4 / DR-4 owns the derivation and banding in
  // the shared module); the frontend re-derives nothing (H-3 single-sourced) and
  // only maps the band NAME to a fill colour. The legend swatches are painted
  // from this same map so colours always agree (R-EN-5).
  var BAND_COLOURS = {
    blue: "#2b6cb0",
    green: "#2f9e44",
    yellow: "#f2b705",
    red: "#e03131",
  };

  // A simplified outline of Taiwan's main island as a vector basemap (GeoJSON,
  // [lng, lat]). It is a project-authored, simplified coastline used only as a
  // backdrop for the markers — no tile server, no external request, so the map
  // works offline and needs no key/account (R-EN-6). fitBounds is over the
  // markers, not this outline.
  var TAIWAN_OUTLINE = {
    type: "Feature",
    properties: { name: "Taiwan (simplified outline, project-authored)" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [121.53, 25.30], [121.66, 25.27], [121.83, 25.13], [121.94, 24.97],
        [121.90, 24.82], [121.82, 24.68], [121.75, 24.45], [121.62, 24.10],
        [121.52, 23.80], [121.43, 23.45], [121.35, 23.10], [121.24, 22.80],
        [121.15, 22.62], [121.02, 22.40], [120.92, 22.20], [120.86, 22.00],
        [120.84, 21.90], [120.76, 21.96], [120.68, 22.12], [120.55, 22.42],
        [120.42, 22.72], [120.28, 22.98], [120.16, 23.25], [120.09, 23.55],
        [120.12, 23.82], [120.22, 24.10], [120.40, 24.33], [120.58, 24.58],
        [120.78, 24.82], [121.00, 25.02], [121.22, 25.14], [121.40, 25.23],
        [121.53, 25.30],
      ]],
    },
  };

  var map = null;          // the Leaflet map, created once
  var markers = {};        // Region name -> L.CircleMarker

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
    // Select Date + Taiwan Map (#24).
    els.dateSelect = document.getElementById("date-select");
    els.mapCaption = document.getElementById("map-caption");
    els.mapStatus = document.getElementById("map-status");
    els.mapLayout = document.getElementById("map-layout");
    els.infocardHint = document.querySelector("#map-infocard .infocard__hint");
    els.infocardBody = document.getElementById("infocard-body");
    els.infocardRegion = document.getElementById("infocard-region");
    els.infocardDate = document.getElementById("infocard-date");
    els.infocardMin = document.getElementById("infocard-min");
    els.infocardMax = document.getElementById("infocard-max");
    els.infocardDerived = document.getElementById("infocard-derived");

    els.regionSelect.addEventListener("change", function () {
      loadRegion(els.regionSelect.value);
    });
    els.dateSelect.addEventListener("change", function () {
      loadDay(els.dateSelect.value);
    });

    // Redraw the chart at the new width on resize (the SVG is drawn at the
    // container's own pixel width so its labels stay legible, F-3) and drop any
    // open tooltip so its pixel maths never goes stale.
    window.addEventListener("resize", function () {
      hideTooltip();
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (currentSeries) renderChart(currentSeries);
        if (map) map.invalidateSize();
      }, 150);
    });

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
      // Select Date + Taiwan Map load independently of the selected Region (#24).
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

  // --- Select Date + Taiwan Map (#24, R-EN-3..R-EN-7) ------------------------
  // Independent of the selected Region. /api/days fills Select Date (seven days,
  // ascending, default first); /api/days/<date> gives the six Regions' values for
  // the chosen day, each already carrying the Derived Map Temperature and its
  // colour band from the shared module — the frontend re-derives nothing.

  function loadDays() {
    setMapStatus("Loading the map…", "loading");
    return fetchJson("/api/days")
      .then(function (res) {
        if (failed(res)) {
          setMapStatus(reasonMessage(res.body), "error"); // DR-19: failure -> error
          return;
        }
        var days = (res.body && res.body.days) || [];
        if (!days.length) {
          setMapStatus("No Forecast Days are available in this snapshot.", "empty");
          return;
        }
        populateDates(days);
        var first = days[0];              // ascending; default the first day (R-EN-3)
        els.dateSelect.value = first;
        loadDay(first);
      })
      .catch(function () {
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

  function loadDay(date) {
    els.mapCaption.textContent = "Showing " + date;
    setMapStatus("Loading " + date + "…", "loading");
    return fetchJson("/api/days/" + encodeURIComponent(date))
      .then(function (res) {
        if (failed(res)) {
          // 404 / 503 / 5xx / unparseable -> inline error (DR-19 per-Region rule).
          setMapStatus(
            res.status === 404
              ? "That date is not available in this snapshot."
              : reasonMessage(res.body),
            "error"
          );
          clearInfocard();
          return;
        }
        var values = (res.body && res.body.values) || [];
        if (!values.length) {
          // Succeeded but nothing to render -> inline empty (DR-19).
          setMapStatus("No values are available for this date yet.", "empty");
          clearInfocard();
          return;
        }
        hideMapStatus();
        applyDay(date, values);
      })
      .catch(function () {
        setMapStatus(
          "Cannot load this date right now. Please try again.",
          "error"
        );
        clearInfocard();
      });
  }

  // Colour the six markers for `date` and (re)bind their hover tooltip, click
  // popup and the side info card. Called only on a successful 2xx with values.
  function applyDay(date, values) {
    els.mapLayout.hidden = false;
    if (!ensureMap()) {
      // Leaflet failed to load (vendored script missing) — treat as an error so
      // the card is never blank.
      setMapStatus("The map library is unavailable.", "error");
      return;
    }

    var byRegion = {};
    values.forEach(function (v) { byRegion[v.regionName] = v; });

    REGION_ORDER.forEach(function (region) {
      var marker = markers[region];
      var v = byRegion[region];
      if (!marker || !v) return;
      // Colour DIRECTLY by the endpoint's band (no re-derivation, H-3).
      marker.setStyle({ fillColor: BAND_COLOURS[v.colourBand] || "#888888" });
      var html = infoHtml(region, date, v);
      marker.bindTooltip(html, { direction: "top", offset: [0, -6] });
      // autoPan off: every marker is already in view (fitBounds), so opening a
      // popup should not jump the map.
      marker.bindPopup(html, { autoPan: false });
      marker._dayInfo = { region: region, date: date, value: v };
    });

    // Seed the side info card with the first Region so it is never blank; hover
    // or click updates it (and opens the marker's own tooltip/popup).
    var firstValue = byRegion[REGION_ORDER[0]];
    if (firstValue) updateInfocard(REGION_ORDER[0], date, firstValue);

    map.invalidateSize();
  }

  // Create the Leaflet map once: the Taiwan outline as a vector basemap and six
  // circle markers, then fit the view to the markers (R-EN-4). Returns false if
  // Leaflet is unavailable.
  function ensureMap() {
    if (map) return true;
    if (typeof L === "undefined") return false;

    // The map container was just revealed (mapLayout.hidden = false in applyDay);
    // force a synchronous reflow so it reports its real width before Leaflet reads
    // it. Without this Leaflet caches a 0px size, fitBounds computes an infinite
    // zoom, and the markers collapse to an invisible point until a later resize.
    var container = document.getElementById("map");
    void container.offsetWidth;

    var palette = mapPalette();
    // Initialise with a Taiwan-centred view BEFORE adding any layer: a vector
    // layer added to a map with no view set has no pixel bounds and Leaflet's
    // renderer throws. fitBounds over the markers refines this view below.
    map = L.map("map", {
      zoomControl: true,
      scrollWheelZoom: true,
      attributionControl: true,
      center: [23.75, 121.0],
      zoom: 7,
    });

    L.geoJSON(TAIWAN_OUTLINE, {
      style: {
        color: palette.landStroke,
        weight: 1,
        fillColor: palette.land,
        fillOpacity: 1,
      },
      interactive: false,
    }).addTo(map);

    var points = [];
    REGION_ORDER.forEach(function (region) {
      var latlng = REGION_POINTS[region];
      var marker = L.circleMarker(latlng, {
        radius: 11,
        color: palette.markerStroke,
        weight: 1.5,
        fillColor: "#cccccc",
        fillOpacity: 0.9,
      });
      marker.on("mouseover", function () {
        var info = marker._dayInfo;
        if (info) updateInfocard(info.region, info.date, info.value);
      });
      marker.on("click", function () {
        var info = marker._dayInfo;
        if (info) updateInfocard(info.region, info.date, info.value);
      });
      marker.addTo(map);
      markers[region] = marker;
      points.push(latlng);
    });

    // Recompute the size now that the container is laid out, THEN fit to the
    // markers so the initial zoom is finite and the six markers are all visible.
    map.invalidateSize();
    map.fitBounds(points, { padding: [26, 26] });
    colourLegend();
    return true;
  }

  // Marker/legend/basemap palette. Colours work in light and dark; the marker
  // FILL colours (BAND_COLOURS) are the same in both so the legend stays valid.
  function mapPalette() {
    var dark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches &&
      document.documentElement.getAttribute("data-theme") !== "light";
    if (document.documentElement.getAttribute("data-theme") === "dark") dark = true;
    return dark
      ? { land: "#243244", landStroke: "#3a4a60", markerStroke: "#0c0f14" }
      : { land: "#e7eef6", landStroke: "#9fb2c4", markerStroke: "#1b1b1b" };
  }

  function infoHtml(region, date, v) {
    return (
      '<div class="mapinfo">' +
      '<strong class="mapinfo__region">' + escapeHtml(region) + "</strong>" +
      '<div class="mapinfo__row">Date: ' + escapeHtml(date) + "</div>" +
      '<div class="mapinfo__row">Min: ' + escapeHtml(formatTemp(v.mint)) +
      "°C &nbsp;·&nbsp; Max: " + escapeHtml(formatTemp(v.maxt)) + "°C</div>" +
      '<div class="mapinfo__row">Derived map temperature: ' +
      escapeHtml(oneDp(v.derivedMapTemperature)) +
      '°C <span class="mapinfo__note">(derived)</span></div>' +
      "</div>"
    );
  }

  function updateInfocard(region, date, v) {
    els.infocardRegion.textContent = region;
    els.infocardDate.textContent = date;
    els.infocardMin.textContent = formatTemp(v.mint);
    els.infocardMax.textContent = formatTemp(v.maxt);
    els.infocardDerived.textContent = oneDp(v.derivedMapTemperature);
    els.infocardHint.hidden = true;
    els.infocardBody.hidden = false;
  }

  function clearInfocard() {
    if (!els.infocardBody) return;
    els.infocardBody.hidden = true;
    els.infocardHint.hidden = false;
  }

  // Paint the legend swatches from the same band->colour map the markers use, so
  // the legend always matches the marker colours (R-EN-5).
  function colourLegend() {
    var swatches = document.querySelectorAll(".band-swatch");
    Array.prototype.forEach.call(swatches, function (el) {
      var band = el.getAttribute("data-band");
      if (BAND_COLOURS[band]) el.style.background = BAND_COLOURS[band];
    });
  }

  // Inline status inside the Taiwan Map card. `kind` is "loading" | "error" |
  // "empty"; the map layout is hidden while a status shows so the card is never
  // blank and the status is never drawn over a stale map (DR-19 §4.1).
  function setMapStatus(message, kind) {
    if (!els.mapStatus) return;
    els.mapStatus.textContent = message;
    els.mapStatus.className = "state state--inline state--inline-" + kind;
    els.mapStatus.setAttribute("role", kind === "error" ? "alert" : "status");
    els.mapStatus.hidden = false;
    if (els.mapLayout) els.mapLayout.hidden = true;
  }

  function hideMapStatus() {
    if (!els.mapStatus) return;
    els.mapStatus.hidden = true;
    els.mapStatus.textContent = "";
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
    // ~1 and the axis labels keep their real size at 375px too (F-3). The chart
    // is re-drawn on resize. A taller box on narrow screens keeps it readable.
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
    // (DR-19 §4.1, fix N-1): an unparseable response is an ERROR. The earlier
    // `.json().catch(() => ({}))` swallowed the parse failure and returned {},
    // which then rendered as an empty state. `parseError` lets every caller treat
    // that case as a failed request via `failed()`.
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
