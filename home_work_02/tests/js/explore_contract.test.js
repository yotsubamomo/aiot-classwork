// Node test of the Exploratory run result contract against the generic Python reference (Spec V2 主 seam;
// #74 V2-T1: All-in; #75 V2-T2: the four path methods, winners, Lasso degeneracy, dependencies).
//
//   HW2_EXPLORE_REFERENCE=<dir written by tests/test_node_explore.py> node --test tests/js/explore_contract.test.js
//
// The reference results are generated at test time by hw2/explore_reference.py (pytest) and written to
// a temporary directory with the CSV files (nothing is tracked). For every case the browser files load
// the same CSV bytes and run the engine; the test compares, with the relative tolerance 1e-6 of the V1
// JS decision (DA decision-20261018-issue63-js-tolerance.md T-1; Spec V2 Testing Decisions):
//   - the LoadResult (identical) and the PRNG (identical integers);
//   - columns and their training-row status, groups and canonical order, split and fold assignment
//     (identical: both sides implement the same PRNG);
//   - every candidate (All-in and each (method, k)): status and reasons (rule, scope, fold); per fold the
//     subset, levels, baseline, metrics and coefficients; CV mean and standard deviation; canonical subset
//     and canonical fit (coef, (X'X)^-1, s2, df_resid, t, R^2, Adjusted R^2, levels, predictor inputs);
//   - the Lasso path of the training set and of every fold: entry alphas (1e-6) in the same order, the
//     groups that did not enter, the degeneracy (first invalid k, cause);
//   - the dependency diagnostic (relations, their columns, coefficients and feature groups);
//   - winners (method winners, overall winner, the models scored, shared models), also on injected
//     candidate lists with ties; test metrics, per-row predicted / lower / upper (1e-6) and covered
//     (exactly), coverage.
// Degenerate cases (Spec 主 seam (c)) are compared modulo exactly tied twin columns: when two columns are
// identical, which of them LARS takes is a floating-point tie (the engine resolves ties in CSV order as the
// Spec says; sklearn takes the first in its internal order), so a twin's name is mapped to the earlier
// twin on both sides before comparing (Brief V2 §8: no unique order is assumed from sklearn in degenerate
// situations). Nothing else is relaxed.
// Every JS result is also checked against the contract invariants with code written here (not the
// engine's): VALID <=> fit <=> CV metrics; covered = lower <= actual <= upper; coverage = covered / n_test;
// test only for the winners, every winner VALID, shared models scored once; REJECTED results have no
// candidates / winners / test; Lasso k beyond its path INVALID; each test row's prediction and PI
// recomputed from the raw CSV values, the encoding rules of `groups` / `encoded_columns` and the fit.
// #77 (V2-T4): a case may carry injected budgets (`budgets` in the manifest) that both sides apply;
// `meta.budget` (unit, constants, estimates, sizes) is compared exactly; SKIPPED_RESOURCE_LIMIT and FAILED
// candidates have no CV metrics, fit or canonical subset; a skipped Lasso has no `lasso_path`.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const L = require('../../assets/explore_load.js');
const E = require('../../assets/explore_engine.js');

const UNIT = path.join(__dirname, '..', '..');
const DIR = process.env.HW2_EXPLORE_REFERENCE;
const MANIFEST = DIR ? JSON.parse(fs.readFileSync(path.join(DIR, 'manifest.json'), 'utf8')) : null;
const needRef = { skip: MANIFEST ? false : 'set HW2_EXPLORE_REFERENCE (tests/test_node_explore.py does)' };
const TOL = 1e-6;

/* Numbers: relative tolerance; integers that are counts or indices compare exactly through the same
 * rule (an off-by-one is far outside 1e-6). Strings, booleans and null exactly. Objects: the keys of
 * the reference must all be present in the JS value. */
function closeTo(actual, expected, where) {
  if (typeof expected === 'number') {
    assert.equal(typeof actual, 'number', `${where}: ${actual} is not a number (expected ${expected})`);
    const diff = Math.abs(actual - expected);
    const ok = expected === 0 ? diff <= 1e-12 : diff <= TOL * Math.abs(expected);
    assert.ok(ok, `${where}: ${actual} vs ${expected} (rel ${diff / Math.abs(expected)})`);
    return;
  }
  if (expected === null || typeof expected !== 'object') {
    assert.equal(actual, expected, where);
    return;
  }
  if (Array.isArray(expected)) {
    assert.ok(Array.isArray(actual), `${where}: not an array`);
    assert.equal(actual.length, expected.length, `${where}: length`);
    expected.forEach((e, i) => closeTo(actual[i], e, `${where}[${i}]`));
    return;
  }
  assert.ok(actual && typeof actual === 'object', `${where}: not an object`);
  Object.keys(expected).forEach((k) => {
    assert.ok(Object.prototype.hasOwnProperty.call(actual, k), `${where}.${k}: missing in the JS result`);
    closeTo(actual[k], expected[k], `${where}.${k}`);
  });
}

function strictEqual(actual, expected, where) { assert.deepEqual(JSON.parse(JSON.stringify(actual)), expected, where); }

/* Twin columns of a degenerate case: relations of exactly two numeric columns with coefficients +1 / -1
 * (identical columns). The later name maps to the earlier one. */
function twinMap(reference) {
  const map = new Map();
  const deps = reference.dependencies;
  (deps ? deps.relations : []).forEach((r) => {
    const cols = r.columns;
    if (cols.length === 2 && cols.every((c) => !c.intercept && c.level === null) &&
        Math.abs(Math.abs(cols[0].coef) - 1) < 1e-9 && Math.abs(Math.abs(cols[1].coef) - 1) < 1e-9) {
      map.set(cols[1].group, cols[0].group);
    }
  });
  return map;
}
function mapNames(value, map) {
  if (!map.size) return value;
  if (typeof value === 'string') return map.has(value) ? map.get(value) : value;
  if (Array.isArray(value)) return value.map((v) => mapNames(v, map));
  if (value && typeof value === 'object') {
    const out = {};
    Object.keys(value).forEach((k) => { out[map.has(k) ? map.get(k) : k] = mapNames(value[k], map); });
    return out;
  }
  return value;
}

/* ---- contract invariants, written independently of the engine -------------------------------- */
function recomputeRow(fit, load, row) {
  const values = load.rows[row];
  const byName = new Map();
  load.columns.forEach((c) => { byName.set(c.name, values[c.index]); });
  const x = [1].concat(fit.encoded_columns.map((c) => (c.level === null ? byName.get(c.group) : (byName.get(c.group) === c.level ? 1 : 0))));
  let yhat = 0;
  x.forEach((v, i) => { yhat += v * fit.coef[i]; });
  let q = 0;
  for (let i = 0; i < x.length; i++) for (let j = 0; j < x.length; j++) q += x[i] * fit.xtx_inv[i][j] * x[j];
  const half = fit.t_crit * Math.sqrt(fit.s2 * (1 + q));
  return { predicted: yhat, lower: yhat - half, upper: yhat + half, actual: values[load.target.index] };
}

function checkInvariants(result, load, where) {
  const status = result.run.status;
  assert.ok(['COMPLETED', 'CANCELLED', 'REJECTED'].includes(status), where);
  if (status !== 'COMPLETED') {
    for (const k of ['candidates', 'winners', 'test']) assert.ok(!(k in result), `${where}: ${status} has ${k}`);
    return;
  }
  const byKey = new Map();
  const p = result.groups.length;
  const expectedKeys = ['allin'];
  ['forward_sfs', 'backward_sfs', 'rfe', 'lasso_path'].forEach((m) => {
    for (let k = 1; k <= p; k++) expectedKeys.push(m + '_k' + String(k).padStart(2, '0'));
  });
  assert.deepEqual(result.candidates.map((c) => c.key), expectedKeys, `${where}: one candidate per (method, k) plus All-in`);
  result.candidates.forEach((c) => {
    byKey.set(c.key, c);
    assert.ok(['VALID', 'INVALID_MODEL', 'SKIPPED_RESOURCE_LIMIT', 'FAILED'].includes(c.status), `${where} ${c.key}`);
    assert.equal(c.status === 'VALID', c.fit !== null, `${where} ${c.key}: VALID <=> fit`);
    assert.equal(c.status === 'VALID', c.cv !== null, `${where} ${c.key}: VALID <=> CV metrics`);
    assert.equal(c.status === 'VALID', c.reasons.length === 0, `${where} ${c.key}: VALID <=> no reason`);
    assert.equal(E.canPredict(c), c.status === 'VALID', `${where} ${c.key}: predictor only for VALID`);
    c.folds.forEach((f) => { if (f.status === 'invalid') assert.equal(f.metrics, null, `${where} ${c.key} fold ${f.fold}`); });
    if (c.status === 'SKIPPED_RESOURCE_LIMIT' || c.status === 'FAILED') {
      assert.equal(c.canonical_groups, null, `${where} ${c.key}: ${c.status} has no canonical subset`);
      assert.deepEqual(c.folds, [], `${where} ${c.key}: ${c.status} has no fold result`);
      assert.equal(c.reasons.length, 1, `${where} ${c.key}: one method-level reason`);
    }
  });
  const w = result.winners;
  const winnerKeys = Object.keys(w.method_winners).map((m) => w.method_winners[m]).filter(Boolean).map((x) => x.key).concat([w.overall.key]);
  winnerKeys.forEach((k) => assert.equal(byKey.get(k).status, 'VALID', `${where}: winner ${k} is VALID`));
  assert.deepEqual(Object.keys(w.test_key_of).sort(), Array.from(new Set(winnerKeys)).sort(), `${where}: every winner maps to its scored model`);
  Object.keys(w.test_key_of).forEach((k) => {
    assert.deepEqual(byKey.get(k).canonical_groups, byKey.get(w.test_key_of[k]).canonical_groups, `${where}: shared model ${k}`);
  });
  assert.deepEqual(Object.keys(result.test).sort(), w.test_keys.slice().sort(), `${where}: test only for winners`);
  assert.deepEqual(Array.from(new Set(Object.values(w.test_key_of))).sort(), w.test_keys.slice().sort(), `${where}: each model scored once`);
  const canon = result.lasso_path ? result.lasso_path.canonical : { degenerate: false };
  if (!result.lasso_path) {
    assert.ok(result.candidates.filter((c) => c.method === 'lasso_path').every((c) => c.status !== 'VALID' && c.status !== 'INVALID_MODEL'),
      `${where}: no Lasso path only when Lasso did not run`);
  }
  if (canon.degenerate) {
    for (let k = canon.first_invalid_k; k <= p; k++) {
      const c = byKey.get('lasso_path_k' + String(k).padStart(2, '0'));
      assert.equal(c.status, 'INVALID_MODEL', `${where}: Lasso k = ${k} beyond the path`);
      assert.equal(c.canonical_groups, null);
      assert.ok(c.reasons.some((r) => r.rule === 'lasso_path_degenerate' && r.scope === 'training_set'));
    }
  }
  Object.keys(result.test).forEach((key) => {
    const t = result.test[key], fit = byKey.get(key).fit;
    assert.equal(byKey.get(key).status, 'VALID');
    let n = 0;
    t.rows.forEach((row, i) => {
      assert.equal(t.covered[i], t.lower[i] <= t.actual[i] && t.actual[i] <= t.upper[i], `${where} covered[${i}]`);
      if (t.covered[i]) n++;
      const r = recomputeRow(fit, load, row);
      assert.equal(r.actual, t.actual[i]);
      for (const k of ['predicted', 'lower', 'upper']) {
        assert.ok(Math.abs(r[k] - t[k][i]) <= 1e-9 * Math.max(1, Math.abs(r[k])), `${where} ${k}[${i}] ${r[k]} vs ${t[k][i]}`);
      }
    });
    assert.equal(t.n_covered, n);
    assert.equal(t.coverage, n / t.n_test);
    assert.equal(t.n_test, result.split.test.length);
  });
}

test('mulberry32 gives the same integers as the Python reference', needRef, () => {
  const next = E.mulberry32(MANIFEST.prng.seed);
  assert.deepEqual(MANIFEST.prng.first.map(() => next()), MANIFEST.prng.first);
});

test('load contract: identical LoadResults for the parity texts', needRef, () => {
  MANIFEST.load_cases.forEach((c) => {
    const bytes = new Uint8Array(fs.readFileSync(path.join(DIR, c.csv)));
    strictEqual(L.loadCsv(bytes), c.reference, c.name);
  });
});

test('winner rules on injected candidates: the same winners as the Python reference (ties included)', needRef, () => {
  assert.ok(MANIFEST.winner_cases.length >= 3);
  MANIFEST.winner_cases.forEach((c) => strictEqual(E.determineWinners(c.candidates), c.winners, c.name));
});

if (MANIFEST) {
  MANIFEST.cases.forEach((c) => {
    test(`case ${c.name}: the JS run reproduces the Python reference`, () => {
      const ref = JSON.parse(fs.readFileSync(path.join(DIR, c.reference), 'utf8'));
      const load = L.loadCsv(new Uint8Array(fs.readFileSync(path.join(DIR, c.csv))));
      strictEqual(load, ref.load, `${c.name} load`);
      const raw = E.run(load, { problem: c.name, budgets: c.budgets || undefined });
      checkInvariants(raw, load, c.name);
      const twins = c.degenerate ? twinMap(ref.result) : new Map();
      const result = mapNames(JSON.parse(JSON.stringify(raw)), twins);
      const r = mapNames(ref.result, twins);
      assert.equal(result.run.status, c.expected_status);
      strictEqual(result.run, r.run, `${c.name} run`);
      strictEqual(result.columns, r.columns, `${c.name} columns`);
      strictEqual(result.groups, r.groups, `${c.name} groups`);
      strictEqual({ train: result.split.train, test: result.split.test, folds: result.split.folds, n_folds: result.split.n_folds },
        r.split, `${c.name} split`);
      for (const k of ['sha256', 'target', 'n_rows_read', 'n_rows', 'n_rows_dropped_missing', 'seed', 'split_injected',
        'pi_level', 'max_levels', 'min_df_resid', 'cv_std_ddof', 'budget']) {
        assert.deepEqual(result.meta[k], r.meta[k], `${c.name} meta.${k}`);
      }
      closeTo(result.dependencies, r.dependencies, `${c.name} dependencies`);
      closeTo(result.lasso_path, r.lasso_path, `${c.name} lasso_path`);
      if (r.run.status === 'COMPLETED') {
        assert.equal(result.candidates.length, r.candidates.length);
        result.candidates.forEach((cand, i) => {
          const rc = r.candidates[i];
          strictEqual([cand.key, cand.method, cand.k, cand.status, cand.reasons, cand.canonical_groups],
            [rc.key, rc.method, rc.k, rc.status, rc.reasons, rc.canonical_groups], `${c.name} ${rc.key}`);
          closeTo(cand.folds, rc.folds, `${c.name} ${rc.key}.folds`);
          closeTo(cand.cv, rc.cv, `${c.name} ${rc.key}.cv`);
          closeTo(cand.fit, rc.fit, `${c.name} ${rc.key}.fit`);
          if (rc.fit) strictEqual(cand.fit.encoded_columns, rc.fit.encoded_columns, `${c.name} encoded columns`);
        });
        strictEqual(result.winners, r.winners, `${c.name} winners`);
        assert.deepEqual(Object.keys(result.test), Object.keys(r.test));
        Object.keys(r.test).forEach((key) => {
          const t = result.test[key], rt = r.test[key];
          strictEqual([t.rows, t.covered, t.n_covered, t.n_test, t.n_unseen_rows], [rt.rows, rt.covered, rt.n_covered, rt.n_test, rt.n_unseen_rows], `${c.name} test.${key}`);
          assert.equal(t.coverage, rt.coverage);
          closeTo(t, rt, `${c.name} test.${key}`);
        });
      }
    });
  });
}

test('A-1: an invalid All-in names the rule and the fold; the run completes from the valid subsets', needRef, () => {
  const load = L.loadCsv(new Uint8Array(fs.readFileSync(path.join(DIR, 'a1_fold_rank_deficient.csv'))));
  const result = E.run(load);
  assert.equal(result.run.status, 'COMPLETED');
  const allin = result.candidates[0];
  assert.equal(allin.key, 'allin');
  assert.equal(allin.status, 'INVALID_MODEL');
  assert.equal(allin.reasons.length, 1);
  assert.equal(allin.reasons[0].rule, 'rank_deficient');
  assert.equal(allin.reasons[0].fold, 2);
  assert.equal(result.winners.method_winners.allin, null);
  assert.notEqual(result.winners.overall.method, 'allin');
  const small = E.run(L.loadCsv(new Uint8Array(fs.readFileSync(path.join(DIR, 'a1_small_df.csv')))));
  assert.equal(small.run.status, 'COMPLETED');
  assert.ok(small.candidates[0].reasons.every((x) => x.rule === 'df_resid_lt_3' && x.df_resid < 3));
  const none = E.run(L.loadCsv(new Uint8Array(fs.readFileSync(path.join(DIR, 'a1_no_groups.csv')))));
  assert.equal(none.run.status, 'REJECTED');
  assert.equal(none.run.reason, 'ALL_CANDIDATES_INVALID');
});

test('50 Startups: every candidate is VALID in the JS run and in the reference (A-1; Brief V2 §8 第 2 條)', needRef, (t) => {
  const ref = JSON.parse(fs.readFileSync(path.join(DIR, 'startups50.json'), 'utf8')).result;
  const res = E.run(L.loadCsv(new Uint8Array(fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv')))));
  const rows = res.candidates.map((c, i) => [c.key, c.status, ref.candidates[i].status, (c.canonical_groups || []).join(' + ')]);
  rows.forEach((r) => t.diagnostic(`state ${r[0]}: JS ${r[1]}, Python ${r[2]} (${r[3]})`));
  assert.equal(rows.length, 17);
  assert.ok(rows.every((r) => r[1] === 'VALID' && r[2] === 'VALID'));
});

test('50 Startups: the embedded text gives the same load and run as the .csv bytes', needRef, () => {
  const jsText = fs.readFileSync(path.join(UNIT, 'assets', 'data', 'startups50.js'), 'utf8');
  const marker = 'window.HW2_STARTUPS50 = ';
  const data = JSON.parse(jsText.slice(jsText.indexOf(marker) + marker.length).trim().replace(/;$/, ''));
  const fromJs = L.loadCsv(data.csv);
  const fromFile = L.loadCsv(new Uint8Array(fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv'))));
  assert.deepEqual(fromJs, fromFile);
  assert.equal(fromJs.sha256, data.sha256);
  const a = E.run(fromJs), b = E.run(fromFile);
  delete a.meta.timing_ms; delete b.meta.timing_ms;
  assert.deepEqual(a, b);
  const ref = JSON.parse(fs.readFileSync(path.join(DIR, 'startups50.json'), 'utf8'));
  closeTo(a.test.allin, ref.result.test.allin, 'startups50 embedded test');
});
