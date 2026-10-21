// Node test of the problem controller and the live predictor (assets/explore_app.js; Spec V2 次 seam
// 「請求隔離（mock fetch）」 first four paths, and 「即時預測器」).
//
//   node --test tests/js/explore_app.test.js
//
// Request isolation: with an injected network function and a global one, both spies, the four paths of
// #74 make no request — initialisation, selecting King County, selecting 50 Startups, loading local text.
// The browser files are also loaded as they are on the page (vm, with a window whose network APIs are
// spies) to check that loading them requests nothing.
// Live predictor: only a VALID candidate predicts; numeric inputs default to the training median and an
// out-of-range value is still computed with a warning; a categorical drop-down lists the training levels
// (baseline included) and an unseen level is computed as the baseline with a warning; a non-VALID
// candidate disables the predictor with its status and reason and gives no number.
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
function startups() {
  const text = fs.readFileSync(path.join(UNIT, 'assets', 'data', 'startups50.js'), 'utf8');
  const marker = 'window.HW2_STARTUPS50 = ';
  return JSON.parse(text.slice(text.indexOf(marker) + marker.length).trim().replace(/;$/, ''));
}

function spy() {
  const f = function () { f.calls.push(Array.from(arguments)); return Promise.reject(new Error('network is not allowed in this test')); };
  f.calls = [];
  return f;
}

function harness() {
  const views = [];
  const injected = spy();
  const controller = A.createController({ loader: L, engine: E, datasets: { startups50: startups() },
    render: (v) => views.push(v), fetchImpl: injected });
  return { controller, views, injected };
}

test('request isolation: init, King County, 50 Startups and local text make no request', () => {
  const globalSpy = spy();
  const saved = globalThis.fetch;
  globalThis.fetch = globalSpy;
  try {
    const { controller, views, injected } = harness();
    controller.init();
    assert.equal(views.at(-1).mode, 'king_county');
    controller.selectProblem('king_county');
    assert.equal(views.at(-1).mode, 'king_county');
    const run = controller.selectProblem('startups50');
    assert.equal(views.at(-1).mode, 'explore');
    assert.equal(run.result.run.status, 'COMPLETED');
    assert.equal(run.source, 'builtin');
    const csv = fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv'), 'utf8');
    const local = controller.loadText(csv, 'file');
    assert.equal(local.result.run.status, 'COMPLETED');
    assert.equal(local.load.sha256, run.load.sha256);
    controller.selectProblem('custom');
    assert.equal(views.at(-1).mode, 'custom');
    controller.selectProblem('king_county');
    assert.equal(injected.calls.length, 0);
    assert.equal(globalSpy.calls.length, 0);
  } finally {
    globalThis.fetch = saved;
  }
});

test('the problem switch: 50 Startups runs on every selection; King County keeps the result in memory only', () => {
  const { controller, views } = harness();
  controller.init();
  controller.selectProblem('startups50');
  controller.selectProblem('king_county');
  assert.deepEqual(controller.state(), { problem: 'king_county', runs: 1, hasResult: true });
  assert.equal(views.at(-1).run, undefined);                 // the King County view carries no exploratory result
  controller.selectProblem('startups50');
  assert.equal(controller.state().runs, 2);                  // selected again: run again
  controller.selectProblem('custom');
  assert.equal(controller.state().runs, 2);                  // custom shows the input panel only, runs nothing
  assert.throws(() => controller.selectProblem('other'));
});

test('loading the browser files as the page does requests nothing', () => {
  const calls = [];
  const trap = (name) => function () { calls.push(name); throw new Error(name + ' is not allowed'); };
  const win = { fetch: trap('fetch'), XMLHttpRequest: trap('XMLHttpRequest'), WebSocket: trap('WebSocket'),
    EventSource: trap('EventSource'), navigator: { sendBeacon: trap('sendBeacon') }, importScripts: trap('importScripts') };
  win.window = win; win.self = win;
  const ctx = vm.createContext(win);
  for (const f of ['assets/data/startups50.js', 'assets/explore_load.js', 'assets/explore_engine.js', 'assets/explore_app.js']) {
    vm.runInContext(fs.readFileSync(path.join(UNIT, f), 'utf8'), ctx, { filename: f });
  }
  assert.ok(win.HW2ExploreLoad && win.HW2ExploreEngine && win.HW2ExploreApp && win.HW2_STARTUPS50);
  const views = [];
  const c = win.HW2ExploreApp.createController({ loader: win.HW2ExploreLoad, engine: win.HW2ExploreEngine,
    datasets: { startups50: win.HW2_STARTUPS50 }, render: (v) => views.push(v), fetchImpl: win.fetch });
  c.init(); c.selectProblem('king_county'); c.selectProblem('startups50'); c.loadText(win.HW2_STARTUPS50.csv, 'file');
  assert.equal(views.at(-1).run.result.run.status, 'COMPLETED');
  assert.deepEqual(calls, []);
});

function allin() {
  const load = L.loadCsv(startups().csv);
  return { load, cand: E.run(load).candidates[0] };
}

test('predictor: inputs are the canonical fit\'s groups; numbers default to the training median', () => {
  const { load, cand } = allin();
  const specs = E.inputSpec(cand.fit);
  assert.deepEqual(specs.map((s) => [s.name, s.type]), [['R&D Spend', 'numeric'], ['Administration', 'numeric'],
    ['Marketing Spend', 'numeric'], ['State', 'categorical']]);
  const result = E.run(load);
  const trainRD = result.split.train.map((r) => load.rows[r][0]).sort((a, b) => a - b);
  const median = (trainRD[19] + trainRD[20]) / 2;
  assert.equal(specs[0].median, median);
  assert.equal(specs[0].default, median);
  assert.equal(specs[0].min, trainRD[0]);
  assert.equal(specs[0].max, trainRD[39]);
  const v = A.predictorView(E, cand, {});
  assert.equal(v.enabled, true);
  assert.deepEqual(v.warnings, []);
  assert.ok(v.lower < v.predicted && v.predicted < v.upper);
});

test('predictor: an out-of-range number is still computed, with a warning', () => {
  const { cand } = allin();
  const spec = E.inputSpec(cand.fit)[0];
  const inRange = A.predictorView(E, cand, {});
  const out = A.predictorView(E, cand, { 'R&D Spend': String(spec.max * 3) });
  assert.equal(out.enabled, true);
  assert.equal(out.warnings.length, 1);
  assert.match(out.warnings[0], /超出訓練範圍/);
  assert.ok(Number.isFinite(out.predicted) && out.predicted !== inRange.predicted);
  const raw = E.predict(cand, Object.assign({}, out.values));
  assert.deepEqual(raw.warnings.map((w) => w.type), ['out_of_range']);
});

test('predictor: the drop-down lists the training levels and the baseline; an unseen level is the baseline, with a warning', () => {
  const { cand } = allin();
  const state = E.inputSpec(cand.fit).find((s) => s.name === 'State');
  assert.deepEqual(state.levels.slice().sort(), ['California', 'Florida', 'New York']);
  assert.equal(state.baseline, cand.fit.levels.State.baseline);
  assert.equal(state.levels[0], state.baseline);
  const atBaseline = E.predict(cand, { 'R&D Spend': 1e5, Administration: 1.2e5, 'Marketing Spend': 2e5, State: state.baseline });
  const unseen = E.predict(cand, { 'R&D Spend': 1e5, Administration: 1.2e5, 'Marketing Spend': 2e5, State: 'Texas' });
  assert.equal(unseen.predicted, atBaseline.predicted);
  assert.equal(unseen.lower, atBaseline.lower);
  assert.deepEqual(unseen.warnings.map((w) => [w.type, w.group, w.baseline]), [['unseen_level', 'State', state.baseline]]);
  assert.match(A.warningText(unseen.warnings[0]), /基準層級/);
  const other = E.predict(cand, { 'R&D Spend': 1e5, Administration: 1.2e5, 'Marketing Spend': 2e5, State: state.levels[1] });
  assert.notEqual(other.predicted, atBaseline.predicted);
});

test('predictor: the point and the PI follow the fit (y_hat +/- t * sqrt(s2 (1 + x\'(X\'X)^-1 x)))', () => {
  const { cand } = allin();
  const p = E.predict(cand, { 'R&D Spend': 50000, Administration: 100000, 'Marketing Spend': 150000, State: 'Florida' });
  const f = cand.fit;
  const x = p.design;
  const yhat = x.reduce((s, v, i) => s + v * f.coef[i], 0);
  let q = 0;
  for (let i = 0; i < x.length; i++) for (let j = 0; j < x.length; j++) q += x[i] * f.xtx_inv[i][j] * x[j];
  const half = f.t_crit * Math.sqrt(f.s2 * (1 + q));
  assert.ok(Math.abs(p.predicted - yhat) <= 1e-9 * Math.abs(yhat));
  assert.ok(Math.abs(p.upper - (yhat + half)) <= 1e-9 * Math.abs(yhat + half));
  assert.ok(Math.abs(p.lower - (yhat - half)) <= 1e-9 * Math.abs(yhat - half));
});

test('predictor: a non-VALID candidate disables it with the status and the reason, and gives no number', () => {
  const invalid = { key: 'allin', status: 'INVALID_MODEL', fit: null,
    reasons: [{ rule: 'rank_deficient', scope: 'fold', fold: 2, rank: 2, n_columns: 3, df_resid: 40 }] };
  const v = A.predictorView(E, invalid, {});
  assert.equal(v.enabled, false);
  assert.equal(v.status, 'INVALID_MODEL');
  assert.match(v.statusText, /INVALID_MODEL/);
  assert.deepEqual(v.reasons, ['第 3 個 fold 的訓練列：設計矩陣（含截距）秩不足，rank 2 < 3 欄']);
  assert.ok(!('predicted' in v) && !('lower' in v) && !('upper' in v));
  for (const status of ['SKIPPED_RESOURCE_LIMIT', 'FAILED']) {
    const w = A.predictorView(E, { key: 'x', status, fit: null, reasons: [] }, {});
    assert.equal(w.enabled, false);
    assert.equal(w.status, status);
  }
  assert.throws(() => E.predict(invalid, {}));
  // even a fit object does not make a non-VALID candidate predict
  const { cand } = allin();
  assert.equal(A.predictorView(E, Object.assign({}, cand, { status: 'FAILED' }), {}).enabled, false);
});

test('predictor: a non-number input gives a message, not a prediction', () => {
  const { cand } = allin();
  for (const bad of ['', 'abc', '1e999']) {
    const v = A.predictorView(E, cand, { 'R&D Spend': bad });
    assert.equal(v.predicted, null, bad);
    assert.match(v.error, /有效的數字/);
  }
});
