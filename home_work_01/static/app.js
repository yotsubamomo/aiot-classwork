/* Taiwan Weather Forecast — dashboard frontend (Issues #23 UI/UX + #24 map,
 * reworked in #28; V2 Now mode / Forecast mode in #36).
 *
 * All data comes from THIS application's own JSON API under the "/api/" prefix
 * (R-DS-5, R-SHR-5, AC-04(b), R-V2-SEC-1); the browser never calls CWA and holds
 * no key.
 *
 * TAIWAN MAP — two modes on one Leaflet map (SPEC-V2 §2.1, Issue #36):
 *   - Now mode (the default: the page opens in it with no user action and
 *     whatever the forecast snapshot does, R-V2-MODE-1). It loads the Latest
 *     Observation from /api/observations/latest on its own — NOT gated on
 *     /api/health (R-V2-DEG-1, INV-V2-7) — and shows at most one marker per
 *     county: the air temperature of the county's representative station, chosen
 *     server-side by the documented rule (representative.py, R-V2-DD-3). A marker
 *     is a station value and is labelled with the station's name; it is never
 *     presented as a county value (R-V2-DD-2, INV-V2-5, H-3). The Now panel shows
 *     the verbatim labels "Observation Time" and "Fetched Time", the valid-station
 *     count and a "Refresh" control with a visible in-progress indicator
 *     (R-V2-OBS-4(c), R-V2-OBS-7(a)(c), R-V2-DD-10). Every Refresh (the first
 *     load included) ends, within a client-side time bound, in exactly one of
 *     three results — newer (applied), not-newer (kept, "already the latest") or
 *     failure — and the Now mode is then in one of the states success, Stale
 *     (a failure while data is shown: the last successful data and both times
 *     stay, labelled Stale with the failure's category) or Unavailable (a failure
 *     with nothing to show). Stale is set only by a failure, never by the data's
 *     age; the dataset Observation Time shown never decreases (R-V2-OBS-7, 8, 10,
 *     12, 13; INV-V2-6; Issue #37). An observation failure touches only this
 *     observation layer (R-V2-DEG-2, INV-V2-7).
 *     Taiwan → County → Station (SPEC-V2 §2.3, Issue #38): a county interaction
 *     layer — the 22 vendored county polygons, each carrying its county name
 *     (static/data/counties.js), drawn transparent over the backdrop, never
 *     coloured by data — highlights a county and shows its name on hover and
 *     selects it on click; the "County" chooser in the Now panel does the same
 *     without the map (R-V2-DD-4, R-V2-DD-9(a)). Selecting a county fits the view
 *     to its stations on the map, shows those stations as markers and the County
 *     context: its name, valid-station count (and how many are on the map), the
 *     highest and lowest station (name / value) and the station list — station
 *     values only, no county average or any aggregate (R-V2-DD-5, R-V2-DD-6,
 *     INV-V2-5). A list item or a marker selects a station and shows its detail
 *     (R-V2-DD-7). A valid station outside the map range E is not placed on the
 *     map but is counted, listed ("not on the map") and has its detail
 *     (R-V2-DD-11). "Back to Taiwan" clears the county and the station and
 *     returns to the Taiwan-wide view (R-V2-DD-8). The county layer and the
 *     County context stay usable when the observation is Stale (the retained data,
 *     still marked Stale) or Unavailable (the county name, every value "—", never
 *     0 — DV-21 §4.2); the county selection survives a Now → Forecast → Now round
 *     trip with the rest of the Now selection (R-V2-MODE-5(a), DV-20).
 *   - Forecast mode: the V1 six-region seven-day map unchanged — Select Date,
 *     six Region pills coloured by the endpoint's band, the DERIVED panel and the
 *     four-band legend (R-V2-MODE-3, R-EN-3..R-EN-7, DR-20/DR-21).
 * Mode-owned elements carry data-mode="now" / "forecast" and are shown only in
 * their mode, so the observation and the derived semantics never share a panel,
 * legend or colour scale (R-V2-MODE-4, R-V2-MODE-6). Switching modes keeps the
 * geographic context (R-V2-MODE-5, DV-8): the Now view and selection are saved on
 * leaving Now mode and restored on return; on entering Forecast mode the view is
 * kept when all six Region markers are already in the clear map area, otherwise
 * it is widened just enough to include them.
 *
 * FORECAST SECTION (below the map) — unchanged V1 behaviour: the page bootstraps
 * the forecast from /api/health, populates "Select Region" from /api/regions, and
 * for the selected Region draws a MaxT / MinT seven-day line chart (hand-drawn
 * inline SVG, no chart library) with a legend, axis labels and an interactive
 * hover tooltip, a Date / MinT / MaxT table whose seven rows equal data.db, and a
 * weekly summary (lowest MinT / highest MaxT) derived in the browser from the
 * same /api/ series — no new business logic (INV-2, AC-04(b)).
 *
 * The Forecast mode's six Region markers are temperature "pills" whose TEXT (the
 * day's derivedMapTemperature to one decimal) and COLOUR (the day's colourBand)
 * come straight from /api/days/<date>; the frontend re-derives nothing and
 * re-bands nothing (H-3 single-sourced, R-SHR-4). oneDp/toFixed(1) is display
 * formatting only. The map is drawn on a vendored VECTOR basemap
 * (window.TAIWAN_BASEMAP, a same-origin <script>, no fetch, no tiles), so it
 * makes no external request and needs no key (R-EN-6, INV-V2-3).
 *
 * State mapping is DR-19 (decision-20260924-dashboard-state-mapping), scoped in
 * V2 to the FORECAST SECTION instead of the whole page (R-V2-DEG-3, DV-17):
 *   - loading : a request is in flight (section-level for /api/health ->
 *               /api/regions; inline in the chart card for a per-Region /series
 *               request, and inline in the Forecast mode map for the /api/days
 *               requests);
 *   - error   : a request FAILED — a network failure, an unparseable response, OR
 *               ANY non-2xx (503 missing/empty/incomplete, 500/502/504, 404). The
 *               server's `error` message is surfaced so those causes stay distinct.
 *               A snapshot-unavailable 503 is ALWAYS error, never empty. A failed
 *               bootstrap also shows the error inline in the Forecast mode map and
 *               disables Select Date; Now mode and the mode switch stay usable;
 *   - empty   : a request SUCCEEDED (2xx) but there is nothing to render —
 *               /api/regions with an empty list (section-level), /series with an
 *               empty series (inline in the chart card), or /api/days[/<date>] with
 *               no days/values (inline in the Forecast mode map) — always a
 *               message, never a blank card.
 * The Forecast mode inline status overlays ONLY the map, never the info panel, so
 * "Select Date" stays visible and operable — the user can switch to a working day
 * to recover from an inline error/empty (DR-19, #28 P-7b). It is shown only in
 * Forecast mode; Now mode's map is never covered by a forecast status.
 */
"use strict";

(function () {
  var els = {};
  var chartState = null;   // geometry + series for the hover tooltip
  var currentSeries = null; // last-rendered series, for responsive re-draw
  var resizeTimer = null;

  // --- modes (R-V2-MODE-1..6) -------------------------------------------------
  var MODE_NOW = "now";
  var MODE_FORECAST = "forecast";
  // The page opens in Now mode before any request is made (R-V2-MODE-1).
  var mode = MODE_NOW;
  var appliedMode = null;  // the mode whose layer is currently on the map
  var nowView = null;      // {center, zoom} saved when leaving Now mode (R-V2-MODE-5)
  var forecastCaption = "";

  // --- Taiwan Map, Forecast mode (R-EN-3..R-EN-7) -----------------------------
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

  // Now mode's initial view: the whole main island plus 澎湖 (SPEC-V2 §5.3
  // instrument for R-V2-MAP-4), [[south, west], [north, east]].
  var NOW_INITIAL_BOUNDS = [[21.85, 119.25], [25.35, 122.05]];

  // Colour per Derived Map Temperature band. The band comes straight from the
  // /api/days/<date> endpoint (R-SHR-4 / DR-4 owns the derivation and banding in
  // the shared module); the frontend re-derives nothing (H-3 single-sourced) and
  // only maps the band NAME to a fill colour. The legend swatches are painted from
  // this same map so the legend always matches the pills (R-EN-5, AC-17). The four
  // tokens are the blue / green / yellow / red family named by R-SHR-4. They are
  // used ONLY by the Forecast mode; the Now mode's station markers use their own
  // neutral style and no colour scale (R-V2-MODE-6(b)).
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
  var forecastLayer = null; // L.layerGroup of the six Region pills (Forecast mode)
  var nowLayer = null;     // L.layerGroup of the representative stations (Now mode)
  var markers = {};        // Region name -> L.marker (pill divIcon)
  var mapReqSeq = 0;       // latest /api/days/<date> request wins (out-of-order)
  var selectedRegion = "北部地區"; // the Region shown in the info panel's selected block
  var latestDay = null;    // {date, byRegion} for the day currently rendered/pending
  var mapInitScheduled = false;
  var lastFitWidth = null; // window width at the last fit; a height-only resize does not re-fit (#28 R2 N-2)
  var zoomAnimating = false; // a Leaflet zoom animation is running (#38)
  var pendingView = null;    // the latest view change asked for during it

  // --- Latest Observation, Now mode (R-V2-OBS-*, R-V2-DD-2/3/10) ----------------
  var obs = null;              // the displayed success body of /api/observations/latest
  var obsById = {};            // stationId -> station of `obs`
  var renderedObs = null;      // the body whose stations are currently the markers
  var stationMarkers = {};     // stationId -> L.marker (representative stations)
  var selectedStationId = null; // Now-mode selection, kept across mode switches
  var obsInFlight = false;     // a Refresh (or the first load) is in progress
  var obsSeq = 0;              // tags each Refresh; only the current one may apply
  // The Now mode's observation state (R-V2-OBS-10): "loading" until the first
  // result, then "success", "stale" (a failure while data is shown) or
  // "unavailable" (a failure with no data to show). Only a failure sets stale or
  // unavailable, and only a success clears them — there is no timer and no age
  // test anywhere (R-V2-OBS-10(d), INV-V2-6).
  var obsState = "loading";
  var obsFailure = null;       // the classified failure behind stale / unavailable
  var MISSING = "—";           // shown for any missing / sentinel value (R-V2-OBS-6)

  // --- Taiwan → County → Station, Now mode (R-V2-DD-1, DD-4..DD-9, DD-11) --------
  // The 22 counties, CWA CountyName verbatim (R-V2-DD-1), in representative.py's
  // COUNTY_ORDER; this order fills the "County" chooser.
  var COUNTY_ORDER = [
    "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣",
    "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣",
    "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣",
    "澎湖縣", "金門縣", "連江縣",
  ];
  // The useful Taiwan map range E (SPEC-V2 §5.3), bounds inclusive — the same
  // numbers as representative.py's MAP_RANGE (a static test keeps them equal). A
  // valid station outside it (e.g. 高雄市's 東沙島) is never placed on the map, but
  // it is counted, listed as "not on the map" and has its detail (R-V2-DD-11).
  var MAP_RANGE = { latitude: [21.2, 26.7], longitude: [117.6, 122.9] };
  var COUNTY_MAX_ZOOM = 11;    // the closest a county fit zooms (a one-station county)
  var countyLayer = null;      // L.geoJSON of the 22 named county polygons (Now mode only)
  var countyShapes = {};       // countyName -> its polygon layer
  var selectedCounty = null;   // Now-mode county selection, kept across mode switches
  var hoveredCounty = null;    // the county under the pointer
  var renderedCounty = null;   // the county whose stations are currently the markers
  var listedKey = null;        // {obs, county} the station list was built for

  // Client-side bound on one Refresh (R-V2-OBS-13, DV-7): if no usable answer has
  // arrived after this long the request is aborted and counted as a failure, so
  // the Refresh never stays in progress. It is above the server's own upstream
  // bound (8 s, observation.py) so a classified server answer normally arrives
  // first, and below the 30 s verification instrument (SPEC-V2 §5.3).
  var OBS_TIMEOUT_MS = 20000;

  // User-visible failure categories (R-V2-OBS-12): the four server reasons of
  // /api/observations/latest (R-V2-OBS-11, DV-6), each with its own fixed text,
  // plus two client-side categories for a request that never got a classified
  // answer (no answer in time / network failure, and a platform-level or other
  // non-classified response such as an HTML 502 page). The text is fixed here:
  // nothing from a response body is ever shown, so no key, upstream URL or
  // upstream body can reach the page (H-1).
  var OBS_FAILURE_TEXT = {
    key_not_configured: "the server has no CWA API key configured",
    upstream_unreachable: "the CWA service could not be reached in time",
    upstream_error: "the CWA service answered with an error status",
    invalid_response: "the CWA response was not usable",
    no_response: "this site's server did not answer in time or could not be reached",
    unexpected_response: "this site's server gave an unexpected answer",
  };
  var OBS_SERVER_REASONS = [
    "key_not_configured", "upstream_unreachable", "upstream_error", "invalid_response",
  ];

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
    els.mapEl = document.getElementById("map");
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
    // Mode switch + Now mode panel (#36).
    els.modeButtons = document.querySelectorAll("[data-mode-target]");
    els.modeOwned = document.querySelectorAll("[data-mode]");
    els.nowPanel = document.getElementById("now-panel");
    els.obsTime = document.getElementById("obs-time");
    els.obsFetched = document.getElementById("obs-fetched");
    els.obsCount = document.getElementById("obs-count");
    els.refreshButton = document.getElementById("refresh-button");
    els.obsStatus = document.getElementById("obs-status");
    // Stale / Unavailable presentation (#37).
    els.obsStateChip = document.getElementById("obs-state-chip");
    els.obsState = document.getElementById("obs-state");
    els.obsStateTitle = document.getElementById("obs-state-title");
    els.obsStateBody = document.getElementById("obs-state-body");
    els.obsStateReason = document.getElementById("obs-state-reason");
    els.obsMapState = document.getElementById("obs-map-state");
    els.obsSelected = document.getElementById("obs-selected");
    els.obsSelName = document.getElementById("obs-sel-name");
    els.obsSelPlace = document.getElementById("obs-sel-place");
    els.obsSelTemp = document.getElementById("obs-sel-temp");
    els.obsSelRh = document.getElementById("obs-sel-rh");
    els.obsSelWind = document.getElementById("obs-sel-wind");
    els.obsSelWeather = document.getElementById("obs-sel-weather");
    els.obsSelTime = document.getElementById("obs-sel-time");
    // Taiwan → County → Station (#38).
    els.obsMarkerNote = document.getElementById("obs-marker-note");
    els.obsSelId = document.getElementById("obs-sel-id");
    els.obsSelWdir = document.getElementById("obs-sel-wdir");
    els.obsSelPres = document.getElementById("obs-sel-pres");
    els.obsSelRain = document.getElementById("obs-sel-rain");
    els.obsSelOffmap = document.getElementById("obs-sel-offmap");
    els.countySelect = document.getElementById("county-select");
    els.county = document.getElementById("county-context");
    els.countyName = document.getElementById("county-name");
    els.countyState = document.getElementById("county-state");
    els.countyCount = document.getElementById("county-count");
    els.countyOnMap = document.getElementById("county-onmap");
    els.countyMax = document.getElementById("county-max");
    els.countyMin = document.getElementById("county-min");
    els.countyStations = document.getElementById("county-stations");
    els.countyListTitle = document.getElementById("county-list-title");
    els.countyListEmpty = document.getElementById("county-list-empty");
    els.countyList = document.getElementById("county-list");
    els.backToTaiwan = document.getElementById("back-to-taiwan");

    els.regionSelect.addEventListener("change", function () {
      loadRegion(els.regionSelect.value);
    });
    els.dateSelect.addEventListener("change", function () {
      loadDay(els.dateSelect.value);
    });
    // The mode buttons are real <button>s: click, Enter and Space all activate
    // them natively, so the switch is keyboard-operable (R-V2-MODE-2(d)).
    Array.prototype.forEach.call(els.modeButtons, function (button) {
      button.addEventListener("click", function () {
        setMode(button.getAttribute("data-mode-target"));
      });
    });
    els.refreshButton.addEventListener("click", function () {
      loadObservation();
    });
    // The county chooser: a native <select>, so it is reachable with Tab and
    // operated with the keyboard without going through the map (R-V2-DD-9(a)).
    COUNTY_ORDER.forEach(function (name) {
      var opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      els.countySelect.appendChild(opt);
    });
    els.countySelect.addEventListener("change", function () {
      if (els.countySelect.value) selectCounty(els.countySelect.value);
      else backToTaiwan();
    });
    // A real <button>: click, Enter and Space (R-V2-DD-8, R-V2-DD-9(c)).
    els.backToTaiwan.addEventListener("click", backToTaiwan);

    // Redraw the chart at the new width on resize (the SVG is drawn at the
    // container's own pixel width so its labels stay legible) and drop any open
    // tooltip so its pixel maths never goes stale. Also keep Leaflet in sync.
    window.addEventListener("resize", function () {
      hideTooltip();
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (currentSeries) renderChart(currentSeries);
        if (map) {
          if (window.innerWidth !== lastFitWidth) {
            // The WIDTH changed, so the layout mode (floating >= 1180px vs stacked)
            // and the reserved padding may differ — re-fit the current mode's view
            // so the markers stay clear of the panels at the new width (#28 F-1).
            // Only a width change re-fits; a Select Date change never does (P-12).
            // A selected county keeps its county view (#38).
            if (mode === MODE_NOW && selectedCounty) fitCounty(selectedCounty);
            else fitToMarkers();
          } else {
            // A height-only change (e.g. a mobile browser toolbar showing/hiding on
            // scroll): keep Leaflet's size in sync WITHOUT re-fitting, so the user's
            // zoom/pan is preserved (#28 R2 N-2).
            map.invalidateSize();
          }
        }
      }, 150);
    });

    // Colour the legend swatches up front so they show the four band colours even
    // before the first day loads / in the loading/empty/error states (#28 F-6).
    colourLegend();

    // Now mode first: show its chrome, bring the map up as soon as it has a size,
    // and load the Latest Observation. The forecast bootstrap runs independently;
    // the Now mode never waits for, or depends on, /api/health (R-V2-DEG-1).
    renderModeChrome();
    bringUpMap();
    loadObservation();
    bootstrap();
  });

  // --- mode switch (R-V2-MODE-1..5) --------------------------------------------

  function setMode(next) {
    if (next !== MODE_NOW && next !== MODE_FORECAST) return;
    if (next === mode) return;
    // Leaving Now mode: remember its view so a round trip restores it (DV-8). The
    // Now selection itself — county (#38) and station — lives in module state
    // that the switch never clears, so it is back on return (R-V2-MODE-5(a), DV-20).
    if (map && appliedMode === MODE_NOW) {
      nowView = { center: map.getCenter(), zoom: map.getZoom() };
    }
    hoveredCounty = null; // the county layer leaves the map with Now mode
    mode = next;
    renderModeChrome();
    // The mode-switch path goes through the same non-zero-size guard as page load
    // (R-V2-MAP-5): the map is only touched once its container has a real size.
    bringUpMap();
  }

  // Show the current mode's controls/panels/legend and hide the other mode's; mark
  // the pressed mode button; set the caption and the map's accessible name.
  function renderModeChrome() {
    Array.prototype.forEach.call(els.modeButtons, function (button) {
      var on = button.getAttribute("data-mode-target") === mode;
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.classList.toggle("is-current", on);
    });
    Array.prototype.forEach.call(els.modeOwned, function (el) {
      el.hidden = el.getAttribute("data-mode") !== mode;
    });
    renderMapStatus();
    renderCaption();
    if (els.mapEl) {
      els.mapEl.setAttribute(
        "aria-label",
        mode === MODE_NOW
          ? "Map of Taiwan with one representative weather station per county and its latest observed air temperature"
          : "Map of Taiwan with six Region markers coloured by the selected day's derived map temperature"
      );
    }
  }

  function renderCaption() {
    if (!els.mapCaption) return;
    els.mapCaption.textContent = mode === MODE_NOW
      ? (selectedCounty
        ? "Latest Observation · the stations of " + selectedCounty
        : "Latest Observation · one representative station per county")
      : forecastCaption;
  }

  // Bring the map up (once its container has a non-zero size) and bring it in line
  // with the current state: mode layer, view, observation markers, forecast pills.
  // Every caller uses this same deferred step, so a call dropped while the map
  // waits for a size is covered by the one that fires (it reads current state).
  function bringUpMap() {
    ensureMapSized(function () {
      if (!initMap()) {
        setMapStatus("The map library is unavailable.", "error");
        setObsStatus("The map library is unavailable.", "error");
        return;
      }
      syncMap();
    });
  }

  function syncMap() {
    if (appliedMode !== mode) {
      // Mode-switch path (R-V2-MAP-5): recompute the container's real pixel size
      // BEFORE any view change, so no view is computed on a stale/0x0 size.
      map.invalidateSize();
      if (mode === MODE_FORECAST) {
        map.removeLayer(nowLayer);
        if (countyLayer) map.removeLayer(countyLayer); // county interaction: Now mode only
        forecastLayer.addTo(map);
        showSixRegions();
      } else {
        map.removeLayer(forecastLayer);
        if (countyLayer) countyLayer.addTo(map);
        nowLayer.addTo(map);
        restoreNowView();
      }
      appliedMode = mode;
      styleCounties();
      raiseSelectedCounty();
    }
    renderStations();
    if (latestDay) renderDay(latestDay.date, latestDay.byRegion);
    refreshMapChrome();
  }

  // Back to Now mode: restore the view it had when it was left (R-V2-MODE-5(c)).
  function restoreNowView() {
    if (zoomAnimating) { pendingView = restoreNowView; return; } // see fitToMarkers
    if (nowView) {
      map.setView(nowView.center, nowView.zoom, { animate: false });
    } else {
      fitToMarkers(); // Now mode was never shown on a sized map: its initial view
    }
  }

  // Entering Forecast mode (R-V2-MODE-5(b), DV-8, AC-17): keep the view when all
  // six Region markers are already inside the map area not covered by the
  // Forecast mode's panels; otherwise widen the view just enough to include them.
  function showSixRegions() {
    var clear = clearArea(fitPadding(MODE_FORECAST));
    var points = regionPoints();
    var allIn = points.every(function (p) { return clear.contains(p); });
    if (!allIn) fitToMarkers(L.latLngBounds(points).extend(clear));
  }

  // The lat/lng box of the map container minus the given panel padding.
  function clearArea(pad) {
    var size = map.getSize();
    return L.latLngBounds(
      map.containerPointToLatLng(L.point(pad.tl[0], pad.tl[1])),
      map.containerPointToLatLng(L.point(size.x - pad.br[0], size.y - pad.br[1]))
    );
  }

  function regionPoints() {
    return REGION_ORDER.map(function (r) { return REGION_POINTS[r]; });
  }

  // --- top-level forecast-section states (DR-19, scoped by R-V2-DEG-3) ---------

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
    // The Forecast mode map shows the same failure inline; there are no days to
    // list, so Select Date is disabled (DR-19 per-Region rule, DV-17).
    setDateSelectEnabled(false);
    setMapStatus(message, "error");
  }
  function showEmpty(message) {
    els.pageEmptyText.textContent = message;
    els.pageEmpty.hidden = false;
    els.pageLoading.hidden = true;
    els.pageError.hidden = true;
    els.dashboard.hidden = true;
    setDateSelectEnabled(false);
    setMapStatus(message, "empty");
  }
  function showDashboard() {
    els.dashboard.hidden = false;
    els.pageLoading.hidden = true;
    els.pageError.hidden = true;
    els.pageEmpty.hidden = true;
  }

  // --- forecast bootstrap: health -> regions -> first region -------------------

  function bootstrap() {
    showLoading();
    setMapStatus("Loading the forecast…", "loading");
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

  // --- Latest Observation (Now mode) -------------------------------------------
  // GET /api/observations/latest answers a normalised success body or a
  // classified non-2xx failure {reason, error} (Issue #35). #36 renders the
  // success path and the in-progress indicator; #37 completes the Refresh
  // semantics:
  //   - one Refresh at a time: a trigger while one is in progress is ignored, and
  //     only the current request may apply its result (R-V2-OBS-7(e));
  //   - bounded time: requestObservation() always settles within OBS_TIMEOUT_MS,
  //     whatever the network or the platform does (R-V2-OBS-13);
  //   - three results (R-V2-OBS-7(d), R-V2-OBS-8, DV-4): newer (the response's
  //     dataset Observation Time is >= the one shown and it is not the same body
  //     again -> applied: data, Observation Time and Fetched Time together);
  //     not-newer (its Observation Time is older, or its Fetched Time equals the
  //     one shown, i.e. the server's reuse window -> nothing changes, the user is
  //     told it is already the latest; this is NOT Stale); failure;
  //   - failure -> Stale when data is shown (kept with both times), Unavailable
  //     otherwise; any later success clears them (R-V2-OBS-10).

  function loadObservation() {
    // A second trigger while one is in progress is ignored (R-V2-OBS-7(e)).
    if (obsInFlight) return;
    obsInFlight = true;
    var seq = ++obsSeq;
    setObsBusy(true);
    requestObservation()
      .then(function (result) {
        if (seq !== obsSeq) return; // not the current Refresh: never applied
        if (result.ok) {
          applyObservation(result.body);
        } else {
          applyObservationFailure(result);
        }
      })
      .then(null, function () {
        // A rendering error must still end the Refresh in a terminal state.
        applyObservationFailure({ ok: false, category: "unexpected_response" });
      })
      .then(function () {
        obsInFlight = false;
        setObsBusy(false);
      });
  }

  // One GET of the Latest Observation, settled exactly once and within
  // OBS_TIMEOUT_MS: {ok: true, body} for a usable success body, otherwise
  // {ok: false, category[, upstreamStatus][, httpStatus]}. When the bound
  // passes, the request is aborted and a late answer is ignored (settle()).
  function requestObservation() {
    return new Promise(function (resolve) {
      var settled = false;
      var controller = typeof AbortController !== "undefined" ? new AbortController() : null;
      var timer = setTimeout(function () {
        if (controller) controller.abort();
        settle({ ok: false, category: "no_response" });
      }, OBS_TIMEOUT_MS);
      function settle(result) {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        resolve(result);
      }
      fetch("/api/observations/latest", {
        headers: { Accept: "application/json" },
        cache: "no-store",
        signal: controller ? controller.signal : undefined,
      })
        .then(function (response) {
          return response.text().then(function (text) {
            settle(classifyObservationResponse(response, text));
          });
        })
        .then(null, function () {
          settle({ ok: false, category: "no_response" }); // network failure / aborted
        });
    });
  }

  // Classify one HTTP answer. A 2xx is a success only when its body is a usable
  // Latest Observation; a non-2xx is one of the four server reasons only when it
  // is JSON naming one of them — anything else (an HTML 502 page from the
  // platform, an empty or unparseable body, an unknown reason) is the
  // "unexpected_response" failure, never a stuck Refresh (R-V2-OBS-13).
  function classifyObservationResponse(response, text) {
    var body = null;
    try {
      body = text ? JSON.parse(text) : null;
    } catch (e) {
      body = null;
    }
    if (response.ok) {
      return usableObservation(body)
        ? { ok: true, body: body }
        : { ok: false, category: "unexpected_response", httpStatus: response.status };
    }
    var reason = body && typeof body.reason === "string" &&
      OBS_SERVER_REASONS.indexOf(body.reason) >= 0 ? body.reason : null;
    if (!reason) {
      return { ok: false, category: "unexpected_response", httpStatus: response.status };
    }
    var failure = { ok: false, category: reason };
    if (reason === "upstream_error" && isHttpStatus(body.upstreamStatus)) {
      failure.upstreamStatus = body.upstreamStatus; // a number only (DV-6, non-secret)
    }
    return failure;
  }

  // A success body the page can show and compare: stations, and an Observation
  // Time and a Fetched Time that parse to instants (so the replacement rule can
  // never compare against NaN and let an older body through).
  function usableObservation(body) {
    return !!body && Array.isArray(body.stations) &&
      typeof body.observationTime === "string" && isFinite(instant(body.observationTime)) &&
      typeof body.fetchedTime === "string" && isFinite(instant(body.fetchedTime));
  }

  function isHttpStatus(v) {
    return typeof v === "number" && Math.floor(v) === v && v >= 100 && v <= 599;
  }

  // A successful answer: apply it (newer) or keep what is shown (not-newer).
  // Either way the result is a success, so any Stale / Unavailable is cleared
  // (R-V2-OBS-10(c)).
  function applyObservation(body) {
    var previousState = obsState;
    var message;
    if (obs && body.fetchedTime === obs.fetchedTime) {
      // The very body already shown (the server's reuse window): not-newer.
      message = "Already the latest: no newer Latest Observation than the one shown.";
      setRefreshResult("not-newer");
    } else if (obs && instant(body.observationTime) < instant(obs.observationTime)) {
      // An OLDER dataset Observation Time never replaces the one displayed; data
      // and both times stay unchanged (R-V2-OBS-8(b), INV-V2-6).
      message = "Already the latest: no newer Latest Observation than the one shown.";
      setRefreshResult("not-newer");
    } else {
      // Newer, or the same Observation Time fetched again (>= applies, DV-4):
      // data, Observation Time and Fetched Time are replaced together.
      var sameHour = !!obs && instant(body.observationTime) === instant(obs.observationTime);
      obs = body;
      obsById = {};
      body.stations.forEach(function (s) { obsById[s.stationId] = s; });
      var reps = representativeIds();
      var kept = selectedStationId ? obsById[selectedStationId] : null;
      if (selectedCounty) {
        // A county is selected (and stays selected): keep the station while it is
        // still a valid station of that county in the new data.
        if (!kept || kept.countyName !== selectedCounty) selectedStationId = null;
      } else if (selectedStationId && reps.indexOf(selectedStationId) < 0) {
        selectedStationId = null; // the selected station is no longer a marker
      }
      if (previousState === "loading") {
        message = ""; // the page's first load: the data itself is the result
      } else if (previousState === "unavailable") {
        message = "Loaded the Latest Observation.";
      } else if (sameHour) {
        message = "Updated: fetched again; the Observation Time is unchanged.";
      } else {
        message = "Updated to a newer Latest Observation.";
      }
      setRefreshResult("newer");
      bringUpMap();
    }
    obsFailure = null;
    obsState = "success";
    renderObservationPanel();
    renderObsState();
    setObsStatus(message, message ? "done" : "idle");
  }

  // A failed Refresh (R-V2-OBS-10(a)(b)): with data shown -> Stale, keeping the
  // last successful data and its Observation Time / Fetched Time; with nothing
  // shown -> Unavailable. The mode never changes and Refresh stays usable.
  function applyObservationFailure(failure) {
    obsFailure = failure;
    obsState = obs ? "stale" : "unavailable";
    setRefreshResult("failure");
    renderObservationPanel();
    renderObsState();
    setObsStatus(obs ? "Refresh failed: data is Stale." : "Latest Observation unavailable.", "error");
  }

  // The last Refresh result, exposed as a data attribute for verification.
  function setRefreshResult(result) {
    els.nowPanel.setAttribute("data-refresh-result", result);
  }

  // The failure's user-visible category: fixed text, the reason code for the
  // four server reasons, and a numeric HTTP status where known (R-V2-OBS-12).
  function failureText(failure) {
    if (!failure) return "";
    var category = OBS_FAILURE_TEXT.hasOwnProperty(failure.category)
      ? failure.category : "unexpected_response";
    var text = OBS_FAILURE_TEXT[category];
    if (failure.upstreamStatus) text += " (HTTP " + failure.upstreamStatus + ")";
    else if (failure.httpStatus) text += " (HTTP " + failure.httpStatus + ")";
    if (OBS_SERVER_REASONS.indexOf(category) >= 0) text += " — " + category;
    return text + ".";
  }

  // Show the Now mode's state (R-V2-OBS-10(e)): success shows no state label;
  // Stale and Unavailable each have their own chip, explanation, category reason,
  // on-map notice and look, so they are distinct from success and from each
  // other in text and visually.
  function renderObsState() {
    var stale = obsState === "stale";
    var unavailable = obsState === "unavailable";
    var shown = stale || unavailable;
    els.nowPanel.setAttribute("data-obs-state", obsState);
    els.obsStateChip.hidden = !shown;
    els.obsStateChip.textContent = stale ? "STALE" : "UNAVAILABLE";
    els.obsStateChip.className = "chip chip--" + (stale ? "stale" : "unavailable");
    els.obsState.hidden = !shown;
    els.obsState.className = "obs-state obs-state--" + (stale ? "stale" : "unavailable");
    els.obsStateTitle.textContent = stale ? "Stale" : "Latest Observation unavailable";
    els.obsStateBody.textContent = stale
      ? "The last Refresh failed. Shown: the last successful Latest Observation " +
        "and its own times."
      : "No Latest Observation to show. Use Refresh to try again.";
    els.obsStateReason.textContent = shown ? "Reason: " + failureText(obsFailure) : "";
    els.obsMapState.hidden = !shown;
    els.obsMapState.className = "obs-map-state obs-map-state--" + (stale ? "stale" : "unavailable");
    els.obsMapState.textContent = stale
      ? "Stale · last successful Latest Observation"
      : "Latest Observation unavailable";
    if (els.mapEl) els.mapEl.classList.toggle("map--obs-stale", stale);
    // The County context repeats the state, so a county selection never hides
    // that its values are the last successful data (Stale) or absent
    // (Unavailable) — R-V2-OBS-10(b)(e), DV-21 §4.2(5).
    els.countyState.hidden = !shown;
    els.countyState.className = "county__state county__state--" + (stale ? "stale" : "unavailable");
    els.countyState.textContent = stale
      ? "Stale — the last successful Latest Observation (the last Refresh failed)."
      : "Latest Observation unavailable — no station data to show.";
  }

  function representativeIds() {
    return obs && Array.isArray(obs.representativeStationIds)
      ? obs.representativeStationIds
      : [];
  }

  function renderObservationPanel() {
    els.obsTime.textContent = obs ? formatObsTime(obs.observationTime, false) : MISSING;
    els.obsFetched.textContent = obs ? formatObsTime(obs.fetchedTime, true) : MISSING;
    els.obsCount.textContent = obs ? String(obs.validStationCount) : MISSING;
    renderCountyContext();
    renderSelectedStation();
  }

  // Show the in-progress indicator while a Refresh is running (R-V2-OBS-7(c)).
  // The button stays focusable (aria-disabled, not disabled) so keyboard focus is
  // not lost; a click while busy is ignored by loadObservation().
  function setObsBusy(busy) {
    els.refreshButton.setAttribute("aria-disabled", busy ? "true" : "false");
    els.nowPanel.setAttribute("aria-busy", busy ? "true" : "false");
    if (busy) {
      setObsStatus(obs ? "Refreshing the Latest Observation…" : "Loading the Latest Observation…", "busy");
    }
  }

  function setObsStatus(message, kind) {
    els.obsStatus.className = "obs-status obs-status--" + kind;
    els.obsStatus.textContent = "";
    if (kind === "busy") {
      var spin = document.createElement("span");
      spin.className = "spinner spinner--sm";
      spin.setAttribute("aria-hidden", "true");
      els.obsStatus.appendChild(spin);
    }
    if (message) els.obsStatus.appendChild(document.createTextNode(message));
  }

  // Rebuild the station markers when a new body is displayed or the county
  // selection changes. Taiwan-wide: one marker per id in
  // representativeStationIds (at most one per county, chosen server-side by the
  // README rule, R-V2-DD-2). A county selected: one marker per valid station of
  // that county inside the map range (R-V2-DD-5(a), R-V2-DD-11). Each marker shows
  // the station's own air temperature and name — never a county value (H-3).
  function renderStations() {
    if (!nowLayer) return;
    if (renderedObs !== obs || renderedCounty !== selectedCounty) {
      nowLayer.clearLayers();
      stationMarkers = {};
      renderedObs = obs;
      renderedCounty = selectedCounty;
      var inCounty = !!selectedCounty;
      var ids = inCounty
        ? countyStations(selectedCounty).filter(onMap).map(function (s) { return s.stationId; })
        : representativeIds();
      ids.forEach(function (id) {
        var s = obsById[id];
        if (!s) return;
        var lat = Number(s.latitude);
        var lng = Number(s.longitude);
        // Never hand Leaflet a non-finite position (the NaN-marker hazard).
        if (!isFinite(lat) || !isFinite(lng)) return;
        var marker = L.marker([lat, lng], {
          icon: stationIcon(s, inCounty),
          keyboard: false,
          title: stationName(s) + " (" + s.countyName + ")",
        });
        marker.on("add", function () { wireStationMarker(marker, id); });
        marker._tipHtml = stationTipHtml(s);
        bindOrUpdateTip(marker, marker._tipHtml);
        nowLayer.addLayer(marker);
        stationMarkers[id] = marker;
      });
    }
    highlightStations();
  }

  // A station marker. In the county view the markers are compact (the name label
  // only on the selected one, so a dense county stays readable) and are not Tab
  // stops: the county's station list is the keyboard path to them (R-V2-DD-9(b),
  // (d)). Taiwan-wide representative markers stay focusable (#36).
  function stationIcon(s, inCounty) {
    return L.divIcon({
      className: "station-icon" + (inCounty ? " station-icon--county" : ""),
      html:
        '<span class="spill" tabindex="' + (inCounty ? "-1" : "0") +
        '" role="button" aria-label="' +
        escapeHtml(stationLabel(s)) + '">' + escapeHtml(formatObsTemp(s.airTemperature)) +
        "°</span>" +
        '<span class="slabel">' + escapeHtml(stationName(s)) + "</span>",
      iconSize: [96, 48],
      iconAnchor: [48, 14],
    });
  }

  // Each time the marker's element is (re)created on the map, bind click and
  // Enter/Space on its pill and re-apply the selection highlight. A pill that
  // receives keyboard focus is brought clear of the floating panel and the on-map
  // notice, so focus is never fully hidden under them (R-V2-DD-9(e), R-V2-RSP-6).
  function wireStationMarker(marker, id) {
    var el = marker.getElement();
    if (!el) return;
    var pill = el.querySelector(".spill");
    function select() { selectStation(id); }
    (pill || el).addEventListener("click", select);
    if (pill) {
      pill.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
          e.preventDefault();
          select();
        }
      });
      // The focused marker is also drawn above its neighbours (a dense cluster
      // must not hide it) until focus leaves it.
      pill.addEventListener("focus", function () {
        marker.setZIndexOffset(2000);
        keepInClearArea(marker.getLatLng());
      });
      pill.addEventListener("blur", function () {
        marker.setZIndexOffset(id === selectedStationId ? 1000 : 0);
      });
    }
    el.classList.toggle("is-active", id === selectedStationId);
  }

  // Pan the map, only if needed, so `latlng` lies in the map area not covered by
  // the current mode's floating panel (and, while shown, the Stale / Unavailable
  // notice at the bottom of the map).
  function keepInClearArea(latlng) {
    if (!map) return;
    var pad = fitPadding(mode);
    var bottom = els.obsMapState && !els.obsMapState.hidden ? Math.max(pad.br[1], 72) : pad.br[1];
    map.panInside(latlng, {
      paddingTopLeft: pad.tl, paddingBottomRight: [pad.br[0], bottom], animate: false,
    });
  }

  // Select a station (a marker, or an item of the county's station list): the
  // marker is highlighted and raised, and the panel shows the station's detail.
  function selectStation(id) {
    if (!obsById[id]) return;
    selectedStationId = id;
    highlightStations();
    markListSelection();
    renderSelectedStation();
    // The detail opening above the list can push the focused list item out of
    // the panel's visible area: bring it back, so keyboard focus is never hidden
    // (R-V2-DD-9(e)).
    var focused = document.activeElement;
    if (focused && focused.classList && focused.classList.contains("county__item") &&
        typeof focused.scrollIntoView === "function") {
      focused.scrollIntoView({ block: "nearest" });
    }
  }

  function highlightStations() {
    Object.keys(stationMarkers).forEach(function (id) {
      var marker = stationMarkers[id];
      var on = id === selectedStationId;
      var el = marker.getElement();
      if (el) el.classList.toggle("is-active", on);
      marker.setZIndexOffset(on ? 1000 : 0); // the selected marker is drawn on top
    });
  }

  // The selected-station detail (R-V2-DD-7): the station's name and StationId,
  // county, town, its own Observation Time and air temperature, and the optional
  // values, any missing / sentinel one shown as "—" (R-V2-OBS-6). A station
  // outside the map range says so (R-V2-DD-11).
  function renderSelectedStation() {
    var s = selectedStationId ? obsById[selectedStationId] : null;
    if (!s) {
      els.obsSelected.hidden = true;
      return;
    }
    els.obsSelName.textContent = stationName(s) + " station";
    els.obsSelPlace.textContent = s.countyName + " · " + (s.townName ? String(s.townName) : MISSING);
    els.obsSelOffmap.hidden = onMap(s);
    els.obsSelId.textContent = s.stationId ? String(s.stationId) : MISSING;
    els.obsSelTemp.textContent = withUnit(formatObsTemp(s.airTemperature), " °C");
    els.obsSelRh.textContent = withUnit(published(s.relativeHumidity), " %");
    els.obsSelWind.textContent = withUnit(published(s.windSpeed), " m/s");
    els.obsSelWdir.textContent = withUnit(published(s.windDirection), "°");
    els.obsSelPres.textContent = withUnit(published(s.airPressure), " hPa");
    els.obsSelRain.textContent = withUnit(published(s.precipitation), " mm");
    els.obsSelWeather.textContent = s.weather ? String(s.weather) : MISSING;
    els.obsSelTime.textContent = formatObsTime(s.observationTime, false);
    els.obsSelected.hidden = false;
  }

  // --- county selection and County context (R-V2-DD-4..DD-9, DD-11; #38) --------

  // The valid stations of `county` in the displayed Latest Observation (every
  // entry of stations[] is already valid, R-V2-OBS-2); none when there is no
  // displayed observation (Unavailable).
  function countyStations(county) {
    if (!obs || !Array.isArray(obs.stations)) return [];
    return obs.stations.filter(function (s) { return s.countyName === county; });
  }

  // Whether a station is placed on the map: a finite WGS84 position inside E.
  function onMap(s) {
    var lat = Number(s.latitude);
    var lng = Number(s.longitude);
    return isFinite(lat) && isFinite(lng) &&
      lat >= MAP_RANGE.latitude[0] && lat <= MAP_RANGE.latitude[1] &&
      lng >= MAP_RANGE.longitude[0] && lng <= MAP_RANGE.longitude[1];
  }

  // Station order for the list and the extremes: air temperature high to low; a
  // tie goes to the smaller stationId (character-code order), so the highest and
  // the lowest station are each one definite station (README).
  function byTemperatureDesc(a, b) {
    var d = Number(b.airTemperature) - Number(a.airTemperature);
    if (d) return d;
    return a.stationId < b.stationId ? -1 : a.stationId > b.stationId ? 1 : 0;
  }

  function highestStation(list) {
    var best = null;
    list.forEach(function (s) {
      var t = Number(s.airTemperature);
      if (!isFinite(t)) return;
      if (!best || t > Number(best.airTemperature) ||
          (t === Number(best.airTemperature) && s.stationId < best.stationId)) best = s;
    });
    return best;
  }

  function lowestStation(list) {
    var best = null;
    list.forEach(function (s) {
      var t = Number(s.airTemperature);
      if (!isFinite(t)) return;
      if (!best || t < Number(best.airTemperature) ||
          (t === Number(best.airTemperature) && s.stationId < best.stationId)) best = s;
    });
    return best;
  }

  // Select a county (a click on its polygon, or the County chooser). The station
  // selection is kept only if it is a station of that county. The view is fitted
  // to the county (R-V2-DD-5(a)).
  function selectCounty(name) {
    if (COUNTY_ORDER.indexOf(name) < 0) return;
    selectedCounty = name;
    var s = selectedStationId ? obsById[selectedStationId] : null;
    if (!s || s.countyName !== name) selectedStationId = null;
    renderCountySelection();
    if (map && mode === MODE_NOW) {
      fitCounty(name);
      renderStations();
    }
    // Floating panel (>= 1180 px): scroll it so the County context is in view
    // (the chooser just above it stays in view too). Stacked layouts keep the
    // page where it is.
    if (window.innerWidth >= 1180 && typeof els.county.scrollIntoView === "function") {
      els.county.scrollIntoView({ block: "nearest" });
    }
  }

  // "Back to Taiwan" (and "All of Taiwan" in the chooser): clear the county and
  // the station and return to the Taiwan-wide initial view (R-V2-DD-8,
  // R-V2-MAP-4). Keyboard focus moves from the (now hidden) button to the county
  // chooser so it is not lost.
  function backToTaiwan() {
    var hadFocus = document.activeElement === els.backToTaiwan;
    selectedCounty = null;
    selectedStationId = null;
    renderCountySelection();
    if (map && mode === MODE_NOW) {
      fitToMarkers();
      renderStations();
    }
    if (hadFocus) els.countySelect.focus();
  }

  // Everything that shows the county selection: the chooser, the polygon styles,
  // the County context, the station list and detail, the marker note.
  function renderCountySelection() {
    els.countySelect.value = selectedCounty || "";
    styleCounties();
    raiseSelectedCounty();
    renderCaption();
    renderCountyContext();
    renderSelectedStation();
    els.obsMarkerNote.textContent = selectedCounty
      ? "Each marker is one " + selectedCounty + " station's air temperature (°C) — a " +
        "station value. Stations outside the map range are listed only."
      : "Each marker is one representative station's air temperature (°C) — a " +
        "station value, not a county temperature.";
  }

  // Fit the view so the county's stations on the map — and the county itself —
  // are inside the map area clear of the panel (R-V2-DD-5(a)). With no station to
  // show (Unavailable, or a county without valid stations) the county's own shape
  // is the view.
  function fitCounty(name) {
    if (!map) return;
    var bounds = L.latLngBounds([]);
    countyStations(name).filter(onMap).forEach(function (s) {
      bounds.extend([Number(s.latitude), Number(s.longitude)]);
    });
    if (countyShapes[name]) bounds.extend(countyShapes[name].getBounds());
    if (bounds.isValid()) fitToMarkers(bounds, COUNTY_MAX_ZOOM);
  }

  // The County context (R-V2-DD-5(b)): name, valid-station count, how many are on
  // the map, highest and lowest station (name / value) and the station list —
  // station values only, never an average or any other aggregate (R-V2-DD-5(c),
  // INV-V2-5). A success with no valid station in the county shows 0 and "—"
  // (not an error, R-V2-DD-5). With no displayed observation (Unavailable) there
  // is no station set to count: every value is "—", never 0, and no station is
  // listed (R-V2-OBS-6, DV-21 §4.2). Stale shows the retained data.
  function renderCountyContext() {
    var name = selectedCounty;
    els.county.hidden = !name;
    els.countyStations.hidden = !name;
    if (!name) {
      listedKey = null;
      els.countyList.innerHTML = "";
      return;
    }
    els.countyName.textContent = name;
    var list = countyStations(name).slice().sort(byTemperatureDesc);
    if (!obs) {
      els.countyCount.textContent = MISSING;
      els.countyOnMap.textContent = MISSING;
      els.countyMax.textContent = MISSING;
      els.countyMin.textContent = MISSING;
    } else {
      var onMapCount = list.filter(onMap).length;
      els.countyCount.textContent = String(list.length);
      els.countyOnMap.textContent = list.length - onMapCount
        ? onMapCount + " (" + (list.length - onMapCount) + " not on the map)"
        : String(onMapCount);
      els.countyMax.textContent = extremeText(highestStation(list));
      els.countyMin.textContent = extremeText(lowestStation(list));
    }
    renderCountyList(name, list);
  }

  function extremeText(s) {
    if (!s) return MISSING;
    return withUnit(formatObsTemp(s.airTemperature), " °C") + " · " + stationName(s);
  }

  // The county's station list: rebuilt only when the data or the county changes
  // (a station selection only re-marks it, so keyboard focus stays on the item).
  function renderCountyList(name, list) {
    if (listedKey && listedKey.obs === obs && listedKey.county === name) {
      markListSelection();
      return;
    }
    listedKey = { obs: obs, county: name };
    els.countyList.innerHTML = "";
    els.countyListTitle.textContent = obs ? "Stations (" + list.length + ")" : "Stations";
    if (!obs) {
      els.countyListEmpty.textContent = "No stations to list: the Latest Observation is unavailable.";
    } else if (!list.length) {
      els.countyListEmpty.textContent = "No valid station in " + name + " in this Latest Observation.";
    }
    els.countyListEmpty.hidden = !!(obs && list.length);
    els.countyList.hidden = !list.length;
    list.forEach(function (s) {
      var li = document.createElement("li");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "county__item";
      btn.setAttribute("data-station-id", s.stationId);
      btn.setAttribute("aria-pressed", "false");
      btn.setAttribute("aria-label", stationLabel(s) + (onMap(s) ? "" : ", not on the map"));
      btn.innerHTML =
        '<span class="county__item-name">' + escapeHtml(stationName(s)) +
        (s.townName ? '<span class="county__item-town">' + escapeHtml(s.townName) + "</span>" : "") +
        (onMap(s) ? "" : '<span class="county__item-off">not on the map</span>') +
        "</span>" +
        '<span class="county__item-temp">' + escapeHtml(withUnit(formatObsTemp(s.airTemperature), " °C")) +
        "</span>";
      btn.addEventListener("click", function () { selectStation(s.stationId); });
      li.appendChild(btn);
      els.countyList.appendChild(li);
    });
    markListSelection();
  }

  function markListSelection() {
    Array.prototype.forEach.call(els.countyList.querySelectorAll(".county__item"), function (btn) {
      var on = btn.getAttribute("data-station-id") === selectedStationId;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.classList.toggle("is-active", on);
    });
  }

  // The county interaction layer (R-V2-DD-4): the vendored basemap's 22 county
  // polygons joined with their names (static/data/counties.js). Transparent,
  // never coloured by data: a fixed outline + faint fill on hover, a fixed
  // outline for the selected county. Hover shows the county name; a click selects
  // the county. Built only when the two vendored files agree (22 polygons, 22
  // names); otherwise the County chooser remains the way to select a county.
  function buildCountyLayer(basemap) {
    var names = window.TAIWAN_COUNTY_NAMES;
    var geoms = basemap.taiwan && basemap.taiwan.geometries;
    if (!Array.isArray(names) || !Array.isArray(geoms) || names.length !== geoms.length ||
        names.length !== COUNTY_ORDER.length) {
      return null;
    }
    var features = geoms.map(function (g, i) {
      return { type: "Feature", properties: { countyName: names[i] }, geometry: g };
    });
    return L.geoJSON({ type: "FeatureCollection", features: features }, {
      style: function (f) { return countyStyle(f.properties.countyName); },
      onEachFeature: function (f, layer) {
        var name = f.properties.countyName;
        countyShapes[name] = layer;
        layer.bindTooltip(escapeHtml(name), {
          sticky: true, direction: "top", offset: [0, -10], className: "county-tip",
        });
        layer.on("mouseover", function () { hoveredCounty = name; styleCounties(); });
        layer.on("mouseout", function () {
          if (hoveredCounty === name) hoveredCounty = null;
          styleCounties();
        });
        layer.on("click", function () { selectCounty(name); });
        // Not a keyboard Tab stop (R-V2-DD-9(d)): the bound tooltip makes Leaflet
        // add focus listeners to the SVG path, and Chromium then puts such a path
        // in the sequential focus order — with no visible focus and no key
        // action. An explicit tabindex="-1" takes it out of the Tab order; the
        // keyboard path to a county is the County chooser (R-V2-DD-9(a)). Leaflet
        // creates a new path element each time the layer is added, so this runs
        // on every "add" (#38 cycle 1 F-1).
        layer.on("add", function () {
          var el = layer.getElement && layer.getElement();
          if (el) el.setAttribute("tabindex", "-1");
        });
      },
    });
  }

  function countyStyle(name) {
    var selected = name === selectedCounty;
    var hovered = name === hoveredCounty;
    return {
      stroke: true,
      color: selected ? "#fbbf24" : "#9ed0ff",
      opacity: selected || hovered ? 1 : 0,
      weight: selected ? 2.5 : 2,
      fill: true,
      fillColor: "#9ed0ff",
      fillOpacity: hovered ? 0.14 : 0,
    };
  }

  // Draw the selected county's outline above its neighbours'. Called on a
  // selection change and when the layer comes back with Now mode — never on
  // hover, so a hovered shape is not re-inserted under the pointer.
  function raiseSelectedCounty() {
    var shape = selectedCounty && countyShapes[selectedCounty];
    if (shape && map && map.hasLayer(shape)) shape.bringToFront();
  }

  function styleCounties() {
    Object.keys(countyShapes).forEach(function (name) {
      countyShapes[name].setStyle(countyStyle(name));
    });
  }

  function stationName(s) {
    return s.stationName ? String(s.stationName) : MISSING;
  }

  function stationLabel(s) {
    return stationName(s) + " station, " + s.countyName + ": air temperature " +
      formatObsTemp(s.airTemperature) + " °C (Latest Observation, station value)";
  }

  function stationTipHtml(s) {
    return (
      '<b class="map-tip__region">' + escapeHtml(stationName(s)) + " station</b>" +
      '<span class="map-tip__row">' + escapeHtml(s.countyName) +
      (s.townName ? " · " + escapeHtml(s.townName) : "") + "</span>" +
      '<span class="map-tip__row">Air temperature ' +
      escapeHtml(formatObsTemp(s.airTemperature)) + " °C</span>" +
      '<span class="map-tip__row">Observation Time ' +
      escapeHtml(formatObsTime(s.observationTime, false)) + "</span>" +
      '<span class="map-tip__row map-tip__note">Station value, not a county value</span>'
    );
  }

  // A published temperature for display: the /api/ number unchanged (never
  // rounded), shown with at least one decimal ("25" -> "25.0").
  function formatObsTemp(v) {
    var n = Number(v);
    if (v === null || v === undefined || v === "" || !isFinite(n)) return MISSING;
    var text = String(n);
    return /[.e]/.test(text) ? text : n.toFixed(1);
  }

  function published(v) {
    if (v === null || v === undefined || v === "") return MISSING;
    var n = Number(v);
    return isFinite(n) ? String(n) : MISSING;
  }

  function withUnit(text, unit) {
    return text === MISSING ? MISSING : text + unit;
  }

  // Display an ISO time exactly as published, to the minute (Observation Time)
  // or the second (Fetched Time), with its UTC offset. The string is re-laid-out,
  // never converted through the browser clock or time zone (R-V2-OBS-4).
  function formatObsTime(text, withSeconds) {
    if (!text) return MISSING;
    var m = /^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(:\d{2})?(?:\.\d+)?(Z|[+-]\d{2}:?\d{2})?$/.exec(String(text));
    if (!m) return String(text);
    return m[1] + " " + m[2] + (withSeconds && m[3] ? m[3] : "") + (m[4] ? " " + m[4] : "");
  }

  function instant(text) {
    return Date.parse(String(text));
  }

  // --- Select Date + Taiwan Map, Forecast mode (R-EN-3..R-EN-7) ----------------
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
    forecastCaption = "Showing " + date;
    renderCaption();
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

  // Keep `date`'s six values and render them: the info panel (day tiles +
  // selected-Region block) always, the pills whenever the Forecast mode layer is
  // on the map. Called only on a successful 2xx with values. The map view is NOT
  // reset when Select Date changes — only the pills/tooltips/panel update
  // (AC-18, P-12).
  function applyDay(date, values) {
    var byRegion = {};
    values.forEach(function (v) { byRegion[v.regionName] = v; });
    latestDay = { date: date, byRegion: byRegion };
    renderDay(date, byRegion);
    // Bring up the map when its container actually has a non-zero size (init
    // hardening, P-12) — syncMap() then paints this day onto the pills.
    bringUpMap();
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
    // colourBand. No re-derivation, no re-banding (H-3, R-SHR-4). A pill that is
    // not on the map (Now mode) has no element yet; it is painted when the
    // Forecast mode layer is added.
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
  // visibilitychange covers a background tab (P-12, init hardening). Page load,
  // data arrival and the mode switch all reach the map through here (R-V2-MAP-5).
  function ensureMapSized(cb) {
    var container = els.mapFrame ? document.getElementById("map") : null;
    function sized() {
      return container && container.clientWidth > 0 && container.clientHeight > 0;
    }
    if (sized()) { cb(); return; }
    if (mapInitScheduled) return; // already waiting; the pending step reads current state
    mapInitScheduled = true;
    var done = false;
    function fire() {
      if (done || !sized()) return;
      done = true;
      mapInitScheduled = false;
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
  // coastlines under the Taiwan county polygons), the Forecast mode's six pill
  // markers in their own layer group, and an (initially empty) layer group for
  // the Now mode's station markers; only the current mode's group is on the map.
  // Then fit the current mode's initial view ONCE (R-EN-4, R-V2-MAP-4). Returns
  // false if Leaflet is unavailable. Assumes the container already has a non-zero
  // size (ensureMapSized).
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

    // The Now mode's county interaction layer (#38): same polygons, drawn
    // transparent above the backdrop, with the county names attached.
    countyLayer = buildCountyLayer(basemap);

    forecastLayer = L.layerGroup();
    nowLayer = L.layerGroup();

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
      // "add" fires each time the Forecast mode layer puts the marker on the map
      // (a fresh element each time), so the listeners are bound to that element.
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
      forecastLayer.addLayer(marker);
      markers[region] = marker;
    });

    if (mode === MODE_NOW && countyLayer) countyLayer.addTo(map);
    (mode === MODE_FORECAST ? forecastLayer : nowLayer).addTo(map);
    appliedMode = mode;

    // On any move (zoom, or a resize re-fit) the markers shift relative to the
    // edges, so refresh the zoom-label class and re-pick each tooltip's direction
    // to keep it unclipped (V-3).
    map.on("moveend", refreshMapChrome);
    // Track Leaflet's zoom animation so a view change requested during it is not
    // lost (fitToMarkers / restoreNowView keep the latest; it is applied here, at
    // the animation's end).
    map.on("zoomanim", function () { zoomAnimating = true; });
    map.on("zoomend", function () {
      zoomAnimating = false;
      if (pendingView) {
        var apply = pendingView;
        pendingView = null;
        apply();
      }
    });

    // Now that the container is laid out, recompute size and fit the current
    // mode's initial view. fitToMarkers() is the ONLY fitBounds call site — used
    // at init, on a width resize and when entering Forecast mode needs a wider
    // view; never on a Select Date change (the view must not reset, P-12).
    fitToMarkers();
    refreshMapChrome();
    colourLegend();
    return true;
  }

  // Hide the marker labels when zoomed far out (the name is still in the tooltip,
  // panel and aria-label) and re-pick every tooltip's direction.
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
    Object.keys(stationMarkers).forEach(function (id) {
      var m = stationMarkers[id];
      if (m._tipHtml) bindOrUpdateTip(m, m._tipHtml);
    });
  }

  // Map padding that keeps markers clear of the mode's panels. When the info
  // panel (and, in Forecast mode, the legend) FLOAT over the map (>= 1180px),
  // reserve their footprint (left for the top-left panel, right for the
  // bottom-right legend) so no marker or its tooltip sits under them (P-7c, #28
  // F-1/F-2/F-3); below 1180px the panels are stacked OUTSIDE the map (CSS), so
  // modest padding keeps the pills separated and their tooltips inside the frame
  // (V-3, V-4). The Forecast mode values are the V1 ones unchanged.
  function fitPadding(forMode) {
    var floating = window.innerWidth >= 1180;
    if (forMode === MODE_FORECAST) {
      return floating
        ? { tl: [392, 64], br: [300, 56] }
        : { tl: [26, 52], br: [26, 44] };
    }
    return floating
      ? { tl: [330, 24], br: [24, 24] }
      : { tl: [24, 24], br: [24, 24] };
  }

  // Fit the view: to `bounds` when given, otherwise to the current mode's initial
  // view (Forecast mode: the six Region markers, as in V1; Now mode: the main
  // island plus 澎湖). `maxZoom` caps how close the fit goes (default 8; a county
  // fit passes its own cap). Tooltip clipping at the top edge is handled
  // per-marker by tipDir(). invalidateSize() always runs first so fitBounds
  // measures real pixels (else an infinite zoom -> NaN markers).
  function fitToMarkers(bounds, maxZoom) {
    if (!map) return;
    // Leaflet drops a zoom requested while a zoom animation is still running, so
    // a fit asked for then (e.g. county choices in quick succession) is kept and
    // applied — only the latest one — when the animation ends (#38).
    if (zoomAnimating) {
      pendingView = function () { fitToMarkers(bounds, maxZoom); };
      return;
    }
    map.invalidateSize();
    var pad = fitPadding(mode);
    var target = bounds || (mode === MODE_FORECAST ? regionPoints() : NOW_INITIAL_BOUNDS);
    map.fitBounds(target, {
      paddingTopLeft: pad.tl,
      paddingBottomRight: pad.br,
      maxZoom: maxZoom || 8,
    });
    lastFitWidth = window.innerWidth; // remember the width this fit was for (#28 R2 N-2)
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

  // Inline status of the Forecast mode map. `kind` is "loading" | "error" |
  // "empty". It is kept as state and shown ONLY in Forecast mode; it overlays
  // ONLY the map frame — the info panel (with Select Date) stays visible and
  // operable so the user can switch to a working day (DR-19, P-7b). The map is
  // hidden while a status shows so a stale map is never left behind an error
  // message; it keeps its layout box (visibility, not display) so ResizeObserver
  // still sees a non-zero size.
  var forecastMapStatus = null;

  function setMapStatus(message, kind) {
    forecastMapStatus = { message: message, kind: kind };
    renderMapStatus();
  }

  function hideMapStatus() {
    forecastMapStatus = null;
    renderMapStatus();
  }

  function renderMapStatus() {
    if (!els.mapStatus) return;
    var st = mode === MODE_FORECAST ? forecastMapStatus : null;
    if (!st) {
      els.mapStatus.hidden = true;
      els.mapStatus.textContent = "";
      if (els.mapFrame) els.mapFrame.classList.remove("map-frame--status");
      return;
    }
    els.mapStatus.textContent = st.message;
    els.mapStatus.className = "map-status state--inline state--inline-" + st.kind;
    els.mapStatus.setAttribute("role", st.kind === "error" ? "alert" : "status");
    els.mapStatus.hidden = false;
    if (els.mapFrame) els.mapFrame.classList.add("map-frame--status");
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
