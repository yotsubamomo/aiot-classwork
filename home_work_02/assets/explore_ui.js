/* HW2 V2 dashboard: the problem drop-down and the Exploratory run blocks on the page (#74 V2-T1; #75
 * V2-T2: the five methods, the metric vs k chart, the winners, the Lasso path and the dependency
 * diagnostic; #76 V2-T3: the custom dataset's input panel).
 *
 * King County (the default) is the V1 dashboard exactly as assets/app.js renders it; this file never
 * changes a V1 element's content. Selecting 50 Startups or 自訂資料集 hides the V1 blocks (the
 * `hidden` attribute of #overview, #model, #predictor, #test, #methods, #load-error) and shows the
 * #explore subtree, whose ids all start with "ex-"; selecting King County again shows the V1 blocks
 * and restores #load-error to what it was. Every exploratory block is labelled 「探索執行，非正式評估」.
 * The V1 footer is hidden while exploring by a body.is-exploring rule of assets/explore.css (its DOM
 * and text are never touched; DA decision-20261022-r1f3-v1-footer R3-2, R3-5).
 *
 * Custom dataset (#76): the #ex-custom panel stays visible in that mode, with the results under it. A
 * URL is read only when the user submits the URL form (「載入 URL」), through the controller and the
 * loader (one GET; DA D-1); a local file is read here with File.arrayBuffer() (no network) and handed
 * over as bytes. The target drop-down lists the columns of the content read (default: the last one);
 * choosing another runs the same content again without reading the URL again. Selecting another
 * problem forgets the submission; selecting 自訂資料集 again shows an empty panel.
 *
 * Model block (#75): a method switch (All-in, Forward SFS, Backward SFS, RFE, Lasso path), a k grid
 * (CV winners marked, INVALID_MODEL candidates striped and still selectable with their reasons), a
 * 「比較全部方法」 toggle, the training-CV KPIs of the selected candidate, the metric vs k chart (training
 * CV only), the table of method winners and the overall winner (training CV and exploratory test in
 * separate column groups; test numbers only for winners), the selected candidate's folds and canonical
 * fit, and the Lasso path of the training set. The predictor follows the selected candidate (VALID
 * only). The test block shows the selected candidate when it is a winner; otherwise its method's
 * winner (or the overall winner) with a hint. The selection starts at the overall CV winner.
 *
 * All text that may come from a dataset (column names, levels, messages) is written with textContent,
 * createTextNode, <option>.text or non-URL attributes only, never parsed as HTML (DA D-2). No network
 * access, no storage: results and the selection live in memory only. */
(function () {
  'use strict';

  var App = window.HW2ExploreApp, Engine = window.HW2ExploreEngine, Loader = window.HW2ExploreLoad;
  var Plot = window.HW2ExplorePlot, DATA = window.HW2_STARTUPS50;
  var V1_BLOCKS = ['overview', 'model', 'predictor', 'test', 'methods'];
  var EX_BLOCKS = ['ex-custom', 'ex-data', 'ex-model', 'ex-predictor', 'ex-test', 'ex-methods'];
  var controller = null;
  var METRICS = { rmse: 'RMSE', mae: 'MAE', mse: 'MSE', r2: 'R²' };
  var loadErrorWasHidden = null;
  var scatter = null, kchart = null;
  var current = null;
  var ui = { result: null, key: null, compareAll: false, metric: 'rmse' };

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
  function metricText(m, v) { return m === 'r2' ? fixed(v, 4) : num(v); }
  function th(text) { return el('th', { scope: 'col', text: text }); }

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

  /* ---- data, preprocessing and the dependency diagnostic ----------------------------------------- */
  function facts(dl, pairs) {
    clear(dl);
    pairs.forEach(function (p) { dl.appendChild(el('dt', { text: p[0] })); dl.appendChild(el('dd', { class: p[2] || null, text: p[1] })); });
  }
  function renderDeps(res) {
    var box = byId('ex-deps');
    clear(box);
    if (!res || !res.dependencies) return;
    var view = App.dependencyView(res);
    if (!view.relations.length) {
      box.appendChild(el('p', { class: 'small', text: '沒有線性相依：All-in 設計矩陣（含截距 ' + view.n_columns + ' 欄）滿秩，rank ' + view.rank + '。' }));
      return;
    }
    box.appendChild(el('p', { class: 'small warn', text: 'All-in 設計矩陣（含截距 ' + view.n_columns + ' 欄）的 rank 只有 ' + view.rank +
      '，找到 ' + view.relations.length + ' 組線性相依的欄位：' }));
    var list = el('ol', { class: 'small ex-deps' });
    view.relations.forEach(function (r) {
      list.appendChild(el('li', {}, [
        el('div', {}, [el('strong', { text: '涉及的 feature group：' }), document.createTextNode(r.groups.join('、') + (r.includesIntercept ? '（另含截距）' : ''))]),
        el('div', {}, [el('span', { text: '編碼欄：' + r.columns.join('、') })]),
        el('div', {}, [el('span', { text: '關係式：' }), el('code', { text: r.formula })])
      ]));
    });
    box.appendChild(list);
  }
  function renderData(run) {
    var load = run.load, res = run.result, sourceText = { builtin: '內建資料（assets/data/50_Startups.csv，取自 Avik-Jain/100-Days-Of-ML-Code，MIT 授權）',
      file: '本機 CSV 檔案', url: 'URL' }[run.source] || String(run.source);
    if (run.label) sourceText += '：' + run.label;              /* the file name or the URL, as text */
    var pairs = [['來源', sourceText], ['內容 sha256', load.sha256 || '—', 'hash']];
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
    renderDeps(res);
    if (!res) return;
    table.appendChild(el('caption', { class: 'small muted', text: '欄位型態（載入時逐格判定）與以訓練列決定的狀態' }));
    table.appendChild(el('thead', {}, [el('tr', {}, ['欄位', '型態', '訓練列的相異值數', '狀態'].map(th))]));
    var body = el('tbody');
    res.columns.forEach(function (c) {
      body.appendChild(el('tr', {}, [el('th', { scope: 'row', text: c.name }), el('td', { text: c.type === 'numeric' ? '數值' : '類別' }),
        el('td', { class: 'num', text: c.role === 'target' ? '—' : nf0.format(c.n_distinct_train) }),
        el('td', { text: App.columnStatusText(c.status) })]));
    });
    table.appendChild(body);
  }

  /* ---- model selection and training CV ------------------------------------------------------------ */
  function kpi(label, value, sub) {
    return el('div', { class: 'kpi' }, [el('div', { class: 'kpi__label' }, [el('span', { text: label })]),
      el('div', { class: 'kpi__value num', text: value }), sub ? el('div', { class: 'kpi__sub', text: sub }) : null]);
  }
  function selected() { return App.candidateByKey(ui.result, ui.key); }
  function select(key) { ui.key = key; renderSelection(); }
  function methodCandidates(m) { return ui.result.candidates.filter(function (c) { return c.method === m; }); }

  function renderControls() {
    var res = ui.result, sel = selected(), w = res.winners, p = res.groups.length;
    var seg = byId('ex-method-seg');
    clear(seg);
    App.METHOD_ORDER.forEach(function (m) {
      var list = methodCandidates(m), nValid = list.filter(function (c) { return c.status === 'VALID'; }).length;
      var meta = m === 'allin' ? 'k = ' + p + ' 固定' : p + ' 個 k' + (nValid < list.length ? '，' + (list.length - nValid) + ' 個無效' : '');
      var b = el('button', { type: 'button', class: 'seg__btn', 'aria-pressed': String(m === sel.method), 'data-method': m },
        [App.methodLabel(m), el('span', { class: 'meta', text: meta })]);
      b.addEventListener('click', function () {
        if (m === sel.method) return;
        var mw = w.method_winners[m];
        select(mw ? mw.key : list[0].key);
      });
      seg.appendChild(b);
    });
    var grid = byId('ex-k-grid');
    clear(grid);
    if (sel.method === 'allin') {
      grid.className = 'kgrid kgrid--fixed';
      grid.appendChild(el('div', { class: 'kfixed' }, [el('span', { class: 'kfixed__k', text: 'k = ' + p + '（固定）' }),
        el('span', { class: 'kfixed__txt', text: 'All-in baseline 是全部 ' + p + ' 個 feature group 的單一 OLS，沒有 k 路徑。' })]));
      byId('ex-k-help').textContent = '';
    } else {
      grid.className = 'kgrid';
      var mw = w.method_winners[sel.method];
      methodCandidates(sel.method).forEach(function (c) {
        var win = !!(mw && mw.key === c.key), bad = c.status !== 'VALID';
        var label = 'k = ' + c.k + (win ? '（該方法 CV winner）' : '') + (bad ? '（' + App.statusText(c.status) + '）' : '');
        var b = el('button', { type: 'button', class: 'kbtn' + (win ? ' is-winner' : '') + (bad ? ' is-invalid' : ''),
          'aria-pressed': String(c.key === sel.key), 'aria-label': label, title: label, text: String(c.k) });
        b.addEventListener('click', function () { select(c.key); });
        grid.appendChild(b);
      });
      byId('ex-k-help').textContent = '綠點：該方法 CV winner；紅斜紋：無效（INVALID_MODEL）候選，仍可選取並顯示原因，但沒有 CV 指標、不提供即時預測。';
    }
    var toggle = byId('ex-compare-all');
    toggle.setAttribute('aria-pressed', String(ui.compareAll));
    var box = byId('ex-selected');
    clear(box);
    box.appendChild(el('strong', { text: App.candidateName(sel) }));
    var tags = App.winnerRoles(res, sel.key).map(function (r) { return el('span', { class: 'tag ' + (r === '整體 CV winner' ? 'tag--overall' : 'tag--winner'), text: r }); });
    if (sel.status !== 'VALID') tags.push(el('span', { class: 'tag tag--invalid', text: App.statusText(sel.status) }));
    if (tags.length) box.appendChild(el('div', { class: 'tags' }, tags));
    box.appendChild(el('span', { class: 'small', text: 'Canonical 子集（整個訓練集上選出）：' +
      (sel.canonical_groups ? sel.canonical_groups.join('、') : '—（Lasso 路徑在整個訓練集上沒有到達這個 k）') }));
    if (sel.method !== 'allin') {
      var items = sel.folds.map(function (f) {
        var text;
        if (!f.groups) text = '—（該 fold 的 Lasso 路徑沒有到達這個 k）';
        else if (sel.canonical_groups && JSON.stringify(f.groups) === JSON.stringify(sel.canonical_groups)) text = '與 canonical 子集相同';
        else text = f.groups.join('、');
        return el('li', { text: 'Fold ' + (f.fold + 1) + '：' + text });
      });
      box.appendChild(el('details', { class: 'small' }, [el('summary', { text: '各 fold 的子集（只在該 fold 的訓練列上選出）' }),
        el('ol', { class: 'folds' }, items)]));
    }
  }

  function renderCv() {
    var c = selected();
    byId('ex-candidate').textContent = '目前選取：' + App.candidateName(c) + '　狀態：' + App.statusText(c.status) +
      (c.canonical_groups ? '　canonical 子集：' + c.canonical_groups.join('、') : '');
    var box = byId('ex-kpi-cv');
    clear(box);
    if (c.status !== 'VALID') {
      box.appendChild(el('div', { class: 'kpi ex-invalid' }, [el('div', { class: 'kpi__label', text: '無訓練 CV 指標' }),
        el('div', { class: 'warn', text: App.statusText(c.status) })].concat(c.reasons.map(function (r) {
        return el('div', { class: 'small', text: App.reasonText(r) });
      }))));
    } else {
      [['CV RMSE', 'rmse'], ['CV MAE', 'mae'], ['CV MSE', 'mse'], ['CV R²', 'r2']].forEach(function (m) {
        box.appendChild(kpi(m[0], metricText(m[1], c.cv.mean[m[1]]), '± ' + metricText(m[1], c.cv.std[m[1]]) + '（5 個 fold 的平均 ± 標準差，訓練 CV）'));
      });
    }
    var table = byId('ex-folds');
    clear(table);
    table.appendChild(el('caption', { class: 'small muted', text: '各 fold（子集與 OLS 只用該 fold 的訓練列，在驗證列上計分；訓練 CV）' }));
    table.appendChild(el('thead', {}, [el('tr', {}, ['Fold', '子集', '訓練列', '驗證列', 'RMSE', 'MAE', 'R²', '驗證列未見層級', '狀態'].map(th))]));
    var body = el('tbody');
    c.folds.forEach(function (f) {
      var m = f.metrics || {};
      body.appendChild(el('tr', {}, [el('th', { scope: 'row', text: String(f.fold + 1) }),
        el('td', { text: f.groups ? f.groups.join('、') : '—' }),
        el('td', { class: 'num', text: String(f.n_train) }), el('td', { class: 'num', text: String(f.n_valid) }),
        el('td', { class: 'num', text: num(m.rmse) }), el('td', { class: 'num', text: num(m.mae) }), el('td', { class: 'num', text: fixed(m.r2, 4) }),
        el('td', { class: 'num', text: f.n_valid_unseen === undefined ? '—' : String(f.n_valid_unseen) }),
        el('td', { text: f.status === 'ok' ? '有效' : '無效（' + f.rule + '）' })]));
    });
    table.appendChild(body);
    var fit = c.fit;
    if (!fit) {
      facts(byId('ex-fit'), [['狀態', App.statusText(c.status)], ['說明', '無效的候選沒有 canonical fit，不參與 winner，也不提供預測']]);
      return;
    }
    facts(byId('ex-fit'), [['訓練列數', nf0.format(fit.n_train), 'num'], ['設計矩陣欄數（含截距）', String(fit.n_columns), 'num'],
      ['Rank', String(fit.rank), 'num'], ['殘差自由度', String(fit.df_resid), 'num'], ['s²', num(fit.s2), 'num'],
      ['訓練 R²', fixed(fit.r2_train, 4), 'num'], ['訓練 Adjusted R²（實際秩）', fixed(fit.adj_r2_train, 4), 'num'],
      ['t(0.975, df)', fixed(fit.t_crit, 4), 'num']]);
  }

  function renderKChart() {
    var res = ui.result, sel = selected(), metric = ui.metric;
    var series = ['forward_sfs', 'backward_sfs', 'rfe', 'lasso_path'].map(function (m) {
      return { method: m, label: App.methodLabel(m), emphasized: ui.compareAll || sel.method === 'allin' || sel.method === m,
        points: App.kSeries(res, m, metric) };
    });
    var allin = App.candidateByKey(res, 'allin');
    var allinValue = allin && allin.status === 'VALID' ? allin.cv.mean[metric] : null;
    var selValue = sel.status === 'VALID' ? sel.cv.mean[metric] : null;
    if (!kchart) kchart = new Plot.KChart(byId('ex-kchart-canvas'));
    var drawn = kchart.set({ p: res.groups.length, yLabel: METRICS[metric] + '（訓練 CV）', format: function (v) { return metricText(metric, v); },
      series: series, allin: { value: allinValue, label: 'All-in baseline（k = ' + res.groups.length + ' 固定，參考線）' },
      selected: sel.method === 'allin' ? null : { k: sel.k, value: selValue, label: App.methodLabel(sel.method), status: sel.status, isWinner: false },
      statusLabel: App.statusText });
    var parts = series.map(function (s) {
      var w = s.points.filter(function (d) { return d.isWinner; })[0];
      return s.label + ' 的 CV winner 為 ' + (w ? 'k = ' + w.k + '（' + metricText(metric, w.value) + '）' : '—（沒有有效候選）');
    });
    parts.push('All-in baseline ' + (allinValue === null ? '無效' : metricText(metric, allinValue)));
    byId('ex-kchart-summary').textContent = drawn ? METRICS[metric] + '（訓練 CV）：' + parts.join('；') + '。'
      : '找不到本機打包的 Chart.js，無法繪製指標 vs k 圖。' + parts.join('；') + '。';
    var lg = byId('ex-kchart-legend');
    clear(lg);
    series.forEach(function (s) {
      lg.appendChild(el('span', { class: 'legend__item' + (s.emphasized ? '' : ' is-dim'), style: 'color:' + Plot.KChart.colors[s.method] },
        [el('span', { class: 'legend__line' }), el('span', { class: 'ex-legend-text', text: s.label })]));
    });
    lg.appendChild(el('span', { class: 'legend__item', style: 'color:' + Plot.KChart.allinColor },
      [el('span', { class: 'legend__line legend__line--dash' }), el('span', { class: 'ex-legend-text', text: 'All-in baseline（參考線）' })]));
    lg.appendChild(el('span', { class: 'legend__item' }, [el('span', { class: 'legend__mark legend__mark--ring' }), '該方法 CV winner（圓環）']));
    lg.appendChild(el('span', { class: 'legend__item' }, [el('span', { class: 'legend__mark legend__mark--cross' }), '無效候選（叉號，沒有 CV 指標）']));
    lg.appendChild(el('span', { class: 'legend__item' }, [el('span', { class: 'legend__mark legend__mark--sel' }), '目前選取']));
  }

  function renderCompare() {
    var res = ui.result, table = byId('ex-compare');
    clear(table);
    table.appendChild(el('caption', { class: 'small muted', text: '「訓練 CV」與「探索 test（非正式評估）」分欄呈現，不混用；test 只對 winner 計算。' }));
    table.appendChild(el('thead', {}, [
      el('tr', {}, [el('th', { scope: 'col', rowspan: '2', text: '方法' }), el('th', { scope: 'col', rowspan: '2', text: 'CV winner' }),
        el('th', { scope: 'colgroup', colspan: '3', class: 'ex-cv-head', text: '訓練 CV' }),
        el('th', { scope: 'colgroup', colspan: '4', class: 'ex-test-head', text: '探索 test（非正式評估）' })]),
      el('tr', {}, ['RMSE', 'MAE', 'R²', 'RMSE', 'MAE', 'R²', 'PI 涵蓋率'].map(th))]));
    var body = el('tbody');
    App.compareRows(res).forEach(function (r) {
      if (!r.winner) {
        body.appendChild(el('tr', { class: 'ex-row-none' }, [el('th', { scope: 'row', text: r.label }),
          el('td', { colspan: '8', text: r.note })]));
        return;
      }
      var name = el('td', {}, [document.createTextNode(r.method === 'allin' ? 'k = ' + r.k + '（全部）' : 'k = ' + r.k),
        r.isOverall ? el('span', { class: 'tag tag--overall', text: '整體 CV winner' }) : null,
        el('div', { class: 'small muted', text: r.groups.join('、') + (r.sharedWith ? '（與「' + r.sharedWith + '」同一模型，test 只算一次）' : '') })]);
      var tr = el('tr', { class: r.isOverall ? 'ex-row-overall' : null }, [el('th', { scope: 'row' }, [
        el('button', { type: 'button', class: 'linklike', text: r.label })]), name,
      el('td', { class: 'num', text: num(r.cv.mean.rmse) }), el('td', { class: 'num', text: num(r.cv.mean.mae) }), el('td', { class: 'num', text: fixed(r.cv.mean.r2, 4) }),
      el('td', { class: 'num ex-test-cell', text: num(r.test.rmse) }), el('td', { class: 'num ex-test-cell', text: num(r.test.mae) }),
      el('td', { class: 'num ex-test-cell', text: fixed(r.test.r2, 4) }),
      el('td', { class: 'num ex-test-cell', text: pct(r.coverage) + '（' + r.n_covered + '/' + r.n_test + '）' })]);
      tr.querySelector('button').addEventListener('click', function () { select(r.winner); });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }

  function renderLasso() {
    var view = App.lassoView(ui.result), table = byId('ex-lasso');
    clear(table);
    byId('ex-lasso-card').hidden = !view;
    if (!view) return;
    byId('ex-lasso-summary').textContent = view.summary;
    table.appendChild(el('thead', {}, [el('tr', {}, ['順序', 'Feature group', 'Entry alpha', '狀態'].map(th))]));
    var body = el('tbody');
    view.rows.forEach(function (r) {
      body.appendChild(el('tr', { class: r.position === null ? 'ex-row-none' : null }, [
        el('th', { scope: 'row', text: r.position === null ? '—' : String(r.position) }), el('td', { text: r.group }),
        el('td', { class: 'num', text: r.alpha === null ? '—' : num(r.alpha) }), el('td', { text: r.state })]));
    });
    table.appendChild(body);
  }

  /* ---- live predictor ----------------------------------------------------------------------------- */
  function renderPredictor(candidate) {
    var fields = byId('ex-pred-fields');
    clear(fields);
    byId('ex-pred-model').textContent = '模型：' + App.candidateName(candidate) + ' 在整個訓練集上的擬合';
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
  function renderTest() {
    var res = ui.result, view = App.testView(res, ui.key), t = view.test;
    byId('ex-test-model').textContent = '展示模型：' + view.shownName + (view.roles.length ? '（' + view.roles.join('、') + '）' : '') +
      (view.sharedWith ? '；與「' + view.sharedWith + '」同一模型，test 只算一次' : '') +
      '；test 列 ' + t.n_test + ' 筆，在全部選擇固定後才讀取，只對 CV winner 計算。';
    var hint = byId('ex-test-hint');
    hint.textContent = view.hint || '';
    hint.hidden = !view.hint;
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

  function renderSelection() {
    renderControls();
    renderCv();
    renderKChart();
    renderPredictor(selected());
    renderTest();
  }

  /* ---- custom dataset input panel (#76) ------------------------------------------------------------ */
  function renderCustom(panel) {
    panel = panel || { busy: false, source: null, label: null, hasData: false, columns: null, target: null };
    var target = byId('ex-target');
    clear(target);
    if (panel.columns && panel.columns.length) {
      panel.columns.forEach(function (c) {
        var opt = document.createElement('option');
        opt.value = String(c.index);
        opt.text = c.name + '（' + (c.type === 'numeric' ? '數值' : '類別') + '）';
        target.appendChild(opt);
      });
      target.value = String(panel.target);
      target.disabled = panel.busy;
    } else {
      var none = document.createElement('option');
      none.value = '';
      none.text = '（載入資料後選擇）';
      target.appendChild(none);
      target.disabled = true;
    }
    byId('ex-url-load').disabled = panel.busy;
    var status = byId('ex-custom-status');
    if (panel.busy) status.textContent = '讀取中：' + panel.label;
    else if (panel.hasData) status.textContent = '目前的資料：' + (panel.source === 'url' ? 'URL ' : '本機 CSV 檔案 ') + (panel.label || '');
    else if (panel.source === 'url') status.textContent = '沒有載入任何資料（URL 讀取失敗）：' + panel.label;
    else status.textContent = '尚未載入資料：請以 URL 或本機 CSV 檔案提交。';
  }

  var fileToken = 0;
  function readFile(input) {
    var file = input.files && input.files[0];
    if (!file || !controller) return;
    var token = ++fileToken;
    file.arrayBuffer().then(function (buffer) {
      input.value = '';                            /* the same file can be chosen again */
      /* dropped if the user has moved to another problem or chosen another file meanwhile */
      if (token !== fileToken || byId('problem-select').value !== 'custom') return;
      controller.submitData(new Uint8Array(buffer), { source: 'file', label: file.name });
    }, function () {
      input.value = '';
      if (token !== fileToken || byId('problem-select').value !== 'custom') return;
      message('無法讀取這個本機檔案（瀏覽器拒絕讀取）。請重新選擇檔案。', 'error');
    });
  }

  /* ---- render ------------------------------------------------------------------------------------- */
  function render(view) {
    current = view;
    if (view.mode === 'king_county') { setExploring(false); return; }
    setExploring(true);
    byId('ex-title').textContent = App.PROBLEM_TITLES[view.problem] || '探索執行';
    var isCustom = view.problem === 'custom';
    var withPanel = function (ids) { return isCustom ? ['ex-custom'].concat(ids) : ids; };
    if (isCustom) renderCustom(view.custom);
    if (view.mode === 'custom') {
      message(view.notice ? view.notice.text : '', view.notice ? view.notice.kind : null);
      showBlocks(['ex-custom']);
      return;
    }
    if (view.mode === 'error') { message(view.message, 'error'); showBlocks(withPanel([])); return; }
    var run = view.run;
    if (!run.load.ok) {
      message('無法載入資料：' + App.loadFailureText(run.load), 'error');
      if (run.load.sha256) {
        renderData(run);
        showBlocks(withPanel(['ex-data']));
      } else {
        showBlocks(withPanel([]));
      }
      return;
    }
    var res = run.result;
    renderData(run);
    if (res.run.status !== 'COMPLETED') {
      var inv = res.run.invalid_candidates || [], lines = [App.runReasonText(res.run.reason)];
      if (inv.length) {
        lines.push('All-in baseline：' + App.statusText(inv[0].status) + '。' + inv[0].reasons.map(App.reasonText).join('；'));
        if (inv.length > 1) lines.push('其餘 ' + (inv.length - 1) + ' 個候選也都無效；原因見下方共線診斷。');
      }
      message(lines.join(' '), 'error');
      showBlocks(withPanel(['ex-data', 'ex-methods']));
      return;
    }
    message('執行完成：五種方法共 ' + res.candidates.length + ' 個候選' + (run.ms === null ? '' : '，耗時 ' + run.ms.toFixed(1) + ' ms（瀏覽器內計算，只供參考）'));
    showBlocks(withPanel(['ex-data', 'ex-model', 'ex-predictor', 'ex-test', 'ex-methods']));
    ui.result = res;
    ui.key = App.defaultKey(res);
    renderCompare();
    renderLasso();
    renderSelection();
  }

  function init() {
    var problemSelect = byId('problem-select');
    if (!problemSelect || !byId('explore')) return;
    if (!App || !Engine || !Loader || !Plot) { problemSelect.disabled = true; return; }
    controller = App.createController({ loader: Loader, engine: Engine, datasets: { startups50: DATA }, render: render,
      now: function () { return performance.now(); } });
    window.HW2_EXPLORE = { state: controller.state, view: function () { return current; },
      selection: function () { return { key: ui.key, compareAll: ui.compareAll, metric: ui.metric }; } };
    problemSelect.value = 'king_county';      /* the default problem, even if the browser restored the form */
    byId('ex-metric').value = 'rmse';
    byId('ex-metric').addEventListener('change', function (ev) { ui.metric = ev.target.value; if (ui.result) renderKChart(); });
    byId('ex-compare-all').addEventListener('click', function () {
      ui.compareAll = !ui.compareAll;
      if (ui.result) { renderControls(); renderKChart(); }
    });
    /* #76: the custom dataset's inputs. Submitting the URL form is the only action that reads a URL;
     * no form is ever sent by the browser itself (that would reload the page and add URL parameters). */
    byId('ex-url-form').addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (byId('ex-url-load').disabled) return;
      controller.submitUrl(byId('ex-url').value);
    });
    byId('ex-file').addEventListener('change', function (ev) { readFile(ev.target); });
    byId('ex-target').addEventListener('change', function (ev) {
      if (ev.target.value !== '') controller.setTarget(Number(ev.target.value));
    });
    byId('ex-pred-form').addEventListener('submit', function (ev) { ev.preventDefault(); });
    controller.init();
    problemSelect.addEventListener('change', function () {
      byId('ex-url').value = '';                   /* a new visit to the custom dataset starts empty */
      byId('ex-file').value = '';
      fileToken++;
      controller.selectProblem(problemSelect.value);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
