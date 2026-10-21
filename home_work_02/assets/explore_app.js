/* HW2 V2 dashboard: the problem controller and the zh-TW texts of the Exploratory run, without the page.
 *
 * createController(deps) owns the problem drop-down's behaviour (Spec V2 「Problem 與頁面結構」):
 *   - init(): King County (the formal analysis; the V1 page as it is).
 *   - selectProblem('king_county'): show the V1 blocks; a previous exploratory result stays in memory
 *     and is not shown. selectProblem('startups50'): run the Exploratory run on the bundled text, again
 *     on every selection. selectProblem('custom'): the input panel only; nothing runs (the URL and file
 *     inputs come with V2-T3).
 *   - loadText(text, source): run on local text (the path a local file takes); no network.
 * Its dependencies are injected (loader, engine, datasets, render, clock, and the network function that
 * only V2-T3's URL path may use), so that tests/js/explore_app.test.js can drive it in Node with a mock
 * and prove that none of these four paths makes a request. Nothing here touches the page; results are
 * never stored (no localStorage, no URL parameter, no file).
 *
 * predictorView() and the *Text() helpers turn engine results into what the page shows; every string
 * that comes from the data stays a plain string (the page writes it as text; DA D-2). */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.HW2ExploreApp = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var PROBLEMS = ['king_county', 'startups50', 'custom'];
  var PROBLEM_TITLES = { king_county: 'King County 房價（正式分析）', startups50: '50 Startups 利潤（探索）',
    custom: '自訂資料集（探索）' };
  var EXPLORE_LABEL = '探索執行，非正式評估';
  var CV_LABEL = '訓練 CV';
  var TEST_LABEL = '探索 test（非正式評估）';
  var CUSTOM_PLACEHOLDER = '自訂資料集的 URL 與本機 CSV 檔案輸入由 V2-T3 提供；目前不接受任何輸入。';

  var STATUS_TEXT = {
    VALID: '有效（VALID）',
    INVALID_MODEL: '無效模型（INVALID_MODEL）',
    SKIPPED_RESOURCE_LIMIT: '超出運算限制，未執行（SKIPPED_RESOURCE_LIMIT）',
    FAILED: '計算失敗（FAILED）'
  };
  var COLUMN_STATUS_TEXT = {
    TARGET: '預測目標',
    KEPT: '保留（feature group）',
    EXCLUDED_CONSTANT: '排除：在訓練列上只有一個值（EXCLUDED_CONSTANT）',
    EXCLUDED_TOO_MANY_LEVELS: '排除：訓練列的類別層級超過 20（EXCLUDED_TOO_MANY_LEVELS）'
  };
  var LOAD_REASON_TEXT = {
    NOT_CSV: '不是可讀取的 CSV（需要逗號分隔、第一列為欄名、至少兩欄）',
    NO_HEADER: '第一列不是欄名（欄名不可空白，也不可全是數字）',
    RAGGED_ROWS: '某些列的欄數與欄名數不同',
    ENCODING: '不是 UTF-8 文字',
    TOO_LARGE: '超過載入上限（列數或欄數）',
    TOO_FEW_ROWS: '刪除含缺值的列後不足 20 列',
    TARGET_NOT_NUMERIC: '預測目標欄不是數值欄，請改選數值欄',
    DUPLICATE_COLUMN: '有重複的欄名'
  };
  var RUN_REASON_TEXT = { ALL_CANDIDATES_INVALID: '全部候選都無效，探索執行被拒絕（ALL_CANDIDATES_INVALID）' };

  function statusText(status) { return STATUS_TEXT[status] || String(status); }
  function columnStatusText(status) { return COLUMN_STATUS_TEXT[status] || String(status); }
  function loadReasonText(reason) { return LOAD_REASON_TEXT[reason] || String(reason); }
  function runReasonText(reason) { return RUN_REASON_TEXT[reason] || String(reason); }

  function reasonText(r) {
    var where = r.scope === 'fold' ? '第 ' + (r.fold + 1) + ' 個 fold 的訓練列' : '整個訓練集';
    if (r.rule === 'rank_deficient') {
      return where + '：設計矩陣（含截距）秩不足，rank ' + r.rank + ' < ' + r.n_columns + ' 欄';
    }
    if (r.rule === 'df_resid_lt_3') return where + '：殘差自由度 ' + r.df_resid + ' < 3';
    if (r.rule === 'no_feature_groups') return '沒有任何 feature group（以訓練列判定後全部欄位都被排除）';
    return where + '：' + String(r.rule);
  }

  function warningText(w) {
    if (w.type === 'out_of_range') {
      return w.group + ' 的輸入超出訓練範圍（' + w.min + '～' + w.max + '），仍照常計算，屬於外推。';
    }
    if (w.type === 'unseen_level') return w.group + ' 的值不在訓練層級中，已以基準層級「' + w.baseline + '」計算。';
    return String(w.type);
  }

  /* What the live predictor shows for the selected candidate and the raw inputs (strings or numbers).
   * Only a VALID candidate with a fit predicts; anything else disables the predictor with its status
   * and reasons and gives no number at all (Spec V2 「即時預測器」; Brief V2 §8 2a). */
  function predictorView(engine, candidate, raw) {
    if (!engine.canPredict(candidate)) {
      return { enabled: false, status: candidate ? candidate.status : null,
        statusText: candidate ? statusText(candidate.status) : '沒有可用的候選',
        reasons: candidate && candidate.reasons ? candidate.reasons.map(reasonText) : [] };
    }
    var specs = engine.inputSpec(candidate.fit);
    var values = {};
    specs.forEach(function (s) {
      values[s.name] = raw && raw[s.name] !== undefined && raw[s.name] !== null ? raw[s.name] : s.default;
    });
    try {
      var p = engine.predict(candidate, values);
      return { enabled: true, specs: specs, values: values, predicted: p.predicted, lower: p.lower, upper: p.upper,
        warnings: p.warnings.map(warningText), error: null };
    } catch (e) {
      return { enabled: true, specs: specs, values: values, predicted: null, lower: null, upper: null, warnings: [],
        error: '請輸入有效的數字：' + e.message };
    }
  }

  function createController(deps) {
    var now = deps.now || function () { return Date.now(); };
    var state = { problem: 'king_county', lastExplore: null, runs: 0 };

    function runText(text, source, problem) {
      var t0 = now();
      var load = deps.loader.loadCsv(text);
      var out = { problem: problem, source: source, load: load, result: null, ms: null };
      if (load.ok) out.result = deps.engine.run(load, { problem: problem, source: source, now: deps.now });
      out.ms = now() - t0;
      state.runs++;
      return out;
    }

    function init() {
      state.problem = 'king_county';
      deps.render({ mode: 'king_county', problem: 'king_county' });
    }

    function selectProblem(problem) {
      if (PROBLEMS.indexOf(problem) < 0) throw new Error('unknown problem ' + problem);
      state.problem = problem;
      if (problem === 'king_county') { deps.render({ mode: 'king_county', problem: problem }); return null; }
      if (problem === 'custom') { deps.render({ mode: 'custom', problem: problem }); return null; }
      var ds = deps.datasets && deps.datasets.startups50;
      if (!ds || typeof ds.csv !== 'string') {
        deps.render({ mode: 'error', problem: problem, message: '找不到內建的 50 Startups 資料（assets/data/startups50.js）。' });
        return null;
      }
      var run = runText(ds.csv, 'builtin', problem);
      state.lastExplore = run;
      if (state.problem === problem) deps.render({ mode: 'explore', problem: problem, run: run });
      return run;
    }

    function loadText(text, source) {
      state.problem = 'custom';
      var run = runText(String(text), source || 'file', 'custom');
      state.lastExplore = run;
      deps.render({ mode: 'explore', problem: 'custom', run: run });
      return run;
    }

    return { init: init, selectProblem: selectProblem, loadText: loadText,
      state: function () { return { problem: state.problem, runs: state.runs, hasResult: !!state.lastExplore }; } };
  }

  return {
    PROBLEMS: PROBLEMS, PROBLEM_TITLES: PROBLEM_TITLES, EXPLORE_LABEL: EXPLORE_LABEL, CV_LABEL: CV_LABEL,
    TEST_LABEL: TEST_LABEL, CUSTOM_PLACEHOLDER: CUSTOM_PLACEHOLDER,
    statusText: statusText, columnStatusText: columnStatusText, loadReasonText: loadReasonText,
    runReasonText: runReasonText, reasonText: reasonText, warningText: warningText,
    predictorView: predictorView, createController: createController
  };
});
