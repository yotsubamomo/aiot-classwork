// Node test of the dashboard's own preprocessing and prediction (assets/hw2core.js).
//
//   node --test tests/js/core.test.js                       (preprocessing cases + official model_data)
//   HW2_FIXTURE_MODEL_DATA=<fixture model_data.json> node --test tests/js/core.test.js
//
// With HW2_FIXTURE_MODEL_DATA (a synthetic fixture written by hw2.fixture; DA TR-01), every
// ols_subset model's prediction, lower, upper and covered are recomputed for every test_inputs
// row from the raw values through the dashboard's own code and compared with the contract
// (tolerance 1e-6). tests/test_node_core.py runs it that way from pytest.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Core = require('../../assets/hw2core.js');

const UNIT = path.join(__dirname, '..', '..');
const TOL = 1e-6;

function loadJs(file) {
  const text = fs.readFileSync(file, 'utf8');
  const start = text.indexOf('window.MODEL_DATA = ');
  return JSON.parse(text.slice(start + 'window.MODEL_DATA = '.length).trim().replace(/;$/, ''));
}
const OFFICIAL = loadJs(path.join(UNIT, 'assets', 'model_data.js'));
const FIXTURE_PATH = process.env.HW2_FIXTURE_MODEL_DATA;
const FIXTURE = FIXTURE_PATH ? JSON.parse(fs.readFileSync(FIXTURE_PATH, 'utf8')) : null;
const needFixture = { skip: FIXTURE ? false : 'set HW2_FIXTURE_MODEL_DATA to a fixture model_data.json' };

const close = (a, b, tol, what) => assert.ok(Math.abs(a - b) <= tol, `${what}: ${a} vs ${b} (tol ${tol})`);

function entries(md) {
  const out = {};
  if (md.baselines && md.baselines.allin) out[md.baselines.allin.model_key] = md.baselines.allin;
  Object.values(md.methods || {}).forEach((list) => list.forEach((e) => { out[e.model_key] = e; }));
  return out;
}

// ---- preprocessing unit cases (official preprocess rules) ------------------------------------
const RULES = OFFICIAL.preprocess;

test('date -> days from the base date', () => {
  assert.equal(RULES.date.base_date, '2014-01-01');
  assert.equal(Core.saleDays('20140101T000000', RULES.date.base_date), 0);
  assert.equal(Core.saleDays('20141013T000000', RULES.date.base_date), 285);
  assert.equal(Core.saleDays('2015-05-27', RULES.date.base_date), 511);
  assert.equal(Core.isoFromDays(285, RULES.date.base_date), '2014-10-13');
  assert.throws(() => Core.saleDays('20140230T000000', RULES.date.base_date));
  assert.throws(() => Core.saleDays('2014/01/01', RULES.date.base_date));
});

test('renovation year: 0 -> flag 0 and effective = built; > 0 -> flag 1', () => {
  assert.deepEqual(Core.renovation(0, 1955), { is_renovated: 0, effective: 1955 });
  assert.deepEqual(Core.renovation(1991, 1955), { is_renovated: 1, effective: 1991 });
  assert.throws(() => Core.renovation(-1, 1955));
});

test('zipcode one-hot: known category, baseline, unseen -> baseline with a warning flag', () => {
  const fit = OFFICIAL.baselines.allin.fit;
  const raw = { date: '2014-10-17', bedrooms: 3, bathrooms: 2, sqft_living: 1900, sqft_lot: 7600, floors: 1,
    waterfront: 0, view: 0, condition: 3, grade: 7, sqft_above: 1560, yr_built: 1975, yr_renovated: 0,
    zipcode: '98103', lat: 47.57, long: -122.23, sqft_living15: 1840, sqft_lot15: 7620 };
  const zipIdx = (enc, z) => 1 + fit.encoded_columns.indexOf('zipcode_' + z);
  const known = Core.encode(fit, raw, RULES);
  assert.equal(known.unseenZipcode, false);
  assert.equal(known.x[zipIdx(known, '98103')], 1);
  const zipCols = fit.encoded_columns.map((c, j) => [c, j + 1]).filter(([c]) => c.startsWith('zipcode_'));
  assert.equal(zipCols.reduce((s, [, j]) => s + known.x[j], 0), 1);
  const base = Core.encode(fit, { ...raw, zipcode: fit.zipcode_baseline }, RULES);
  assert.equal(base.unseenZipcode, false);
  assert.equal(zipCols.reduce((s, [, j]) => s + base.x[j], 0), 0);
  const unseen = Core.encode(fit, { ...raw, zipcode: '99999' }, RULES);
  assert.equal(unseen.unseenZipcode, true);
  assert.deepEqual(unseen.x, base.x);
  const reno = Core.encode(fit, { ...raw, yr_renovated: 2005 }, RULES);
  assert.equal(reno.x[1 + fit.encoded_columns.indexOf('is_renovated')], 1);
  assert.equal(reno.x[1 + fit.encoded_columns.indexOf('yr_renovated_effective')], 2005);
  assert.equal(known.x[1 + fit.encoded_columns.indexOf('yr_renovated_effective')], 1975);
});

test('official All-in: prediction = intercept + sum of contributions; PI contains it; k fixed at 18', () => {
  const allin = OFFICIAL.baselines.allin;
  assert.equal(allin.k, 18);
  assert.equal(allin.canonical_groups.length, 18);
  assert.equal(Core.testModelKey(OFFICIAL, 'allin'), 'allin');
  const raw = {};
  Core.inputSpec(allin.fit, OFFICIAL.inputs).forEach((s) => { raw[s.name] = s.default; });
  const out = Core.predict(allin.fit, raw, RULES);
  close(out.logPrediction, out.intercept + out.contributions.reduce((a, c) => a + c.contribution, 0), 1e-9, 'sum');
  assert.ok(out.lower < out.prediction && out.prediction < out.upper);
  close(out.prediction, Math.exp(out.logPrediction), 1e-6, 'exp');
});

test('official model_data has no test results and no test rows (TR-01)', () => {
  assert.equal(OFFICIAL.test, undefined);
  assert.equal(OFFICIAL.test_inputs.written, false);
  assert.equal(OFFICIAL.test_inputs.rows.length, 0);
});

test('predictor inputs: only the source features the model uses, training medians as defaults', () => {
  const fit = OFFICIAL.baselines.allin.fit;
  const specs = Core.inputSpec(fit, OFFICIAL.inputs);
  assert.deepEqual(specs.map((s) => s.name), fit.uses_source_features);
  assert.ok(!specs.some((s) => s.name === 'sqft_basement'));
  const sqft = specs.find((s) => s.name === 'sqft_living');
  assert.equal(sqft.default, OFFICIAL.inputs.features.sqft_living.median);
  assert.equal(Core.outOfRange(sqft, sqft.max + 1), true);
  assert.equal(Core.outOfRange(sqft, sqft.median), false);
  const zip = specs.find((s) => s.name === 'zipcode');
  assert.deepEqual(zip.categories, fit.zipcode_categories);
  assert.equal(zip.baseline, fit.zipcode_baseline);
});

test('metric-only models offer no prediction', () => {
  assert.equal(Core.canPredict({ kind: 'metric_only', model_key: 'ridge' }), false);
  assert.equal(Core.canPredict({ status: { state: 'invalid' }, fit: null }), false);
  assert.equal(Core.canPredict(OFFICIAL.baselines.allin), true);
  assert.throws(() => Core.predict(null, {}, RULES));
});

// ---- fixture: every test row of every ols_subset model ---------------------------------------
test('JS prediction, PI and covered reproduce the contract on every test row', needFixture, () => {
  const md = FIXTURE;
  const byKey = entries(md);
  const iActual = md.test_inputs.fields.indexOf('actual_price');
  let checked = 0;
  for (const [key, t] of Object.entries(md.test)) {
    if (t.kind !== 'ols_subset') continue;
    const fit = byKey[key].fit;
    for (let i = 0; i < md.test_inputs.rows.length; i++) {
      const raw = Core.rowObject(md.test_inputs, i);
      const out = Core.predict(fit, raw, md.preprocess);
      close(out.prediction, t.predicted[i], TOL, `${key} row ${i} predicted`);
      close(out.lower, t.lower[i], TOL, `${key} row ${i} lower`);
      close(out.upper, t.upper[i], TOL, `${key} row ${i} upper`);
      const actual = md.test_inputs.rows[i][iActual];
      assert.equal(out.lower <= actual && actual <= out.upper, t.covered[i], `${key} row ${i} covered`);
      checked++;
    }
  }
  assert.ok(checked > 0);
});

test('fixture: Test block model per method follows the winners; invalid entries never win', needFixture, () => {
  const md = FIXTURE;
  assert.equal(Core.testModelKey(md, 'allin'), 'allin');
  for (const [method, w] of Object.entries(md.winners.method_winners)) {
    assert.equal(Core.testModelKey(md, method), w.model_key);
    const list = md.methods[method];
    const flagged = list.filter((e) => e.is_method_winner).map((e) => e.model_key);
    assert.deepEqual(flagged, [w.model_key]);
    const best = list.filter((e) => e.status.state === 'valid')
      .sort((a, b) => a.cv.mean.rmse - b.cv.mean.rmse || a.k - b.k)[0];
    assert.equal(best.model_key, w.model_key);
    list.filter((e) => e.status.state === 'invalid').forEach((e) => assert.equal(e.is_method_winner, false));
  }
  assert.ok(md.test[md.winners.overall.model_key]);
});
