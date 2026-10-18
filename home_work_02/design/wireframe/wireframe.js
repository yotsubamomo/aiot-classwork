/* HW2 Dashboard Wireframe — 互動（示意）
 * 只讀取 window.MOCK；所有數字都是模擬數值。
 */
(function () {
  'use strict';
  const M = window.MOCK;
  const $ = (s, el) => (el || document).querySelector(s);
  const el = (tag, attrs, html) => {
    const n = document.createElement(tag);
    if (attrs) Object.entries(attrs).forEach(([k, v]) => { if (v === false || v == null) return; if (k === 'class') n.className = v; else n.setAttribute(k, v); });
    if (html != null) n.innerHTML = html;
    return n;
  };
  const fmtUSD = v => '$' + Math.round(v).toLocaleString('en-US');
  const fmtUSDk = v => '$' + (v / 1000).toFixed(0) + 'k';
  const fmtPct = (v, d) => (v * 100).toFixed(d == null ? 1 : d) + '%';
  const groupLabel = id => M.GROUPS.find(g => g.id === id).label;
  const METHOD_SERIES_COLOR = { forward: 'var(--s-forward)', backward: 'var(--s-backward)', rfe: 'var(--s-rfe)', lasso: 'var(--s-lasso)', allin: 'var(--s-allin)' };

  const state = { method: M.OVERALL.method, k: M.OVERALL.k, compareAll: false, metric: 'rmse' };

  function currentModel() { return M.MODELS[state.method]; }
  function currentItem() { return currentModel().items[state.k]; }
  function isWinner() { return currentModel().winnerK === state.k; }
  function isOverall() { return M.OVERALL.method === state.method && M.OVERALL.k === state.k; }
  function testKeyFor(methodId) { const m = M.MODELS[methodId]; return methodId + ':' + m.winnerK; }

  // ---------- A. meta ----------
  (function renderMeta() {
    $('#meta-dataset').textContent = M.meta.dataset;
    $('#meta-rows').textContent = M.meta.rows.toLocaleString();
    $('#meta-houses').textContent = M.meta.houses.toLocaleString();
    $('#meta-repeat').textContent = M.meta.repeat;
    $('#meta-sf').textContent = M.meta.sourceFeatures;
    $('#meta-groups').textContent = M.meta.groups;
  })();

  // ---------- B. controls ----------
  function renderMethodSeg() {
    const seg = $('#method-seg'); seg.innerHTML = '';
    M.METHODS.forEach(m => {
      const model = M.MODELS[m.id];
      const b = el('button', { type: 'button', class: 'seg__btn', 'aria-pressed': String(state.method === m.id), 'data-method': m.id });
      b.innerHTML = `<span class="dot" style="background:${METHOD_SERIES_COLOR[m.id]}"></span><span>${m.name}</span><span class="meta">${m.kind === 'single' ? 'k = 18 固定' : 'winner k = ' + model.winnerK}</span>`;
      b.addEventListener('click', () => { state.method = m.id; state.k = m.kind === 'single' ? 18 : (state.k > 0 ? state.k : model.winnerK); if (m.kind === 'single') state.k = 18; update(); });
      seg.appendChild(b);
    });
  }
  function renderKGrid() {
    const grid = $('#k-grid'); grid.innerHTML = '';
    const model = currentModel();
    const single = model.kind === 'single';
    const legend = $('#k-legend');
    if (single) {
      // UI 決策 4：All-in 只顯示固定 k = 18，不顯示 1–17 的停用按鈕
      grid.classList.add('kgrid--fixed');
      grid.innerHTML = `<div class="kfixed" role="status"><span class="kfixed__k num">k = 18</span><span class="kfixed__txt">All-in baseline 使用全部 18 個 feature group，沒有 k 路徑，k 固定。</span></div>`;
      legend.hidden = true;
      $('#k-help').textContent = '要瀏覽不同 k，請改選四種有 k 路徑的方法。';
      return;
    }
    grid.classList.remove('kgrid--fixed');
    legend.hidden = false;
    for (let k = 1; k <= 18; k++) {
      const it = model.items[k];
      const b = el('button', { type: 'button', class: 'kbtn num', 'aria-pressed': String(state.k === k) });
      b.textContent = k;
      if (model.winnerK === k) { b.classList.add('is-winner'); b.setAttribute('aria-label', `k = ${k}（CV winner）`); }
      if (it.status === 'invalid') { b.classList.add('is-invalid'); b.setAttribute('aria-label', `k = ${k}（invalid：canonical fit 秩不足）`); }
      b.addEventListener('click', () => { state.k = k; update(); });
      grid.appendChild(b);
    }
    $('#k-help').textContent = `${model.name} 的 CV winner 為 k = ${model.winnerK}（以 CV RMSE 最小者決定）。`;
  }
  function renderSelected() {
    const m = currentModel(), it = currentItem();
    const tags = [];
    if (it.status === 'invalid') tags.push('<span class="tag tag--invalid">invalid · canonical_rank_deficient</span>');
    if (isWinner()) tags.push('<span class="tag tag--winner">該方法 CV winner</span>');
    if (isOverall()) tags.push('<span class="tag tag--overall">整體 CV winner</span>');
    $('#selected-model').innerHTML = `<span class="muted small">目前選取</span><strong>${m.name} · k = ${state.k}</strong><span class="small muted">canonical subset：${it.groups.map(groupLabel).join('、')}</span>${it.status === 'valid' && m.kind === 'path' ? `<span class="small muted">各 fold 子集與 canonical 相同：${it.foldsAgree}/5</span>` : ''}<div class="legend">${tags.join('')}</div>`;
  }
  $('#compare-all').addEventListener('click', e => { state.compareAll = !state.compareAll; e.currentTarget.setAttribute('aria-pressed', String(state.compareAll)); update(); });
  $('#metric-select').addEventListener('change', e => { state.metric = e.target.value; renderKChart(); });

  // ---------- C. KPI + chart ----------
  function kpi(label, value, sub, tag) {
    return `<div class="kpi"><div class="kpi__label"><span>${label}</span>${tag ? `<span class="tag ${tag.cls}">${tag.txt}</span>` : ''}</div><div class="kpi__value">${value}</div><div class="kpi__sub">${sub || ''}</div></div>`;
  }
  function renderCvKpi() {
    const it = currentItem(); const box = $('#kpi-cv');
    if (it.status === 'invalid') {
      box.innerHTML = `<div class="kpi" style="grid-column:1/-1"><div class="kpi__label"><span class="tag tag--invalid">invalid 候選</span></div><div class="kpi__value" style="font-size:1.125rem">此 (方法, k) 的 canonical subset 在整個 training set 上秩不足</div><div class="kpi__sub">沒有 fit、不提供即時預測、不參與 CV winner。原因：<code>canonical_rank_deficient</code>。其他有效候選的比較照常進行。</div></div>`;
      return;
    }
    const c = it.cv;
    box.innerHTML = [
      kpi('CV RMSE', fmtUSD(c.rmse), '5 折平均 ± 約 $2,100（示意）'),
      kpi('CV MAE', fmtUSD(c.mae), 'USD'),
      kpi('CV MSE', (c.mse / 1e9).toFixed(2) + ' ×10⁹', 'USD²'),
      kpi('CV R²（USD 尺度）', c.r2.toFixed(3), '以回轉後預測計算'),
      kpi('Adjusted R²（log 尺度）', c.adj_r2_log.toFixed(3), `全訓練集擬合・rank = ${c.rank}`, { cls: 'tag--fit', txt: 'fit' }),
    ].join('');
  }

  function metricValue(it, metric) {
    if (!it || it.status !== 'valid') return null;
    return metric === 'r2' ? it.cv.r2 : it.cv[metric];
  }
  function renderKChart() {
    const W = 860, H = 360, pad = { l: 64, r: 20, t: 16, b: 40 };
    const metric = state.metric;
    const pathMethods = M.METHODS.filter(m => m.kind === 'path');
    let vals = [];
    pathMethods.forEach(m => { for (let k = 1; k <= 18; k++) { const v = metricValue(M.MODELS[m.id].items[k], metric); if (v != null) vals.push(v); } });
    const refs = [
      { id: 'allin', label: 'All-in', v: metricValue(M.MODELS.allin.items[18], metric), color: 'var(--s-allin)', dash: '6 4' },
      { id: 'ridge', label: 'Ridge（對照）', v: metric === 'rmse' ? M.BASELINES.ridge.cvRmse : (metric === 'mae' ? M.BASELINES.ridge.cvRmse * 0.68 : 1 - Math.pow(M.BASELINES.ridge.cvRmse / 367000, 2)), color: 'var(--s-ridge)', dash: '2 4' },
      { id: 'lasso_ref', label: 'Lasso（對照）', v: metric === 'rmse' ? M.BASELINES.lasso_ref.cvRmse : (metric === 'mae' ? M.BASELINES.lasso_ref.cvRmse * 0.68 : 1 - Math.pow(M.BASELINES.lasso_ref.cvRmse / 367000, 2)), color: 'var(--s-lassoref)', dash: '2 4' },
    ];
    refs.forEach(r => vals.push(r.v));
    let lo = Math.min(...vals), hi = Math.max(...vals);
    const span = hi - lo || 1; lo -= span * 0.08; hi += span * 0.08;
    const x = k => pad.l + (k - 1) / 17 * (W - pad.l - pad.r);
    const y = v => pad.t + (hi - v) / (hi - lo) * (H - pad.t - pad.b);
    const fmtY = v => metric === 'r2' ? v.toFixed(3) : fmtUSDk(v);
    let s = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">`;
    // grid + axes
    for (let i = 0; i <= 5; i++) { const v = lo + (hi - lo) * i / 5; s += `<line class="gridline" x1="${pad.l}" x2="${W - pad.r}" y1="${y(v)}" y2="${y(v)}"/><text class="axis" x="${pad.l - 8}" y="${y(v) + 4}" text-anchor="end" style="font-size:11px;fill:var(--c-muted)">${fmtY(v)}</text>`; }
    for (let k = 1; k <= 18; k++) s += `<text x="${x(k)}" y="${H - 14}" text-anchor="middle" style="font-size:11px;fill:var(--c-muted)">${k}</text>`;
    s += `<text x="${(pad.l + W - pad.r) / 2}" y="${H - 2}" text-anchor="middle" style="font-size:11px;fill:var(--c-muted)">k（source feature groups）</text>`;
    // ref lines
    refs.forEach(r => { s += `<line class="refline" x1="${pad.l}" x2="${W - pad.r}" y1="${y(r.v)}" y2="${y(r.v)}" stroke="${r.color}" stroke-dasharray="${r.dash}"/><text x="${W - pad.r - 4}" y="${y(r.v) - 4}" text-anchor="end" style="font-size:10px;fill:${r.color}">${r.label}</text>`; });
    // series
    pathMethods.forEach(m => {
      const model = M.MODELS[m.id];
      const dim = !state.compareAll && state.method !== m.id && state.method !== 'allin';
      let d = '', pen = false;
      for (let k = 1; k <= 18; k++) { const v = metricValue(model.items[k], metric); if (v == null) { pen = false; continue; } d += (pen ? 'L' : 'M') + x(k) + ' ' + y(v) + ' '; pen = true; }
      s += `<path class="series${dim ? ' is-dim' : ''}" d="${d}" stroke="${METHOD_SERIES_COLOR[m.id]}"/>`;
      // markers
      for (let k = 1; k <= 18; k++) {
        const it = model.items[k];
        if (it.status === 'invalid') { const yy = y(lo + (hi - lo) * 0.5); s += `<g class="marker-invalid${dim ? ' is-dim' : ''}" opacity="${dim ? 0.3 : 1}"><line x1="${x(k) - 5}" y1="${yy - 5}" x2="${x(k) + 5}" y2="${yy + 5}"/><line x1="${x(k) - 5}" y1="${yy + 5}" x2="${x(k) + 5}" y2="${yy - 5}"/></g>`; continue; }
        if (model.winnerK === k) s += `<circle class="marker-winner" cx="${x(k)}" cy="${y(metricValue(it, metric))}" r="6" stroke="${METHOD_SERIES_COLOR[m.id]}" opacity="${dim ? 0.3 : 1}"/>`;
      }
    });
    // selected marker
    const sel = currentItem();
    if (state.method !== 'allin' && sel.status === 'valid') s += `<circle class="marker-sel" cx="${x(state.k)}" cy="${y(metricValue(sel, metric))}" r="10"/>`;
    s += '</svg>';
    $('#kchart').innerHTML = s;
    // legend
    const lg = $('#kchart-legend'); lg.innerHTML = '';
    pathMethods.forEach(m => { const dim = !state.compareAll && state.method !== m.id && state.method !== 'allin'; lg.innerHTML += `<span class="legend__item${dim ? ' is-dim' : ''}" style="color:${METHOD_SERIES_COLOR[m.id]}"><span class="legend__line"></span><span style="color:var(--c-ink-2)">${m.name}</span></span>`; });
    refs.forEach(r => { lg.innerHTML += `<span class="legend__item" style="color:${r.color}"><span class="legend__line ${r.id === 'allin' ? 'legend__line--dash' : 'legend__line--dot'}"></span><span style="color:var(--c-ink-2)">${r.label}</span></span>`; });
    lg.innerHTML += `<span class="legend__item"><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="5" fill="#fff" stroke="var(--c-ink-2)" stroke-width="2"/></svg>CV winner</span><span class="legend__item" style="color:var(--c-danger)"><svg width="16" height="16" viewBox="0 0 16 16" stroke="currentColor" stroke-width="2"><path d="M3 3l10 10M13 3L3 13"/></svg><span style="color:var(--c-ink-2)">invalid 候選</span></span>`;
  }

  function renderCompareTable() {
    const card = $('#compare-table-card'); card.hidden = !state.compareAll;
    if (!state.compareAll) return;
    const rows = M.METHODS.map(m => { const model = M.MODELS[m.id]; const it = model.items[model.winnerK]; const t = M.TEST[m.id + ':' + model.winnerK]; return { name: m.name, k: model.winnerK, cv: it.cv, test: t, overall: isOverallKey(m.id, model.winnerK) }; });
    let h = `<thead><tr><th>方法</th><th class="num">CV winner k</th><th class="num">CV RMSE</th><th class="num">CV MAE</th><th class="num">CV R²（USD）</th><th class="num">Adj R²（log）</th><th class="num">Test RMSE</th><th>備註</th></tr></thead><tbody>`;
    rows.forEach(r => { h += `<tr class="${r.overall ? 'is-winner' : ''}"><td>${r.name}</td><td class="num">${r.k}</td><td class="num">${fmtUSD(r.cv.rmse)}</td><td class="num">${fmtUSD(r.cv.mae)}</td><td class="num">${r.cv.r2.toFixed(3)}</td><td class="num">${r.cv.adj_r2_log.toFixed(3)}</td><td class="num">${fmtUSD(r.test.rmse)}</td><td>${r.overall ? '<span class="tag tag--overall">整體 CV winner</span>' : ''}</td></tr>`; });
    [['ridge', M.BASELINES.ridge], ['lasso_ref', M.BASELINES.lasso_ref]].forEach(([id, b]) => { h += `<tr><td>${b.name}</td><td class="num">—</td><td class="num">${fmtUSD(b.cvRmse)}</td><td class="num">${fmtUSD(b.cvRmse * 0.68)}</td><td class="num">${(1 - Math.pow(b.cvRmse / 367000, 2)).toFixed(3)}</td><td class="num">不適用</td><td class="num">${fmtUSD(M.TEST[id].rmse)}</td><td><span class="tag tag--fit">metric only</span>α = ${b.alpha}</td></tr>`; });
    h += `<tr><td>${M.BASELINES.pvalue.name}</td><td class="num">${M.BASELINES.pvalue.groups}</td><td class="num">${fmtUSD(M.BASELINES.pvalue.cvRmse)}</td><td class="num">${fmtUSD(M.BASELINES.pvalue.cvRmse * 0.68)}</td><td class="num">${(1 - Math.pow(M.BASELINES.pvalue.cvRmse / 367000, 2)).toFixed(3)}</td><td class="num">—</td><td class="num">未評估</td><td>講義方法對照，不進 winner</td></tr></tbody>`;
    $('#compare-table').innerHTML = h;
  }
  function isOverallKey(method, k) { return M.OVERALL.method === method && M.OVERALL.k === k; }

  // ---------- D. predictor ----------
  const predValues = {};
  function renderPredictor() {
    const it = currentItem(); const box = $('#pred-fields'); box.innerHTML = '';
    $('#pred-model').textContent = `${currentModel().name} · k = ${state.k}`;
    if (it.status === 'invalid') {
      $('#pred-intro').textContent = '此 (方法, k) 為 invalid 候選，沒有可用的擬合模型，即時預測不可用。請選擇其他 k。';
      $('#pred-price').textContent = '—'; $('#pred-pi').textContent = '—'; $('#pred-status').innerHTML = '<span class="tag tag--invalid">invalid 候選：無預測</span>';
      return;
    }
    $('#pred-intro').textContent = `只顯示目前模型 canonical subset 用到的 ${it.groups.length} 個 source feature（原始值）；預設為 training 中位數，範圍為 training min–max。頁面依 preprocess 規則重做日期天數、整修旗標與 one-hot。`;
    it.groups.forEach(gid => {
      const g = M.GROUPS.find(x => x.id === gid);
      const f = el('div', { class: 'field', 'data-group': gid });
      const id = 'f-' + gid;
      const label = el('label', { for: id }, `${g.label}${g.unit ? ` <span class="muted small">(${g.unit})</span>` : ''}`);
      f.appendChild(label);
      let input;
      if (g.type === 'number' || g.type === 'date') {
        input = el('input', { class: 'input', id, type: g.type, min: g.min, max: g.max, step: g.step || 'any', value: predValues[gid] != null ? predValues[gid] : g.def, inputmode: 'decimal' });
        f.appendChild(input);
        f.appendChild(el('div', { class: 'help' }, g.type === 'date' ? `training 範圍 ${g.min} ～ ${g.max}` : `training 範圍 ${Number(g.min).toLocaleString()} ～ ${Number(g.max).toLocaleString()}（中位數 ${Number(g.def).toLocaleString()}）`));
      } else if (g.type === 'select') {
        input = el('select', { class: 'input', id });
        g.options.forEach(o => input.appendChild(el('option', { value: o, selected: (predValues[gid] != null ? predValues[gid] : g.def) === o }, o)));
        f.appendChild(input);
      } else if (g.type === 'renovated') {
        const wrap = el('div', { class: 'renov' });
        const chk = el('label', { class: 'check' }); const cb = el('input', { type: 'checkbox', id: id + '-none' }); cb.checked = (predValues[gid] == null || predValues[gid] === 0); chk.appendChild(cb); chk.appendChild(document.createTextNode('未整修（旗標 = 0，有效年份 = 建造年）'));
        const row = el('div', { class: 'renov__row' });
        input = el('input', { class: 'input', id, type: 'number', min: g.min, max: g.max, step: 1, value: predValues[gid] || 2000, 'aria-label': '整修年份' }); input.disabled = cb.checked;
        row.appendChild(input);
        wrap.appendChild(chk); wrap.appendChild(row); f.appendChild(wrap);
        cb.addEventListener('change', () => { input.disabled = cb.checked; predValues[gid] = cb.checked ? 0 : Number(input.value); recompute(); });
      } else if (g.type === 'zipcode') {
        input = el('select', { class: 'input', id });
        M.ZIPCODES.forEach(z => input.appendChild(el('option', { value: z, selected: (predValues[gid] || g.def) === z }, z)));
        input.appendChild(el('option', { value: M.UNSEEN_ZIP, selected: predValues[gid] === M.UNSEEN_ZIP }, `${M.UNSEEN_ZIP}（示意：不在模型訓練類別）`));
        f.appendChild(input);
        f.appendChild(el('div', { class: 'help' }, '下拉只列出目前模型 fit 的類別（基準類別：98001）。'));
      }
      const warnBox = el('div', { class: 'warnbox', id: id + '-warn', role: 'status' });
      f.appendChild(warnBox);
      input.setAttribute('aria-describedby', id + '-warn');
      input.addEventListener('input', () => { predValues[gid] = g.type === 'number' || g.type === 'renovated' ? Number(input.value) : input.value; recompute(); });
      input.addEventListener('change', () => { predValues[gid] = g.type === 'number' || g.type === 'renovated' ? Number(input.value) : input.value; recompute(); });
      box.appendChild(f);
    });
    recompute();
  }
  const WARN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>';
  function recompute() {
    const it = currentItem(); if (it.status !== 'valid') return;
    let logp = 12.45, warnings = [];
    it.groups.forEach(gid => {
      const g = M.GROUPS.find(x => x.id === gid);
      const f = $(`[data-group="${gid}"]`); const wb = $('#f-' + gid + '-warn');
      let v = predValues[gid] != null ? predValues[gid] : g.def;
      let msg = '';
      if (g.type === 'number') {
        v = Number(v);
        if (!Number.isFinite(v)) { msg = '請輸入數值'; }
        else if (v < g.min || v > g.max) msg = `超出 training 範圍（${Number(g.min).toLocaleString()} ～ ${Number(g.max).toLocaleString()}），仍以外推計算。`;
        const span = (g.max - g.min) || 1; const z = (v - g.def) / span;
        const w = { sqft_living: 1.4, grade: 1.2, lat: 1.6, sqft_above: 0.5, sqft_living15: 0.6, bathrooms: 0.5, yr_built: -0.25, bedrooms: -0.15, long: -0.3, sqft_lot: 0.1, sqft_lot15: 0.05 }[gid] || 0.05;
        logp += w * z * 1.3;
      } else if (g.type === 'date') {
        const d = new Date(v), lo = new Date(g.min), hi = new Date(g.max);
        if (isNaN(d)) msg = '請輸入日期'; else if (d < lo || d > hi) msg = `超出 training 期間（${g.min} ～ ${g.max}），屬外推。`;
        if (!isNaN(d)) logp += 0.04 * ((d - lo) / (hi - lo) - 0.5);
      } else if (g.type === 'select') {
        const idx = g.options.indexOf(String(v)); const w = { waterfront: 0.45, view: 0.07, condition: 0.05, floors: 0.03 }[gid] || 0;
        logp += w * (idx - g.options.indexOf(g.def));
      } else if (g.type === 'renovated') {
        if (v > 0) { logp += 0.06; if (v < g.min || v > g.max) msg = `整修年超出 training 範圍（${g.min} ～ ${g.max}）。`; }
      } else if (g.type === 'zipcode') {
        if (v === M.UNSEEN_ZIP) { msg = '此 zipcode 不在模型的訓練類別中，已以基準類別計算。'; }
        else { const idx = M.ZIPCODES.indexOf(v); logp += ((idx * 37) % 23 - 11) / 60; }
      }
      if (msg) { warnings.push(`${g.label}：${msg}`); f.classList.add('is-warn'); wb.innerHTML = `<div class="warn">${WARN_ICON}<span>${msg}</span></div>`; }
      else { f.classList.remove('is-warn'); wb.innerHTML = ''; }
    });
    const pred = Math.exp(logp);
    const hw = 0.62 - state.k * 0.006;
    const lower = pred * Math.exp(-hw), upper = pred * Math.exp(hw);
    $('#pred-price').textContent = fmtUSD(pred);
    $('#pred-pi').textContent = `${fmtUSD(lower)} ～ ${fmtUSD(upper)}`;
    // bar on log scale within [50k, 8M]
    const L = Math.log(50000), R = Math.log(8000000);
    const pct = x => Math.max(0, Math.min(100, (Math.log(x) - L) / (R - L) * 100));
    $('#pred-bar-span').style.left = pct(lower) + '%'; $('#pred-bar-span').style.width = (pct(upper) - pct(lower)) + '%'; $('#pred-bar-pt').style.left = `calc(${pct(pred)}% - 1px)`;
    const st = $('#pred-status');
    st.innerHTML = warnings.length ? warnings.map(w => `<div class="warn">${WARN_ICON}<span>${w}</span></div>`).join('') : '<span class="tag tag--cv">輸入皆在 training 範圍內</span>';
    st.innerHTML += '<span class="small muted">模擬數值：預測與區間由示意公式產生，不代表模型輸出。</span>';
  }

  // ---------- E. test ----------
  let scatterState = { pts: [], zoom: 1, cx: 0, cy: 0, dragging: false, last: null };
  function renderTest() {
    const model = currentModel();
    const key = testKeyFor(state.method);
    const t = M.TEST[key];
    const shownIsSelected = model.winnerK === state.k;
    $('#test-model').textContent = `${model.name} · k = ${t.k}`;
    const wt = $('#test-winner-tag'); wt.textContent = isOverallKey(t.method, t.k) ? '整體 CV winner' : '該方法 CV winner'; wt.className = 'tag ' + (isOverallKey(t.method, t.k) ? 'tag--overall' : 'tag--winner');
    const notice = $('#test-notice');
    if (!shownIsSelected) {
      notice.hidden = false;
      $('#test-notice-text').innerHTML = `<strong>目前選取的 ${model.name} · k = ${state.k} 不是 CV winner，未在 test 上評估。</strong> 本區塊展示的是 ${model.name} 的 CV winner（k = ${t.k}）的 test 結果。Test 只對各方法 CV winner、All-in 與整體 CV winner 各評估一次；切換不會觸發新的評估。`;
    } else notice.hidden = true;
    $('#kpi-test').innerHTML = [
      kpi('Test RMSE', fmtUSD(t.rmse), 'USD・一次評估', { cls: 'tag--test', txt: 'Test' }),
      kpi('Test MAE', fmtUSD(t.mae), 'USD', { cls: 'tag--test', txt: 'Test' }),
      kpi('Test MSE', (t.mse / 1e9).toFixed(2) + ' ×10⁹', 'USD²', { cls: 'tag--test', txt: 'Test' }),
      kpi('Test R²（USD 尺度）', t.r2.toFixed(3), '以回轉後預測計算', { cls: 'tag--test', txt: 'Test' }),
    ].join('');
    $('#covstats').innerHTML = [
      kpi('經驗涵蓋率', fmtPct(t.coverage), '名目 95%・不保證'),
      kpi('涵蓋筆數', `${t.covered.toLocaleString()} / ${t.nTest.toLocaleString()}`, 'covered / n_test'),
      kpi('n_test', t.nTest.toLocaleString(), `${t.houses.toLocaleString()} 棟房屋・${t.repeatSales} 筆重複交易`),
      kpi('平均 PI 寬度', fmtUSD(t.meanWidth), 'USD・upper − lower 的平均'),
      kpi('不確定性（二項近似）', '± ' + fmtPct(t.uncertainty, 2), '1.96·√(p(1−p)/n)・假設獨立'),
    ].join('');
    scatterState.pts = t.pts; scatterState.zoom = 1; scatterState.cx = 0; scatterState.cy = 0;
    drawScatter(true);
    renderResidTable(t);
  }

  const canvas = $('#scatter-canvas'); const ctx = canvas.getContext('2d');
  const LOGMIN = Math.log10(60000), LOGMAX = Math.log10(9000000);
  function viewport() {
    const span = (LOGMAX - LOGMIN) / scatterState.zoom;
    const mid = (LOGMIN + LOGMAX) / 2;
    const x0 = mid + scatterState.cx - span / 2, y0 = mid + scatterState.cy - span / 2;
    return { x0, x1: x0 + span, y0, y1: y0 + span };
  }
  function drawScatter(measure) {
    const t0 = performance.now();
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    if (canvas.width !== Math.round(rect.width * dpr)) { canvas.width = Math.round(rect.width * dpr); canvas.height = Math.round(rect.height * dpr); }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = rect.width, H = rect.height, pad = { l: 56, r: 12, t: 10, b: 36 };
    const v = viewport();
    const sx = lx => pad.l + (lx - v.x0) / (v.x1 - v.x0) * (W - pad.l - pad.r);
    const sy = ly => H - pad.b - (ly - v.y0) / (v.y1 - v.y0) * (H - pad.t - pad.b);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
    // grid at decades & 2,5 steps
    ctx.font = '11px system-ui, "Noto Sans TC", sans-serif'; ctx.fillStyle = '#475569'; ctx.strokeStyle = '#E6ECF4'; ctx.lineWidth = 1;
    const ticks = [];
    for (let e = 4; e <= 7; e++) [1, 2, 5].forEach(m => { const val = m * Math.pow(10, e); const l = Math.log10(val); if (l >= LOGMIN - 0.3 && l <= LOGMAX + 0.3) ticks.push({ val, l }); });
    ticks.forEach(tk => {
      const X = sx(tk.l), Y = sy(tk.l);
      if (X >= pad.l && X <= W - pad.r) { ctx.beginPath(); ctx.moveTo(X, pad.t); ctx.lineTo(X, H - pad.b); ctx.stroke(); ctx.textAlign = 'center'; ctx.fillText(fmtUSDk(tk.val), X, H - pad.b + 16); }
      if (Y >= pad.t && Y <= H - pad.b) { ctx.beginPath(); ctx.moveTo(pad.l, Y); ctx.lineTo(W - pad.r, Y); ctx.stroke(); ctx.textAlign = 'right'; ctx.fillText(fmtUSDk(tk.val), pad.l - 6, Y + 4); }
    });
    ctx.textAlign = 'center'; ctx.fillText('預測價格（USD，log）', (pad.l + W - pad.r) / 2, H - 4);
    ctx.save(); ctx.translate(12, (pad.t + H - pad.b) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText('實際價格（USD，log）', 0, 0); ctx.restore();
    // clip plot area
    ctx.save(); ctx.beginPath(); ctx.rect(pad.l, pad.t, W - pad.l - pad.r, H - pad.t - pad.b); ctx.clip();
    // PI segments
    const pts = scatterState.pts;
    const segAlpha = Math.min(0.45, 0.07 * scatterState.zoom);
    ctx.lineWidth = 1;
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i]; const X = sx(Math.log10(p.pred));
      if (X < pad.l - 2 || X > W - pad.r + 2) continue;
      ctx.strokeStyle = p.covered ? `rgba(30,64,175,${segAlpha})` : `rgba(180,83,9,${segAlpha + 0.1})`;
      ctx.beginPath(); ctx.moveTo(X, sy(Math.log10(p.lower))); ctx.lineTo(X, sy(Math.log10(p.upper))); ctx.stroke();
    }
    // y = x
    ctx.strokeStyle = '#0F172A'; ctx.lineWidth = 1.25; ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(sx(v.x0), sy(v.x0)); ctx.lineTo(sx(v.x1), sy(v.x1)); ctx.stroke(); ctx.setLineDash([]);
    // points
    const r = Math.min(3.2, 1.5 + 0.35 * scatterState.zoom);
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i]; const X = sx(Math.log10(p.pred)), Y = sy(Math.log10(p.actual));
      if (X < pad.l || X > W - pad.r || Y < pad.t || Y > H - pad.b) continue;
      ctx.fillStyle = p.covered ? 'rgba(30,64,175,0.55)' : 'rgba(180,83,9,0.85)';
      ctx.beginPath(); ctx.arc(X, Y, r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
    // frame
    ctx.strokeStyle = '#D9E2EF'; ctx.strokeRect(pad.l, pad.t, W - pad.l - pad.r, H - pad.t - pad.b);
    scatterState.sx = sx; scatterState.sy = sy; scatterState.pad = pad; scatterState.W = W; scatterState.H = H;
    if (measure) $('#scatter-perf').textContent = `首次繪製 ${Math.round(performance.now() - t0)} ms（本機量測，${pts.length.toLocaleString()} 筆）`;
  }
  function zoomAt(factor, px, py) {
    const v = viewport(); const { sx, sy } = scatterState;
    // keep the log coords under cursor fixed
    const lx = px != null ? v.x0 + (px - scatterState.pad.l) / (scatterState.W - scatterState.pad.l - scatterState.pad.r) * (v.x1 - v.x0) : (v.x0 + v.x1) / 2;
    const ly = py != null ? v.y0 + (scatterState.H - scatterState.pad.b - py) / (scatterState.H - scatterState.pad.t - scatterState.pad.b) * (v.y1 - v.y0) : (v.y0 + v.y1) / 2;
    const newZoom = Math.max(1, Math.min(40, scatterState.zoom * factor));
    const span = (LOGMAX - LOGMIN) / newZoom; const mid = (LOGMIN + LOGMAX) / 2;
    const fx = (lx - v.x0) / (v.x1 - v.x0), fy = (ly - v.y0) / (v.y1 - v.y0);
    scatterState.zoom = newZoom;
    scatterState.cx = lx - fx * span + span / 2 - mid;
    scatterState.cy = ly - fy * span + span / 2 - mid;
    if (newZoom === 1) { scatterState.cx = 0; scatterState.cy = 0; }
    drawScatter(false);
  }
  canvas.addEventListener('wheel', e => { e.preventDefault(); const rect = canvas.getBoundingClientRect(); zoomAt(e.deltaY < 0 ? 1.25 : 0.8, e.clientX - rect.left, e.clientY - rect.top); }, { passive: false });
  canvas.addEventListener('pointerdown', e => { scatterState.dragging = true; scatterState.last = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointerup', () => { scatterState.dragging = false; });
  canvas.addEventListener('pointermove', e => {
    const rect = canvas.getBoundingClientRect(); const px = e.clientX - rect.left, py = e.clientY - rect.top;
    if (scatterState.dragging && scatterState.zoom > 1) {
      const v = viewport(); const dx = (e.clientX - scatterState.last[0]) / (scatterState.W - scatterState.pad.l - scatterState.pad.r) * (v.x1 - v.x0);
      const dy = (e.clientY - scatterState.last[1]) / (scatterState.H - scatterState.pad.t - scatterState.pad.b) * (v.y1 - v.y0);
      scatterState.cx -= dx; scatterState.cy += dy; scatterState.last = [e.clientX, e.clientY]; drawScatter(false); return;
    }
    // hover nearest
    const { sx, sy } = scatterState; let best = null, bd = 100;
    const pts = scatterState.pts;
    for (let i = 0; i < pts.length; i++) { const p = pts[i]; const X = sx(Math.log10(p.pred)), Y = sy(Math.log10(p.actual)); const d = (X - px) * (X - px) + (Y - py) * (Y - py); if (d < bd) { bd = d; best = p; } }
    const tip = $('#scatter-tip');
    if (best) { tip.hidden = false; tip.style.left = px + 'px'; tip.style.top = py + 'px'; tip.innerHTML = `<div>房屋 id ${best.id}（示意）</div><div>實際 ${fmtUSD(best.actual)}</div><div>預測 ${fmtUSD(best.pred)}</div><div>PI ${fmtUSD(best.lower)} ～ ${fmtUSD(best.upper)}</div><div>${best.covered ? '✓ 落入 PI' : '✕ 未落入 PI'}</div>`; }
    else tip.hidden = true;
  });
  canvas.addEventListener('pointerleave', () => { $('#scatter-tip').hidden = true; scatterState.dragging = false; });
  $('#zoom-in').addEventListener('click', () => zoomAt(1.5));
  $('#zoom-out').addEventListener('click', () => zoomAt(1 / 1.5));
  $('#zoom-reset').addEventListener('click', () => { scatterState.zoom = 1; scatterState.cx = 0; scatterState.cy = 0; drawScatter(false); });
  window.addEventListener('resize', () => drawScatter(false));

  // ---------- 選配表 ----------
  function renderCoefTable() {
    const it = currentItem(); const tb = $('#coef-table');
    if (it.status !== 'valid') { tb.innerHTML = '<tbody><tr><td>invalid 候選，沒有 fit。</td></tr></tbody>'; return; }
    let h = `<thead><tr><th>項目</th><th class="num">係數（log 尺度）</th><th class="num">標準誤</th><th class="num">t</th><th class="num">p</th><th>解讀（示意）</th></tr></thead><tbody>`;
    h += `<tr><td>截距</td><td class="num">12.4512</td><td class="num">0.0210</td><td class="num">592.9</td><td class="num">&lt;0.001</td><td>—</td></tr>`;
    it.groups.forEach((gid, i) => { const g = M.GROUPS.find(x => x.id === gid); const coef = (0.3 / (i + 1)) * (i % 3 === 2 ? -1 : 1); h += `<tr><td>${g.label}${gid === 'zipcode' ? '（69 個 dummy，相對基準 98001）' : ''}</td><td class="num">${coef.toFixed(4)}</td><td class="num">${(Math.abs(coef) / 8).toFixed(4)}</td><td class="num">${(8 * Math.sign(coef)).toFixed(1)}</td><td class="num">&lt;0.001</td><td>每增加一單位，價格約變動 ${(Math.exp(coef) * 100 - 100).toFixed(1)}%（其他不變）</td></tr>`; });
    h += `</tbody>`;
    tb.innerHTML = h;
  }
  function renderResidTable(t) {
    const top = t.pts.slice().sort((a, b) => Math.abs(Math.log(b.actual / b.pred)) - Math.abs(Math.log(a.actual / a.pred))).slice(0, 10);
    let h = `<thead><tr><th>#</th><th>房屋 id</th><th class="num">實際</th><th class="num">預測</th><th class="num">殘差（USD）</th><th class="num">PI 下界</th><th class="num">PI 上界</th><th>涵蓋</th></tr></thead><tbody>`;
    top.forEach((p, i) => { h += `<tr><td>${i + 1}</td><td class="num">${p.id}</td><td class="num">${fmtUSD(p.actual)}</td><td class="num">${fmtUSD(p.pred)}</td><td class="num">${(p.actual - p.pred >= 0 ? '+' : '−') + fmtUSD(Math.abs(p.actual - p.pred))}</td><td class="num">${fmtUSD(p.lower)}</td><td class="num">${fmtUSD(p.upper)}</td><td>${p.covered ? '<span class="tag tag--cv">是</span>' : '<span class="tag tag--invalid">否</span>'}</td></tr>`; });
    $('#resid-table').innerHTML = h + '</tbody>';
  }
  function renderAllTable() {
    let h = `<thead><tr><th>方法</th><th class="num">k</th><th>狀態</th><th class="num">CV RMSE</th><th class="num">CV MAE</th><th class="num">CV R²（USD）</th><th class="num">Adj R²（log）</th><th class="num">fold 一致</th></tr></thead><tbody>`;
    M.METHODS.filter(m => m.kind === 'path').forEach(m => { const model = M.MODELS[m.id]; for (let k = 1; k <= 18; k++) { const it = model.items[k]; const w = model.winnerK === k; h += `<tr class="${it.status === 'invalid' ? 'is-invalid' : (w ? 'is-winner' : '')}"><td>${m.name}</td><td class="num">${k}</td><td>${it.status === 'invalid' ? '<span class="tag tag--invalid">invalid</span>' : (w ? '<span class="tag tag--winner">CV winner</span>' : 'valid')}</td><td class="num">${it.cv ? fmtUSD(it.cv.rmse) : '—'}</td><td class="num">${it.cv ? fmtUSD(it.cv.mae) : '—'}</td><td class="num">${it.cv ? it.cv.r2.toFixed(3) : '—'}</td><td class="num">${it.cv ? it.cv.adj_r2_log.toFixed(3) : '—'}</td><td class="num">${it.cv ? it.foldsAgree + '/5' : '—'}</td></tr>`; } });
    $('#all-table').innerHTML = h + '</tbody>';
  }

  // ---------- update ----------
  function update() {
    renderMethodSeg(); renderKGrid(); renderSelected();
    ['#kpi-cv', '#kpi-test'].forEach(s => $(s).classList.add('is-updating'));
    renderCvKpi(); renderKChart(); renderCompareTable(); renderPredictor(); renderTest(); renderCoefTable();
    requestAnimationFrame(() => ['#kpi-cv', '#kpi-test'].forEach(s => $(s).classList.remove('is-updating')));
    // nav current
    document.querySelectorAll('.topnav a').forEach(a => a.removeAttribute('aria-current'));
  }
  renderAllTable();
  update();

  // ---------- 手機導覽（UI 決策 7）----------
  (function mobileNav() {
    const btn = $('#nav-toggle'), nav = $('#topnav');
    if (!btn || !nav) return;
    const setOpen = open => {
      nav.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? '關閉頁內導覽' : '開啟頁內導覽');
      if (open) { const first = nav.querySelector('a'); if (first) first.focus(); }
    };
    btn.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
    nav.addEventListener('click', e => { if (e.target.closest('a')) { setOpen(false); } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); btn.focus(); } });
    // 焦點離開選單與按鈕時關閉（鍵盤 Tab 出去）
    document.addEventListener('focusin', e => { if (nav.classList.contains('is-open') && !nav.contains(e.target) && e.target !== btn) setOpen(false); });
    const mq = window.matchMedia('(min-width: 769px)');
    const onMq = () => { if (mq.matches) setOpen(false); };
    mq.addEventListener ? mq.addEventListener('change', onMq) : mq.addListener(onMq);
  })();

  // scrollspy (簡單版)
  const secs = ['overview', 'model', 'predictor', 'test', 'methods'].map(id => document.getElementById(id));
  const links = Array.from(document.querySelectorAll('.topnav a'));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => { entries.forEach(e => { if (e.isIntersecting) { links.forEach(a => a.removeAttribute('aria-current')); const a = links.find(l => l.getAttribute('href') === '#' + e.target.id); if (a) a.setAttribute('aria-current', 'true'); } }); }, { rootMargin: '-40% 0px -55% 0px' });
    secs.forEach(s => io.observe(s));
  }
})();
