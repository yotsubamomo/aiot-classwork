/* HW2 dashboard core: the dashboard's own preprocessing and OLS prediction with the 95% PI.
 *
 * Works in the browser (window.HW2Core) and in Node (module.exports) so that the Node test can
 * check it against the exported model_data. It redoes the fixed transforms of
 * model_data.preprocess (sale_days from the base date; is_renovated and the effective renovation
 * year; zipcode one-hot over the categories of the model's fit, unseen category -> baseline) and
 * evaluates, on the log scale, yhat = x'b and yhat +/- t * sqrt(s2 * (1 + x'(X'X)^-1 x)), then exp.
 *
 * This module only predicts from raw inputs. It computes no test metric, no coverage and no
 * selection: the dashboard reads every test number from model_data.test (BR-01; DA B-3, G-3).
 */
(function (root, factory) {
  'use strict';
  var core = factory();
  if (typeof module === 'object' && module.exports) module.exports = core;
  else root.HW2Core = core;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var DAY_MS = 86400000;
  var CSV_DATE = /^(\d{4})(\d{2})(\d{2})T000000$/;
  var ISO_DATE = /^(\d{4})-(\d{2})-(\d{2})$/;
  var ZIP_PREFIX = 'zipcode_';

  function utcDay(y, m, d) {
    var t = Date.UTC(y, m - 1, d);
    var check = new Date(t);
    if (check.getUTCFullYear() !== y || check.getUTCMonth() !== m - 1 || check.getUTCDate() !== d) {
      throw new Error('not a calendar date: ' + y + '-' + m + '-' + d);
    }
    return t / DAY_MS;
  }

  function parseDate(text) {
    var s = String(text);
    var m = CSV_DATE.exec(s) || ISO_DATE.exec(s);
    if (!m) throw new Error('date ' + JSON.stringify(s) + ' is neither YYYYMMDDT000000 nor YYYY-MM-DD');
    return utcDay(Number(m[1]), Number(m[2]), Number(m[3]));
  }

  /* Days from the base date (model_data.preprocess.date.base_date, ISO) to a sale date. */
  function saleDays(dateText, baseDateIso) {
    return parseDate(dateText) - parseDate(baseDateIso);
  }

  function isoFromDays(days, baseDateIso) {
    var t = (parseDate(baseDateIso) + Math.floor(days)) * DAY_MS;
    return new Date(t).toISOString().slice(0, 10);
  }

  /* is_renovated = 1 if yr_renovated > 0 else 0; effective = yr_renovated if > 0 else yr_built. */
  function renovation(yrRenovated, yrBuilt) {
    var r = Number(yrRenovated);
    if (!(r >= 0)) throw new Error('yr_renovated must be 0 (never renovated) or a year');
    return r > 0 ? { is_renovated: 1, effective: r } : { is_renovated: 0, effective: Number(yrBuilt) };
  }

  /* Raw source-feature values -> design row [1, encoded columns in fit.encoded_columns order]. */
  function encode(fit, raw, rules) {
    var base = rules.date.base_date;
    var zipcode = raw.zipcode == null ? null : String(raw.zipcode);
    var categories = fit.zipcode_categories || [];
    var usesZip = fit.groups.indexOf('zipcode') >= 0;
    var unseen = usesZip && categories.indexOf(zipcode) < 0;
    var reno = fit.groups.indexOf('yr_renovated') >= 0 ? renovation(raw.yr_renovated, raw.yr_built) : null;
    var x = [1];
    fit.encoded_columns.forEach(function (col) {
      var v;
      if (col === 'sale_days') v = saleDays(raw.date, base);
      else if (col === 'is_renovated') v = reno.is_renovated;
      else if (col === 'yr_renovated_effective') v = reno.effective;
      else if (col.indexOf(ZIP_PREFIX) === 0) v = zipcode === col.slice(ZIP_PREFIX.length) ? 1 : 0;
      else {
        v = Number(raw[col]);
        if (!isFinite(v)) throw new Error('input ' + col + ' is not a number');
      }
      x.push(v);
    });
    return { x: x, unseenZipcode: unseen };
  }

  function dot(a, b) {
    var s = 0;
    for (var i = 0; i < a.length; i++) s += a[i] * b[i];
    return s;
  }

  function quadForm(x, m) {
    var s = 0;
    for (var i = 0; i < x.length; i++) s += x[i] * dot(m[i], x);
    return s;
  }

  /* Point prediction and 95% PI in USD for one raw input (OLS subset models only). */
  function predict(fit, raw, rules) {
    if (!fit || !fit.coef || !fit.xtx_inv) throw new Error('this model has no OLS fit: no prediction');
    var enc = encode(fit, raw, rules);
    var yhat = dot(enc.x, fit.coef);
    var half = fit.t_crit * Math.sqrt(fit.s2 * (1 + quadForm(enc.x, fit.xtx_inv)));
    var contributions = fit.encoded_columns.map(function (col, j) {
      return { column: col, value: enc.x[j + 1], coef: fit.coef[j + 1], contribution: fit.coef[j + 1] * enc.x[j + 1] };
    });
    return {
      logPrediction: yhat,
      prediction: Math.exp(yhat),
      lower: Math.exp(yhat - half),
      upper: Math.exp(yhat + half),
      intercept: fit.coef[0],
      contributions: contributions,
      unseenZipcode: enc.unseenZipcode
    };
  }

  /* One test_inputs row as an object keyed by test_inputs.fields. */
  function rowObject(testInputs, i) {
    var row = testInputs.rows[i];
    var out = {};
    testInputs.fields.forEach(function (f, j) { out[f] = row[j]; });
    return out;
  }

  /* A model entry offers a live prediction only if it is a valid OLS subset model with a fit. */
  function canPredict(entry) {
    return !!(entry && entry.kind !== 'metric_only' && entry.status && entry.status.state === 'valid' &&
      entry.fit && entry.fit.coef && entry.fit.xtx_inv);
  }

  /* BR-01 point 5: the Test block shows the selected method's CV winner (All-in shows itself). */
  function testModelKey(modelData, method) {
    var w = modelData.winners || {};
    if (method === 'allin') return (w.allin && w.allin.model_key) || 'allin';
    var mw = (w.method_winners || {})[method];
    return mw ? mw.model_key : null;
  }

  /* Raw inputs the predictor asks for: the source features used by the model's groups. */
  function inputSpec(fit, inputs) {
    return fit.uses_source_features.map(function (name) {
      var info = inputs.features[name] || {};
      var spec = { name: name, kind: info.kind, min: info.min, max: info.max, median: info.median };
      if (name === 'zipcode') {
        spec.kind = 'nominal';
        spec.categories = fit.zipcode_categories.slice();
        spec.baseline = fit.zipcode_baseline;
        spec.default = info.mode != null && fit.zipcode_categories.indexOf(info.mode) >= 0 ? info.mode : fit.zipcode_baseline;
      } else if (name === 'yr_renovated') {
        spec.kind = 'renovation';
        spec.min = info.renovated_min;
        spec.max = info.renovated_max;
        spec.default = Number(info.median) > 0 ? info.median : 0;
      } else {
        spec.default = info.median;
      }
      return spec;
    });
  }

  /* Out-of-range check against the training min..max (still computed; SR-07, Q32). */
  function outOfRange(spec, value) {
    if (spec.kind === 'nominal') return false;
    if (spec.kind === 'renovation' && Number(value) === 0) return false;
    if (spec.kind === 'date') return String(value) < String(spec.min) || String(value) > String(spec.max);
    var v = Number(value);
    return v < Number(spec.min) || v > Number(spec.max);
  }

  return {
    saleDays: saleDays,
    isoFromDays: isoFromDays,
    renovation: renovation,
    encode: encode,
    predict: predict,
    rowObject: rowObject,
    canPredict: canPredict,
    testModelKey: testModelKey,
    inputSpec: inputSpec,
    outOfRange: outOfRange
  };
});
