// Node test of the #75 (V2-T2) method layer of the Exploratory run engine, without the Python reference
// (Spec V2 主 seam 「聚合與凍結」, A-2, the tie rules; 次 seam 「三層邊界」 for the selection paths).
//
//   node --test tests/js/explore_methods.test.js
//
// - Aggregation: on a small case whose fold fits are simple regressions, every fold's metrics are
//   recomputed here by the closed-form slope and intercept, and the CV metrics must be their arithmetic
//   mean and sample standard deviation (SR-V2-02 point 3).
// - Freezing: changing the target of the test rows changes no candidate (state, reasons, folds, CV,
//   canonical subset, fit), no winner, no Lasso path and no dependency; only the test numbers move.
// - Lasso degeneracy (A-2): k beyond the groups the path reached is INVALID_MODEL / lasso_path_degenerate
//   in every fold and on the training set; the groups that did not enter are listed after the path in CSV
//   order and are not part of any subset; exactly tied twin columns enter in CSV order (Spec tie rule).
// - Fold boundary of the paths: a fold's subsets and Lasso entries ignore its validation rows; the
//   canonical subsets ignore the test rows (layer 3 / canonical; the split is injected).
// - Winner ties: equal CV RMSE in a method -> smaller k; between methods -> All-in, Forward, Backward, RFE,
//   Lasso; models with the same canonical subset are scored once.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const L = require('../../assets/explore_load.js');
const E = require('../../assets/explore_engine.js');

const strip = (x) => JSON.parse(JSON.stringify(x));
function load(header, rows) {
  const r = L.loadCsv(header.join(',') + '\n' + rows.map((x) => x.join(',')).join('\n') + '\n');
  assert.equal(r.ok, true, JSON.stringify(r));
  return r;
}

/* ---- aggregation: closed-form simple regressions ------------------------------------------------ */
test('CV metrics are the arithmetic mean (and sample sd) of fold metrics computed by hand', () => {
  const x = [], y = [];
  for (let i = 0; i < 25; i++) { x.push(i + 1); y.push(2 * (i + 1) + [3, -1, 0, 2, -4][i % 5] + (i % 3)); }
  const data = load(['x', 'y'], x.map((v, i) => [v, y[i]]));
  const split = { train: Array.from({ length: 20 }, (_, i) => i), test: [20, 21, 22, 23, 24], folds: [] };
  split.folds = split.train.map((r) => r % 5);
  const res = E.run(data, { split });
  assert.equal(res.run.status, 'COMPLETED');
  const hand = [0, 1, 2, 3, 4].map((f) => {
    const tr = split.train.filter((r) => r % 5 !== f), va = split.train.filter((r) => r % 5 === f);
    const mx = tr.reduce((a, r) => a + x[r], 0) / tr.length, my = tr.reduce((a, r) => a + y[r], 0) / tr.length;
    let sxy = 0, sxx = 0;
    tr.forEach((r) => { sxy += (x[r] - mx) * (y[r] - my); sxx += (x[r] - mx) * (x[r] - mx); });
    const b = sxy / sxx, a = my - b * mx;
    const err = va.map((r) => a + b * x[r] - y[r]);
    const mse = err.reduce((s, e) => s + e * e, 0) / va.length;
    const vm = va.reduce((s, r) => s + y[r], 0) / va.length;
    const sst = va.reduce((s, r) => s + (y[r] - vm) * (y[r] - vm), 0);
    return { mae: err.reduce((s, e) => s + Math.abs(e), 0) / va.length, mse, rmse: Math.sqrt(mse), r2: 1 - mse * va.length / sst };
  });
  for (const key of ['allin', 'forward_sfs_k01', 'backward_sfs_k01', 'rfe_k01', 'lasso_path_k01']) {
    const c = res.candidates.find((z) => z.key === key);
    assert.equal(c.status, 'VALID', key);
    ['mae', 'mse', 'rmse', 'r2'].forEach((m) => {
      const folds = hand.map((h) => h[m]);
      c.folds.forEach((f, i) => assert.ok(Math.abs(f.metrics[m] - folds[i]) <= 1e-9 * Math.abs(folds[i]), `${key} fold ${i} ${m}`));
      const mean = folds.reduce((s, v) => s + v, 0) / 5;
      const sd = Math.sqrt(folds.reduce((s, v) => s + (v - mean) * (v - mean), 0) / 4);
      assert.ok(Math.abs(c.cv.mean[m] - mean) <= 1e-9 * Math.abs(mean), `${key} mean ${m}`);
      assert.ok(Math.abs(c.cv.std[m] - sd) <= 1e-9 * Math.abs(sd), `${key} sd ${m}`);
      // and the mean is exactly the mean of the fold values the engine reports
      const own = c.folds.map((f) => f.metrics[m]);
      assert.equal(c.cv.mean[m], own.reduce((s, v) => s + v, 0) / own.length);
    });
  }
});

/* ---- freezing ------------------------------------------------------------------------------------ */
function mixedRows(seed) {
  const next = E.mulberry32(seed), u = () => next() / 4294967296, rows = [];
  for (let i = 0; i < 90; i++) {
    const a = Math.round(u() * 1000) / 10, b = Math.round((u() - 0.5) * 600) / 10, c = Math.round(u() * 100) / 100;
    const cat = ['n', 's', 'e', 'w'][Math.floor(u() * 4)];
    const y = 2 * a - 1.5 * b + 30 * c + { n: 0, s: 8, e: -5, w: 2 }[cat] + (u() - 0.5) * 30;
    rows.push([a, b, c, cat, Math.round(y * 1000) / 1000]);
  }
  return rows;
}
const MIXED = ['a', 'b', 'c', 'cat', 'y'];

test('freezing: changing the target of the test rows moves only the test numbers', () => {
  const rows = mixedRows(75);
  const a = E.run(load(MIXED, rows));
  const changed = rows.map((r) => r.slice());
  a.split.test.forEach((r) => { changed[r][4] = changed[r][4] * 3 + 1000; });
  const b = E.run(load(MIXED, changed));
  assert.equal(a.run.status, 'COMPLETED');
  for (const k of ['columns', 'groups', 'split', 'dependencies', 'lasso_path', 'winners']) assert.deepEqual(strip(b[k]), strip(a[k]), k);
  assert.deepEqual(strip(b.candidates), strip(a.candidates));
  assert.deepEqual(Object.keys(b.test), Object.keys(a.test));
  Object.keys(a.test).forEach((k) => {
    assert.notDeepEqual(b.test[k].metrics, a.test[k].metrics, k);
    assert.deepEqual(b.test[k].rows, a.test[k].rows);
  });
  assert.equal(a.candidates.length, 1 + 4 * 4);
});

/* ---- Lasso degeneracy and the tie rule ----------------------------------------------------------- */
function degenerateRows() {
  const next = E.mulberry32(81), u = () => next() / 4294967296, rows = [];
  for (let i = 0; i < 80; i++) {
    const x1 = Math.round(u() * 1000) / 100, x2 = Math.round(u() * 1000) / 100, x4 = Math.round((u() - 0.5) * 20000) / 1000;
    const dup = Math.round((u() - 0.5) * 2000) / 1000, cat = ['p', 'q', 'r'][Math.floor(u() * 3)];
    const y = 3 * x1 - 2 * x2 + 4 * x4 + 0.5 * dup + { p: 0, q: 6, r: -4 }[cat] + (u() - 0.5) * 4;
    rows.push([x1, x2, x1 + x2, x4, dup, dup, cat, Math.round(y * 1000) / 1000]);
  }
  return rows;
}
const DEG = ['x1', 'x2', 'x_sum', 'x4', 'dup_a', 'dup_b', 'cat', 'y'];

test('A-2: Lasso candidates beyond the path are INVALID_MODEL / lasso_path_degenerate everywhere', () => {
  const res = E.run(load(DEG, degenerateRows()));
  assert.equal(res.run.status, 'COMPLETED');
  const infos = [res.lasso_path.canonical].concat(res.lasso_path.folds);
  infos.forEach((info) => {
    assert.equal(info.degenerate, true);
    assert.ok(info.first_invalid_k <= 6 && info.n_entered === info.first_invalid_k - 1);
    assert.equal(info.entries.length + info.not_entered.length, 7);
    // the groups that did not enter are listed in CSV order, after the path, and never in a subset
    assert.deepEqual(info.not_entered, DEG.filter((g) => info.not_entered.includes(g)));
    assert.ok(info.not_entered.includes('x_sum'));
    // the twins tie exactly: the earlier one in CSV order is the one that enters
    assert.ok(!info.entries.some((e) => e.group === 'dup_b'));
  });
  const canon = res.lasso_path.canonical;
  for (let k = 1; k <= 7; k++) {
    const c = res.candidates.find((z) => z.key === 'lasso_path_k0' + k);
    if (k < canon.first_invalid_k) {
      assert.deepEqual(c.canonical_groups, DEG.filter((g) => canon.entries.slice(0, k).some((e) => e.group === g)));
      continue;
    }
    assert.equal(c.status, 'INVALID_MODEL');
    assert.equal(c.canonical_groups, null);
    assert.equal(c.fit, null);
    const deg = c.reasons.filter((r) => r.rule === 'lasso_path_degenerate');
    assert.ok(deg.some((r) => r.scope === 'training_set' && r.n_groups_entered === canon.n_entered));
    res.lasso_path.folds.forEach((info, f) => {
      if (k >= info.first_invalid_k) {
        assert.ok(deg.some((r) => r.scope === 'fold' && r.fold === f));
        assert.equal(c.folds[f].groups, null);
        assert.equal(c.folds[f].metrics, null);
      }
    });
  }
  // collinear subsets are INVALID_MODEL by A-1, the All-in among them; winners are VALID only
  res.candidates.forEach((c) => {
    const g = c.canonical_groups || [];
    if (['x1', 'x2', 'x_sum'].every((v) => g.includes(v)) || ['dup_a', 'dup_b'].every((v) => g.includes(v))) {
      assert.equal(c.status, 'INVALID_MODEL', c.key);
      assert.ok(c.reasons.every((r) => r.rule === 'rank_deficient'), c.key);
    }
  });
  assert.equal(res.candidates[0].status, 'INVALID_MODEL');
  assert.equal(res.winners.method_winners.allin, null);
  Object.values(res.winners.method_winners).filter(Boolean).forEach((w) => {
    assert.equal(res.candidates.find((c) => c.key === w.key).status, 'VALID');
  });
  // A-3: the two relations, their columns and feature groups; no single column is named as the cause
  assert.deepEqual(res.dependencies.relations.map((r) => r.feature_groups), [['x1', 'x2', 'x_sum'], ['dup_a', 'dup_b']]);
  assert.equal(res.dependencies.rank, res.dependencies.n_columns - 2);
});

test('A-2: an entering column that is an exact twin of an active one stops the path (active_set_degenerate)', () => {
  // `twin` equals `x1`, the strongest predictor: after x1 enters, the twin's correlation stays tied with the
  // active level; ties go to CSV order, so the twin (column 2) is tried before x2 / x3 and the active set would
  // become rank deficient. JS-only: which tied column sklearn tries is a floating-point accident (Brief V2 §8).
  const next = E.mulberry32(91), u = () => next() / 4294967296, rows = [];
  for (let i = 0; i < 60; i++) {
    const x1 = Math.round(u() * 10000) / 100, x2 = Math.round(u() * 1000) / 100, x3 = Math.round(u() * 1000) / 100;
    rows.push([x1, x1, x2, x3, Math.round((5 * x1 + 2 * x2 - x3 + (u() - 0.5) * 6) * 1000) / 1000]);
  }
  const res = E.run(load(['x1', 'twin', 'x2', 'x3', 'y'], rows));
  [res.lasso_path.canonical].concat(res.lasso_path.folds).forEach((info) => {
    assert.equal(info.cause, 'active_set_degenerate');
    assert.deepEqual(info.entries.map((e) => e.group), ['x1']);
    assert.deepEqual(info.not_entered, ['twin', 'x2', 'x3']);
    assert.equal(info.first_invalid_k, 2);
  });
  assert.equal(res.candidates.find((c) => c.key === 'lasso_path_k01').status, 'VALID');
  ['lasso_path_k02', 'lasso_path_k03', 'lasso_path_k04'].forEach((key) => {
    const c = res.candidates.find((z) => z.key === key);
    assert.equal(c.status, 'INVALID_MODEL');
    assert.ok(c.reasons.every((r) => r.rule === 'lasso_path_degenerate' && r.cause === 'active_set_degenerate'));
  });
  // the other methods are not affected: forward keeps the twin for last (it adds nothing)
  assert.deepEqual(res.candidates.find((c) => c.key === 'forward_sfs_k03').canonical_groups, ['x1', 'x2', 'x3']);
});

test('LARS: on a non-degenerate path every group enters, ordered by entry alpha', () => {
  const res = E.run(load(MIXED, mixedRows(76)));
  [res.lasso_path.canonical].concat(res.lasso_path.folds).forEach((info) => {
    assert.equal(info.degenerate, false);
    assert.equal(info.first_invalid_k, null);
    assert.equal(info.cause, null);
    assert.equal(info.entries.length, 4);
    for (let i = 1; i < 4; i++) assert.ok(info.entries[i - 1].entry_alpha >= info.entries[i].entry_alpha);
  });
});

/* ---- fold boundary of the selection paths --------------------------------------------------------- */
test('layer 3 / canonical: subsets ignore the fold\'s validation rows and the test rows', () => {
  const rows = mixedRows(77);
  const split = { train: Array.from({ length: 72 }, (_, i) => i), test: Array.from({ length: 18 }, (_, i) => 72 + i), folds: [] };
  split.folds = split.train.map((r) => r % 5);
  const base = E.run(load(MIXED, rows), { split });
  const f = 3;
  // (1) fold f's validation rows (values, target, a new level): fold f's paths and fits do not move
  const valid = rows.map((r) => r.slice());
  split.train.filter((r) => r % 5 === f).forEach((r, j) => { valid[r][0] += 40; valid[r][4] -= 500; if (j < 2) valid[r][3] = 'zz'; });
  const v = E.run(load(MIXED, valid), { split });
  base.candidates.forEach((c, i) => {
    const d = v.candidates[i];
    assert.deepEqual(d.folds[f].groups, c.folds[f].groups, `${c.key} fold ${f} subset`);
    assert.deepEqual(d.folds[f].coef, c.folds[f].coef, `${c.key} fold ${f} fit`);
    assert.deepEqual(d.folds[f].levels, c.folds[f].levels, `${c.key} fold ${f} levels`);
  });
  assert.deepEqual(strip(v.lasso_path.folds[f]), strip(base.lasso_path.folds[f]));
  // those rows are training rows of the other folds and of the training set: those paths see them
  const moved = [0, 1, 2, 4].filter((g) => JSON.stringify(v.lasso_path.folds[g]) !== JSON.stringify(base.lasso_path.folds[g]));
  assert.ok(moved.length > 0);
  assert.notDeepEqual(strip(v.lasso_path.canonical), strip(base.lasso_path.canonical));
  // (2) the test rows (values, target, a new level): no canonical subset, fit or path moves
  const testRows = rows.map((r) => r.slice());
  split.test.forEach((r) => { testRows[r][1] *= 7; testRows[r][4] += 999; testRows[r][3] = 'yy'; });
  const t = E.run(load(MIXED, testRows), { split });
  base.candidates.forEach((c, i) => {
    const d = t.candidates[i];
    assert.deepEqual(d.canonical_groups, c.canonical_groups, `${c.key} canonical subset`);
    assert.deepEqual(strip(d.fit), strip(c.fit), `${c.key} canonical fit`);
    assert.deepEqual(strip(d.folds), strip(c.folds), `${c.key} folds`);
  });
  assert.deepEqual(strip(t.lasso_path), strip(base.lasso_path));
  assert.deepEqual(strip(t.winners), strip(base.winners));
});

/* ---- winner ties ---------------------------------------------------------------------------------- */
function cand(key, method, k, rmse, groups) {
  return { key, method, k, status: rmse === null ? 'INVALID_MODEL' : 'VALID', cv: rmse === null ? null : { mean: { rmse } }, canonical_groups: groups };
}
test('winners: equal CV RMSE in a method -> smaller k; between methods -> method order; shared models once', () => {
  const w = E.determineWinners([
    cand('allin', 'allin', 3, 4.0, ['a', 'b', 'c']),
    cand('forward_sfs_k01', 'forward_sfs', 1, 4.0, ['b']), cand('forward_sfs_k02', 'forward_sfs', 2, 4.0, ['a', 'b']),
    cand('backward_sfs_k02', 'backward_sfs', 2, 4.0, ['a', 'b']),
    cand('rfe_k01', 'rfe', 1, null, ['a']),
    cand('lasso_path_k01', 'lasso_path', 1, 4.0, ['b'])]);
  assert.deepEqual(w.method_winners.forward_sfs, { key: 'forward_sfs_k01', k: 1 });
  assert.equal(w.method_winners.rfe, null);
  assert.deepEqual(w.overall, { method: 'allin', key: 'allin', k: 3 });
  assert.deepEqual(w.test_keys, ['allin', 'forward_sfs_k01', 'backward_sfs_k02']);
  assert.equal(w.test_key_of.lasso_path_k01, 'forward_sfs_k01');
  const w2 = E.determineWinners([cand('allin', 'allin', 2, 5.0, ['a', 'b']), cand('rfe_k01', 'rfe', 1, 3.0, ['a']), cand('lasso_path_k01', 'lasso_path', 1, 3.0, ['a'])]);
  assert.deepEqual(w2.overall, { method: 'rfe', key: 'rfe_k01', k: 1 });
  assert.deepEqual(w2.test_keys, ['allin', 'rfe_k01']);
});
