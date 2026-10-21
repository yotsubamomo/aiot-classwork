/* HW2 V2 dashboard: the problem drop-down and the Exploratory run blocks on the page (#74 V2-T1).
 *
 * King County (the default) is the V1 dashboard exactly as assets/app.js renders it; this file never
 * changes a V1 element's content. Selecting 50 Startups or 自訂資料集 hides the V1 blocks (the
 * `hidden` attribute of #overview, #model, #predictor, #test, #methods, #load-error) and shows the
 * #explore subtree, whose ids all start with "ex-"; selecting King County again shows the V1 blocks
 * and restores #load-error to what it was. Every exploratory block is labelled 「探索執行，非正式評估」.
 *
 * All text that may come from a dataset (column names, levels, messages) is written with textContent,
 * createTextNode, <option>.text or non-URL attributes only, never parsed as HTML (DA D-2). No network
 * access, no storage: results live in memory only. */
(function () {
  'use strict';

  var App = window.HW2ExploreApp, Engine = window.HW2ExploreEngine, Loader = window.HW2ExploreLoad;
  var Plot = window.HW2ExplorePlot, DATA = window.HW2_STARTUPS50;
  var V1_BLOCKS = ['overview', 'model', 'predictor', 'test', 'methods'];
  var EX_BLOCKS = ['ex-custom', 'ex-data', 'ex-model', 'ex-predictor', 'ex-test'];
  var loadErrorWasHidden = null;
  var scatter = null;
  var current = null;

  function byId(id) { return document.getElementById(id); }
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'text') node.textContent = attrs[k];
      else if (k === 'class') node.className = attrs[k];
      else if (attrs[k] !== null && attrs[k] !== undefined && attrs[k] !== false) node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return node;
  }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  var nf0 = new Intl.NumberFormat('zh-TW', { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat('zh-TW', { maximumFractionDigits: 2 });
  var nf4 = new Intl.NumberFormat('zh-TW', { maximumFractionDigits: 4 });
  function num(v) {
    if (v === null || v === undefined || !isFinite(v)) return '—';
    var a = Math.abs(v);
    if (a >= 1e12 || (a > 0 && a < 1e-4)) return Number(v).toExponential(3);
    if (a >= 1000) return nf0.format(v);
    if (a >= 1) return nf2.format(v);
    return nf4.format(v);
  }
  function fixed(v, d) { return v === null || v === undefined || !isFinite(v) ? '—' : Number(v).toFixed(d); }
  function pct(v) { return v === null || v === undefined ? '—' : (100 * v).toFixed(1) + '%'; }
  function tag(cls, text) { return el('span', { class: 'tag ' + cls, text: text }); }

  /* ---- showing and hiding the two worlds ------------------------------------------------------ */
  function setExploring(on) {
    var loadError = byId('load-error');
    if (on && loadErrorWasHidden === null && loadError) { loadErrorWasHidden = loadError.hidden; loadError.hidden = true; }
    if (!on && loadErrorWasHidden !== null && loadError) { loadError.hidden = loadErrorWasHidden; loadErrorWasHidden = null; }
    V1_BLOCKS.forEach(function (id) { var n = byId(id); if (n) n.hidden = on; });
    byId('explore').hidden = !on;
    document.body.classList.toggle('is-exploring', on);
  }
  function showBlocks(ids) { EX_BLOCKS.forEach(function (id) { byId(id).hidden = ids.indexOf(id) < 0; }); }
  function message(text, kind) {
    var box = byId('ex-message');
    box.textContent = text || '';
    box.hidden = !text;
    box.className = 'notice explore__message' + (kind === 'error' ? ' explore__message--error' : '');
  }

  /* ---- data and preprocessing ------------------------------------------------------------------- */
  function facts(dl, pairs) {
    clear(dl);
    pairs.forEach(function (p) { dl.appendChild(el('dt', { text: p[0] })); dl.appendChild(el('dd', { class: p[2] || null, text: p[1] })); });
  }
  function renderData(run) {
    var load = run.load, res = run.result, sourceText = { builtin: '內建資料（assets/data/50_Startups.csv，取自 Avik-Jain/100-Days-Of-ML-Code，MIT 授權）',
      file: '本機文字', url: 'URL' }[run.source] || String(run.source);
    var pairs = [['來源', sourceText], ['內容 sha256', load.sha256, 'hash']];
    if (load.ok) {
      pairs.push(['預測目標', load.target.name + '（原始尺度，不取 log）']);
      pairs.push(['列數', nf0.format(load.n_rows_read) + ' 列讀入；刪除含缺值的列 ' + nf0.format(load.n_rows_dropped_missing) + ' 列；分析 ' + nf0.format(load.n_rows) + ' 列']);
    }
    if (res) {
      pairs.push(['切分', '固定 seed 的逐列 80/20：訓練 ' + res.split.train.length + ' 列、test ' + res.split.test.length + ' 列']);
      pairs.push(['交叉驗證', '訓練列內 ' + res.split.n_folds + ' 個 fold（固定 seed）']);
      pairs.push(['Seed', String(res.meta.seed)]);
      pairs.push(['引擎版本', res.meta.engine_version]);
    }
    facts(byId('ex-facts'), pairs);
    var table = byId('ex-columns');
    clear(table);
    if (!res) return;
    table.appendChild(el('caption', { class: 'small muted', text: '欄位型態（載入時逐格判定）與以訓練列決定的狀態' }));
    table.appendChild(el('thead', {}, [el('tr', {}, ['欄位', '型態', '訓練列的相異值數', '狀態'].map(function (h) { return el('th', { scope: 'col', text: h }); }))]));
    var body = el('tbody');
    res.columns.forEach(function (c) {
      body.appendChild(el('tr', {}, [el('th', { scope: 'row', text: c.name }), el('td', { text: c.type === 'numeric' ? '數值' : '類別' }),
        el('td', { class: 'num', text: c.role === 'target' ? '—' : nf0.format(c.n_distinct_train) }),
        el('td', { text: App.columnStatusText(c.status) })]));
    });
    table.appendChild(body);
  }

  /* ---- model and training CV -------------------------------------------------------------------- */
  function kpi(label, value, sub) {
    return el('div', { class: 'kpi' }, [el('div', { class: 'kpi__label' }, [el('span', { text: label })]),
      el('div', { class: 'kpi__value num', text: value }), sub ? el('div', { class: 'kpi__sub', text: sub }) : null]);
  }
  function renderModel(res) {
    var c = res.candidates[0];
    var cand = byId('ex-candidate');
    clear(cand);
    cand.appendChild(el('strong', { text: 'All-in baseline' }));
    cand.appendChild(document.createTextNode('（全部 ' + c.k + ' 個 feature group 的 OLS：' + c.canonical_groups.join('、') + '）　狀態：' + App.statusText(c.status)));
    var box = byId('ex-kpi-cv');
    clear(box);
    [['CV RMSE', 'rmse', num], ['CV MAE', 'mae', num], ['CV MSE', 'mse', num], ['CV R²', 'r2', function (v) { return fixed(v, 4); }]].forEach(function (m) {
      var mean = c.cv ? c.cv.mean[m[1]] : null, sd = c.cv ? c.cv.std[m[1]] : null;
      box.appendChild(kpi(m[0], m[2](mean), '± ' + m[2](sd) + '（5 個 fold 的平均 ± 標準差）'));
    });
    var table = byId('ex-folds');
    clear(table);
    table.appendChild(el('caption', { class: 'small muted', text: '各 fold（只用該 fold 的訓練列擬合，在驗證列上計分）' }));
    table.appendChild(el('thead', {}, [el('tr', {}, ['Fold', '訓練列', '驗證列', 'RMSE', 'MAE', 'R²', '驗證列未見層級'].map(function (h) { return el('th', { scope: 'col', text: h }); }))]));
    var body = el('tbody');
    c.folds.forEach(function (f) {
      var m = f.metrics || {};
      body.appendChild(el('tr', {}, [el('th', { scope: 'row', text: String(f.fold + 1) }), el('td', { class: 'num', text: String(f.n_train) }),
        el('td', { class: 'num', text: String(f.n_valid) }), el('td', { class: 'num', text: num(m.rmse) }), el('td', { class: 'num', text: num(m.mae) }),
        el('td', { class: 'num', text: fixed(m.r2, 4) }), el('td', { class: 'num', text: f.n_valid_unseen === undefined ? '—' : String(f.n_valid_unseen) })]));
    });
    table.appendChild(body);
    var f = c.fit;
    facts(byId('ex-fit'), [['訓練列數', nf0.format(f.n_train), 'num'], ['設計矩陣欄數（含截距）', String(f.n_columns), 'num'],
      ['Rank', String(f.rank), 'num'], ['殘差自由度', String(f.df_resid), 'num'], ['s²', num(f.s2), 'num'],
      ['訓練 R²', fixed(f.r2_train, 4), 'num'], ['訓練 Adjusted R²（實際秩）', fixed(f.adj_r2_train, 4), 'num'],
      ['t(0.975, df)', fixed(f.t_crit, 4), 'num']]);
  }

  /* ---- live predictor ----------------------------------------------------------------------------- */
  function renderPredictor(candidate) {
    var fields = byId('ex-pred-fields');
    clear(fields);
    var view = App.predictorView(Engine, candidate, {});
    var status = byId('ex-pred-status');
    if (!view.enabled) {
      byId('ex-pred-form').setAttribute('aria-disabled', 'true');
      byId('ex-pred-value').textContent = '—';
      byId('ex-pred-pi').textContent = '—';
      clear(status);
      status.appendChild(el('div', { class: 'warn', text: '預測器停用：目前的候選狀態為 ' + view.statusText }));
      view.reasons.forEach(function (t) { status.appendChild(el('div', { class: 'small', text: t })); });
      return;
    }
    byId('ex-pred-form').removeAttribute('aria-disabled');
    var inputs = [];
    view.specs.forEach(function (spec, i) {
      var id = 'ex-in-' + i, field = el('div', { class: 'field' });
      field.appendChild(el('label', { for: id, text: spec.name }));
      var input;
      if (spec.type === 'categorical') {
        input = el('select', { class: 'input', id: id });
        spec.levels.forEach(function (lv) {
          var opt = document.createElement('option');
          opt.value = lv; opt.text = lv === spec.baseline ? lv + '（基準）' : lv;
          input.appendChild(opt);
        });
        input.value = spec.default;
        field.appendChild(input);
        field.appendChild(el('p', { class: 'help', text: '只列出訓練層級；基準層級沒有自己的欄。' }));
      } else {
        input = el('input', { class: 'input num', id: id, type: 'number', step: 'any', inputmode: 'decimal' });
        input.value = String(Number(spec.default.toPrecision(12)));   /* the median without float noise */
        field.appendChild(input);
        field.appendChild(el('p', { class: 'help', text: '訓練範圍 ' + num(spec.min) + '～' + num(spec.max) + '，預設為訓練中位數 ' + num(spec.median) }));
      }
      input.addEventListener(spec.type === 'categorical' ? 'change' : 'input', update);
      inputs.push({ spec: spec, input: input });
      fields.appendChild(field);
    });
    function update() {
      var raw = {};
      inputs.forEach(function (x) { raw[x.spec.name] = x.input.value; });
      var v = App.predictorView(Engine, candidate, raw);
      clear(status);
      if (v.error) {
        byId('ex-pred-value').textContent = '—';
        byId('ex-pred-pi').textContent = '—';
        status.appendChild(el('div', { class: 'warn', text: v.error }));
        return;
      }
      byId('ex-pred-value').textContent = num(v.predicted);
      byId('ex-pred-pi').textContent = num(v.lower) + ' ～ ' + num(v.upper);
      v.warnings.forEach(function (t) { status.appendChild(el('div', { class: 'warn', text: t })); });
    }
    update();
  }

  /* ---- exploratory test ------------------------------------------------------------------------- */
  function renderTest(res) {
    var key = res.winners.overall.key, t = res.test[key];
    byId('ex-test-model').textContent = '展示模型：All-in baseline（k = ' + res.winners.overall.k + '，整體 CV winner；本版本只有這一個候選）；test 列 ' + t.n_test + ' 筆，在全部選擇固定後才讀取。';
    var box = byId('ex-kpi-test');
    clear(box);
    [['Test RMSE', num(t.metrics.rmse)], ['Test MAE', num(t.metrics.mae)], ['Test MSE', num(t.metrics.mse)], ['Test R²', fixed(t.metrics.r2, 4)],
      ['PI 涵蓋率', pct(t.coverage), t.n_covered + ' / ' + t.n_test + ' 筆落入 95% PI']].forEach(function (p) {
      box.appendChild(kpi(p[0], p[1], p[2]));
    });
    if (!scatter) {
      scatter = new Plot.Scatter(byId('ex-scatter-canvas'), byId('ex-scatter-tip'),
        { format: num, buttons: { zoomIn: byId('ex-zoom-in'), zoomOut: byId('ex-zoom-out'), reset: byId('ex-zoom-reset') } });
    }
    var points = t.rows.map(function (row, i) {
      return { row: row, actual: t.actual[i], predicted: t.predicted[i], lower: t.lower[i], upper: t.upper[i], covered: t.covered[i] };
    });
    scatter.setData(points, { x: '預測值（' + res.meta.target + '，線性刻度）', y: '實際值（' + res.meta.target + '，線性刻度）' });
  }

  /* ---- render ------------------------------------------------------------------------------------- */
  function render(view) {
    current = view;
    if (view.mode === 'king_county') { setExploring(false); return; }
    setExploring(true);
    byId('ex-title').textContent = App.PROBLEM_TITLES[view.problem] || '探索執行';
    if (view.mode === 'custom') { message(''); showBlocks(['ex-custom']); return; }
    if (view.mode === 'error') { message(view.message, 'error'); showBlocks([]); return; }
    var run = view.run;
    if (!run.load.ok) {
      message('無法載入資料：' + App.loadReasonText(run.load.reason) + '（' + run.load.reason + '）', 'error');
      renderData(run);
      showBlocks(['ex-data']);
      return;
    }
    var res = run.result;
    renderData(run);
    if (res.run.status !== 'COMPLETED') {
      var lines = [App.runReasonText(res.run.reason)];
      (res.run.invalid_candidates || []).forEach(function (c) {
        lines.push('All-in baseline：' + App.statusText(c.status) + '。' + c.reasons.map(App.reasonText).join('；'));
      });
      message(lines.join(' '), 'error');
      showBlocks(['ex-data']);
      return;
    }
    message('執行完成：' + (run.ms === null ? '' : '耗時 ' + run.ms.toFixed(1) + ' ms（瀏覽器內計算，只供參考）'));
    showBlocks(['ex-data', 'ex-model', 'ex-predictor', 'ex-test']);
    renderModel(res);
    renderPredictor(res.candidates[0]);
    renderTest(res);
  }

  function init() {
    var select = byId('problem-select');
    if (!select || !byId('explore')) return;
    if (!App || !Engine || !Loader || !Plot) { select.disabled = true; return; }
    var controller = App.createController({ loader: Loader, engine: Engine, datasets: { startups50: DATA }, render: render,
      now: function () { return performance.now(); } });
    window.HW2_EXPLORE = { state: controller.state, view: function () { return current; } };
    select.value = 'king_county';             /* the default problem, even if the browser restored the form */
    controller.init();
    select.addEventListener('change', function () { controller.selectProblem(select.value); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
