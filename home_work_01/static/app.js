/* Taiwan Weather Forecast — dashboard frontend (Issue #23, ENHANCED UI/UX).
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

    els.regionSelect.addEventListener("change", function () {
      loadRegion(els.regionSelect.value);
    });

    // Redraw the chart at the new width on resize (the SVG is drawn at the
    // container's own pixel width so its labels stay legible, F-3) and drop any
    // open tooltip so its pixel maths never goes stale.
    window.addEventListener("resize", function () {
      hideTooltip();
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (currentSeries) renderChart(currentSeries);
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
        if (!res.ok) {
          // Any non-2xx (503 missing/empty/incomplete, 5xx, 404) is an error
          // (DR-19); surface the server's message so the cause stays visible.
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
      if (!res.ok) {
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
        if (!res.ok) {
          // Failed request (404 / 503 / 5xx) -> inline error (DR-19).
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
    return fetch(url, { headers: { Accept: "application/json" } }).then(
      function (response) {
        return response
          .json()
          .catch(function () { return {}; })
          .then(function (body) {
            return { ok: response.ok, status: response.status, body: body };
          });
      }
    );
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
