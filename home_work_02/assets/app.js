/* HW2 dashboard: reads window.MODEL_DATA (assets/model_data.js) and renders the overview (A).
 * No network access: every resource is a local file so the page works from file://. */
(function () {
  'use strict';

  var nf = new Intl.NumberFormat('zh-TW');

  function byId(id) { return document.getElementById(id); }
  function setText(id, value) {
    var el = byId(id);
    if (el) el.textContent = value == null ? '—' : String(value);
  }
  function showError(message) {
    var box = byId('load-error');
    box.textContent = message;
    box.hidden = false;
  }

  function renderOverview(meta) {
    var ds = meta.dataset || {};
    setText('meta-dataset-name', ds.name);
    setText('meta-dataset-slug', ds.kaggle_slug);
    var link = byId('meta-dataset-link');
    if (ds.url) link.setAttribute('href', ds.url);
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
    setText('meta-fold-rows', (cv.fold_rows || []).map(function (n) { return nf.format(n); }).join('／'));
    setText('meta-seed', meta.seed);

    var versions = meta.versions || {};
    setText('meta-versions', Object.keys(versions).map(function (k) {
      return k + ' ' + versions[k];
    }).join('、'));
    var timing = meta.timing_s || {};
    setText('meta-timing', Object.keys(timing).map(function (k) {
      return k + ' ' + Number(timing[k]).toFixed(2) + ' 秒';
    }).join('、'));
    setText('meta-generated', meta.generated_at);
    setText('meta-sections', (meta.sections_written || []).join('、'));
  }

  function renderExcluded(preprocess) {
    var items = (preprocess && preprocess.excluded_source_features) || [];
    setText('meta-excluded', items.length
      ? '不進模型：' + items.map(function (x) { return x.name; }).join('、') +
        '（sqft_living = sqft_above + sqft_basement，三欄完全共線）'
      : '');
  }

  function init() {
    if (window.Chart && window.Chart.version) {
      setText('chartjs-version', 'Chart.js ' + window.Chart.version + '（本機打包）');
    }
    var data = window.MODEL_DATA;
    if (!data || !data.meta) {
      showError('找不到 model_data：請先執行 hw2.ipynb 產生 assets/model_data.js。');
      return;
    }
    if (data.meta.fixture) {
      showError('目前載入的是測試用 fixture 資料，不是正式結果。');
    }
    renderOverview(data.meta);
    renderExcluded(data.preprocess);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
