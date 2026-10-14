// Run with: node --test week06/tests/core.test.js   (after running week06/analysis/nested_cv_comparison.py)
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const Core = require('../assets/core.js');
const DATA = require(path.join(__dirname, '..', 'assets', 'model_data.json'));

const close = (a, b, tol) => assert.ok(Math.abs(a - b) <= tol, `${a} vs ${b} (tol ${tol})`);

test('every scheme has k = 1..5 with k features each', () => {
  for (const scheme of DATA.schemes) {
    const list = DATA.models[scheme.name];
    assert.deepEqual(list.map((m) => m.k), [1, 2, 3, 4, 5]);
    list.forEach((m) => assert.equal(m.features.length, m.k));
  }
});

test('bestK matches the Python summary (lowest CV RMSE per scheme)', () => {
  for (const b of DATA.best) assert.equal(Core.bestK(DATA.models[b.method]), b.best_k);
});

test('JS prediction and 95% PI reproduce the Python values on every test row', () => {
  for (const b of DATA.best) {
    const model = DATA.models[b.method].find((m) => m.k === b.best_k);
    for (const row of b.test_predictions) {
      const r = DATA.test_rows.find((t) => t.row === row.row);   // raw inputs of that test row
      const out = Core.predict(model, { ...r, state: r.State });
      close(out.prediction, row.predicted, 1e-6);
      close(out.lower, row.pi_lower, 1e-6);
      close(out.upper, row.pi_upper, 1e-6);
    }
  }
});

test('California sets both state dummies to 0; Florida sets only State_Florida', () => {
  assert.equal(Core.featureValue('State_Florida', { state: 'California' }), 0);
  assert.equal(Core.featureValue('State_New York', { state: 'California' }), 0);
  assert.equal(Core.featureValue('State_Florida', { state: 'Florida' }), 1);
  assert.equal(Core.featureValue('State_New York', { state: 'Florida' }), 0);
});

test('prediction = intercept + sum of contributions, and the PI contains the prediction', () => {
  const model = DATA.models['Exhaustive Search'][4];
  const out = Core.predict(model, { 'R&D Spend': 100000, Administration: 120000, 'Marketing Spend': 150000, state: 'New York' });
  close(out.prediction, out.intercept + out.contributions.reduce((a, c) => a + c.contribution, 0), 1e-6);
  assert.ok(out.lower < out.prediction && out.prediction < out.upper);
});
