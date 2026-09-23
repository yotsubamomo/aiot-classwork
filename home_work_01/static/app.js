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
 * Three visible states cover every outcome (R-EN-1 item 5, R-DS-6):
 *   - loading  : the initial requests are in flight;
 *   - empty    : /api/health returns 503 (snapshot missing / empty / incomplete);
 *   - error    : a network failure or unexpected error.
 * A 404 / 503 on a per-Region request shows an inline message inside the chart
 * card rather than a blank chart.
 */
"use strict";

(function () {
  var els = {};
  var chartState = null; // geometry + series for the hover tooltip

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

    // Reposition/redraw is not needed on resize because the SVG scales with the
    // container; only the tooltip's pixel maths reads the live width, so hide any
    // open tooltip on resize to avoid a stale position.
    window.addEventListener("resize", hideTooltip);

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
          // 503: the snapshot is missing / empty / incomplete -> empty state.
          showEmpty(reasonMessage(res.body));
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
        showEmpty(reasonMessage(res.body));
        return;
      }
      var regions = (res.body && res.body.regions) || [];
      if (!regions.length) {
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
    // visible panel (finding F-1, R-DS-6), and show an inline loading message
    // while the request is in flight.
    els.panel.hidden = false;
    els.panelHeading.textContent = "Temperature Forecast – " + region;
    hideTooltip();
    showChartStatus("Loading " + region + "…");
    fetchJson("/api/regions/" + encodeURIComponent(region) + "/series")
      .then(function (res) {
        if (!res.ok) {
          els.summary.hidden = true;
          showChartStatus(
            res.status === 404
              ? "That Region is not available in this snapshot."
              : reasonMessage(res.body)
          );
          return;
        }
        hideChartStatus();
        var series = (res.body && res.body.series) || [];
        renderSummary(series);
        renderChart(series);
        renderTable(series);
      })
      .catch(function () {
        els.summary.hidden = true;
        showChartStatus("Cannot load this Region right now. Please try again.");
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
    var W = 720;
    var H = 340;
    var m = { top: 18, right: 18, bottom: 46, left: 46 };
    var innerW = W - m.left - m.right;
    var innerH = H - m.top - m.bottom;

    els.chart.innerHTML = "";
    hideTooltip();
    chartState = null;
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
    var half = n === 1 ? innerW / 2 : innerW / (n - 1) / 2;
    series.forEach(function (r, i) {
      var x0 = xAt(i) - half;
      var w = half * 2;
      if (i === 0) { x0 = m.left; }
      if (i === n - 1) { w = m.left + innerW - x0; }
      var hit = svgEl("rect", {
        class: "chart__hit", x: x0, y: m.top, width: Math.max(w, 1), height: innerH,
      });
      hit.addEventListener("mouseenter", function () { showTooltip(i); });
      hit.addEventListener("mousemove", function () { showTooltip(i); });
      svg.appendChild(hit);
    });

    var canvas = els.chart;
    canvas.addEventListener("mouseleave", hideTooltip);

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

  function showTooltip(i) {
    if (!chartState) return;
    var s = chartState;
    var row = s.series[i];
    if (!row) return;

    // Highlight the two dots for this date.
    clearActiveDots();
    if (s.maxtDots[i]) s.maxtDots[i].classList.add("chart__dot--active");
    if (s.mintDots[i]) s.mintDots[i].classList.add("chart__dot--active");

    // Move the vertical guide line.
    var gx = s.xAt(i);
    s.guide.setAttribute("x1", gx);
    s.guide.setAttribute("x2", gx);
    s.guide.setAttribute("visibility", "visible");

    // Fill and position the HTML tooltip. Convert SVG viewBox coords to canvas
    // pixels using the live render scale (SVG width:100%, uniform aspect ratio).
    els.chartTooltip.innerHTML =
      '<div class="chart-tooltip__date">' + escapeHtml(row.dataDate) + "</div>" +
      '<div class="chart-tooltip__row"><span class="chart-tooltip__dot chart-tooltip__dot--maxt"></span>MaxT ' +
      escapeHtml(formatTemp(row.maxt)) + "°C</div>" +
      '<div class="chart-tooltip__row"><span class="chart-tooltip__dot chart-tooltip__dot--mint"></span>MinT ' +
      escapeHtml(formatTemp(row.mint)) + "°C</div>";
    var scale = (s.svg.clientWidth || s.W) / s.W;
    var px = s.xAt(i) * scale;
    var py = s.yAt(row.maxt) * scale;
    els.chartTooltip.style.left = px + "px";
    els.chartTooltip.style.top = py + "px";
    els.chartTooltip.hidden = false;
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

  function showChartStatus(message) {
    els.chartStatus.textContent = message;
    els.chartStatus.hidden = false;
    els.chart.innerHTML = "";
    els.tableBody.innerHTML = "";
    hideTooltip();
    chartState = null;
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
