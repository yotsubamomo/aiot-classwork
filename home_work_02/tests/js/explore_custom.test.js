// Node test of the custom dataset (#76 V2-T3; Spec V2 次 seam 「請求隔離（mock fetch）」 fifth path,
// 「載入契約」入口, 「Problem 與頁面結構」 switching; DA derivation D-1, D-2; #74 R1-F2).
//
//   node --test tests/js/explore_custom.test.js
//
// The network function is a mock injected into the controller (and from there into the loader): only a
// submitted URL makes a request, exactly one GET to that URL with credentials 'omit', redirect 'error'
// and no header, never retried; each failure is URL_FETCH_FAILED with its cause and nothing is sent
// again. Local content (bytes or text), the target drop-down and every problem switch make no request.
// The URL, file and built-in entrances give the same deterministic result for the same content. The
// browser files are also run in a vm context whose storage, history and cookie are traps, to show that
// no path stores anything. Column names such as `__proto__` and `constructor` are ordinary names for
// the loader, the engine and the predictor (#74 R1-F2).
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const L = require('../../assets/explore_load.js');
const E = require('../../assets/explore_engine.js');
const A = require('../../assets/explore_app.js');

const UNIT = path.join(__dirname, '..', '..');
const TEACHER_URL = 'https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv';
const CSV_BYTES = new Uint8Array(fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv')));
const STARTUPS_SHA256 = 'c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d';

function startups() {
  const text = fs.readFileSync(path.join(UNIT, 'assets', 'data', 'startups50.js'), 'utf8');
  const marker = 'window.HW2_STARTUPS50 = ';
  return JSON.parse(text.slice(text.indexOf(marker) + marker.length).trim().replace(/;$/, ''));
}

function bodyOf(bytes) { return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength); }
function okResponse(bytes) {
  return { ok: true, status: 200, statusText: 'OK', arrayBuffer: () => Promise.resolve(bodyOf(bytes)) };
}

/* A mock network function: records every call; `answer` decides the outcome of each call. */
function mockFetch(answer) {
  const f = function (url, init) {
    f.calls.push({ url, init });
    return answer(url, init, f.calls.length);
  };
  f.calls = [];
  return f;
}

function harness(answer, extra) {
  const views = [];
  const net = mockFetch(answer || (() => Promise.resolve(okResponse(CSV_BYTES))));
  const controller = A.createController(Object.assign({ loader: L, engine: E, datasets: { startups50: startups() },
    render: (v) => views.push(v), fetchImpl: net }, extra || {}));
  return { controller, views, net };
}

const tick = (ms) => new Promise((resolve) => setTimeout(resolve, ms || 0));

/* The deterministic part of a result (Spec V2 「可重現性」): everything except timings and the entrance labels. */
function deterministic(result) {
  const copy = JSON.parse(JSON.stringify(result));
  delete copy.meta.timing_ms;
  delete copy.meta.problem;
  delete copy.meta.source;
  return copy;
}

test('request isolation, fifth path: a submitted URL gets exactly one GET, without credentials, redirects or headers', async () => {
  const globalSpy = mockFetch(() => Promise.reject(new Error('the global network function must not be used')));
  const saved = globalThis.fetch;
  globalThis.fetch = globalSpy;
  try {
    const { controller, views, net } = harness();
    controller.init();
    controller.selectProblem('custom');
    assert.equal(net.calls.length, 0);                        // selecting the custom dataset requests nothing
    const run = await controller.submitUrl(TEACHER_URL);
    assert.equal(net.calls.length, 1);
    const call = net.calls[0];
    assert.equal(call.url, TEACHER_URL);
    assert.deepEqual(Object.keys(call.init).sort(), ['credentials', 'method', 'redirect', 'signal']);
    assert.equal(call.init.method, 'GET');
    assert.equal(call.init.credentials, 'omit');
    assert.equal(call.init.redirect, 'error');
    assert.ok(!('headers' in call.init) && !('mode' in call.init) && !('body' in call.init));
    assert.equal(run.source, 'url');
    assert.equal(run.label, TEACHER_URL);
    assert.equal(run.load.sha256, STARTUPS_SHA256);
    assert.equal(run.result.run.status, 'COMPLETED');
    assert.equal(views.at(-1).mode, 'explore');
    assert.equal(views.at(-1).custom.hasData, true);
    // what follows on the same content never reads the URL again: another target, the same target, waiting
    controller.setTarget(0);
    controller.setTarget(4);
    await tick(30);
    assert.equal(net.calls.length, 1);
    assert.equal(globalSpy.calls.length, 0);
  } finally {
    globalThis.fetch = saved;
  }
});

test('the loader\'s request init is exactly the D-1 options', () => {
  assert.deepEqual(L.requestInit(null), { method: 'GET', credentials: 'omit', redirect: 'error' });
  const signal = new AbortController().signal;
  assert.deepEqual(L.requestInit(signal), { method: 'GET', credentials: 'omit', redirect: 'error', signal });
});

const FAILURES = [
  ['network (cross-origin refusal, network error or a refused redirect)', () => Promise.reject(new TypeError('Failed to fetch')),
    { cause: 'network' }],
  ['HTTP status', () => Promise.resolve({ ok: false, status: 404, statusText: 'Not Found', arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)) }),
    { cause: 'http_status', status: 404, status_text: 'Not Found' }],
  ['not text', () => Promise.resolve(okResponse(Uint8Array.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d]))),
    { cause: 'not_text', bytes: 12 }],
  ['the network function throws', () => { throw new TypeError('bad request'); }, { cause: 'network' }]
];

for (const [name, answer, detail] of FAILURES) {
  test(`URL failure, ${name}: URL_FETCH_FAILED with its cause, one request, nothing sent again`, async () => {
    const { controller, views, net } = harness(answer);
    controller.selectProblem('custom');
    const run = await controller.submitUrl(TEACHER_URL);
    assert.equal(run.load.ok, false);
    assert.equal(run.load.reason, 'URL_FETCH_FAILED');
    assert.deepEqual(run.load.detail, detail);
    assert.equal(run.result, null);
    assert.equal(views.at(-1).mode, 'explore');
    assert.equal(views.at(-1).custom.hasData, false);
    const text = A.loadFailureText(run.load);
    assert.match(text, /URL_FETCH_FAILED/);
    assert.match(text, /下載該 CSV/);
    assert.match(text, /本機 CSV 檔案/);
    await tick(30);
    assert.equal(net.calls.length, 1);                         // no retry
    assert.equal(controller.setTarget(0), null);               // nothing to run on, and no request either
    // the way out the message gives: the same CSV as a local file succeeds
    const local = controller.submitData(CSV_BYTES, { source: 'file', label: '50_Startups.csv' });
    assert.equal(local.result.run.status, 'COMPLETED');
    assert.equal(local.load.sha256, STARTUPS_SHA256);
    assert.equal(net.calls.length, 1);
  });
}

test('URL failure, timeout: the read is aborted after the time limit and not sent again', async () => {
  let aborted = false;
  const { controller, net } = harness((url, init) => new Promise((resolve, reject) => {
    init.signal.addEventListener('abort', () => { aborted = true; reject(new Error('AbortError')); });
  }), { urlTimeoutMs: 40 });
  controller.selectProblem('custom');
  const run = await controller.submitUrl(TEACHER_URL);
  assert.equal(run.load.reason, 'URL_FETCH_FAILED');
  assert.deepEqual(run.load.detail, { cause: 'timeout', timeout_ms: 40 });
  assert.equal(aborted, true);
  assert.match(A.loadFailureText(run.load), /逾時/);
  await tick(80);
  assert.equal(net.calls.length, 1);
  assert.equal(L.URL_TIMEOUT_MS, 20000);                     // the page's limit (recorded in ACCEPTANCE)
});

test('a body that is text but not UTF-8 is ENCODING, exactly as the same bytes from a local file', async () => {
  const big5 = Uint8Array.from([0xa4, 0xa4, 0xa4, 0xe5, 0x2c, 0x79, 0x0a, 0x31, 0x2c, 0x32, 0x0a]);
  const { controller } = harness(() => Promise.resolve(okResponse(big5)));
  controller.selectProblem('custom');
  const viaUrl = await controller.submitUrl(TEACHER_URL);
  const viaFile = controller.submitData(big5, { source: 'file' });
  assert.equal(viaUrl.load.reason, 'ENCODING');
  assert.deepEqual(viaUrl.load, viaFile.load);
});

test('input that is not an absolute http(s) URL is refused before any request', async () => {
  const { controller, views, net } = harness();
  controller.selectProblem('custom');
  const cases = [['', 'empty'], ['   ', 'empty'], ['assets/data/50_Startups.csv', 'not_absolute_url'],
    ['javascript:alert(1)', 'not_http'], ['data:text/csv,a,y', 'not_http'], ['file:///C:/x.csv', 'not_http'],
    ['ftp://example.org/x.csv', 'not_http'], ['https://user:secret@example.org/x.csv', 'has_credentials']];
  for (const [input, problem] of cases) {
    assert.deepEqual(L.checkUrl(input), { ok: false, problem }, input);
    assert.equal(await controller.submitUrl(input), null);
    assert.equal(views.at(-1).mode, 'custom');
    assert.equal(views.at(-1).notice.kind, 'error');
    assert.equal(views.at(-1).notice.text, A.urlInputText(problem));
  }
  assert.deepEqual(await L.fetchCsvBytes('javascript:alert(1)', { fetchImpl: net }), { ok: false, input_error: 'not_http' });
  assert.equal(net.calls.length, 0);
  assert.deepEqual(L.checkUrl('  ' + TEACHER_URL + '  '), { ok: true, url: TEACHER_URL });
});

test('target column: default last; a categorical target is TARGET_NOT_NUMERIC and does not run; another target runs again', async () => {
  const { controller, views, net } = harness();
  controller.selectProblem('custom');
  const first = await controller.submitUrl(TEACHER_URL);
  assert.equal(first.load.target.name, 'Profit');
  const panel = views.at(-1).custom;
  assert.deepEqual(panel.columns.map((c) => [c.name, c.type]), [['R&D Spend', 'numeric'], ['Administration', 'numeric'],
    ['Marketing Spend', 'numeric'], ['State', 'categorical'], ['Profit', 'numeric']]);
  assert.equal(panel.target, 4);
  const runsBefore = controller.state().runs;
  const cat = controller.setTarget(3);
  assert.equal(cat.load.ok, false);
  assert.equal(cat.load.reason, 'TARGET_NOT_NUMERIC');
  assert.deepEqual(cat.load.detail, { target: 'State', index: 3 });
  assert.equal(cat.result, null);                            // not executed
  assert.match(A.loadFailureText(cat.load), /「State」不是數值欄.*改選數值欄/);
  assert.equal(views.at(-1).custom.target, 3);
  assert.equal(views.at(-1).custom.columns.length, 5);        // the drop-down keeps every column to choose again
  const other = controller.setTarget(1);
  assert.equal(other.result.run.status, 'COMPLETED');
  assert.equal(other.result.meta.target, 'Administration');
  assert.equal(controller.state().runs, runsBefore + 2);
  assert.equal(controller.setTarget(9), null);
  assert.equal(controller.setTarget(1.5), null);
  assert.equal(net.calls.length, 1);
  // a file whose last column is categorical: rejected by default, the columns are still offered
  const text = 'x,z,label\n' + Array.from({ length: 25 }, (_, i) => `${i},${i % 7},${i % 2 ? 'a' : 'b'}`).join('\n');
  const rejected = controller.loadText(text, 'file');
  assert.equal(rejected.load.reason, 'TARGET_NOT_NUMERIC');
  assert.deepEqual(views.at(-1).custom.columns.map((c) => c.name), ['x', 'z', 'label']);
  assert.equal(controller.setTarget(0).result.run.status, 'COMPLETED');
});

test('every load rejection has its own zh-TW message', () => {
  const cases = {
    NOT_CSV: 'a,y\n"x,1\n' + Array.from({ length: 25 }, (_, i) => `${i},${i}`).join('\n'),
    NO_HEADER: '1,2,3\n' + Array.from({ length: 25 }, (_, i) => `${i},${i},${i}`).join('\n'),
    RAGGED_ROWS: 'a,b,y\n' + Array.from({ length: 25 }, (_, i) => `${i},x,${i}`).join('\n') + '\n1,2\n',
    TOO_FEW_ROWS: 'a,y\n' + Array.from({ length: 19 }, (_, i) => `${i},${i}`).join('\n'),
    TARGET_NOT_NUMERIC: 'a,y\n' + Array.from({ length: 25 }, (_, i) => `${i},v${i}`).join('\n'),
    DUPLICATE_COLUMN: 'a, a ,y\n' + Array.from({ length: 25 }, (_, i) => `${i},x,${i}`).join('\n'),
    TOO_LARGE: 'h,' + Array.from({ length: 60 }, (_, i) => 'c' + i).join(',') + '\n'
  };
  const texts = new Set();
  for (const [reason, text] of Object.entries(cases)) {
    const load = L.loadCsv(text);
    assert.equal(load.reason, reason);
    const msg = A.loadFailureText(load);
    assert.match(msg, new RegExp(reason));
    assert.match(msg, /[\u4e00-\u9fff]/);
    texts.add(msg);
  }
  const enc = L.loadCsv(Uint8Array.from([0xff, 0xfe, 0x2c, 0x0a]));
  assert.equal(enc.reason, 'ENCODING');
  texts.add(A.loadFailureText(enc));
  const rows = L.loadCsv('a,y\n' + Array.from({ length: 30 }, (_, i) => `${i},${i}`).join('\n'), { limits: { maxRows: 25 } });
  assert.equal(rows.reason, 'TOO_LARGE');
  assert.match(A.loadFailureText(rows), /25 列/);
  assert.equal(texts.size, 8);
  for (const cause of L.URL_CAUSES) {
    assert.match(A.loadFailureText({ ok: false, reason: 'URL_FETCH_FAILED', detail: { cause, status: 500, timeout_ms: 20000 } }),
      /下載該 CSV/);
  }
  assert.match(A.urlCauseText('network'), /跨來源/);
});

test('the URL, file and built-in entrances give the same deterministic result for the same content', async () => {
  const { controller } = harness();
  const builtin = controller.selectProblem('startups50');
  controller.selectProblem('custom');
  const viaUrl = await controller.submitUrl(TEACHER_URL);
  const viaBytes = controller.submitData(CSV_BYTES, { source: 'file', label: '50_Startups.csv' });
  const viaText = controller.loadText(new TextDecoder().decode(CSV_BYTES), 'file');
  for (const run of [builtin, viaUrl, viaBytes, viaText]) assert.equal(run.load.sha256, STARTUPS_SHA256);
  assert.deepEqual([builtin.source, viaUrl.source, viaBytes.source, viaText.source], ['builtin', 'url', 'file', 'file']);
  const ref = deterministic(builtin.result);
  for (const run of [viaUrl, viaBytes, viaText]) assert.deepEqual(deterministic(run.result), ref);
  assert.equal(viaUrl.result.meta.source, 'url');
  assert.equal(viaBytes.result.meta.problem, 'custom');
});

test('switching King County -> 50 Startups -> custom -> King County; a pending read is aborted and dropped', async () => {
  let release, seenSignal;
  const { controller, views, net } = harness((url, init) => {
    seenSignal = init.signal;
    return new Promise((resolve) => { release = () => resolve(okResponse(CSV_BYTES)); });
  });
  controller.init();
  controller.selectProblem('startups50');
  controller.selectProblem('custom');
  const pending = controller.submitUrl(TEACHER_URL);
  assert.equal(views.at(-1).custom.busy, true);
  controller.selectProblem('king_county');
  assert.equal(seenSignal.aborted, true);                    // leaving the custom dataset aborts the read
  release();
  assert.equal(await pending, null);                         // its late answer is dropped
  assert.equal(views.at(-1).mode, 'king_county');
  assert.equal(views.at(-1).run, undefined);
  controller.selectProblem('custom');                        // selecting it again asks for a new submission
  assert.deepEqual(views.at(-1).custom, { busy: false, source: null, label: null, hasData: false, columns: null, target: null });
  assert.equal(controller.setTarget(0), null);
  // a successful custom run, then King County, then custom again: forgotten
  net.calls.length = 0;
  const ok = controller.submitData(CSV_BYTES, { source: 'file', label: 'a.csv' });
  assert.equal(ok.result.run.status, 'COMPLETED');
  controller.selectProblem('king_county');
  assert.equal(views.at(-1).mode, 'king_county');
  controller.selectProblem('custom');
  assert.equal(views.at(-1).custom.hasData, false);
  controller.selectProblem('startups50');                     // 50 Startups runs again on every selection
  assert.equal(views.at(-1).run.result.run.status, 'COMPLETED');
  assert.equal(net.calls.length, 0);
});

test('a new submission replaces a pending one: one request per submission, the older answer dropped', async () => {
  const releases = [];
  const { controller, views, net } = harness(() => new Promise((resolve) => releases.push(() => resolve(okResponse(CSV_BYTES)))));
  controller.selectProblem('custom');
  const first = controller.submitUrl(TEACHER_URL);
  const second = controller.submitUrl(TEACHER_URL);
  assert.equal(net.calls.length, 2);
  assert.equal(net.calls[0].init.signal.aborted, true);
  releases[0]();
  releases[1]();
  assert.equal(await first, null);
  const run = await second;
  assert.equal(run.result.run.status, 'COMPLETED');
  assert.equal(views.filter((v) => v.mode === 'explore').length, 1);
  const local = controller.submitData(CSV_BYTES, { source: 'file' });     // a file replaces a finished URL run too
  assert.equal(local.source, 'file');
  assert.equal(net.calls.length, 2);
});

test('nothing is stored: storage, history, cookie and the address are never touched (vm, traps)', async () => {
  const touched = [];
  const trapObject = (name) => new Proxy({}, { get(t, k) { touched.push(name + '.' + String(k)); return () => null; },
    set(t, k) { touched.push(name + '.' + String(k) + '='); return true; } });
  const net = mockFetch(() => Promise.resolve(okResponse(CSV_BYTES)));
  const doc = {};
  Object.defineProperty(doc, 'cookie', { get() { touched.push('cookie'); return ''; }, set() { touched.push('cookie='); } });
  const win = { localStorage: trapObject('localStorage'), sessionStorage: trapObject('sessionStorage'),
    indexedDB: trapObject('indexedDB'), history: trapObject('history'), document: doc, URL, TextEncoder, TextDecoder,
    AbortController, setTimeout, clearTimeout, Promise };
  win.window = win; win.self = win;
  const ctx = vm.createContext(win);
  for (const f of ['assets/data/startups50.js', 'assets/explore_load.js', 'assets/explore_engine.js', 'assets/explore_app.js']) {
    vm.runInContext(fs.readFileSync(path.join(UNIT, f), 'utf8'), ctx, { filename: f });
  }
  const views = [];
  const c = win.HW2ExploreApp.createController({ loader: win.HW2ExploreLoad, engine: win.HW2ExploreEngine,
    datasets: { startups50: win.HW2_STARTUPS50 }, render: (v) => views.push(v), fetchImpl: net });
  c.init(); c.selectProblem('startups50'); c.selectProblem('custom');
  const run = await c.submitUrl(TEACHER_URL);
  assert.equal(run.result.run.status, 'COMPLETED');
  c.setTarget(1); c.submitData(CSV_BYTES, { source: 'file', label: 'x.csv' }); c.loadText(win.HW2_STARTUPS50.csv, 'file');
  c.selectProblem('king_county'); c.selectProblem('custom');
  const failing = win.HW2ExploreApp.createController({ loader: win.HW2ExploreLoad, engine: win.HW2ExploreEngine,
    datasets: {}, render: () => {}, fetchImpl: mockFetch(() => Promise.reject(new TypeError('x'))) });
  await failing.submitUrl(TEACHER_URL);
  assert.deepEqual(touched, []);
  assert.equal(net.calls.length, 1);
});

test('#74 R1-F2: `__proto__`, `constructor`, `toString` are ordinary column names for the loader, the engine and the predictor', () => {
  assert.deepEqual(L.loadCsv('__proto__,__proto__,y\n' + Array.from({ length: 25 }, (_, i) => `${i},x,${i}`).join('\n')),
    { ok: false, reason: 'DUPLICATE_COLUMN', detail: { name: '__proto__', columns: [0, 1] },
      sha256: L.loadCsv('__proto__,__proto__,y\n' + Array.from({ length: 25 }, (_, i) => `${i},x,${i}`).join('\n')).sha256 });
  const next = E.mulberry32(76), u = () => next() / 4294967296;
  const rows = [];
  for (let i = 0; i < 60; i++) {
    const a = Math.round(u() * 5000) / 100, b = Math.round(u() * 300) / 10, lv = ['__proto__', 'constructor', 'plain'][i % 3];
    const effect = lv === 'plain' ? 5 : lv === 'constructor' ? -3 : 0;
    rows.push([a, b, lv, Math.round((2 * a - b + effect + (u() - 0.5)) * 1000) / 1000]);
  }
  const csv = 'constructor,toString,__proto__,y\n' + rows.map((r) => r.join(',')).join('\n') + '\n';
  const load = L.loadCsv(csv);
  assert.equal(load.ok, true);
  const result = E.run(load);
  assert.equal(result.run.status, 'COMPLETED');
  const allin = result.candidates[0];
  assert.deepEqual(Object.keys(allin.fit.levels), ['__proto__']);
  assert.deepEqual(Object.keys(allin.fit.inputs), ['constructor', 'toString']);
  assert.ok(Object.prototype.hasOwnProperty.call(allin.fit.levels, '__proto__'));
  assert.equal(Object.getPrototypeOf(allin.fit.levels), Object.prototype);
  assert.deepEqual(JSON.parse(JSON.stringify(allin.fit.levels)).__proto__.levels.slice().sort(), ['__proto__', 'constructor', 'plain']);
  const specs = E.inputSpec(allin.fit);
  assert.deepEqual(specs.map((s) => [s.name, s.type]), [['constructor', 'numeric'], ['toString', 'numeric'], ['__proto__', 'categorical']]);
  const view = A.predictorView(E, allin, {});
  assert.equal(view.enabled, true);
  assert.ok(Number.isFinite(view.predicted) && view.lower < view.predicted && view.predicted < view.upper);
  assert.deepEqual(view.warnings, []);
  const raw = {};
  E.putOwn(raw, 'constructor', '10'); E.putOwn(raw, 'toString', '12'); E.putOwn(raw, '__proto__', 'plain');
  const plain = A.predictorView(E, allin, raw);
  const viaMap = A.predictorView(E, allin, new Map([['constructor', '10'], ['toString', '12'], ['__proto__', 'plain']]));
  assert.equal(plain.predicted, viaMap.predicted);
  E.putOwn(raw, '__proto__', 'constructor');
  assert.notEqual(A.predictorView(E, allin, raw).predicted, plain.predicted);
  E.putOwn(raw, '__proto__', 'unseen-level');
  assert.deepEqual(A.predictorView(E, allin, raw).warnings.length, 1);
  // test rows' unseen counts are own keys too
  Object.values(result.test).forEach((t) => assert.equal(Object.getPrototypeOf(t.n_unseen_by_group), Object.prototype));
});
