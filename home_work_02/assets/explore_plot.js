/* HW2 V2 Exploratory run: actual vs predicted with every test row's 95% PI (Spec V2 「實際 vs 預測圖」).
 *
 * V2's own drawing module (Tickets Review adjustment A): it does not reuse or change the V1 dashboard
 * script. Linear axes on the target's own units (the target may be negative or zero; no log). Every
 * test row is drawn with its vertical PI segment, coloured and shaped by covered (circle = inside the
 * PI, square = outside, so the state is not told by colour alone), and the y = x line. Interaction
 * follows the V1 plot: wheel zoom, drag pan, keyboard (arrows pan, + / - zoom, 0 reset), buttons, and a
 * tooltip with the row, prediction, actual value and PI. Text goes to the canvas with fillText and to the
 * tooltip with textContent only (DA D-2). Browser only (window.HW2ExplorePlot). */
(function (root) {
  'use strict';

  var nf = new Intl.NumberFormat('zh-TW', { maximumFractionDigits: 2 });

  function niceStep(span, target) {
    var raw = span / target, mag = Math.pow(10, Math.floor(Math.log10(raw))), r = raw / mag;
    return (r <= 1 ? 1 : r <= 2 ? 2 : r <= 2.5 ? 2.5 : r <= 5 ? 5 : 10) * mag;
  }
  function linearTicks(a, b, target) {
    if (!(b > a)) return [a];
    var step = niceStep(b - a, target || 6), out = [];
    for (var v = Math.ceil(a / step) * step; v <= b + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    return out;
  }
  function tickLabel(v) {
    var a = Math.abs(v);
    if (a >= 1e9 || (a > 0 && a < 1e-3)) return v.toExponential(1);
    if (a >= 1e4) return nf.format(Math.round(v));
    return nf.format(v);
  }

  function Scatter(canvas, tip, opts) {
    this.canvas = canvas; this.tip = tip; this.opts = opts || {};
    this.pts = []; this.view = null; this.home = null; this.drag = null; this.hover = null;
    this.margin = { l: 78, r: 14, t: 12, b: 46 };
    this.xLabel = '預測值'; this.yLabel = '實際值';
    this.bind();
  }

  /* points: [{row, actual, predicted, lower, upper, covered}] */
  Scatter.prototype.setData = function (points, labels) {
    this.pts = points.slice();
    if (labels) { this.xLabel = labels.x; this.yLabel = labels.y; }
    var lo = Infinity, hi = -Infinity;
    this.pts.forEach(function (p) {
      lo = Math.min(lo, p.predicted, p.actual, p.lower);
      hi = Math.max(hi, p.predicted, p.actual, p.upper);
    });
    if (!(hi > lo)) { lo -= 1; hi += 1; }
    var pad = (hi - lo) * 0.04;
    this.home = { x0: lo - pad, x1: hi + pad, y0: lo - pad, y1: hi + pad };
    this.view = Object.assign({}, this.home);
    this.hover = null;
    if (this.tip) this.tip.hidden = true;
    this.draw();
  };
  Scatter.prototype.clear = function () { this.pts = []; this.view = null; this.home = null; if (this.tip) this.tip.hidden = true; };

  Scatter.prototype.size = function () {
    var rect = this.canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    var w = Math.max(1, Math.round(rect.width)), h = Math.max(1, Math.round(rect.height));
    if (this.canvas.width !== Math.round(w * dpr) || this.canvas.height !== Math.round(h * dpr)) {
      this.canvas.width = Math.round(w * dpr); this.canvas.height = Math.round(h * dpr);
    }
    return { w: w, h: h, dpr: dpr };
  };
  Scatter.prototype.sx = function (v) { var m = this.margin, w = this.view; return m.l + (v - w.x0) / (w.x1 - w.x0) * (this.w - m.l - m.r); };
  Scatter.prototype.sy = function (v) { var m = this.margin, w = this.view; return this.h - m.b - (v - w.y0) / (w.y1 - w.y0) * (this.h - m.t - m.b); };
  Scatter.prototype.ix = function (px) { var m = this.margin, w = this.view; return w.x0 + (px - m.l) / (this.w - m.l - m.r) * (w.x1 - w.x0); };
  Scatter.prototype.iy = function (py) { var m = this.margin, w = this.view; return w.y0 + (this.h - m.b - py) / (this.h - m.t - m.b) * (w.y1 - w.y0); };

  Scatter.prototype.draw = function () {
    if (!this.view) return;
    var dim = this.size();
    if (dim.w < 4 || dim.h < 4) return;                     /* hidden: drawn again when shown */
    this.w = dim.w; this.h = dim.h;
    var ctx = this.canvas.getContext('2d'), m = this.margin, w = this.w, h = this.h, v = this.view, self = this;
    ctx.setTransform(dim.dpr, 0, 0, dim.dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, w, h);
    ctx.font = '11px "Noto Sans TC","Microsoft JhengHei","PingFang TC",system-ui,sans-serif';
    ctx.strokeStyle = '#E6ECF4'; ctx.fillStyle = '#475569'; ctx.lineWidth = 1;
    var lastX = -Infinity;
    linearTicks(v.x0, v.x1, Math.max(3, Math.floor((w - m.l - m.r) / 90))).forEach(function (t) {
      var x = self.sx(t); ctx.beginPath(); ctx.moveTo(x, m.t); ctx.lineTo(x, h - m.b); ctx.stroke();
      var label = tickLabel(t), half = ctx.measureText(label).width / 2;
      if (x - half > lastX + 6) { ctx.textAlign = 'center'; ctx.fillText(label, x, h - m.b + 14); lastX = x + half; }
    });
    linearTicks(v.y0, v.y1, Math.max(3, Math.floor((h - m.t - m.b) / 50))).forEach(function (t) {
      var y = self.sy(t); ctx.beginPath(); ctx.moveTo(m.l, y); ctx.lineTo(w - m.r, y); ctx.stroke();
      ctx.textAlign = 'right'; ctx.fillText(tickLabel(t), m.l - 6, y + 4);
    });
    ctx.fillStyle = '#334155'; ctx.textAlign = 'center';
    ctx.fillText(this.xLabel, m.l + (w - m.l - m.r) / 2, h - 8);
    ctx.save(); ctx.translate(14, m.t + (h - m.t - m.b) / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText(this.yLabel, 0, 0); ctx.restore();

    ctx.save();
    ctx.beginPath(); ctx.rect(m.l, m.t, w - m.l - m.r, h - m.t - m.b); ctx.clip();
    var a = Math.max(v.x0, v.y0), b = Math.min(v.x1, v.y1);
    ctx.setLineDash([6, 4]); ctx.strokeStyle = '#0F172A'; ctx.lineWidth = 1.25;
    ctx.beginPath(); ctx.moveTo(this.sx(a), this.sy(a)); ctx.lineTo(this.sx(b), this.sy(b)); ctx.stroke();
    ctx.setLineDash([]);
    var i, p, x, y;
    for (i = 0; i < this.pts.length; i++) {
      p = this.pts[i]; x = this.sx(p.predicted);
      ctx.strokeStyle = p.covered ? 'rgba(30,64,175,0.45)' : 'rgba(180,83,9,0.8)'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(x, this.sy(p.lower)); ctx.lineTo(x, this.sy(p.upper)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x - 3, this.sy(p.lower)); ctx.lineTo(x + 3, this.sy(p.lower));
      ctx.moveTo(x - 3, this.sy(p.upper)); ctx.lineTo(x + 3, this.sy(p.upper)); ctx.stroke();
    }
    for (i = 0; i < this.pts.length; i++) {
      p = this.pts[i]; x = this.sx(p.predicted); y = this.sy(p.actual);
      if (p.covered) { ctx.fillStyle = '#1E40AF'; ctx.beginPath(); ctx.arc(x, y, 4, 0, 2 * Math.PI); ctx.fill(); }
      else { ctx.fillStyle = '#B45309'; ctx.fillRect(x - 4, y - 4, 8, 8); }
    }
    if (this.hover) {
      p = this.hover; x = this.sx(p.predicted);
      ctx.strokeStyle = '#0F172A'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x, this.sy(p.lower)); ctx.lineTo(x, this.sy(p.upper)); ctx.stroke();
      ctx.beginPath(); ctx.arc(x, this.sy(p.actual), 6, 0, 2 * Math.PI); ctx.stroke();
    }
    ctx.restore();
    ctx.strokeStyle = '#94A3B8'; ctx.lineWidth = 1; ctx.strokeRect(m.l, m.t, w - m.l - m.r, h - m.t - m.b);
  };

  Scatter.prototype.zoomAt = function (px, py, factor) {
    var v = this.view, cx = this.ix(px), cy = this.iy(py);
    var span = (v.x1 - v.x0) * factor, homeSpan = this.home.x1 - this.home.x0;
    if (span < homeSpan * 1e-3) factor = homeSpan * 1e-3 / (v.x1 - v.x0);
    if (span > homeSpan * 1.5) factor = homeSpan * 1.5 / (v.x1 - v.x0);
    this.view = { x0: cx - (cx - v.x0) * factor, x1: cx + (v.x1 - cx) * factor,
      y0: cy - (cy - v.y0) * factor, y1: cy + (v.y1 - cy) * factor };
  };
  Scatter.prototype.panBy = function (dx, dy) {
    var v = this.view, m = this.margin;
    var kx = (v.x1 - v.x0) / (this.w - m.l - m.r), ky = (v.y1 - v.y0) / (this.h - m.t - m.b);
    this.view = { x0: v.x0 - dx * kx, x1: v.x1 - dx * kx, y0: v.y0 + dy * ky, y1: v.y1 + dy * ky };
  };
  Scatter.prototype.center = function () {
    var m = this.margin;
    return [m.l + (this.w - m.l - m.r) / 2, m.t + (this.h - m.t - m.b) / 2];
  };
  Scatter.prototype.nearest = function (px, py) {
    var best = null, bestD = 144;
    for (var i = 0; i < this.pts.length; i++) {
      var dx = this.sx(this.pts[i].predicted) - px, dy = this.sy(this.pts[i].actual) - py, d = dx * dx + dy * dy;
      if (d < bestD) { bestD = d; best = this.pts[i]; }
    }
    return best;
  };
  Scatter.prototype.showTip = function (p, px, py) {
    if (!this.tip) return;
    if (!p) { this.tip.hidden = true; return; }
    var fmt = this.opts.format || tickLabel, tip = this.tip;
    tip.textContent = '';
    ['第 ' + (p.row + 1) + ' 列（載入後的列序）', '預測 ' + fmt(p.predicted), '實際 ' + fmt(p.actual),
      '95% PI ' + fmt(p.lower) + ' – ' + fmt(p.upper), p.covered ? '落入區間（圓點）' : '未落入區間（方塊）'].forEach(function (t) {
      var d = document.createElement('div'); d.textContent = t; tip.appendChild(d);
    });
    tip.hidden = false;
    var flip = px > this.w / 2;
    tip.style.transform = flip ? 'translate(calc(-100% - 12px), -50%)' : 'translate(12px, -50%)';
    tip.style.left = px + 'px';
    tip.style.top = Math.min(Math.max(py, 50), this.h - 50) + 'px';
  };

  Scatter.prototype.bind = function () {
    var self = this, c = this.canvas;
    c.addEventListener('wheel', function (ev) {
      if (!self.view) return;
      ev.preventDefault();
      var r = c.getBoundingClientRect();
      self.zoomAt(ev.clientX - r.left, ev.clientY - r.top, Math.exp(ev.deltaY * 0.0015));
      self.draw();
    }, { passive: false });
    c.addEventListener('pointerdown', function (ev) {
      if (!self.view) return;
      self.drag = { x: ev.clientX, y: ev.clientY };
      if (c.setPointerCapture) c.setPointerCapture(ev.pointerId);
    });
    c.addEventListener('pointermove', function (ev) {
      if (!self.view) return;
      var r = c.getBoundingClientRect();
      if (self.drag) {
        self.panBy(ev.clientX - self.drag.x, ev.clientY - self.drag.y);
        self.drag.x = ev.clientX; self.drag.y = ev.clientY;
        self.hover = null; if (self.tip) self.tip.hidden = true;
        self.draw();
        return;
      }
      var p = self.nearest(ev.clientX - r.left, ev.clientY - r.top);
      if (p !== self.hover) { self.hover = p; self.draw(); }
      self.showTip(p, ev.clientX - r.left, ev.clientY - r.top);
    });
    c.addEventListener('pointerup', function () { self.drag = null; });
    c.addEventListener('pointerleave', function () { self.hover = null; if (self.tip) self.tip.hidden = true; if (self.view) self.draw(); });
    c.addEventListener('keydown', function (ev) {
      if (!self.view) return;
      var step = 40, done = true, ctr = self.center();
      if (ev.key === 'ArrowLeft') self.panBy(step, 0);
      else if (ev.key === 'ArrowRight') self.panBy(-step, 0);
      else if (ev.key === 'ArrowUp') self.panBy(0, step);
      else if (ev.key === 'ArrowDown') self.panBy(0, -step);
      else if (ev.key === '+' || ev.key === '=') self.zoomAt(ctr[0], ctr[1], 0.7);
      else if (ev.key === '-' || ev.key === '_') self.zoomAt(ctr[0], ctr[1], 1 / 0.7);
      else if (ev.key === '0') self.view = Object.assign({}, self.home);
      else done = false;
      if (done) { ev.preventDefault(); self.draw(); }
    });
    var buttons = this.opts.buttons || {};
    function bindButton(el, factor) {
      if (!el) return;
      el.addEventListener('click', function () {
        if (!self.view) return;
        if (factor === 0) self.view = Object.assign({}, self.home);
        else { var ctr = self.center(); self.zoomAt(ctr[0], ctr[1], factor); }
        self.draw();
      });
    }
    bindButton(buttons.zoomIn, 0.6);
    bindButton(buttons.zoomOut, 1 / 0.6);
    bindButton(buttons.reset, 0);
    if (window.ResizeObserver) new ResizeObserver(function () { if (self.view) self.draw(); }).observe(c);
  };

  root.HW2ExplorePlot = { Scatter: Scatter, linearTicks: linearTicks, tickLabel: tickLabel };
})(typeof self !== 'undefined' ? self : this);
