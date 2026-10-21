// Node test of the three-layer preprocessing boundary (Spec V2 「前處理與洩漏邊界」, SR-V2-01; 次 seam).
//
//   node --test tests/js/explore_boundary.test.js
//
// Layer 2 sees the training rows only: the 20 / 21 level limit and the constant-column rule are
// counted on them; changing test rows changes no group, no canonical order, no canonical fit and no
// level of the live predictor. Layer 3 sees one fold's training rows only: changing that fold's
// validation rows changes none of its levels, baseline or fit; changing its training rows does.
// The split is injected (the engine accepts an external split for tests) so the rows are known.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const L = require('../../assets/explore_load.js');
const E = require('../../assets/explore_engine.js');

const N = 100;
const TRAIN = Array.from({ length: 80 }, (_, i) => i);
const TEST = Array.from({ length: 20 }, (_, i) => 80 + i);
const FOLDS = TRAIN.map((i) => i % 5);
const SPLIT = { train: TRAIN, test: TEST, folds: FOLDS };
const COLS = ['x1', 'x2', 'cat5', 'cat20', 'cat21', 'varies_in_test', 'const_in_test', 'y'];

function baseRows() {
  const next = E.mulberry32(2026);
  const u = () => next() / 4294967296;
  const out = [];
  for (let i = 0; i < N; i++) {
    const isTest = i >= 80;
    const x1 = Math.round(u() * 1000) / 10;
    const x2 = Math.round((u() - 0.5) * 400) / 10;
    const cat5 = 'C' + (Math.floor(i / 7) % 5);                                     // not a function of cat20 or the fold
    const cat20 = i === 85 ? 'L20' : 'L' + (Math.floor(i / 3) % 20);              // 21st level only in a test row
    const cat21 = 'M' + (i % 21);                                                    // 21 levels on the training rows
    const variesInTest = isTest ? String(i) : '5';                                   // constant on the training rows
    const constInTest = isTest ? '7' : String(i % 9);                                // constant on the test rows only
    const y = 3 * x1 - 2 * x2 + 10 * (Math.floor(i / 7) % 5) + (u() - 0.5) * 20;
    out.push([x1, x2, cat5, cat20, cat21, variesInTest, constInTest, Math.round(y * 100) / 100]);
  }
  return out;
}

function toCsv(rowList) { return COLS.join(',') + '\n' + rowList.map((r) => r.join(',')).join('\n') + '\n'; }
function load(rowList) {
  const r = L.loadCsv(toCsv(rowList));
  assert.equal(r.ok, true, JSON.stringify(r));
  return r;
}
function runOn(rowList) { return E.run(load(rowList), { split: SPLIT }); }
function statusOf(result, name) { return result.columns.find((c) => c.name === name); }
const strip = (x) => JSON.parse(JSON.stringify(x));

test('layer 2: the 20 / 21 level limit and the constant rule are counted on the training rows', () => {
  const r = runOn(baseRows());
  assert.equal(r.run.status, 'COMPLETED');
  assert.equal(statusOf(r, 'cat20').status, 'KEPT');
  assert.equal(statusOf(r, 'cat20').n_distinct_train, 20);        // the 21st level of a test row does not count
  assert.equal(statusOf(r, 'cat21').status, 'EXCLUDED_TOO_MANY_LEVELS');
  assert.equal(statusOf(r, 'cat21').n_distinct_train, 21);
  assert.equal(statusOf(r, 'varies_in_test').status, 'EXCLUDED_CONSTANT');
  assert.equal(statusOf(r, 'const_in_test').status, 'KEPT');
  assert.deepEqual(r.groups.map((g) => g.name), ['x1', 'x2', 'cat5', 'cat20', 'const_in_test']);
  assert.deepEqual(r.candidates[0].canonical_groups, ['x1', 'x2', 'cat5', 'cat20', 'const_in_test']);
  // the unseen 21st level of the test row is encoded as the baseline and counted
  assert.equal(r.test.allin.n_unseen_by_group.cat20, 1);
});

test('layer 2 and canonical: changing test rows changes no decision, no canonical fit and no predictor level', () => {
  const a = runOn(baseRows());
  const rows = baseRows();
  for (const i of TEST) {
    rows[i][0] = rows[i][0] * 3 + 1;           // values
    rows[i][3] = 'L' + (100 + i);              // new levels
    rows[i][4] = 'M0';
    rows[i][5] = '5';                          // make the training-constant column constant everywhere
    rows[i][6] = String(i);                    // make the test-constant column vary on the test rows
    rows[i][7] = rows[i][7] + 1000;            // target
  }
  const b = runOn(rows);
  assert.deepEqual(strip(b.columns), strip(a.columns));
  assert.deepEqual(b.groups, a.groups);
  const ca = a.candidates[0], cb = b.candidates[0];
  assert.deepEqual(cb.canonical_groups, ca.canonical_groups);
  assert.deepEqual(strip(cb.fit), strip(ca.fit));               // coef, (X'X)^-1, s2, levels, inputs
  assert.deepEqual(strip(cb.folds), strip(ca.folds));
  assert.deepEqual(strip(cb.cv), strip(ca.cv));
  assert.deepEqual(E.inputSpec(cb.fit), E.inputSpec(ca.fit));   // the predictor's drop-downs and defaults
  assert.deepEqual(b.winners, a.winners);
  assert.notDeepEqual(b.test.allin.metrics, a.test.allin.metrics);   // only the test numbers move
  assert.equal(b.test.allin.n_unseen_by_group.cat20, 20);
});

test('layer 2: changing training rows does change the decisions', () => {
  const rows = baseRows();
  rows[3][5] = '6';                            // the training-constant column now varies on a training row
  rows[10][3] = 'L99';                         // a 21st level of cat20 on a training row
  const r = runOn(rows);
  assert.equal(statusOf(r, 'varies_in_test').status, 'KEPT');
  assert.equal(statusOf(r, 'cat20').status, 'EXCLUDED_TOO_MANY_LEVELS');
  assert.deepEqual(r.groups.map((g) => g.name), ['x1', 'x2', 'cat5', 'varies_in_test', 'const_in_test']);
});

test('layer 3: a fold\'s levels, baseline and fit ignore its validation rows and follow its training rows', () => {
  const f = 2;
  const a = runOn(baseRows());
  const validOfF = TRAIN.filter((r, i) => FOLDS[i] === f);
  const rows = baseRows();
  validOfF.forEach((r, j) => { rows[r][0] += 50; rows[r][7] += 999; if (j < 2) rows[r][2] = 'C_new'; });
  const b = runOn(rows);
  const fa = a.candidates[0].folds[f], fb = b.candidates[0].folds[f];
  assert.deepEqual(fb.levels, fa.levels);                        // levels and baseline of every categorical group
  assert.deepEqual(fb.coef, fa.coef);                            // the fold's OLS fit
  assert.equal(fb.n_columns, fa.n_columns);
  assert.notDeepEqual(fb.metrics, fa.metrics);                   // only the validation score moves
  assert.equal(fb.n_valid_unseen, fa.n_valid_unseen + 2);        // the new level is unseen: baseline, counted
  // those rows are training rows of every other fold: their fits change
  for (let g = 0; g < 5; g++) if (g !== f) assert.notDeepEqual(b.candidates[0].folds[g].coef, a.candidates[0].folds[g].coef);
});

test('layer 3: changing one training row of a fold changes that fold, not the fold where the row is validation', () => {
  const a = runOn(baseRows());
  const row = TRAIN.find((r, i) => FOLDS[i] === 4);             // a validation row of fold 4
  const rows = baseRows();
  rows[row][2] = 'C_first';                                      // a new level, seen first in its folds
  rows[row][0] += 7;
  const b = runOn(rows);
  for (let g = 0; g < 4; g++) {
    const fa = a.candidates[0].folds[g], fb = b.candidates[0].folds[g];
    assert.notDeepEqual(fb.coef, fa.coef, `fold ${g}`);
    assert.ok(fb.levels.cat5.levels.includes('C_first'), `fold ${g}`);
  }
  const fa4 = a.candidates[0].folds[4], fb4 = b.candidates[0].folds[4];
  assert.deepEqual(fb4.levels, fa4.levels);
  assert.deepEqual(fb4.coef, fa4.coef);
  // the baseline is the level seen first in the fold's training rows
  assert.equal(fb4.levels.cat5.baseline, 'C0');
});

test('the baseline is the first level in the training rows; one-hot columns follow first appearance', () => {
  const r = runOn(baseRows());
  const fit = r.candidates[0].fit;
  assert.deepEqual(fit.levels.cat5, { levels: ['C0', 'C1', 'C2', 'C3', 'C4'], baseline: 'C0' });
  const cat5Cols = fit.encoded_columns.filter((c) => c.group === 'cat5').map((c) => c.level);
  assert.deepEqual(cat5Cols, ['C1', 'C2', 'C3', 'C4']);
  const spec = E.inputSpec(fit).find((s) => s.name === 'cat5');
  assert.deepEqual(spec.levels, ['C0', 'C1', 'C2', 'C3', 'C4']);  // the training levels plus the baseline
  assert.equal(spec.default, 'C0');
});

test('the split is reproducible and the folds cover the training rows evenly', () => {
  const s1 = E.makeSplit(50, 42), s2 = E.makeSplit(50, 42);
  assert.deepEqual(s1, s2);
  assert.equal(s1.test.length, 10);
  assert.equal(s1.train.length, 40);
  assert.deepEqual([0, 1, 2, 3, 4].map((f) => s1.folds.filter((x) => x === f).length), [8, 8, 8, 8, 8]);
  assert.deepEqual(s1.train.concat(s1.test).sort((a, b) => a - b), Array.from({ length: 50 }, (_, i) => i));
  assert.notDeepEqual(E.makeSplit(50, 43).test, s1.test);
  assert.equal(E.makeSplit(20, 42).test.length, 4);
  assert.equal(E.makeSplit(22, 42).test.length, 4);
  assert.equal(E.makeSplit(23, 42).test.length, 5);
});
