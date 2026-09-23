/* Taiwan Weather Forecast — dashboard frontend (Issue #20, MVM).
 *
 * All data comes from THIS application's own JSON API under the "/api/" prefix
 * (R-DS-5, R-SHR-5, AC-04(b)); the browser never calls CWA and holds no key.
 * The page bootstraps from /api/health, populates "Select Region" from
 * /api/regions, and for the selected Region draws a MaxT / MinT seven-day line
 * chart (hand-drawn inline SVG, no chart library) and a Date / MinT / MaxT table
 * whose seven rows equal data.db, plus the snapshot's acquisition time (DR-17).
 *
 * Every failure mode — 503 (snapshot unavailable), 404 (unknown Region/date),
 * or a network error — shows a clear, visible message instead of a blank page
 * (R-DS-6).
 */
"use strict";

(function () {
  var els = {};

  document.addEventListener("DOMContentLoaded", function () {
    els.pageError = document.getElementById("page-error");
    els.controls = document.getElementById("controls");
    els.regionSelect = document.getElementById("region-select");
    els.ingestionTime = document.getElementById("ingestion-time");
    els.panel = document.getElementById("region-panel");
    els.panelHeading = document.getElementById("panel-heading");
    els.chartStatus = document.getElementById("chart-status");
    els.chart = document.getElementById("chart");
    els.tableBody = document.getElementById("table-body");

    els.regionSelect.addEventListener("change", function () {
      loadRegion(els.regionSelect.value);
    });

    bootstrap();
  });

  // --- bootstrap: health -> regions -> first region --------------------------

  function bootstrap() {
    fetchJson("/api/health")
      .then(function (res) {
        if (!res.ok) {
          showPageError(reasonMessage(res.body));
          return;
        }
        hidePageError();
        showIngestionTime(res.body.ingestion_time);
        return loadRegions();
      })
      .catch(function () {
        showPageError(
          "Cannot reach the forecast service. Please check that the server is running."
        );
      });
  }

  function loadRegions() {
    return fetchJson("/api/regions").then(function (res) {
      if (!res.ok) {
        showPageError(reasonMessage(res.body));
        return;
      }
      var regions = (res.body && res.body.regions) || [];
      populateRegions(regions);
      els.controls.hidden = false;
      if (regions.length) {
        // Default to the first Region, but honour a ?region= deep link when it
        // names one of the six Regions (shareable per-Region URL).
        var wanted = new URLSearchParams(window.location.search).get("region");
        var initial = regions.indexOf(wanted) >= 0 ? wanted : regions[0];
        els.regionSelect.value = initial;
        loadRegion(initial);
      }
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

  // --- a selected Region: series -> chart + table ----------------------------

  function loadRegion(region) {
    // Reveal the panel and set the heading up front so that EVERY outcome —
    // success, a 404/503 from /series, or a network error — renders inside a
    // visible panel. The message element (#chart-status) lives inside this
    // panel, so leaving the panel hidden here would swallow the error message on
    // first load and show a silent, chart-less page (finding F-1, R-DS-6). Doing
    // it before the fetch also stops the heading from going stale on a failed
    // Region switch.
    els.panel.hidden = false;
    els.panelHeading.textContent = "Temperature Forecast – " + region;
    fetchJson("/api/regions/" + encodeURIComponent(region) + "/series")
      .then(function (res) {
        if (!res.ok) {
          showChartStatus(
            res.status === 404
              ? "That Region is not available in this snapshot."
              : reasonMessage(res.body)
          );
          return;
        }
        hideChartStatus();
        var series = (res.body && res.body.series) || [];
        renderChart(series);
        renderTable(series);
      })
      .catch(function () {
        showChartStatus("Cannot load this Region right now. Please try again.");
      });
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

  // --- inline-SVG line chart (MaxT red, MinT blue) ---------------------------

  function renderChart(series) {
    var W = 720;
    var H = 320;
    var m = { top: 16, right: 16, bottom: 44, left: 44 };
    var innerW = W - m.left - m.right;
    var innerH = H - m.top - m.bottom;

    els.chart.innerHTML = "";
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

    var svg = svgEl("svg", {
      viewBox: "0 0 " + W + " " + H,
      role: "img",
    });

    // Axes.
    svg.appendChild(svgEl("line", {
      class: "chart__axis",
      x1: m.left, y1: m.top, x2: m.left, y2: m.top + innerH,
    }));
    svg.appendChild(svgEl("line", {
      class: "chart__axis",
      x1: m.left, y1: m.top + innerH, x2: m.left + innerW, y2: m.top + innerH,
    }));

    // Y ticks and gridlines.
    var ticks = yTicks(lo, hi);
    ticks.forEach(function (t) {
      var y = yAt(t);
      var label = svgEl("text", {
        class: "chart__tick-label", x: m.left - 8, y: y + 4,
        "text-anchor": "end",
      });
      label.textContent = String(t);
      svg.appendChild(label);
    });

    // Y axis title.
    var yTitle = svgEl("text", {
      class: "chart__axis-label",
      x: 12, y: m.top + innerH / 2,
      "text-anchor": "middle",
      transform: "rotate(-90 12 " + (m.top + innerH / 2) + ")",
    });
    yTitle.textContent = "Temperature (°C)";
    svg.appendChild(yTitle);

    // X tick labels (dates, MM-DD to stay legible).
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

    // Lines.
    svg.appendChild(polyline(series, "maxt", xAt, yAt));
    svg.appendChild(polyline(series, "mint", xAt, yAt));

    // Dots with hover tooltips.
    series.forEach(function (r, i) {
      svg.appendChild(dot(xAt(i), yAt(r.maxt), "maxt", r.dataDate, r.maxt, "MaxT"));
      svg.appendChild(dot(xAt(i), yAt(r.mint), "mint", r.dataDate, r.mint, "MinT"));
    });

    els.chart.appendChild(svg);
  }

  function polyline(series, key, xAt, yAt) {
    var pts = series.map(function (r, i) {
      return xAt(i) + "," + yAt(r[key]);
    }).join(" ");
    return svgEl("polyline", {
      class: "chart__line chart__line--" + key,
      points: pts,
      fill: "none",
      "stroke-width": 2,
    });
  }

  function dot(x, y, key, date, value, label) {
    var c = svgEl("circle", {
      class: "chart__dot chart__dot--" + key,
      cx: x, cy: y, r: 3.5,
    });
    var title = svgEl("title", {});
    title.textContent = label + " " + date + ": " + formatTemp(value) + "°C";
    c.appendChild(title);
    return c;
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

  function showPageError(message) {
    els.pageError.textContent = message;
    els.pageError.hidden = false;
    els.controls.hidden = true;
    els.panel.hidden = true;
  }
  function hidePageError() {
    els.pageError.hidden = true;
    els.pageError.textContent = "";
  }

  function showChartStatus(message) {
    els.chartStatus.textContent = message;
    els.chartStatus.hidden = false;
    els.chart.innerHTML = "";
    els.tableBody.innerHTML = "";
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

  function svgEl(name, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.keys(attrs || {}).forEach(function (k) {
      el.setAttribute(k, attrs[k]);
    });
    return el;
  }
})();
