// Node test of #77 (V2-T4): the computing budget, failure isolation, cancellation, one run at a time,
// progress and reproducibility of the Exploratory run, and the target-unit independence of its path
// criteria (Spec V2 「候選有效性、狀態與運算預算」 SR-V2-03, 「可重現性」 SR-V2-04, 主 seam 「取消與失敗」;
// Tickets Review adjustment B; DA decision-20261022-issue75-lasso-early-stop R4-2, R4-3, R4-4; DA G-4).
//
//   node --test tests/js/explore_run.test.js
//
// The engine's options.hooks count the work actually started (candidates, fold fits, path computations)
// and throw to inject a failure; options.onProgress sees every candidate boundary. The scheduled
// controller is driven by a manual scheduler and a counting clock (one engine step per time slice), so
// the order of runs, cancellations and results is observable event by event (deps.trace). These are
// tests of the result contract and of the controller; that the page itself stays operable is checked in
// the browser (ACCEPTANCE V2-29), not here.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const L = require('../../assets/explore_load.js');
const E = require('../../assets/explore_engine.js');
const A = require('../../assets/explore_app.js');

const UNIT = path.join(__dirname, '..', '..');
const CSV_BYTES = new Uint8Array(fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv')));
const CSV_TEXT = new TextDecoder().decode(CSV_BYTES);
function startups() {
  const text = fs.readFileSync(path.join(UNIT, 'assets', 'data', 'startups50.js'), 'utf8');
  const marker = 'window.HW2_STARTUPS50 = ';
  return JSON.parse(text.slice(text.indexOf(marker) + marker.length).trim().replace(/;$/, ''));
}
function csvOf(header, rows) { return header.join(',') + '\n' + rows.map((r) => r.join(',')).join('\n') + '\n'; }
function load(text) { const r = L.loadCsv(text); assert.equal(r.ok, true, JSON.stringify(r)); return r; }

/* Mixed data: three numeric columns, one categorical (as tests/js/explore_methods.test.js). */
function mixedRows(seed, n) {
  const next = E.mulberry32(seed), u = () => next() / 4294967296, rows = [];
  for (let i = 0; i < (n || 90); i++) {
    const a = Math.round(u() * 1000) / 10, b = Math.round((u() - 0.5) * 600) / 10, c = Math.round(u() * 100) / 100;
    const cat = ['n', 's', 'e', 'w'][Math.floor(u() * 4)];
    const y = 2 * a - 1.5 * b + 30 * c + { n: 0, s: 8, e: -5, w: 2 }[cat] + (u() - 0.5) * 30;
    rows.push([a, b, c, cat, Math.round(y * 1000) / 1000]);
  }
  return rows;
}
const MIXED = ['a', 'b', 'c', 'cat', 'y'];
const MIXED_LOAD = load(csvOf(MIXED, mixedRows(77)));
const S50 = load(CSV_BYTES);

/* The deterministic part (Spec V2 「可重現性」): everything except meta.timing_ms. */
function det(result) {
  const copy = structuredClone(result);
  delete copy.meta.timing_ms;
  return copy;
}
function counter() {
  const counts = { candidate: [], fold: [], path: [] };
  return {
    counts,
    hooks: {
      candidate: (m, k) => counts.candidate.push(m + ':' + k),
      fold: (m, k, f) => counts.fold.push(m + ':' + k + ':' + f),
      path: (m, s) => counts.path.push(m + ':' + s)
    }
  };
}
const byMethod = (list, m) => list.filter((x) => x.startsWith(m + ':'));
function drive(run) { while (!run.step().done) { /* to the end */ } return run.result(); }

/* ---- the computing budget ------------------------------------------------------------------------ */
test('budget: an injected small budget skips whole methods before they run (counted); All-in and the others run', () => {
  const full = E.run(MIXED_LOAD);
  const { counts, hooks } = counter();
  const res = E.run(MIXED_LOAD, { budgets: { forward_sfs: 0, lasso_path: 1 }, hooks });
  assert.equal(res.run.status, 'COMPLETED');
  const p = res.groups.length;
  // nothing of the skipped methods was started: no path, no candidate, no fold fit
  for (const m of ['forward_sfs', 'lasso_path']) {
    assert.deepEqual(byMethod(counts.candidate, m), [], m + ' candidates');
    assert.deepEqual(byMethod(counts.path, m), [], m + ' paths');
    assert.deepEqual(byMethod(counts.fold, m), [], m + ' fits');
    const list = res.candidates.filter((c) => c.method === m);
    assert.equal(list.length, p);
    list.forEach((c) => {
      assert.equal(c.status, 'SKIPPED_RESOURCE_LIMIT');
      assert.deepEqual(c.reasons, [{ rule: 'resource_limit', scope: 'method', fold: null,
        estimate: res.meta.budget.estimates[m], budget: m === 'forward_sfs' ? 0 : 1 }]);
      assert.equal(c.cv, null); assert.equal(c.fit, null); assert.equal(c.canonical_groups, null); assert.deepEqual(c.folds, []);
      assert.equal(E.canPredict(c), false);
    });
  }
  assert.equal(res.lasso_path, null);
  // All-in is attempted (never skipped) and the other methods run in full
  assert.deepEqual(byMethod(counts.candidate, 'allin'), ['allin:' + p]);
  assert.equal(byMethod(counts.candidate, 'backward_sfs').length, p);
  assert.equal(byMethod(counts.candidate, 'rfe').length, p);
  // the executed candidates are exactly those of the run without the small budgets
  res.candidates.filter((c) => c.status !== 'SKIPPED_RESOURCE_LIMIT').forEach((c) => {
    assert.deepEqual(c, full.candidates.find((x) => x.key === c.key), c.key);
  });
  // winners only from executed VALID candidates
  assert.equal(res.winners.method_winners.forward_sfs, null);
  assert.equal(res.winners.method_winners.lasso_path, null);
  Object.keys(res.winners.test_key_of).forEach((k) => assert.equal(res.candidates.find((c) => c.key === k).status, 'VALID'));
  assert.ok(['allin', 'backward_sfs', 'rfe'].includes(res.winners.overall.method));
});

test('budget: the decision uses the estimate only -- the same with any clock, and > budget (not >=) skips', () => {
  const est = E.run(MIXED_LOAD).meta.budget.estimates.rfe;
  let t = 0;
  const slow = E.run(MIXED_LOAD, { budgets: { rfe: est }, now: () => (t += 1e9) });          // a clock that races
  const fast = E.run(MIXED_LOAD, { budgets: { rfe: est }, now: () => 0 });                   // a clock that stops
  assert.deepEqual(det(slow), det(fast));
  assert.ok(slow.candidates.filter((c) => c.method === 'rfe').every((c) => c.status === 'VALID'));  // est == budget: runs
  const over = E.run(MIXED_LOAD, { budgets: { rfe: est - 1 } });
  assert.ok(over.candidates.filter((c) => c.method === 'rfe').every((c) => c.status === 'SKIPPED_RESOURCE_LIMIT'));
  assert.deepEqual(det(E.run(MIXED_LOAD, { budgets: { rfe: est - 1 } })), det(over));       // same input, same decision
  assert.deepEqual(E.resourceEstimates(over.meta.budget.n_train, over.meta.budget.encoded_columns, over.meta.budget.feature_groups),
    over.meta.budget.estimates);
});

test('G-4: under the final budget constants 50 Startups runs all five methods; every candidate VALID', () => {
  const res = E.run(S50);
  assert.deepEqual(res.meta.budget.constants, E.BUDGETS);
  assert.equal(res.meta.budget.unit, E.BUDGET_UNIT);
  E.PATH_METHODS.forEach((m) => assert.ok(res.meta.budget.estimates[m] <= E.BUDGETS[m], m));
  assert.equal(res.candidates.length, 17);
  assert.ok(res.candidates.every((c) => c.status === 'VALID'));
  assert.equal(res.lasso_path.canonical.degenerate, false);
});

/* ---- failure isolation --------------------------------------------------------------------------- */
test('failure: an exception in one candidate makes that whole method FAILED with its message; the others complete', () => {
  const full = E.run(MIXED_LOAD);
  const hooks = { candidate: (m, k) => { if (m === 'rfe' && k === 2) throw new RangeError('Array buffer allocation failed'); } };
  const res = E.run(MIXED_LOAD, { hooks });
  assert.equal(res.run.status, 'COMPLETED');
  const rfe = res.candidates.filter((c) => c.method === 'rfe');
  assert.equal(rfe.length, res.groups.length);
  rfe.forEach((c) => {
    assert.equal(c.status, 'FAILED');
    assert.equal(c.reasons.length, 1);
    const r = c.reasons[0];
    assert.equal(r.rule, 'unexpected_error'); assert.equal(r.scope, 'method'); assert.equal(r.k, 2);
    assert.equal(r.error, 'RangeError'); assert.equal(r.message, 'Array buffer allocation failed');
    assert.equal(r.environment.engine_version, E.ENGINE_VERSION);
    assert.ok(r.environment.user_agent || r.environment.runtime, 'environment information');
    assert.equal(c.cv, null); assert.equal(c.fit, null); assert.equal(c.canonical_groups, null);
    assert.equal(E.canPredict(c), false);
  });
  res.candidates.filter((c) => c.method !== 'rfe').forEach((c) => {
    assert.deepEqual(c, full.candidates.find((x) => x.key === c.key), c.key);
  });
  assert.equal(res.winners.method_winners.rfe, null);
  assert.notEqual(res.winners.overall.method, 'rfe');
  assert.ok(Object.keys(res.winners.test_key_of).every((k) => !k.startsWith('rfe_')));
});

test('failure: in a path computation, in All-in, and in every method (then the run is rejected)', () => {
  const pathFail = E.run(MIXED_LOAD, { hooks: { path: (m, s) => { if (m === 'backward_sfs' && s === 'training_set') throw new Error('boom'); } } });
  assert.ok(pathFail.candidates.filter((c) => c.method === 'backward_sfs').every((c) => c.status === 'FAILED' && c.reasons[0].k === 1));
  assert.ok(pathFail.candidates.filter((c) => c.method === 'forward_sfs').every((c) => c.status === 'VALID'));
  const allinFail = E.run(MIXED_LOAD, { hooks: { fold: (m, k, f) => { if (m === 'allin' && f === 3) throw new Error('allin boom'); } } });
  assert.equal(allinFail.candidates[0].status, 'FAILED');
  assert.equal(allinFail.candidates[0].reasons[0].message, 'allin boom');
  assert.equal(allinFail.winners.method_winners.allin, null);
  assert.equal(allinFail.run.status, 'COMPLETED');
  const none = E.run(MIXED_LOAD, { hooks: { candidate: () => { throw new Error('nothing works'); } } });
  assert.equal(none.run.status, 'REJECTED');
  assert.equal(none.run.reason, 'ALL_CANDIDATES_INVALID');
  assert.ok(none.run.invalid_candidates.every((c) => c.status === 'FAILED'));
  for (const k of ['candidates', 'winners', 'test']) assert.ok(!(k in none));
});

/* ---- cancellation: at the next candidate boundary -------------------------------------------------- */
test('cancel after the n-th candidate: the run stops at that boundary, CANCELLED, no partial result (counted)', () => {
  const total = 1 + 4 * MIXED_LOAD.columns.filter((c) => c.index !== MIXED_LOAD.target.index).length;
  for (const n of [0, 1, 2, 5, 9, total - 1]) {
    const { counts, hooks } = counter();
    const events = [];
    const run = E.createRun(MIXED_LOAD, { hooks, onProgress: (e) => {
      events.push(e);
      if (e.candidates_done === n && e.phase !== 'diagnostic') run.cancel();
    } });
    const res = drive(run);
    assert.equal(res.run.status, 'CANCELLED', 'n = ' + n);
    assert.equal(res.run.candidates_completed, n);
    assert.equal(res.run.candidates_total, total);
    assert.equal(counts.candidate.length, n, 'no candidate after the boundary was started (n = ' + n + ')');
    assert.equal(res.run.methods_completed, events.at(-1).methods_done);
    for (const k of ['candidates', 'winners', 'test', 'columns', 'groups', 'split', 'lasso_path', 'dependencies']) {
      assert.ok(!(k in res), 'n = ' + n + ': CANCELLED has no ' + k);
    }
    assert.equal(res.meta.sha256, MIXED_LOAD.sha256);
  }
});

test('cancel requested in the middle of a candidate: that candidate is finished, then the run stops (never cut)', () => {
  const { counts, hooks } = counter();
  let run;
  hooks.fold = ((orig) => (m, k, f) => { orig(m, k, f); if (m === 'backward_sfs' && k === 2 && f === 1) run.cancel(); })(hooks.fold);
  run = E.createRun(MIXED_LOAD, { hooks });
  const res = drive(run);
  assert.equal(res.run.status, 'CANCELLED');
  // backward k = 2 ran its five folds and the training-set fit, and nothing started after it
  assert.deepEqual(byMethod(counts.fold, 'backward_sfs').filter((x) => x.startsWith('backward_sfs:2:')),
    ['backward_sfs:2:0', 'backward_sfs:2:1', 'backward_sfs:2:2', 'backward_sfs:2:3', 'backward_sfs:2:4', 'backward_sfs:2:training_set']);
  assert.equal(counts.candidate.at(-1), 'backward_sfs:2');
  const p = 4;
  assert.equal(res.run.candidates_completed, 1 + p + 2);
  assert.equal(counts.candidate.length, 1 + p + 2);
  assert.equal(res.run.methods_completed, 2);
});

test('a rerun after a cancellation starts from the beginning and equals an uncancelled run (deterministic part)', () => {
  const run = E.createRun(S50, { onProgress: (e) => { if (e.candidates_done === 6) run.cancel(); } });
  assert.equal(drive(run).run.status, 'CANCELLED');
  const { counts, hooks } = counter();
  const again = E.run(S50, { hooks });
  assert.equal(again.run.status, 'COMPLETED');
  assert.equal(counts.candidate[0], 'allin:4');                    // from the beginning: All-in first
  assert.equal(counts.candidate.length, 17);
  assert.deepEqual(det(again), det(E.run(S50)));
});

/* ---- progress -------------------------------------------------------------------------------------- */
test('progress: an event at the start and at every candidate boundary; counts monotone; ends at 1', () => {
  const events = [];
  const res = E.run(MIXED_LOAD, { budgets: { rfe: 0 }, onProgress: (e) => events.push(e) });
  assert.equal(res.run.status, 'COMPLETED');
  assert.equal(events[0].phase, 'start');
  assert.equal(events[0].candidates_done, 0);
  const total = events[0].candidates_total;
  assert.equal(total, res.candidates.length);
  for (let i = 1; i < events.length; i++) {
    assert.ok(events[i].candidates_done >= events[i - 1].candidates_done);
    assert.ok(events[i].elapsed_ms >= events[i - 1].elapsed_ms);
    assert.equal(events[i].fraction, events[i].candidates_done / total);
  }
  assert.deepEqual(events.filter((e) => e.phase === 'skipped').map((e) => e.method), ['rfe']);
  assert.equal(events.filter((e) => e.phase === 'candidate').length, total - 4);   // rfe's 4 come in one 'skipped'
  assert.equal(events.at(-1).phase, 'diagnostic');
  assert.equal(events.at(-1).fraction, 1);
  assert.equal(events.at(-1).methods_done, 5);
  assert.ok(events.filter((e) => e.phase === 'candidate').every((e) => typeof e.method === 'string' && e.k >= 1));
});

/* ---- reproducibility ----------------------------------------------------------------------------- */
test('reproducibility: the same input twice gives bit-identical deterministic parts; timings are outside it', () => {
  for (const ld of [S50, MIXED_LOAD]) {
    const a = E.run(ld), b = E.run(ld);
    assert.deepStrictEqual(det(a), det(b));                          // Object.is on every number
    assert.ok(typeof a.meta.timing_ms.started_at_epoch_ms === 'number' && typeof a.meta.timing_ms.total === 'number');
    for (const m of E.METHOD_ORDER) assert.equal(typeof a.meta.timing_ms[m], 'number', m);
  }
  // the deterministic part also includes the budget constants: other constants, other (recorded) meta
  const other = E.run(S50, { budgets: { rfe: 1e12 } });
  assert.notDeepEqual(det(other).meta.budget, det(E.run(S50)).meta.budget);
});

/* ---- target units: R4-3, R4-4 (and R4-2's causes) ------------------------------------------------- */
function scaledCsv(text, c) {
  const lines = text.split(/\r?\n/).filter((x) => x.trim());
  return lines[0] + '\n' + lines.slice(1).map((ln) => {
    const cells = ln.split(',');
    cells[cells.length - 1] = String(Number(cells[cells.length - 1]) * c);
    return cells.join(',');
  }).join('\n') + '\n';
}
function unitFree(res) {
  return {
    candidates: res.candidates.map((c) => [c.key, c.status, c.canonical_groups, c.folds.map((f) => f.groups),
      c.reasons.map((r) => [r.rule, r.scope, r.fold, r.cause, r.n_groups_entered])]),
    lasso: [res.lasso_path.canonical].concat(res.lasso_path.folds).map((i) => [i.n_entered, i.cause, i.not_entered,
      i.entries.map((e) => e.group)]),
    winners: res.winners, columns: res.columns, groups: res.groups
  };
}
test('R4-3 / R4-4: multiplying the target by c > 0 leaves every path, stop, cause, state and winner unchanged', () => {
  const cases = [[CSV_TEXT, 'startups50'], [csvOf(MIXED, mixedRows(78)), 'mixed']];
  for (const [text, name] of cases) {
    const base = E.run(load(text));
    for (const c of [1e-12, 1e-10, 1e-9, 1e-6, 1e6]) {
      const res = E.run(load(scaledCsv(text, c)));
      assert.deepEqual(unitFree(res), unitFree(base), name + ' x ' + c);
      const pairs = [[base.lasso_path.canonical, res.lasso_path.canonical]].concat(base.lasso_path.folds.map((f, i) => [f, res.lasso_path.folds[i]]));
      pairs.forEach(([a, b]) => a.entries.forEach((e, i) => {
        const rel = Math.abs(b.entries[i].entry_alpha - e.entry_alpha * c) / Math.abs(e.entry_alpha * c);
        assert.ok(rel <= 1e-9, name + ' x ' + c + ' alpha ' + e.group + ' rel ' + rel);
      }));
    }
  }
});

test('R4-2: an exact fit ends the path with the true cause (path_ended), and the page text claims no collinearity', () => {
  const next = E.mulberry32(84), u = () => next() / 4294967296, rows = [];
  for (let i = 0; i < 60; i++) { const x1 = Math.round(u() * 10000) / 1000, x2 = Math.round(u() * 10000) / 1000; rows.push([x1, x2, 2 * x1 + 3]); }
  const res = E.run(load(csvOf(['x1', 'x2', 'y'], rows)));
  [res.lasso_path.canonical].concat(res.lasso_path.folds).forEach((info) => {
    assert.equal(info.cause, 'path_ended');
    assert.deepEqual(info.not_entered, ['x2']);
    assert.equal(info.n_entered, 1);
  });
  const k2 = res.candidates.find((c) => c.key === 'lasso_path_k02');
  assert.equal(k2.status, 'INVALID_MODEL');
  assert.ok(k2.reasons.every((r) => r.rule === 'lasso_path_degenerate' && r.cause === 'path_ended'));
  const text = A.causeText('path_ended');
  assert.match(text, /走到終點/);
  assert.match(text, /例如/);                                        // possibilities only as examples
  assert.ok(!/^.{0,20}線性相依/.test(text) && text.indexOf('已完全擬合目標') > 0);
  for (const c of ['alpha_increasing', 'max_iter', 'multiple_drops']) assert.match(A.causeText(c), /數值|上限/, c);
  assert.match(A.causeText('target_constant'), /沒有變化/);
  assert.match(A.reasonText(k2.reasons[0]), /停止原因：路徑已走到終點/);
});

test('R4-2: a constant target on the rows has its own cause; nothing is divided by zero', () => {
  const rows = [];
  for (let i = 0; i < 30; i++) rows.push([i % 7, (i * 3) % 5, 5]);
  const res = E.run(load(csvOf(['a', 'b', 'y'], rows)));
  const info = res.lasso_path.canonical;
  assert.equal(info.n_entered, 0);
  assert.equal(info.cause, 'target_constant');
  assert.ok(res.candidates.filter((c) => c.method === 'lasso_path').every((c) => c.status === 'INVALID_MODEL'));
});

/* ---- the scheduled controller: one run at a time -------------------------------------------------- */
function scheduledHarness(extra) {
  const queue = [], views = [], trace = [];
  let clock = 0;
  const net = Object.assign(function (url, init) { net.calls.push({ url, init }); return Promise.resolve({ ok: true, status: 200, statusText: 'OK',
    arrayBuffer: () => Promise.resolve(CSV_BYTES.buffer.slice(CSV_BYTES.byteOffset, CSV_BYTES.byteOffset + CSV_BYTES.byteLength)) }); }, { calls: [] });
  const controller = A.createController(Object.assign({ loader: L, engine: E, datasets: { startups50: startups() },
    render: (v) => views.push(v), trace: (e) => trace.push(e), fetchImpl: net,
    schedule: (fn) => queue.push(fn), sliceMs: 1, now: () => ++clock }, extra || {}));
  const pump = (n) => { let i = 0; while (queue.length && (n === undefined || i < n)) { queue.shift()(); i++; } return i; };
  return { controller, views, trace, queue, pump, net };
}
const tick = () => new Promise((resolve) => setImmediate(resolve));
async function settle(h) { for (let i = 0; i < 200000; i++) { if (!h.pump() && !h.queue.length) { await tick(); if (!h.queue.length) return; } } }
function neverTwoAtOnce(trace) {
  let open = 0;
  trace.forEach((e) => { if (e.type === 'start') open++; if (e.type === 'end') open--; assert.ok(open <= 1, 'two runs in progress'); });
  assert.equal(open, 0);
}

test('scheduled: the run advances in steps; the controller hands control back between them', async () => {
  const h = scheduledHarness();
  const pending = h.controller.selectProblem('startups50');
  assert.ok(pending instanceof Promise);
  assert.equal(h.views.at(-1).mode, 'running');
  assert.equal(h.controller.runState().running, 1);
  let slices = 0;
  while (h.queue.length) { h.pump(1); slices++; }
  const run = await pending;
  assert.ok(slices > 17, 'more time slices than candidates: ' + slices);
  assert.equal(run.result.run.status, 'COMPLETED');
  assert.ok(h.views.some((v) => v.mode === 'progress'));
  assert.equal(h.views.at(-1).mode, 'explore');
  assert.deepEqual(det(run.result), det(E.run(S50, { problem: 'startups50', source: 'builtin' })));
  assert.equal(h.controller.runState().running, null);
});

test('scheduled: a new submission cancels the run in progress at its next boundary, then starts from the beginning', async () => {
  const h = scheduledHarness();
  const first = h.controller.selectProblem('startups50');
  h.pump(12);                                                       // part of the way
  const second = h.controller.submitData(new TextEncoder().encode(csvOf(MIXED, mixedRows(79))), { source: 'file', label: 'm.csv' });
  assert.equal(h.controller.runState().running, 1);                // still the first one until its boundary
  assert.equal(h.controller.runState().waiting, true);
  await settle(h);
  assert.equal(await first, null);                                  // superseded: no result for the page
  const run = await second;
  assert.equal(run.result.run.status, 'COMPLETED');
  assert.deepEqual(h.trace.map((e) => [e.type, e.id, e.status || null]),
    [['start', 1, null], ['cancel', 1, null], ['end', 1, 'CANCELLED'], ['start', 2, null], ['end', 2, 'COMPLETED']]);
  neverTwoAtOnce(h.trace);
  // the cancelled run was never shown; the new one was shown once, from the beginning
  assert.equal(h.views.filter((v) => v.mode === 'explore').length, 1);
  assert.equal(h.views.filter((v) => v.mode === 'explore')[0].run.id, 2);
  assert.deepEqual(det(run.result), det(E.run(load(csvOf(MIXED, mixedRows(79))), { problem: 'custom', source: 'file' })));
});

test('scheduled: several requests while one runs -- only the latest starts; each URL submission reads once', async () => {
  const h = scheduledHarness();
  const a = h.controller.selectProblem('startups50');
  h.pump(5);
  const b = h.controller.selectProblem('startups50');               // rerun: waits for the boundary
  const c = h.controller.submitUrl('https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv');
  assert.equal(h.net.calls.length, 1);
  await settle(h);
  assert.equal(await a, null);
  assert.equal(await b, null);
  const run = await c;
  assert.equal(run.result.run.status, 'COMPLETED');
  assert.equal(run.source, 'url');
  assert.equal(h.net.calls.length, 1);                              // D-1: one read per submission, no retry
  neverTwoAtOnce(h.trace);
  assert.deepEqual(h.trace.filter((e) => e.type === 'end').map((e) => e.status), ['CANCELLED', 'COMPLETED']);
});

test('scheduled: 取消執行 shows CANCELLED with the finished methods and nothing else; a rerun is complete', async () => {
  const h = scheduledHarness();
  const pending = h.controller.selectProblem('startups50');
  h.pump(20);
  assert.equal(h.controller.cancel(), true);
  assert.equal(h.controller.runState().cancelling, true);
  await settle(h);
  const run = await pending;
  const res = run.result;
  assert.equal(res.run.status, 'CANCELLED');
  assert.ok(res.run.candidates_completed < 17);
  for (const k of ['candidates', 'winners', 'test']) assert.ok(!(k in res));
  const last = h.views.at(-1);
  assert.equal(last.mode, 'explore');
  assert.equal(last.run.result.run.status, 'CANCELLED');
  assert.match(A.cancelledText(res.run), /^已取消：.*已完成 \d+／5 個方法/);
  assert.equal(h.controller.cancel(), false);                       // nothing in progress any more
  const again = h.controller.selectProblem('startups50');
  await settle(h);
  const rerun = await again;
  assert.equal(rerun.result.run.status, 'COMPLETED');
  assert.deepEqual(det(rerun.result), det(E.run(S50, { problem: 'startups50', source: 'builtin' })));
  neverTwoAtOnce(h.trace);
});

test('scheduled: 取消執行 while a new request waits for the previous run: the waiting one never starts', async () => {
  const h = scheduledHarness();
  const first = h.controller.selectProblem('startups50');
  h.pump(6);
  const second = h.controller.selectProblem('startups50');         // waits for the first one's boundary
  assert.equal(h.controller.runState().waiting, true);
  assert.equal(h.controller.cancel(), true);
  assert.equal(h.views.at(-1).mode, 'cancelled');
  assert.equal(h.controller.runState().waiting, false);
  await settle(h);
  assert.equal(await first, null);
  assert.equal(await second, null);
  assert.deepEqual(h.trace.map((e) => [e.type, e.id, e.status || null]), [['start', 1, null], ['cancel', 1, null], ['end', 1, 'CANCELLED']]);
  assert.equal(h.views.at(-1).mode, 'cancelled');                  // the stopped run is not shown afterwards
});

test('scheduled: switching to King County during a run cancels it; nothing exploratory is shown afterwards', async () => {
  const h = scheduledHarness();
  const pending = h.controller.selectProblem('startups50');
  h.pump(8);
  h.controller.selectProblem('king_county');
  assert.equal(h.views.at(-1).mode, 'king_county');
  await settle(h);
  assert.equal(await pending, null);
  assert.equal(h.views.at(-1).mode, 'king_county');                // the cancelled run did not take the page back
  assert.deepEqual(h.trace.map((e) => e.type), ['start', 'cancel', 'end']);
  assert.equal(h.trace.at(-1).status, 'CANCELLED');
  assert.ok(!h.views.slice(h.views.findIndex((v) => v.mode === 'king_county')).some((v) => v.mode !== 'king_county'));
});

test('scheduled: the target drop-down during a run cancels it and runs the new target from the beginning (no new read)', async () => {
  const h = scheduledHarness();
  h.controller.selectProblem('custom');
  const first = h.controller.submitUrl('https://example.org/data.csv');
  await tick(); await tick();
  h.pump(6);
  assert.equal(h.controller.runState().running !== null, true);
  const second = h.controller.setTarget(1);                         // Administration, while the Profit run is in progress
  await settle(h);
  assert.equal(await first, null);
  const run = await second;
  assert.equal(run.result.run.status, 'COMPLETED');
  assert.equal(run.result.meta.target, 'Administration');
  assert.equal(h.net.calls.length, 1);
  neverTwoAtOnce(h.trace);
});

test('scheduled: the three entrances give the same deterministic part (shared case with V2-T3)', async () => {
  const h = scheduledHarness();
  const builtin = h.controller.selectProblem('startups50');
  await settle(h);
  const fromFile = h.controller.submitData(CSV_BYTES, { source: 'file', label: '50_Startups.csv' });
  await settle(h);
  const fromUrl = h.controller.submitUrl('https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv');
  await settle(h);
  const runs = [await builtin, await fromFile, await fromUrl];
  const strip = (r) => { const d = det(r.result); delete d.meta.problem; delete d.meta.source; return d; };
  assert.deepStrictEqual(strip(runs[1]), strip(runs[0]));
  assert.deepStrictEqual(strip(runs[2]), strip(runs[0]));
});
