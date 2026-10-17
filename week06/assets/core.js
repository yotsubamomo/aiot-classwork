/* DIC-02 Feature Selection Explorer - pure functions (no DOM), testable in Node. */
(function (root) {
  'use strict';

  const STATE_DUMMIES = { Florida: 'State_Florida', 'New York': 'State_New York' };

  /** Value of one model feature for the given inputs (State is one-hot, California = 0, 0). */
  function featureValue(feature, inputs) {
    if (feature === 'State_Florida' || feature === 'State_New York') {
      return STATE_DUMMIES[inputs.state] === feature ? 1 : 0;
    }
    return Number(inputs[feature]) || 0;
  }

  /** Point prediction, 95% prediction interval and per-feature contributions of an OLS model. */
  function predict(model, inputs) {
    const coefs = model.coefficients;
    const x = [1, ...model.features.map((f) => featureValue(f, inputs))];
    let pred = 0;
    const contributions = [];
    coefs.forEach((c, i) => {
      const term = c.coef * x[i];
      pred += term;
      if (i > 0) contributions.push({ feature: c.feature, value: x[i], contribution: term });
    });
    // Var(prediction error) = s^2 * (1 + x0' (X'X)^-1 x0)
    let quad = 0;
    for (let i = 0; i < x.length; i++) {
      for (let j = 0; j < x.length; j++) quad += x[i] * model.xtx_inv[i][j] * x[j];
    }
    const half = model.t_crit * Math.sqrt(model.s2 * (1 + quad));
    return { prediction: pred, lower: pred - half, upper: pred + half, intercept: coefs[0].coef, contributions };
  }

  /** The k with the lowest CV RMSE for one scheme (ties -> smaller k). */
  function bestK(modelsForScheme) {
    return modelsForScheme.reduce((best, m) => (m.cv_rmse < best.cv_rmse ? m : best)).k;
  }

  /** The (scheme, k) entry with the lowest CV RMSE across all schemes. */
  function bestOverall(models) {
    let best = null;
    Object.entries(models).forEach(([scheme, list]) => list.forEach((m) => {
      if (!best || m.cv_rmse < best.model.cv_rmse) best = { scheme, model: m };
    }));
    return best;
  }

  function mean(values) { return values.reduce((a, b) => a + b, 0) / values.length; }

  function std(values) {
    const m = mean(values);
    return Math.sqrt(values.reduce((a, v) => a + (v - m) ** 2, 0) / (values.length - 1));
  }

  function usd(value, digits = 0) {
    const sign = value < 0 ? '-' : '';
    return sign + '$' + Math.abs(value).toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
  }

  function num(value, digits = 4) {
    return Number(value).toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
  }

  function pValue(p) {
    if (p < 0.0001) return '< 0.0001';
    return p.toFixed(4);
  }

  /** "Profit = b0 + b1 x (feature) ..." with signs written out. */
  function equation(model) {
    const [b0, ...rest] = model.coefficients;
    const terms = rest.map((c) => `${c.coef < 0 ? '-' : '+'} ${Math.abs(c.coef).toFixed(4)} × (${c.feature})`);
    return `Profit = ${num(b0.coef, 2)} ${terms.join(' ')}`.trim();
  }

  const api = { featureValue, predict, bestK, bestOverall, mean, std, usd, num, pValue, equation };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Core = api;
})(typeof window !== 'undefined' ? window : globalThis);
