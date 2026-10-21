/* HW2 V2 dashboard: the problem controller and the zh-TW texts of the Exploratory run, without the page.
 *
 * createController(deps) owns the problem drop-down's behaviour (Spec V2 「Problem 與頁面結構」):
 *   - init(): King County (the formal analysis; the V1 page as it is).
 *   - selectProblem('king_county'): show the V1 blocks; a previous exploratory result stays in memory
 *     and is not shown. selectProblem('startups50'): run the Exploratory run on the bundled text, again
 *     on every selection. selectProblem('custom'): the input panel only; nothing runs, and whatever was
 *     submitted before is forgotten (selecting the custom dataset again asks for a new submission).
 *   - The custom dataset (#76 V2-T3): submitUrl(text) reads the URL once through the loader (the only
 *     network path: one GET, no credentials, no redirect, no retry; DA D-1) and returns a Promise;
 *     submitData(bytesOrText, {source, label}) runs a local file's content (no network); loadText(text,
 *     source) is the same for text. Both entrances give the same bytes to the same load contract and
 *     engine. setTarget(index) runs the kept content again with another target column (default: the
 *     last column) and never reads the URL again. Leaving the custom dataset, or a new submission,
 *     aborts a read in progress, and its late answer is dropped (it never replaces another view).
 * Its dependencies are injected (loader, engine, datasets, render, clock, fetchImpl: the network
 * function handed to the loader's URL read), so that the Node tests (tests/js/explore_app.test.js,
 * tests/js/explore_custom.test.js) can drive it with a mock and prove that only a URL submission makes
 * a request, exactly one. Nothing here touches the page; results are never stored (no localStorage, no
 * URL parameter, no file).
 *
 * predictorView() and the *Text() helpers turn engine results into what the page shows; every string
 * that comes from the data stays a plain string (the page writes it as text; DA D-2). #75 adds the views
 * of the five methods: testView() (the test block shows a winner itself, a non-winner's method winner
 * with a hint, a method without a VALID candidate the overall winner with a hint), compareRows() (one row
 * per method winner, training CV and exploratory test kept apart, test numbers only for winners),
 * kSeries() (training-CV metric vs k), lassoView() and dependencyView(). */
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
  var FILE_GUIDE = '請用瀏覽器下載該 CSV，再以下方的「本機 CSV 檔案」載入（本機讀取，不發出請求）。';

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
    DUPLICATE_COLUMN: '有重複的欄名',
    URL_FETCH_FAILED: 'URL 讀取失敗'
  };
  var URL_CAUSE_TEXT = {
    network: '網路或跨來源限制：沒有取得回應。可能是網路中斷、對方伺服器不允許跨來源讀取（CORS），或該網址會重新導向（本頁不跟隨重新導向）',
    http_status: '伺服器回應錯誤的 HTTP 狀態',
    timeout: '逾時：超過時間沒有讀完，已中止',
    not_text: '回應不是文字：內容含有二進位資料（例如圖片、壓縮檔或試算表檔），不是 CSV 文字'
  };
  var URL_INPUT_TEXT = {
    empty: '請先輸入 CSV 的 URL。',
    not_absolute_url: 'URL 格式不正確：請輸入完整的網址（以 http:// 或 https:// 開頭）。',
    not_http: '只接受 http:// 或 https:// 開頭的網址。',
    has_credentials: 'URL 不可包含帳號或密碼（本頁讀取 URL 時不帶任何憑證）。'
  };
  var RUN_REASON_TEXT = { ALL_CANDIDATES_INVALID: '全部候選都無效，探索執行被拒絕（ALL_CANDIDATES_INVALID）' };
  var METHOD_ORDER = ['allin', 'forward_sfs', 'backward_sfs', 'rfe', 'lasso_path'];
  var METHOD_LABELS = { allin: 'All-in baseline', forward_sfs: 'Forward SFS', backward_sfs: 'Backward SFS', rfe: 'RFE',
    lasso_path: 'Lasso 路徑排序' };
  var CAUSE_TEXT = {
    active_set_degenerate: '要加入的欄與路徑中已有的欄線性相依（active set 退化）',
    path_ended: '路徑結束時仍有 feature group 沒有進入（它們與已進入的欄線性相依，或在這些列上沒有變化）'
  };

  function statusText(status) { return STATUS_TEXT[status] || String(status); }
  function columnStatusText(status) { return COLUMN_STATUS_TEXT[status] || String(status); }
  function loadReasonText(reason) { return LOAD_REASON_TEXT[reason] || String(reason); }
  function urlCauseText(cause) { return URL_CAUSE_TEXT[cause] || String(cause); }
  function urlInputText(problem) { return URL_INPUT_TEXT[problem] || String(problem); }
  function count(n) { return Number(n).toLocaleString('zh-TW'); }

  /* The full zh-TW message of a rejected LoadResult or a URL_FETCH_FAILED read, with what to do next.
   * Names from the data are quoted as plain text (the page writes this string with textContent). */
  function loadFailureText(load) {
    var d = load.detail || {}, r = load.reason, text;
    if (r === 'URL_FETCH_FAILED') {
      text = urlCauseText(d.cause);
      if (d.cause === 'http_status') text += '：HTTP ' + d.status + (d.status_text ? ' ' + d.status_text : '');
      if (d.cause === 'timeout') text += '（' + Math.round(d.timeout_ms / 1000) + ' 秒）';
      return 'URL 讀取失敗（URL_FETCH_FAILED，' + d.cause + '）：' + text + '。' + FILE_GUIDE;
    }
    if (r === 'NOT_CSV') {
      text = { empty: '內容是空的', fewer_than_two_columns: '只有 ' + d.columns + ' 欄（至少需要兩欄：特徵與預測目標）',
        unterminated_quoted_field: '有沒有結束的引號欄位', text_after_closing_quote: '引號欄位結束後還有其他文字' }[d.problem];
      return '不是可讀取的 CSV（NOT_CSV）' + (text ? '：' + text : '') + '。需要 UTF-8 文字、逗號分隔、第一列為欄名、至少兩欄。';
    }
    if (r === 'NO_HEADER') {
      text = d.problem === 'empty_column_name' ? '第 ' + (d.column + 1) + ' 欄的欄名是空白' : '第一列全是數字，看起來沒有欄名列';
      return '第一列不是欄名（NO_HEADER）：' + text + '。請在第一列放欄名（不可空白，也不可全是數字）。';
    }
    if (r === 'RAGGED_ROWS') {
      return '欄數不一致（RAGGED_ROWS）：第 ' + count(d.record) + ' 筆資料列有 ' + d.found + ' 欄，欄名有 ' + d.expected + ' 欄。';
    }
    if (r === 'ENCODING') return '不是 UTF-8 文字（ENCODING）：請把檔案以 UTF-8 另存後再載入。';
    if (r === 'TOO_LARGE') {
      if (d.columns !== undefined) return '超過載入上限（TOO_LARGE）：有 ' + d.columns + ' 欄，上限 ' + d.max_columns + ' 欄；不會截斷。';
      return '超過載入上限（TOO_LARGE）：資料列超過 ' + count(d.rows_over !== undefined ? d.rows_over : d.max_rows) + ' 列的上限；不會截斷。';
    }
    if (r === 'TOO_FEW_ROWS') {
      return '列數不足（TOO_FEW_ROWS）：刪除含缺值的列（' + count(d.dropped_missing) + ' 列）後只剩 ' + count(d.rows) +
        ' 列，至少需要 ' + d.min_rows + ' 列。';
    }
    if (r === 'TARGET_NOT_NUMERIC') {
      return '預測目標欄「' + d.target + '」不是數值欄（TARGET_NOT_NUMERIC），沒有執行分析。請在「預測目標欄」下拉改選數值欄；改選後以同一份資料重新執行。';
    }
    if (r === 'DUPLICATE_COLUMN') {
      return '欄名重複（DUPLICATE_COLUMN）：「' + d.name + '」出現在第 ' + (d.columns[0] + 1) + ' 與第 ' + (d.columns[1] + 1) + ' 欄。每一欄需要不同的欄名。';
    }
    return loadReasonText(r) + '（' + r + '）';
  }
  function runReasonText(reason) { return RUN_REASON_TEXT[reason] || String(reason); }
  function methodLabel(m) { return METHOD_LABELS[m] || String(m); }
  function causeText(c) { return CAUSE_TEXT[c] || String(c); }

  function reasonText(r) {
    var where = r.scope === 'fold' ? '第 ' + (r.fold + 1) + ' 個 fold 的訓練列' : '整個訓練集';
    if (r.rule === 'rank_deficient') {
      return where + '：設計矩陣（含截距）秩不足，rank ' + r.rank + ' < ' + r.n_columns + ' 欄';
    }
    if (r.rule === 'df_resid_lt_3') return where + '：殘差自由度 ' + r.df_resid + ' < 3';
    if (r.rule === 'no_feature_groups') return '沒有任何 feature group（以訓練列判定後全部欄位都被排除）';
    if (r.rule === 'lasso_path_degenerate') {
      return where + '：Lasso 路徑只求得前 ' + r.n_groups_entered + ' 個 feature group 就停止（' + causeText(r.cause) +
        '），k ≥ ' + (r.n_groups_entered + 1) + ' 沒有實際路徑（lasso_path_degenerate）';
    }
    return where + '：' + String(r.rule);
  }

  /* ---- views of a COMPLETED ExploratoryResult (#75); plain strings and numbers only --------------- */
  function candidateName(c) {
    return c.method === 'allin' ? 'All-in baseline（全部 ' + c.k + ' 個 feature group）' : methodLabel(c.method) + ' · k = ' + c.k;
  }
  function candidateByKey(result, key) {
    var list = result && result.candidates ? result.candidates : [];
    for (var i = 0; i < list.length; i++) if (list[i].key === key) return list[i];
    return null;
  }
  function defaultKey(result) { return result.winners.overall.key; }

  /* The winner roles a candidate holds: its method's CV winner and / or the overall CV winner. */
  function winnerRoles(result, key) {
    var w = result.winners, c = candidateByKey(result, key), roles = [];
    if (!c) return roles;
    var mw = w.method_winners[c.method];
    if (mw && mw.key === key) roles.push(c.method === 'allin' ? 'All-in baseline（自身即 CV winner）' : methodLabel(c.method) + ' 的 CV winner');
    if (w.overall.key === key) roles.push('整體 CV winner');
    return roles;
  }

  /* What the exploratory test block shows for the selected candidate. Test numbers exist only for the
   * winners: a winner shows its own; a non-winner shows its method's CV winner with a hint; a method
   * without a VALID candidate shows the overall CV winner with a hint (Spec V2 「評估、預測區間」). */
  function testView(result, selectedKey) {
    var w = result.winners;
    var sel = candidateByKey(result, selectedKey) || candidateByKey(result, w.overall.key);
    var mw = w.method_winners[sel.method], shownKey, hint = null;
    if (Object.prototype.hasOwnProperty.call(w.test_key_of, sel.key)) shownKey = sel.key;
    else if (mw) {
      shownKey = mw.key;
      hint = '目前選取的「' + candidateName(sel) + '」不是該方法的 CV winner；test 只對 CV winner 計算，下面展示「' +
        methodLabel(sel.method) + '」的 CV winner（k = ' + mw.k + '）。';
    } else {
      shownKey = w.overall.key;
      hint = '「' + methodLabel(sel.method) + '」沒有有效（VALID）的候選，所以沒有 CV winner；下面展示整體 CV winner。';
    }
    var testKey = w.test_key_of[shownKey], shown = candidateByKey(result, shownKey);
    return { selectedKey: sel.key, shownKey: shownKey, shownName: candidateName(shown), testKey: testKey,
      sharedWith: testKey !== shownKey ? candidateName(candidateByKey(result, testKey)) : null,
      roles: winnerRoles(result, shownKey), hint: hint, test: result.test[testKey] };
  }

  /* One row per method: its CV winner (training CV) and that winner's exploratory test numbers. Only
   * winners have test numbers; a method without a VALID candidate has no winner and no numbers. */
  function compareRows(result) {
    var w = result.winners;
    return METHOD_ORDER.map(function (m) {
      var mw = w.method_winners[m];
      if (!mw) return { method: m, label: methodLabel(m), winner: null, note: '沒有有效（VALID）的候選，沒有 CV winner' };
      var c = candidateByKey(result, mw.key), tk = w.test_key_of[mw.key], t = result.test[tk];
      return { method: m, label: methodLabel(m), winner: mw.key, k: mw.k, groups: c.canonical_groups.slice(), cv: c.cv,
        test: t.metrics, coverage: t.coverage, n_covered: t.n_covered, n_test: t.n_test,
        isOverall: w.overall.key === mw.key && w.overall.method === m,
        sharedWith: tk !== mw.key ? candidateName(candidateByKey(result, tk)) : null };
    });
  }

  /* Training-CV metric vs k for one method (null where the candidate is not VALID). */
  function kSeries(result, method, metric) {
    var mw = result.winners.method_winners[method];
    return result.candidates.filter(function (c) { return c.method === method; }).map(function (c) {
      return { key: c.key, k: c.k, status: c.status, value: c.status === 'VALID' ? c.cv.mean[metric] : null,
        isWinner: !!(mw && mw.key === c.key) };
    });
  }

  function coefText(v) {
    var a = Math.abs(v), s = String(Number(a.toPrecision(4)));
    return (v < 0 ? '− ' : '+ ') + (s === '1' ? '' : s + '·');
  }
  function columnText(c) { return c.intercept ? '截距' : c.level === null ? c.group : c.group + '＝' + c.level; }

  /* The dependency diagnostic as text: one relation per line, every column it involves (A-3). */
  function dependencyView(result) {
    var deps = result.dependencies;
    if (!deps) return { rank: null, n_columns: null, relations: [] };
    return { rank: deps.rank, n_columns: deps.n_columns, relations: deps.relations.map(function (r) {
      var text = r.columns.map(function (c, i) {
        var t = coefText(c.coef) + columnText(c);
        return i === 0 ? t.replace(/^\+ /, '') : t;
      }).join(' ') + ' ≈ 0';
      return { formula: text, columns: r.columns.map(columnText), groups: r.feature_groups.slice(), includesIntercept: r.includes_intercept };
    }) };
  }

  /* The Lasso path of the training set as rows: the actual path, then the groups shown after it. */
  function lassoView(result) {
    var info = result.lasso_path ? result.lasso_path.canonical : null;
    if (!info) return null;
    var rows = info.entries.map(function (e, i) {
      return { position: i + 1, group: e.group, alpha: e.entry_alpha, state: '實際路徑' };
    }).concat(info.not_entered.map(function (g) {
      return { position: null, group: g, alpha: null, state: info.degenerate ? '未進入（退化後，只作展示）' : '未進入' };
    }));
    var summary = info.degenerate
      ? '路徑在加入第 ' + (info.n_entered + 1) + ' 個 feature group 前停止（' + causeText(info.cause) + '）：只有前 ' +
        info.n_entered + ' 個 group 是實際路徑，k ≥ ' + info.first_invalid_k + ' 的 Lasso 候選無效。'
      : '全部 ' + info.n_entered + ' 個 feature group 都進入路徑，沒有退化。';
    var folds = result.lasso_path.folds.filter(function (f) { return f.degenerate; }).length;
    if (folds) summary += '另有 ' + folds + ' 個 fold 的路徑退化（見各候選的原因）。';
    return { rows: rows, summary: summary, degenerate: info.degenerate };
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
    specs.forEach(function (s) {       /* own keys only: a column may be called `__proto__` (#74 R1-F2) */
      var given = raw instanceof Map ? raw.get(s.name) : engine.getOwn(raw, s.name);
      engine.putOwn(values, s.name, given !== undefined && given !== null ? given : s.default);
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
    var custom = null;      /* this visit's custom dataset: content, target, a URL read in progress */
    var generation = 0;     /* bumped by every selection and submission; an older read's late answer is dropped */

    function emptyCustom() {
      return { source: null, label: null, input: null, columns: null, target: null, busy: false, cancel: null };
    }

    /* What the input panel shows: the entrance, whether a read is in progress, the columns (for the
     * target drop-down) and the effective target (default: the last column). Plain values only. */
    function panelView() {
      var c = custom || emptyCustom();
      var cols = c.columns ? c.columns.map(function (col) { return { name: col.name, index: col.index, type: col.type }; }) : null;
      var target = c.target !== null ? c.target : cols && cols.length ? cols.length - 1 : null;
      return { busy: c.busy, source: c.source, label: c.label, hasData: c.input !== null, columns: cols, target: target };
    }

    function inspect(input, target) {
      var options = target === null || target === undefined ? {} : { target: target };
      if (deps.loader.inspectCsv) return deps.loader.inspectCsv(input, options);
      return { load: deps.loader.loadCsv(input, options), columns: null };
    }

    function runInput(input, source, problem, target) {
      var t0 = now();
      var inspected = inspect(input, target);
      var load = inspected.load;
      var out = { problem: problem, source: source, load: load, result: null, ms: null };
      if (load.ok) out.result = deps.engine.run(load, { problem: problem, source: source, now: deps.now });
      out.ms = now() - t0;
      state.runs++;
      return { run: out, columns: inspected.columns };
    }

    /* Leaving the custom dataset (or replacing its submission): abort a read in progress and forget
     * the content; nothing of it is kept anywhere. */
    function leaveCustom() {
      generation++;
      if (custom && custom.cancel) custom.cancel();
      custom = null;
    }

    function init() {
      leaveCustom();
      state.problem = 'king_county';
      deps.render({ mode: 'king_county', problem: 'king_county' });
    }

    function selectProblem(problem) {
      if (PROBLEMS.indexOf(problem) < 0) throw new Error('unknown problem ' + problem);
      leaveCustom();
      state.problem = problem;
      if (problem === 'king_county') { deps.render({ mode: 'king_county', problem: problem }); return null; }
      if (problem === 'custom') {
        custom = emptyCustom();
        deps.render({ mode: 'custom', problem: problem, custom: panelView() });
        return null;
      }
      var ds = deps.datasets && deps.datasets.startups50;
      if (!ds || typeof ds.csv !== 'string') {
        deps.render({ mode: 'error', problem: problem, message: '找不到內建的 50 Startups 資料（assets/data/startups50.js）。' });
        return null;
      }
      var run = runInput(ds.csv, 'builtin', problem, null).run;
      state.lastExplore = run;
      if (state.problem === problem) deps.render({ mode: 'explore', problem: problem, run: run });
      return run;
    }

    function runCustom() {
      var out = runInput(custom.input, custom.source, 'custom', custom.target);
      if (out.columns) custom.columns = out.columns;
      out.run.label = custom.label;
      state.lastExplore = out.run;
      deps.render({ mode: 'explore', problem: 'custom', run: out.run, custom: panelView() });
      return out.run;
    }

    /* A local file's content (bytes or text): no network. */
    function submitData(input, info) {
      info = info || {};
      leaveCustom();
      state.problem = 'custom';
      custom = emptyCustom();
      custom.input = input;
      custom.source = info.source || 'file';
      custom.label = info.label === undefined || info.label === null ? null : String(info.label);
      return runCustom();
    }

    function loadText(text, source) { return submitData(String(text), { source: source || 'file' }); }

    /* Another target column for the content already read: runs again, never reads the URL again. */
    function setTarget(index) {
      if (state.problem !== 'custom' || !custom || custom.input === null || custom.busy) return null;
      var i = Number(index);
      if (!custom.columns || Math.floor(i) !== i || i < 0 || i >= custom.columns.length) return null;
      custom.target = i;
      return runCustom();
    }

    /* The URL entrance: one read of the submitted URL (the loader's fetchCsvBytes; DA D-1). Returns a
     * Promise of the run, or null when the input was refused before any request or the answer arrived
     * after the user had moved on. */
    function submitUrl(text) {
      leaveCustom();
      state.problem = 'custom';
      custom = emptyCustom();
      var gen = generation;
      var checked = deps.loader.checkUrl(text);
      if (!checked.ok) {
        deps.render({ mode: 'custom', problem: 'custom', custom: panelView(),
          notice: { kind: 'error', text: urlInputText(checked.problem) } });
        return Promise.resolve(null);
      }
      var abort = typeof AbortController === 'function' ? new AbortController() : null;
      custom.source = 'url';
      custom.label = checked.url;
      custom.busy = true;
      custom.cancel = function () { if (abort) abort.abort(); };
      deps.render({ mode: 'custom', problem: 'custom', custom: panelView(),
        notice: { kind: 'info', text: '讀取中：對這個 URL 發出一次 GET（不帶憑證、不跟隨重新導向、不重試）。' } });
      return deps.loader.fetchCsvBytes(checked.url, { fetchImpl: deps.fetchImpl, signal: abort ? abort.signal : null,
        timeoutMs: deps.urlTimeoutMs }).then(function (got) {
        if (gen !== generation || state.problem !== 'custom' || !custom) return null;   /* superseded: dropped */
        custom.busy = false;
        custom.cancel = null;
        if (!got.ok && (got.cancelled || got.input_error)) {
          deps.render({ mode: 'custom', problem: 'custom', custom: panelView(),
            notice: got.input_error ? { kind: 'error', text: urlInputText(got.input_error) } : null });
          return null;
        }
        if (!got.ok) {
          var run = { problem: 'custom', source: 'url', label: custom.label, load: got, result: null, ms: null };
          state.lastExplore = run;
          deps.render({ mode: 'explore', problem: 'custom', run: run, custom: panelView() });
          return run;
        }
        custom.input = got.bytes;
        return runCustom();
      });
    }

    return { init: init, selectProblem: selectProblem, loadText: loadText, submitData: submitData,
      submitUrl: submitUrl, setTarget: setTarget, custom: panelView,
      state: function () { return { problem: state.problem, runs: state.runs, hasResult: !!state.lastExplore }; } };
  }

  return {
    PROBLEMS: PROBLEMS, PROBLEM_TITLES: PROBLEM_TITLES, EXPLORE_LABEL: EXPLORE_LABEL, CV_LABEL: CV_LABEL,
    TEST_LABEL: TEST_LABEL, FILE_GUIDE: FILE_GUIDE,
    METHOD_ORDER: METHOD_ORDER, METHOD_LABELS: METHOD_LABELS,
    statusText: statusText, columnStatusText: columnStatusText, loadReasonText: loadReasonText,
    loadFailureText: loadFailureText, urlCauseText: urlCauseText, urlInputText: urlInputText,
    runReasonText: runReasonText, reasonText: reasonText, warningText: warningText, methodLabel: methodLabel,
    causeText: causeText, candidateName: candidateName, candidateByKey: candidateByKey, defaultKey: defaultKey,
    winnerRoles: winnerRoles, testView: testView, compareRows: compareRows, kSeries: kSeries,
    dependencyView: dependencyView, lassoView: lassoView,
    predictorView: predictorView, createController: createController
  };
});
