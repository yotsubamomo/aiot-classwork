/* HW2 dashboard: reads window.MODEL_DATA (assets/model_data.js) and renders
 *   A overview (meta), B/C model selection and training-CV KPI (cv; "訓練 CV（USD）"),
 *   D live predictor (fit; OLS subset models only), E Test block (test only; "Test 評估（USD）").
 *
 * Layering (BR-01): every KPI comes from the selected model's `cv`, the predictor from its `fit`,
 * and every Test number from model_data.test. Nothing here scores a model on test data: the Test
 * block only displays the exported `test` entries (DA B-3, G-3); test_inputs is read only for the
 * identifiers and actual prices that the scatter plot draws (see testRows()).
 *
 * OV-6 / SR-09 measurement: window.HW2_PERF.firstDraw is the time from navigation start
 * (performance.timeOrigin) to the end of the first complete draw of the scatter plot;
 * window.HW2_PERF.interactions[] holds {type, start, end, ms} from the input event's timeStamp to
 * the end of the redraw of the affected blocks (method/k switch, wheel zoom, drag pan, buttons).
 *
 * No network access: every resource is a local file so the page works from file://. */
(function () {
  'use strict';

  var Core = window.HW2Core;
  var MD = window.MODEL_DATA;
  var PERF = window.HW2_PERF = { clock: 'performance.now() (ms since navigation start)',
    firstDraw: null, interactions: [], nTestPoints: 0 };

  var METHOD_ORDER = ['allin', 'forward_sfs', 'backward_sfs', 'rfe', 'lasso_path'];
  var METHOD_LABELS = { allin: 'All-in baseline', forward_sfs: 'Forward SFS', backward_sfs: 'Backward SFS',
    rfe: 'RFE', lasso_path: 'Lasso 路徑排序' };
  var FEATURE_LABELS = { date: '交易日期', bedrooms: '臥室數', bathrooms: '浴室數', sqft_living: '室內面積（sqft）',
    sqft_lot: '土地面積（sqft）', floors: '樓層數', waterfront: '臨水（0／1）', view: '景觀評分（0–4）',
    condition: '屋況（1–5）', grade: '建築等級（1–13）', sqft_above: '地上面積（sqft）', yr_built: '建造年',
    yr_renovated: '整修年', zipcode: 'Zipcode', lat: '緯度', long: '經度', sqft_living15: '鄰近 15 戶室內面積（sqft）',
    sqft_lot15: '鄰近 15 戶土地面積（sqft）' };

  var nf = new Intl.NumberFormat('zh-TW');
  var usdFmt = new Intl.NumberFormat('zh-TW', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  var state = { method: 'allin', k: null, zipOverride: null };
  var scatter = null;
  var shownTestKey = null;

  function byId(id) { return document.getElementById(id); }
  function setText(id, value) {
    var el = byId(id);
    if (el) el.textContent = value == null ? '—' : String(value);
  }
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
  function usd(v) { return v == null || !isFinite(v) ? '—' : usdFmt.format(v); }
  function sci(v) {
    if (v == null || !isFinite(v)) return '—';
    var e = Math.floor(Math.log10(Math.abs(v)));
    return (v / Math.pow(10, e)).toFixed(3) + ' × 10^' + e;
  }
  function pct(v, d) { return v == null ? '—' : (100 * v).toFixed(d == null ? 1 : d) + '%'; }
  function fixed(v, d) { return v == null || !isFinite(v) ? '—' : Number(v).toFixed(d); }
  function showError(message) {
    var box = byId('load-error');
    box.textContent = message;
    box.hidden = false;
  }

  /* ---- A. overview ------------------------------------------------------------------------ */
  function renderOverview(meta, preprocess) {
    var ds = meta.dataset || {};
    setText('meta-dataset-name', ds.name);
    setText('meta-dataset-slug', ds.kaggle_slug);
    if (ds.url) byId('meta-dataset-link').setAttribute('href', ds.url);
    setText('meta-license', ds.license);
    setText('meta-rows', nf.format(meta.n_rows));
    setText('meta-houses', nf.format(meta.n_unique_ids));
    setText('meta-repeat', nf.format(meta.n_repeat_sales));
    setText('meta-sha', meta.csv_sha256);
    setText('meta-sf', meta.n_source_features);
    setText('meta-groups', meta.n_feature_groups);
    var split = meta.split || {};
    var cv = meta.cv || {};
    setText('meta-ntrain', nf.format(split.n_train));
    setText('meta-ntest', nf.format(split.n_test));
    setText('meta-folds', cv.n_folds);
    setText('cv-nfolds', cv.n_folds);
    setText('meta-fold-rows', (cv.fold_rows || []).map(function (n) { return nf.format(n); }).join('／'));
    setText('meta-seed', meta.seed);
    var versions = meta.versions || {};
    setText('meta-versions', Object.keys(versions).map(function (k) { return k + ' ' + versions[k]; }).join('、'));
    var timing = meta.timing_s || {};
    setText('meta-timing', Object.keys(timing).map(function (k) {
      return k + ' ' + Number(timing[k]).toFixed(2) + ' 秒';
    }).join('、'));
    setText('meta-generated', meta.generated_at);
    setText('meta-sections', (meta.sections_written || []).join('、'));
    var items = (preprocess && preprocess.excluded_source_features) || [];
    setText('meta-excluded', items.length
      ? '不進模型：' + items.map(function (x) { return x.name; }).join('、') +
        '（sqft_living = sqft_above + sqft_basement，三欄完全共線）' : '');
  }

  /* ---- model catalogue -------------------------------------------------------------------- */
  function catalogue() {
    var out = {};
    var allin = MD.baselines && MD.baselines.allin;
    if (allin) out.allin = [allin];
    Object.keys(MD.methods || {}).forEach(function (m) {
      out[m] = MD.methods[m].slice().sort(function (a, b) { return a.k - b.k; });
    });
    return out;
  }
  var CAT = {};
  function methodsAvailable() { return METHOD_ORDER.filter(function (m) { return CAT[m] && CAT[m].length; }); }
  function entryFor(method, k) {
    var list = CAT[method] || [];
    for (var i = 0; i < list.length; i++) if (list[i].k === k) return list[i];
    return null;
  }
  function entryByKey(key) {
    var found = null;
    Object.keys(CAT).forEach(function (m) { CAT[m].forEach(function (e) { if (e.model_key === key) found = e; }); });
    return found;
  }
  function modelName(entry) {
    return entry ? (METHOD_LABELS[entry.method] || entry.method) + ' · k = ' + entry.k : '—';
  }
  function defaultK(method) {
    var list = CAT[method] || [];
    var winner = list.filter(function (e) { return e.is_method_winner; })[0];
    return (winner || list[0] || {}).k;
  }

  /* ---- B. controls ------------------------------------------------------------------------ */
  function renderControls() {
    var seg = byId('method-seg');
    seg.textContent = '';
    methodsAvailable().forEach(function (m) {
      var b = el('button', { type: 'button', class: 'seg__btn', 'aria-pressed': String(m === state.method), 'data-method': m },
        [METHOD_LABELS[m] || m, el('span', { class: 'meta', text: m === 'allin' ? 'k = 18 固定' : (CAT[m].length + ' 個 k') })]);
      b.addEventListener('click', function (ev) {
        timed('method', ev, function () { state.method = m; state.k = defaultK(m); state.zipOverride = null; update(); });
      });
      seg.appendChild(b);
    });
    var grid = byId('k-grid');
    grid.textContent = '';
    if (state.method === 'allin') {
      grid.className = 'kgrid kgrid--fixed';
      grid.appendChild(el('div', { class: 'kfixed' }, [el('span', { class: 'kfixed__k', text: 'k = 18（固定）' }),
        el('span', { class: 'kfixed__txt', text: 'All-in baseline 是全部 18 個 feature group 的單一 OLS，沒有 k 路徑。' })]));
      setText('k-help', '');
      return;
    }
    grid.className = 'kgrid';
    CAT[state.method].forEach(function (e) {
      var cls = 'kbtn' + (e.is_method_winner ? ' is-winner' : '') + (e.status.state === 'invalid' ? ' is-invalid' : '');
      var label = 'k = ' + e.k + (e.is_method_winner ? '（該方法 CV winner）' : '') + (e.status.state === 'invalid' ? '（invalid）' : '');
      var b = el('button', { type: 'button', class: cls, 'aria-pressed': String(e.k === state.k), 'aria-label': label, text: String(e.k) });
      b.addEventListener('click', function (ev) {
        timed('k', ev, function () { state.k = e.k; state.zipOverride = null; update(); });
      });
      grid.appendChild(b);
    });
    setText('k-help', '綠點：該方法 CV winner；紅斜紋：invalid 候選。');
  }

  function renderSelected(entry) {
    var box = byId('selected-model');
    box.textContent = '';
    if (!entry) return;
    var tags = [];
    if (entry.is_method_winner) tags.push(el('span', { class: 'tag tag--winner', text: entry.method === 'allin' ? 'All-in baseline' : '該方法 CV winner' }));
    if (MD.winners && MD.winners.overall && MD.winners.overall.model_key === entry.model_key) tags.push(el('span', { class: 'tag tag--overall', text: '整體 CV winner' }));
    if (entry.status.state === 'invalid') tags.push(el('span', { class: 'tag tag--invalid', text: 'invalid：' + entry.status.reason }));
    box.appendChild(el('strong', { text: modelName(entry) }));
    if (tags.length) box.appendChild(el('div', { class: 'tags' }, tags));
    box.appendChild(el('span', { class: 'small', text: 'Canonical subset（整個 training set 上計算）：' + entry.canonical_groups.join('、') }));
    box.appendChild(el('span', { class: 'small muted', text: entry.folds_agree + '／' + entry.fold_groups.length + ' 個 fold 的子集與 canonical subset 相同' }));
  }

  /* ---- C. KPI (cv) and fit --------------------------------------------------------------- */
  function kpi(label, value, sub, tagText) {
    return el('div', { class: 'kpi' }, [
      el('div', { class: 'kpi__label' }, [el('span', { text: label }), tagText ? el('span', { class: 'tag tag--cv', text: tagText }) : null]),
      el('div', { class: 'kpi__value num', text: value }),
      sub ? el('div', { class: 'kpi__sub num', text: sub }) : null]);
  }

  function renderKpi(entry) {
    var box = byId('kpi-cv');
    box.textContent = '';
    var status = byId('status-box');
    var cv = entry && entry.cv;
    if (!entry || !cv || !cv.mean) {
      status.textContent = entry ? 'invalid 候選：' + entry.status.reason + '；沒有可比較的 CV 指標。' : '';
      return;
    }
    var m = cv.mean, s = cv.std;
    box.appendChild(kpi('CV RMSE', usd(m.rmse), '± ' + usd(s.rmse) + '（' + cv.n_folds + ' 折標準差）', '訓練 CV（USD）'));
    box.appendChild(kpi('CV MAE', usd(m.mae), '± ' + usd(s.mae), '訓練 CV（USD）'));
    box.appendChild(kpi('CV MSE（USD²）', sci(m.mse), '± ' + sci(s.mse), '訓練 CV（USD）'));
    box.appendChild(kpi('CV R²（USD 尺度）', fixed(m.r2, 4), '± ' + fixed(s.r2, 4), '訓練 CV（USD）'));
    status.textContent = '這些是訓練集內分組交叉驗證的指標（以 exp(log 預測) 回轉到 USD 計算），不是 Test 結果。';
  }

  function renderFit(entry) {
    var dl = byId('fit-facts');
    dl.textContent = '';
    var f = entry && entry.fit;
    if (!f) {
      dl.appendChild(el('dt', { text: '狀態' }));
      dl.appendChild(el('dd', { text: entry ? 'invalid 候選（' + entry.status.reason + '）：沒有 fit' : '—' }));
      return;
    }
    [['R²（log 尺度）', fixed(f.r2_log, 4)], ['Adjusted R²（log 尺度，以實際 rank）', fixed(f.adj_r2_log, 4)],
      ['n_train', nf.format(f.n_train)], ['design matrix 欄數／rank', f.n_columns + '／' + f.rank],
      ['df_resid', nf.format(f.df_resid)], ['s²（log 尺度）', fixed(f.s2, 6)], ['t(0.975, df)', fixed(f.t_crit, 4)]
    ].forEach(function (p) { dl.appendChild(el('dt', { text: p[0] })); dl.appendChild(el('dd', { class: 'num', text: p[1] })); });
  }

  /* ---- D. predictor (fit) ----------------------------------------------------------------- */
  var URL_PARAMS = (function () { try { return new URLSearchParams(window.location.search); } catch (e) { return null; } })();

  function renderPredictor(entry) {
    var box = byId('pred-fields');
    box.textContent = '';
    setText('pred-model', modelName(entry));
    if (!Core.canPredict(entry)) {
      setText('pred-intro', entry ? 'invalid 候選：沒有 fit，不提供即時預測。' : '沒有可用的模型。');
      setText('pred-price', '—'); setText('pred-pi', '—');
      byId('pred-status').textContent = '';
      return;
    }
    var specs = Core.inputSpec(entry.fit, MD.inputs);
    setText('pred-intro', '只列出這個模型用到的 source feature（共 ' + specs.length + ' 項），輸入原始值；預設為 training set 的中位數（zipcode 為最常見的類別）。超出 training 範圍時會警告，但仍照常計算。');
    specs.forEach(function (spec) {
      var id = 'in-' + spec.name;
      var fromUrl = URL_PARAMS && URL_PARAMS.has(spec.name) ? URL_PARAMS.get(spec.name) : null;
      var field = el('div', { class: 'field', 'data-feature': spec.name });
      field.appendChild(el('label', { for: id, text: FEATURE_LABELS[spec.name] || spec.name }));
      var warn = el('div', { class: 'warn', id: id + '-warn', hidden: 'hidden' });
      if (spec.kind === 'nominal') {
        var sel = el('select', { id: id, class: 'input', 'aria-describedby': id + '-warn' });
        spec.categories.forEach(function (c) {
          sel.appendChild(el('option', { value: c, text: c === spec.baseline ? c + '（基準類別）' : c }));
        });
        sel.value = spec.default;
        if (fromUrl !== null) {
          if (spec.categories.indexOf(fromUrl) >= 0) sel.value = fromUrl;
          else state.zipOverride = fromUrl;
        }
        sel.addEventListener('change', function () { state.zipOverride = null; predictNow(entry, specs); });
        field.appendChild(sel);
      } else if (spec.kind === 'renovation') {
        var num = el('input', { id: id, class: 'input', type: 'number', step: '1', min: '0', inputmode: 'numeric', 'aria-describedby': id + '-warn' });
        var chk = el('input', { id: id + '-none', type: 'checkbox' });
        var start = fromUrl !== null ? fromUrl : spec.default;
        chk.checked = Number(start) === 0;
        num.value = Number(start) === 0 ? '' : start;
        num.disabled = chk.checked;
        chk.addEventListener('change', function () { num.disabled = chk.checked; if (!chk.checked && !num.value) num.value = spec.max; predictNow(entry, specs); });
        num.addEventListener('input', function () { predictNow(entry, specs); });
        field.appendChild(el('div', { class: 'renov__row' }, [num, el('label', { class: 'check', for: id + '-none' }, [chk, '未整修'])]));
      } else {
        var input = el('input', { id: id, class: 'input', type: spec.kind === 'date' ? 'date' : 'number', step: 'any', 'aria-describedby': id + '-warn' });
        input.value = fromUrl !== null ? fromUrl : spec.default;
        input.addEventListener('input', function () { predictNow(entry, specs); });
        field.appendChild(input);
      }
      field.appendChild(el('div', { class: 'help small muted', text: rangeText(spec) }));
      field.appendChild(warn);
      box.appendChild(field);
    });
    predictNow(entry, specs);
  }

  function rangeText(spec) {
    if (spec.kind === 'nominal') return 'training 類別 ' + spec.categories.length + ' 個；基準類別 ' + spec.baseline;
    if (spec.kind === 'renovation') return '有整修時 training 範圍 ' + spec.min + '–' + spec.max + '；未整修請勾選';
    return 'training 範圍 ' + spec.min + '–' + spec.max + '；中位數 ' + spec.median;
  }

  function readInputs(specs) {
    var raw = {}, warnings = [], errors = [];
    specs.forEach(function (spec) {
      var id = 'in-' + spec.name;
      var warn = byId(id + '-warn');
      var value;
      warn.hidden = true;
      warn.textContent = '';
      if (spec.kind === 'renovation') {
        value = byId(id + '-none').checked ? 0 : byId(id).value;
      } else {
        value = byId(id).value;
      }
      if (spec.kind === 'nominal') {
        if (state.zipOverride !== null) {
          value = state.zipOverride;
          warn.textContent = '此 zipcode 不在模型的訓練類別中，已以基準類別計算（輸入值：' + value + '）';
          warn.hidden = false;
          warnings.push(warn.textContent);
        }
      } else if (value === '' || value === null || (spec.kind !== 'date' && !isFinite(Number(value)))) {
        errors.push((FEATURE_LABELS[spec.name] || spec.name) + '：請輸入' + (spec.kind === 'date' ? '日期' : '數值'));
        return;
      }
      if (spec.kind !== 'nominal' && Core.outOfRange(spec, value)) {
        warn.textContent = '超出 training 範圍（' + spec.min + '–' + spec.max + '），仍照常計算，屬於外推。';
        warn.hidden = false;
        warnings.push((FEATURE_LABELS[spec.name] || spec.name) + '：' + warn.textContent);
      }
      raw[spec.name] = spec.kind === 'date' || spec.kind === 'nominal' ? value : Number(value);
    });
    return { raw: raw, warnings: warnings, errors: errors };
  }

  function predictNow(entry, specs) {
    var status = byId('pred-status');
    status.textContent = '';
    var read = readInputs(specs);
    if (read.errors.length) {
      setText('pred-price', '—'); setText('pred-pi', '—');
      read.errors.forEach(function (t) { status.appendChild(el('div', { class: 'warn', text: t })); });
      return;
    }
    var out;
    try { out = Core.predict(entry.fit, read.raw, MD.preprocess); } catch (e) {
      setText('pred-price', '—'); setText('pred-pi', '—');
      status.appendChild(el('div', { class: 'warn', text: '無法計算：' + e.message }));
      return;
    }
    setText('pred-price', usd(out.prediction));
    setText('pred-pi', usd(out.lower) + ' – ' + usd(out.upper));
    read.warnings.forEach(function (t) { status.appendChild(el('div', { class: 'warn', text: t })); });
  }

  /* ---- E. Test block (test only) ---------------------------------------------------------- */
  function testRows() {
    /* Identifiers and actual prices of the test sales, in test_inputs order (for drawing only). */
    var ti = MD.test_inputs;
    var iRow = ti.fields.indexOf('row'), iId = ti.fields.indexOf('id'), iActual = ti.fields.indexOf('actual_price');
    return ti.rows.map(function (r) { return { row: r[iRow], id: r[iId], actual: r[iActual] }; });
  }

  function renderTest(entry, interactive) {
    var hasTest = !!(MD.test && MD.test_inputs && MD.test_inputs.written);
    byId('test-empty').hidden = hasTest;
    byId('test-body').hidden = !hasTest;
    var notice = byId('test-notice');
    notice.hidden = true;
    var key = Core.testModelKey(MD, state.method);
    var tEntry = hasTest && key ? MD.test[key] : null;
    var shown = key ? entryByKey(key) : null;
    setText('test-model', shown ? modelName(shown) : '—');
    var tag = byId('test-winner-tag');
    tag.hidden = !shown;
    if (shown) {
      var overall = MD.winners && MD.winners.overall && MD.winners.overall.model_key === key;
      tag.textContent = overall ? '整體 CV winner' : (shown.method === 'allin' ? 'All-in baseline' : '該方法 CV winner');
    }
    if (!hasTest) return;
    if (entry && shown && entry.model_key !== shown.model_key) {
      notice.textContent = '目前選取的 ' + modelName(entry) + ' 不是該方法的 CV winner。Test 區塊展示的是該方法的 CV winner：' +
        modelName(shown) + '。Test 只對被授權的模型各評估一次，切換選取不會產生新的 Test 評估。';
      notice.hidden = false;
    }
    if (!tEntry) {
      notice.textContent = '這個方法沒有可展示的 Test 結果。';
      notice.hidden = false;
      return;
    }
    var box = byId('kpi-test');
    box.textContent = '';
    [['Test RMSE', usd(tEntry.rmse)], ['Test MAE', usd(tEntry.mae)], ['Test MSE（USD²）', sci(tEntry.mse)],
      ['Test R²（USD 尺度）', fixed(tEntry.r2, 4)]].forEach(function (p) {
      box.appendChild(el('div', { class: 'kpi kpi--test' }, [
        el('div', { class: 'kpi__label' }, [el('span', { text: p[0] }), el('span', { class: 'tag tag--test', text: 'Test 評估（USD）' })]),
        el('div', { class: 'kpi__value num', text: p[1] }),
        el('div', { class: 'kpi__sub', text: modelName(shown) + '・n_test ' + nf.format(tEntry.n_test) })]));
    });
    var cov = byId('covstats');
    cov.textContent = '';
    var u = tEntry.coverage_uncertainty || {};
    [['經驗涵蓋率', pct(tEntry.coverage, 2), '名目 95%'],
      ['涵蓋筆數', nf.format(tEntry.n_covered) + '／' + nf.format(tEntry.n_test), '閉區間 lower ≤ 實際 ≤ upper'],
      ['平均區間寬度', usd(tEntry.mean_width), 'USD'],
      ['二項近似 ±', '± ' + pct(u.half_width_95, 2), '假設各筆獨立（見下方說明）'],
      ['Test 房屋／重複交易', nf.format(MD.test_inputs.n_houses) + '／' + nf.format(MD.test_inputs.n_repeat_sales), '同一房屋的多筆交易'],
      ['未見 zipcode', nf.format(tEntry.n_unseen_zipcode), '以基準類別計算的筆數']].forEach(function (p) {
      cov.appendChild(el('div', { class: 'kpi kpi--test' }, [el('div', { class: 'kpi__label', text: p[0] }),
        el('div', { class: 'kpi__value num', text: p[1] }), el('div', { class: 'kpi__sub', text: p[2] })]));
    });
    if (shownTestKey !== key) {
      shownTestKey = key;
      scatter.setData(tEntry, testRows());
      scatter.reset();
    }
  }

  /* ---- scatter (canvas; every test row, no sampling) -------------------------------------- */
  function Scatter(canvas, tip) {
    this.canvas = canvas; this.tip = tip;
    this.pts = []; this.view = null; this.home = null; this.drag = null;
    this.margin = { l: 70, r: 14, t: 12, b: 46 };
    this.bind();
  }
  Scatter.prototype.setData = function (tEntry, rows) {
    var pts = [];
    for (var i = 0; i < rows.length; i++) {
      pts.push({ row: rows[i].row, id: rows[i].id, actual: rows[i].actual, pred: tEntry.predicted[i],
        lo: tEntry.lower[i], hi: tEntry.upper[i], covered: tEntry.covered[i],
        lx: Math.log10(tEntry.predicted[i]), ly: Math.log10(rows[i].actual),
        llo: Math.log10(tEntry.lower[i]), lhi: Math.log10(tEntry.upper[i]) });
    }
    this.pts = pts;
    PERF.nTestPoints = pts.length;
    var lo = Infinity, hi = -Infinity;
    pts.forEach(function (p) {
      lo = Math.min(lo, p.lx, p.ly, p.llo); hi = Math.max(hi, p.lx, p.ly, p.lhi);
    });
    var pad = (hi - lo) * 0.03;
    this.home = { x0: lo - pad, x1: hi + pad, y0: lo - pad, y1: hi + pad };
  };
  Scatter.prototype.reset = function () { this.view = Object.assign({}, this.home); this.draw(); };
  Scatter.prototype.size = function () {
    var rect = this.canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    var w = Math.max(1, Math.round(rect.width)), h = Math.max(1, Math.round(rect.height));
    if (this.canvas.width !== Math.round(w * dpr) || this.canvas.height !== Math.round(h * dpr)) {
      this.canvas.width = Math.round(w * dpr); this.canvas.height = Math.round(h * dpr);
    }
    return { w: w, h: h, dpr: dpr };
  };
  Scatter.prototype.sx = function (lx) { var m = this.margin, v = this.view; return m.l + (lx - v.x0) / (v.x1 - v.x0) * (this.w - m.l - m.r); };
  Scatter.prototype.sy = function (ly) { var m = this.margin, v = this.view; return this.h - m.b - (ly - v.y0) / (v.y1 - v.y0) * (this.h - m.t - m.b); };
  Scatter.prototype.ix = function (px) { var m = this.margin, v = this.view; return v.x0 + (px - m.l) / (this.w - m.l - m.r) * (v.x1 - v.x0); };
  Scatter.prototype.iy = function (py) { var m = this.margin, v = this.view; return v.y0 + (this.h - m.b - py) / (this.h - m.t - m.b) * (v.y1 - v.y0); };

  function ticks(a, b) {
    /* Decades if at least 3 fit, else 1-2-5, else 1..9 per decade, else 5 linear ticks. */
    var sets = [[1], [1, 2, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]];
    for (var s = 0; s < sets.length; s++) {
      var out = [];
      for (var e = Math.floor(a) - 1; e <= Math.ceil(b); e++) {
        for (var j = 0; j < sets[s].length; j++) {
          var v = Math.log10(sets[s][j]) + e;
          if (v >= a && v <= b) out.push(v);
        }
      }
      if (out.length >= 3) return out;
    }
    var lin = [];
    for (var i = 0; i <= 4; i++) lin.push(a + i * (b - a) / 4);
    return lin;
  }
  function trimZeros(text) {
    /* '200' stays '200'; '2.50' -> '2.5'; '3.00' -> '3' (only zeros after a decimal point). */
    return text.indexOf('.') < 0 ? text : text.replace(/0+$/, '').replace(/\.$/, '');
  }
  function priceLabel(lv) {
    var v = Math.pow(10, lv);
    if (v >= 1e8) return trimZeros((v / 1e8).toPrecision(3)) + ' 億';
    if (v >= 1e4) return trimZeros((v / 1e4).toPrecision(3)) + ' 萬';
    return String(Math.round(v));
  }

  Scatter.prototype.draw = function () {
    if (!this.view) return;
    var dim = this.size();
    this.w = dim.w; this.h = dim.h;
    var ctx = this.canvas.getContext('2d');
    ctx.setTransform(dim.dpr, 0, 0, dim.dpr, 0, 0);
    var m = this.margin, w = this.w, h = this.h, v = this.view, self = this;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, w, h);
    ctx.font = '11px "Noto Sans TC","Microsoft JhengHei","PingFang TC",system-ui,sans-serif';
    ctx.strokeStyle = '#E6ECF4'; ctx.fillStyle = '#475569'; ctx.lineWidth = 1;
    var lastX = -Infinity, lastY = Infinity;          /* skip labels that would overlap */
    ticks(v.x0, v.x1).forEach(function (t) {
      var x = self.sx(t); ctx.beginPath(); ctx.moveTo(x, m.t); ctx.lineTo(x, h - m.b); ctx.stroke();
      var label = priceLabel(t), half = ctx.measureText(label).width / 2;
      if (x - half > lastX + 6) { ctx.textAlign = 'center'; ctx.fillText(label, x, h - m.b + 14); lastX = x + half; }
    });
    ticks(v.y0, v.y1).forEach(function (t) {
      var y = self.sy(t); ctx.beginPath(); ctx.moveTo(m.l, y); ctx.lineTo(w - m.r, y); ctx.stroke();
      if (y < lastY - 14) { ctx.textAlign = 'right'; ctx.fillText(priceLabel(t), m.l - 6, y + 4); lastY = y; }
    });
    ctx.fillStyle = '#334155'; ctx.textAlign = 'center';
    ctx.fillText('預測價格（USD，log 刻度）', m.l + (w - m.l - m.r) / 2, h - 8);
    ctx.save(); ctx.translate(14, m.t + (h - m.t - m.b) / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('實際價格（USD，log 刻度）', 0, 0); ctx.restore();

    ctx.save();
    ctx.beginPath(); ctx.rect(m.l, m.t, w - m.l - m.r, h - m.t - m.b); ctx.clip();
    var pts = this.pts, i, p, x;
    var segIn = new Path2D(), segOut = new Path2D(), dotIn = new Path2D(), dotOut = new Path2D();
    for (i = 0; i < pts.length; i++) {
      p = pts[i]; x = this.sx(p.lx);
      var seg = p.covered ? segIn : segOut;
      seg.moveTo(x, this.sy(p.llo)); seg.lineTo(x, this.sy(p.lhi));
    }
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(30,64,175,0.22)'; ctx.stroke(segIn);
    ctx.strokeStyle = 'rgba(180,83,9,0.55)'; ctx.stroke(segOut);
    for (i = 0; i < pts.length; i++) {
      p = pts[i]; x = this.sx(p.lx); var y = this.sy(p.ly);
      if (p.covered) { dotIn.moveTo(x + 2, y); dotIn.arc(x, y, 2, 0, 2 * Math.PI); }
      else dotOut.rect(x - 2.5, y - 2.5, 5, 5);
    }
    ctx.fillStyle = 'rgba(30,64,175,0.75)'; ctx.fill(dotIn);
    ctx.fillStyle = 'rgba(180,83,9,0.95)'; ctx.fill(dotOut);
    var a = Math.max(v.x0, v.y0), b = Math.min(v.x1, v.y1);
    ctx.setLineDash([6, 4]); ctx.strokeStyle = '#0F172A'; ctx.lineWidth = 1.25;
    ctx.beginPath(); ctx.moveTo(this.sx(a), this.sy(a)); ctx.lineTo(this.sx(b), this.sy(b)); ctx.stroke();
    ctx.setLineDash([]);
    if (this.hover) {
      p = this.hover; x = this.sx(p.lx);
      ctx.strokeStyle = '#0F172A'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x, this.sy(p.llo)); ctx.lineTo(x, this.sy(p.lhi)); ctx.stroke();
      ctx.beginPath(); ctx.arc(x, this.sy(p.ly), 4, 0, 2 * Math.PI); ctx.stroke();
    }
    ctx.restore();
    ctx.strokeStyle = '#94A3B8'; ctx.lineWidth = 1; ctx.strokeRect(m.l, m.t, w - m.l - m.r, h - m.t - m.b);
    var end = performance.now();
    if (!PERF.firstDraw && pts.length) {
      PERF.firstDraw = { start: 0, end: end, ms: end, nPoints: pts.length };
      reportPerf();
    }
    return end;
  };

  Scatter.prototype.zoomAt = function (px, py, factor) {
    var v = this.view, cx = this.ix(px), cy = this.iy(py);
    var span = (v.x1 - v.x0) * factor;
    var homeSpan = this.home.x1 - this.home.x0;
    if (span < 0.02) factor = 0.02 / (v.x1 - v.x0);
    if (span > homeSpan * 1.5) factor = homeSpan * 1.5 / (v.x1 - v.x0);
    this.view = { x0: cx - (cx - v.x0) * factor, x1: cx + (v.x1 - cx) * factor,
      y0: cy - (cy - v.y0) * factor, y1: cy + (v.y1 - cy) * factor };
  };
  Scatter.prototype.panBy = function (dx, dy) {
    var v = this.view, m = this.margin;
    var kx = (v.x1 - v.x0) / (this.w - m.l - m.r), ky = (v.y1 - v.y0) / (this.h - m.t - m.b);
    this.view = { x0: v.x0 - dx * kx, x1: v.x1 - dx * kx, y0: v.y0 + dy * ky, y1: v.y1 + dy * ky };
  };
  Scatter.prototype.nearest = function (px, py) {
    var best = null, bestD = 100, pts = this.pts;
    for (var i = 0; i < pts.length; i++) {
      var dx = this.sx(pts[i].lx) - px, dy = this.sy(pts[i].ly) - py, d = dx * dx + dy * dy;
      if (d < bestD) { bestD = d; best = pts[i]; }
    }
    return best;
  };
  Scatter.prototype.showTip = function (p, px, py) {
    if (!p) { this.tip.hidden = true; return; }
    this.tip.textContent = '';
    [['第 ' + nf.format(p.row) + ' 列（房屋 ' + p.id + '）'], ['預測 ' + usd(p.pred)], ['實際 ' + usd(p.actual)],
      ['95% PI ' + usd(p.lo) + ' – ' + usd(p.hi)], [p.covered ? '落入區間' : '未落入區間']].forEach(function (t) {
      this.tip.appendChild(el('div', { text: t[0] }));
    }, this);
    this.tip.hidden = false;
    var flip = px > this.w / 2;                        /* keep the tip inside the plot */
    this.tip.style.transform = flip ? 'translate(calc(-100% - 12px), -50%)' : 'translate(12px, -50%)';
    this.tip.style.left = px + 'px';
    this.tip.style.top = Math.min(Math.max(py, 50), this.h - 50) + 'px';
  };
  Scatter.prototype.bind = function () {
    var self = this, c = this.canvas;
    c.addEventListener('wheel', function (ev) {
      if (!self.view) return;
      ev.preventDefault();
      var r = c.getBoundingClientRect();
      timed('wheel-zoom', ev, function () { self.zoomAt(ev.clientX - r.left, ev.clientY - r.top, Math.exp(ev.deltaY * 0.0015)); self.draw(); });
    }, { passive: false });
    c.addEventListener('pointerdown', function (ev) {
      if (!self.view) return;
      self.drag = { x: ev.clientX, y: ev.clientY, moved: false };
      c.setPointerCapture(ev.pointerId);
    });
    c.addEventListener('pointermove', function (ev) {
      if (!self.view) return;
      var r = c.getBoundingClientRect();
      if (self.drag) {
        self.panBy(ev.clientX - self.drag.x, ev.clientY - self.drag.y);
        self.drag.x = ev.clientX; self.drag.y = ev.clientY; self.drag.moved = true;
        self.hover = null; self.tip.hidden = true;
        self.draw();
        return;
      }
      var p = self.nearest(ev.clientX - r.left, ev.clientY - r.top);
      if (p !== self.hover) { self.hover = p; self.draw(); }
      self.showTip(p, ev.clientX - r.left, ev.clientY - r.top);
    });
    c.addEventListener('pointerup', function (ev) {
      if (self.drag && self.drag.moved) timed('drag-pan', ev, function () { self.draw(); });
      self.drag = null;
    });
    c.addEventListener('pointerleave', function () { self.hover = null; self.tip.hidden = true; if (self.view) self.draw(); });
    c.addEventListener('keydown', function (ev) {
      if (!self.view) return;
      var step = 40, done = true;
      var cx = self.margin.l + (self.w - self.margin.l - self.margin.r) / 2, cy = self.margin.t + (self.h - self.margin.t - self.margin.b) / 2;
      timed('key', ev, function () {
        if (ev.key === 'ArrowLeft') self.panBy(step, 0);
        else if (ev.key === 'ArrowRight') self.panBy(-step, 0);
        else if (ev.key === 'ArrowUp') self.panBy(0, step);
        else if (ev.key === 'ArrowDown') self.panBy(0, -step);
        else if (ev.key === '+' || ev.key === '=') self.zoomAt(cx, cy, 0.7);
        else if (ev.key === '-' || ev.key === '_') self.zoomAt(cx, cy, 1 / 0.7);
        else if (ev.key === '0') self.view = Object.assign({}, self.home);
        else done = false;
        if (done) self.draw();
      }, !done);
      if (done) ev.preventDefault();
    });
    function centerZoom(id, factor, type) {
      byId(id).addEventListener('click', function (ev) {
        if (!self.view) return;
        timed(type, ev, function () {
          if (factor === 0) self.view = Object.assign({}, self.home);
          else self.zoomAt(self.margin.l + (self.w - self.margin.l - self.margin.r) / 2, self.margin.t + (self.h - self.margin.t - self.margin.b) / 2, factor);
          self.draw();
        });
      });
    }
    centerZoom('zoom-in', 0.6, 'button-zoom-in');
    centerZoom('zoom-out', 1 / 0.6, 'button-zoom-out');
    centerZoom('zoom-reset', 0, 'button-reset');
    if (window.ResizeObserver) new ResizeObserver(function () { if (self.view) self.draw(); }).observe(c);
  };

  /* ---- timing ---------------------------------------------------------------------------- */
  function timed(type, ev, fn, skip) {
    /* ms: from the input event's timeStamp to the end of the redraw (SR-09 (b)); handler_ms: the
     * work inside the handler only, so that queueing before the handler can be told apart. */
    var start = ev && typeof ev.timeStamp === 'number' ? ev.timeStamp : performance.now();
    var handlerStart = performance.now();
    fn();
    if (skip) return;
    var end = performance.now();
    PERF.interactions.push({ type: type, start: start, end: end, ms: end - start,
      handler_ms: end - handlerStart, visibility: document.visibilityState });
    if (PERF.interactions.length > 200) PERF.interactions.shift();
    reportPerf();
  }
  function reportPerf() {
    var box = byId('scatter-perf');
    if (!box) return;
    var parts = [];
    if (PERF.firstDraw) parts.push('首次繪製：' + PERF.firstDraw.ms.toFixed(0) + ' ms（自 navigation start，' + nf.format(PERF.firstDraw.nPoints) + ' 筆）');
    var last = PERF.interactions[PERF.interactions.length - 1];
    if (last) parts.push('最近一次互動（' + last.type + '）：' + last.ms.toFixed(1) + ' ms');
    box.textContent = parts.join('；');
  }

  /* ---- mobile navigation ----------------------------------------------------------------- */
  function bindNav() {
    var btn = byId('nav-toggle'), nav = byId('topnav');
    function set(open) { btn.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); }
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      set(open);
      if (open) { var first = nav.querySelector('a'); if (first) first.focus(); }
    });
    nav.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') { set(false); btn.focus(); } });
    nav.addEventListener('click', function (ev) { if (ev.target.tagName === 'A') set(false); });
    nav.addEventListener('focusout', function (ev) { if (!nav.contains(ev.relatedTarget) && ev.relatedTarget !== btn) set(false); });
  }

  /* ---- update ----------------------------------------------------------------------------- */
  function update() {
    var entry = entryFor(state.method, state.k);
    renderControls();
    renderSelected(entry);
    renderKpi(entry);
    renderFit(entry);
    renderPredictor(entry);
    renderTest(entry);
  }

  function init() {
    if (window.Chart && window.Chart.version) setText('chartjs-version', 'Chart.js ' + window.Chart.version + '（本機打包）');
    bindNav();
    if (!MD || !MD.meta) { showError('找不到 model_data：請先執行 hw2.ipynb 產生 assets/model_data.js。'); return; }
    if (!Core) { showError('找不到 assets/hw2core.js。'); return; }
    if (MD.meta.fixture) showError('目前載入的是測試用 synthetic fixture 資料，不是正式結果。');
    renderOverview(MD.meta, MD.preprocess);
    CAT = catalogue();
    if (!CAT.allin) { showError('model_data 尚未包含 All-in baseline（baselines.allin）。'); return; }
    state.method = 'allin';
    state.k = defaultK('allin');
    scatter = new Scatter(byId('scatter-canvas'), byId('scatter-tip'));
    update();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
