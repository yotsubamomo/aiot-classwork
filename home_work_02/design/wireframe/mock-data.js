/* HW2 Dashboard Wireframe — 示意資料（mock）
 * 全部數值由固定種子的亂數產生，只用來評估 UI／UX，
 * 不是 Python 模型的輸出，也沒有經過任何統計驗證。
 */
(function () {
  'use strict';

  // ---- 固定種子亂數（mulberry32）----
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function randn(r) { // Box–Muller
    let u = 0, v = 0;
    while (u === 0) u = r();
    while (v === 0) v = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  // ---- Source feature groups（canonical order；18 個建模 group）----
  const GROUPS = [
    { id: 'date',          label: '交易日期',        type: 'date',   min: '2014-05-02', max: '2015-05-27', def: '2014-10-16', unit: '' },
    { id: 'bedrooms',      label: '臥室數',          type: 'number', min: 0, max: 33, def: 3, step: 1, unit: '間' },
    { id: 'bathrooms',     label: '浴室數',          type: 'number', min: 0, max: 8, def: 2.25, step: 0.25, unit: '間' },
    { id: 'sqft_living',   label: '室內面積',        type: 'number', min: 290, max: 13540, def: 1910, step: 10, unit: 'sq ft' },
    { id: 'sqft_lot',      label: '土地面積',        type: 'number', min: 520, max: 1651359, def: 7618, step: 10, unit: 'sq ft' },
    { id: 'floors',        label: '樓層數',          type: 'select', options: ['1', '1.5', '2', '2.5', '3', '3.5'], def: '1.5', unit: '' },
    { id: 'waterfront',    label: '臨水',            type: 'select', options: ['否', '是'], def: '否', unit: '' },
    { id: 'view',          label: '景觀等級',        type: 'select', options: ['0', '1', '2', '3', '4'], def: '0', unit: '' },
    { id: 'condition',     label: '屋況等級',        type: 'select', options: ['1', '2', '3', '4', '5'], def: '3', unit: '' },
    { id: 'grade',         label: '建築等級',        type: 'number', min: 1, max: 13, def: 7, step: 1, unit: '' },
    { id: 'sqft_above',    label: '地上面積',        type: 'number', min: 290, max: 9410, def: 1560, step: 10, unit: 'sq ft' },
    { id: 'yr_built',      label: '建造年',          type: 'number', min: 1900, max: 2015, def: 1975, step: 1, unit: '' },
    { id: 'yr_renovated',  label: '整修年',          type: 'renovated', min: 1934, max: 2015, def: 0, unit: '' },
    { id: 'zipcode',       label: '郵遞區號 zipcode', type: 'zipcode', def: '98103', unit: '' },
    { id: 'lat',           label: '緯度 lat',        type: 'number', min: 47.1559, max: 47.7776, def: 47.5718, step: 0.0001, unit: '' },
    { id: 'long',          label: '經度 long',       type: 'number', min: -122.519, max: -121.315, def: -122.23, step: 0.001, unit: '' },
    { id: 'sqft_living15', label: '鄰近室內面積',    type: 'number', min: 399, max: 6210, def: 1840, step: 10, unit: 'sq ft' },
    { id: 'sqft_lot15',    label: '鄰近土地面積',    type: 'number', min: 651, max: 871200, def: 7620, step: 10, unit: 'sq ft' },
  ];

  // 訓練集中的 zipcode（示意：取 70 個中的一部分；最後一個用來示範「未見類別」）
  const ZIPCODES = ['98001','98002','98003','98004','98005','98006','98007','98008','98010','98011',
    '98014','98019','98022','98023','98024','98027','98028','98029','98030','98031','98032','98033',
    '98034','98038','98039','98040','98042','98045','98052','98053','98055','98056','98058','98059',
    '98065','98070','98072','98074','98075','98077','98092','98102','98103','98105','98106','98107',
    '98108','98109','98112','98115','98116','98117','98118','98119','98122','98125','98126','98133',
    '98136','98144','98146','98148','98155','98166','98168','98177','98178','98188','98198','98199'];
  const UNSEEN_ZIP = '98000'; // 不在訓練類別中（示意）

  // ---- 四種路徑方法 + All-in ----
  // 每個方法有自己的 group 排序（示意），canonical subset(k) = 前 k 個
  const ORDERS = {
    forward:  ['sqft_living','grade','lat','zipcode','yr_built','view','waterfront','sqft_living15','bathrooms','condition','long','sqft_above','date','floors','bedrooms','sqft_lot15','yr_renovated','sqft_lot'],
    backward: ['sqft_living','lat','grade','zipcode','yr_built','waterfront','view','sqft_living15','condition','bathrooms','date','long','sqft_above','bedrooms','floors','yr_renovated','sqft_lot15','sqft_lot'],
    rfe:      ['grade','sqft_living','lat','zipcode','waterfront','yr_built','view','condition','sqft_living15','bathrooms','long','date','floors','sqft_above','bedrooms','yr_renovated','sqft_lot','sqft_lot15'],
    lasso:    ['sqft_living','lat','grade','waterfront','zipcode','view','yr_built','sqft_living15','condition','bathrooms','long','date','bedrooms','floors','sqft_above','sqft_lot15','yr_renovated','sqft_lot'],
  };

  const METHODS = [
    { id: 'forward',  name: 'Forward SFS',   short: 'Forward',  color: '#1E40AF', kind: 'path' },
    { id: 'backward', name: 'Backward SFS',  short: 'Backward', color: '#0E7490', kind: 'path' },
    { id: 'rfe',      name: 'RFE',           short: 'RFE',      color: '#6D28D9', kind: 'path' },
    { id: 'lasso',    name: 'Lasso 路徑排序', short: 'Lasso',    color: '#C2410C', kind: 'path' },
    { id: 'allin',    name: 'All-in baseline', short: 'All-in', color: '#334155', kind: 'single' },
  ];

  const PRICE_SD = 367000; // 示意：價格標準差（USD），只用來換算 R²

  function curve(seed, bias) {
    const r = rng(seed);
    const out = [];
    for (let k = 1; k <= 18; k++) {
      const base = 126000 + 118000 * Math.exp(-0.30 * k) + bias * (1 - k / 18);
      const noise = randn(r) * 1800;
      const bump = (k === 17 || k === 18) ? 1500 * (k - 16) : 0; // 示意：接近全特徵時略為變差
      out.push(Math.round(base + noise + bump));
    }
    return out;
  }
  const CV_RMSE = {
    forward:  curve(11, 2600),
    backward: curve(23, 2300),
    rfe:      curve(37, 3800),
    lasso:    curve(41, 4200),
  };

  // 示意：無效候選（canonical fit 秩不足）
  const INVALID = { rfe: { 17: 'canonical_rank_deficient' } };

  function metricsFromRmse(rmse, k) {
    const mse = rmse * rmse;
    const r2 = 1 - mse / (PRICE_SD * PRICE_SD);
    return {
      rmse, mse, mae: Math.round(rmse * 0.68), r2,
      r2_log: Math.min(0.92, 0.55 + 0.022 * k),          // 示意：log 尺度 R²
      adj_r2_log: Math.min(0.918, 0.55 + 0.0215 * k),    // 示意：log 尺度 Adjusted R²
      rank: 1 + k + (k >= 14 ? 68 : 0),                   // 示意：含 zipcode 時多 69 欄
    };
  }

  function buildMethod(m) {
    if (m.kind === 'single') {
      const rmse = Math.round((CV_RMSE.forward[17] + CV_RMSE.backward[17]) / 2) - 400;
      return { ...m, items: { 18: { k: 18, groups: GROUPS.map(g => g.id), status: 'valid', cv: metricsFromRmse(rmse, 18), foldsAgree: 5 } }, winnerK: 18 };
    }
    const items = {};
    let bestK = 1, bestV = Infinity;
    for (let k = 1; k <= 18; k++) {
      const invalid = INVALID[m.id] && INVALID[m.id][k];
      const rmse = CV_RMSE[m.id][k - 1];
      items[k] = {
        k, groups: ORDERS[m.id].slice(0, k),
        status: invalid ? 'invalid' : 'valid',
        reason: invalid || null,
        cv: invalid ? null : metricsFromRmse(rmse, k),
        foldsAgree: invalid ? 0 : (k <= 3 ? 5 : (k <= 10 ? 4 : 3)),
      };
      if (!invalid && rmse < bestV) { bestV = rmse; bestK = k; }
    }
    return { ...m, items, winnerK: bestK };
  }

  const MODELS = {};
  METHODS.forEach(m => { MODELS[m.id] = buildMethod(m); });

  // 整體 CV winner
  let overall = null;
  Object.values(MODELS).forEach(m => {
    const it = m.items[m.winnerK];
    if (!overall || it.cv.rmse < overall.rmse) overall = { method: m.id, k: m.winnerK, rmse: it.cv.rmse };
  });

  // 對照模型（metric only）
  const BASELINES = {
    ridge: { name: 'Ridge（對照）', cvRmse: CV_RMSE.backward[17] - 900, alpha: 3.16 },
    lasso_ref: { name: 'Lasso（對照）', cvRmse: CV_RMSE.backward[17] - 300, alpha: 0.0032 },
    pvalue: { name: 'p-value backward（講義對照）', cvRmse: CV_RMSE.forward[13] + 2100, groups: 12 },
  };

  // ---- Test（只對被授權的模型）----
  const N_TEST = 4287;
  function genScatter(seed, hw) {
    const r = rng(seed);
    const pts = new Array(N_TEST);
    let covered = 0;
    for (let i = 0; i < N_TEST; i++) {
      const logA = 13.05 + 0.52 * randn(r);
      const actual = Math.exp(logA);
      const err = 0.33 * randn(r) * (1 + 0.15 * Math.max(0, logA - 13.8)); // 高價略不穩
      const pred = Math.exp(logA + err);
      const h = hw * (0.92 + 0.16 * r());
      const lower = pred * Math.exp(-h), upper = pred * Math.exp(h);
      const cov = actual >= lower && actual <= upper;
      if (cov) covered++;
      pts[i] = { actual, pred, lower, upper, covered: cov, id: 1000000 + Math.floor(r() * 9000000) };
    }
    return { pts, covered };
  }

  const TEST = {};
  const authorized = [];
  Object.values(MODELS).forEach(m => authorized.push({ method: m.id, k: m.winnerK }));
  authorized.forEach((a, i) => {
    const m = MODELS[a.method];
    const cv = m.items[a.k].cv;
    const sc = genScatter(100 + i * 7, 0.60 - a.k * 0.004);
    const rmse = Math.round(cv.rmse * (1.012 + 0.006 * i));
    const coverage = sc.covered / N_TEST;
    let widthSum = 0;
    sc.pts.forEach(p => { widthSum += p.upper - p.lower; });
    TEST[a.method + ':' + a.k] = {
      method: a.method, k: a.k, kind: 'ols_subset',
      rmse, mae: Math.round(rmse * 0.69), mse: rmse * rmse, r2: 1 - (rmse * rmse) / (PRICE_SD * PRICE_SD),
      nTest: N_TEST, coverage, covered: sc.covered,
      meanWidth: Math.round(widthSum / N_TEST),
      uncertainty: 1.96 * Math.sqrt(coverage * (1 - coverage) / N_TEST),
      houses: 4253, repeatSales: 34, unseenZip: 0,
      pts: sc.pts,
    };
  });
  TEST['ridge'] = { kind: 'metric_only', name: 'Ridge（對照）', rmse: BASELINES.ridge.cvRmse + 1400 };
  TEST['lasso_ref'] = { kind: 'metric_only', name: 'Lasso（對照）', rmse: BASELINES.lasso_ref.cvRmse + 1700 };

  window.MOCK = {
    GROUPS, ZIPCODES, UNSEEN_ZIP, METHODS, MODELS, BASELINES, TEST, OVERALL: overall, N_TEST,
    meta: {
      dataset: 'House Sales in King County, USA（Kaggle harlfoxem/housesalesprediction，CC0-1.0）',
      rows: 21613, sourceFeatures: 19, groups: 18, houses: 21436, repeat: 177,
      nTrain: 17326, nTest: N_TEST, seed: '（示意）', folds: 5,
    },
  };
})();
