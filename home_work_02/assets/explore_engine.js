/* HW2 V2 Exploratory run engine (Spec V2 「前處理與洩漏邊界」「切分與交叉驗證」「候選有效性」「評估、預測區間與
 * 即時預測器」「Exploratory run 結果契約」). Pure functions: no page, no network, no storage; the same file
 * runs in the browser (window.HW2ExploreEngine) and in Node (module.exports).
 *
 * #74 (V2-T1) builds the All-in candidate only. The chain, in this order (Brief V2 §5.5, E-1):
 *   1. LoadResult (assets/explore_load.js): CSV structure checks only, any row.
 *   2. Fixed-seed row-wise 80/20 split, then a fixed-seed 5-fold assignment of the training rows.
 *      PRNG: mulberry32 (32-bit integer arithmetic) with Fisher-Yates; the split draws from
 *      mulberry32(seed), the folds from mulberry32(seed + 1). n_test = floor(0.2 n + 0.5), kept in
 *      [1, n - 1]; the first n_test shuffled rows are the test rows. Fold of the training row at
 *      shuffled position q is q mod 5. hw2/explore_reference.py implements the same algorithm.
 *   3. Training-set layer (whole training set only): a categorical column with more than 20 distinct
 *      values on the training rows is excluded (EXCLUDED_TOO_MANY_LEVELS), a column with one distinct
 *      value on the training rows is excluded (EXCLUDED_CONSTANT); the kept columns, in CSV order,
 *      are the feature groups and their canonical order. Test rows have no say.
 *   4. Fold layer: each fold's levels, baseline (the level seen first in that fold's training rows),
 *      one-hot columns and OLS come from that fold's training rows only; its validation rows are only
 *      scored (an unseen level is encoded as the baseline and counted). The canonical fit uses the same
 *      rules on the whole training set.
 *   5. A-1 validity: on every fold's training rows and on the whole training set the design (with
 *      the intercept) has full rank and df_resid >= 3, else INVALID_MODEL with the rule and the fold.
 *      Rank comes from a column-pivoted Householder QR of the column-equilibrated design, with the
 *      tolerance |r_00| * max(n, p) * eps (the rule of hw2/ols.py).
 *   6. CV metrics of a candidate = arithmetic mean of the five fold metrics, with the sample standard
 *      deviation (ddof 1), as in the formal package (hw2/models.py CV_STD_DDOF).
 *   7. Winners are fixed; only then are the test rows read, for the winners' canonical fits only:
 *      test metrics, per-row prediction, 95% PI y_hat +/- t(0.975, df_resid) * sqrt(s2 (1 + x0'(X'X)^-1 x0))
 *      on the original target scale (no log, no exp), covered = lower <= actual <= upper, coverage.
 *
 * Metrics are MAE, MSE, RMSE and R^2 (1 - SSE/SST around the mean of the scored rows; null when SST is
 * 0) in the target's own units. Nothing here reads model_data: the formal King County analysis is a
 * different problem. Strings from the data are carried as data only (DA D-2). */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.HW2ExploreEngine = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var ENGINE_VERSION = 'explore-engine 1 (V2-T1: All-in)';
  var SEED = 42;
  var TEST_FRACTION = 0.2;
  var N_FOLDS = 5;
  var MAX_LEVELS = 20;
  var MIN_DF_RESID = 3;
  var PI_LEVEL = 0.95;
  var CV_STD_DDOF = 1;
  var EPS = 2.220446049250313e-16;
  var METRICS = ['mae', 'mse', 'rmse', 'r2'];

  /* ---- PRNG, split and folds ---------------------------------------------------------------- */
  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return (t ^ (t >>> 14)) >>> 0;
    };
  }

  function shuffledIndices(n, next) {
    var a = [];
    for (var i = 0; i < n; i++) a.push(i);
    for (i = n - 1; i >= 1; i--) {
      var j = Math.floor((next() / 4294967296) * (i + 1));
      var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }
    return a;
  }

  function ascending(a, b) { return a - b; }

  function makeSplit(n, seed) {
    if (seed === undefined || seed === null) seed = SEED;
    var perm = shuffledIndices(n, mulberry32(seed));
    var nTest = Math.floor(TEST_FRACTION * n + 0.5);
    nTest = Math.min(Math.max(nTest, 1), n - 1);
    var test = perm.slice(0, nTest).sort(ascending);
    var train = perm.slice(nTest).sort(ascending);
    var order = shuffledIndices(train.length, mulberry32((seed + 1) >>> 0));
    var folds = new Array(train.length);
    for (var q = 0; q < order.length; q++) folds[order[q]] = q % N_FOLDS;
    return { train: train, test: test, folds: folds };
  }

  function checkSplit(split, n) {
    var seen = new Array(n);
    split.train.concat(split.test).forEach(function (r) {
      if (!(r >= 0 && r < n) || seen[r]) throw new Error('split: bad or repeated row ' + r);
      seen[r] = true;
    });
    if (split.folds.length !== split.train.length) throw new Error('split: one fold per training row');
    for (var f = 0; f < N_FOLDS; f++) {
      if (split.folds.indexOf(f) < 0) throw new Error('split: fold ' + f + ' is empty');
    }
  }

  /* ---- training-set layer: which columns become feature groups -------------------------------- */
  function trainDecisions(load, trainRows) {
    var columns = [], groups = [];
    load.columns.forEach(function (col) {
      if (col.index === load.target.index) {
        columns.push({ name: col.name, index: col.index, type: col.type, role: 'target', status: 'TARGET' });
        return;
      }
      var distinct = new Set();
      trainRows.forEach(function (r) { distinct.add(load.rows[r][col.index]); });
      var status = 'KEPT';
      if (distinct.size <= 1) status = 'EXCLUDED_CONSTANT';
      else if (col.type === 'categorical' && distinct.size > MAX_LEVELS) status = 'EXCLUDED_TOO_MANY_LEVELS';
      var entry = { name: col.name, index: col.index, type: col.type, role: 'feature', status: status,
        n_distinct_train: distinct.size };
      columns.push(entry);
      if (status === 'KEPT') groups.push({ name: col.name, index: col.index, type: col.type });
    });
    return { columns: columns, groups: groups };
  }

  /* ---- fold layer: levels, baseline and one-hot columns from the given rows only -------------- */
  function fitEncoding(load, groups, rows) {
    var encGroups = [], columns = [];
    groups.forEach(function (g) {
      if (g.type === 'numeric') {
        encGroups.push({ name: g.name, index: g.index, type: 'numeric' });
        columns.push({ group: g.name, level: null });
        return;
      }
      var levels = [], seen = new Set();
      rows.forEach(function (r) {
        var v = load.rows[r][g.index];
        if (!seen.has(v)) { seen.add(v); levels.push(v); }
      });
      encGroups.push({ name: g.name, index: g.index, type: 'categorical', levels: levels, baseline: levels.length ? levels[0] : null });
      levels.slice(1).forEach(function (lv) { columns.push({ group: g.name, level: lv }); });
    });
    return { groups: encGroups, columns: columns };
  }

  /* Rows -> encoded matrix (no intercept). Unseen levels are the baseline (all zeros), counted. */
  function encodeRows(load, enc, rows) {
    var X = [], unseenRows = 0, unseenByGroup = {};
    rows.forEach(function (r) {
      var src = load.rows[r], x = [], unseen = false;
      enc.groups.forEach(function (g) {
        var v = src[g.index];
        if (g.type === 'numeric') { x.push(v); return; }
        if (g.levels.indexOf(v) < 0) {
          unseen = true;
          unseenByGroup[g.name] = (unseenByGroup[g.name] || 0) + 1;
        }
        for (var l = 1; l < g.levels.length; l++) x.push(v === g.levels[l] ? 1 : 0);
      });
      if (unseen) unseenRows++;
      X.push(x);
    });
    return { X: X, unseenRows: unseenRows, unseenByGroup: unseenByGroup };
  }

  function targetOf(load, rows) { return rows.map(function (r) { return load.rows[r][load.target.index]; }); }

  /* ---- Student t quantile (regularized incomplete beta, Lentz continued fraction) ------------- */
  var LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  function logGamma(x) {
    if (x < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * x)) - logGamma(1 - x);
    x -= 1;
    var a = LANCZOS[0], t = x + 7.5;
    for (var i = 1; i < 9; i++) a += LANCZOS[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }
  function betaCf(a, b, x) {
    var tiny = 1e-300, qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < tiny) d = tiny;
    d = 1 / d;
    var h = d;
    for (var m = 1; m <= 20000; m++) {
      var m2 = 2 * m, aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < tiny) d = tiny;
      c = 1 + aa / c; if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < tiny) d = tiny;
      c = 1 + aa / c; if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d;
      var del = d * c;
      h *= del;
      if (Math.abs(del - 1) < 1e-16) break;
    }
    return h;
  }
  function incBeta(a, b, x) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    var front = Math.exp(logGamma(a + b) - logGamma(a) - logGamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    if (x < (a + 1) / (a + b + 2)) return front * betaCf(a, b, x) / a;
    return 1 - front * betaCf(b, a, 1 - x) / b;
  }
  function tCdf(t, df) {
    var tail = 0.5 * incBeta(df / 2, 0.5, df / (df + t * t));
    return t >= 0 ? 1 - tail : tail;
  }
  function tQuantile(p, df) {
    if (!(p > 0.5 && p < 1) || !(df > 0)) throw new Error('tQuantile: p in (0.5, 1), df > 0');
    var lo = 0, hi = 1;
    while (tCdf(hi, df) < p) { lo = hi; hi *= 2; }
    for (var i = 0; i < 300 && hi - lo > 1e-15 * hi; i++) {
      var mid = 0.5 * (lo + hi);
      if (tCdf(mid, df) < p) lo = mid; else hi = mid;
    }
    return 0.5 * (lo + hi);
  }

  /* ---- OLS with the actual rank (pivoted Householder QR on the equilibrated design) ----------- */
  function fitOls(X, y) {
    var n = X.length, p = (X.length ? X[0].length : 0) + 1;
    var D = X.map(function (row) { return [1].concat(row); });
    if (n === 0) D = [];
    var norms = new Float64Array(p), j, i, k;
    for (j = 0; j < p; j++) {
      var s = 0;
      for (i = 0; i < n; i++) s += D[i][j] * D[i][j];
      norms[j] = s > 0 ? Math.sqrt(s) : 1;
    }
    var A = [];
    for (j = 0; j < p; j++) {
      var col = new Float64Array(n);
      for (i = 0; i < n; i++) col[i] = D[i][j] / norms[j];
      A.push(col);
    }
    var b = Float64Array.from(y);
    var perm = [];
    for (j = 0; j < p; j++) perm.push(j);
    var kmax = Math.min(n, p), rdiag = new Float64Array(kmax);
    for (k = 0; k < kmax; k++) {
      var best = k, bestN = -1;
      for (j = k; j < p; j++) {
        var ss = 0, cj = A[j];
        for (i = k; i < n; i++) ss += cj[i] * cj[i];
        if (ss > bestN) { bestN = ss; best = j; }
      }
      if (best !== k) {
        var tc = A[k]; A[k] = A[best]; A[best] = tc;
        var tp = perm[k]; perm[k] = perm[best]; perm[best] = tp;
      }
      var x = A[k], norm = 0;
      for (i = k; i < n; i++) norm += x[i] * x[i];
      norm = Math.sqrt(norm);
      if (norm === 0) { rdiag[k] = 0; continue; }
      var alpha = x[k] > 0 ? -norm : norm;
      var v0 = x[k] - alpha, vtv = v0 * v0;
      for (i = k + 1; i < n; i++) vtv += x[i] * x[i];
      var apply = function (c) {
        var dot = v0 * c[k];
        for (var ii = k + 1; ii < n; ii++) dot += x[ii] * c[ii];
        var f = 2 * dot / vtv;
        c[k] -= f * v0;
        for (ii = k + 1; ii < n; ii++) c[ii] -= f * x[ii];
      };
      for (j = k + 1; j < p; j++) apply(A[j]);
      apply(b);
      x[k] = alpha;
      for (i = k + 1; i < n; i++) x[i] = 0;
      rdiag[k] = alpha;
    }
    var tol = (kmax ? Math.abs(rdiag[0]) : 0) * Math.max(n, p) * EPS;
    var rank = 0;
    for (k = 0; k < kmax; k++) if (Math.abs(rdiag[k]) > tol) rank++;
    if (rank < p) return { ok: false, rule: 'rank_deficient', rank: rank, n_columns: p, n: n, df_resid: n - rank };
    var dfResid = n - rank;
    if (dfResid < MIN_DF_RESID) return { ok: false, rule: 'df_resid_lt_3', rank: rank, n_columns: p, n: n, df_resid: dfResid };
    /* R is A[j][i] for i <= j. Solve R z = (Q'y)[0:p]; invert R. */
    var z = new Float64Array(p);
    for (i = p - 1; i >= 0; i--) {
      var acc = b[i];
      for (j = i + 1; j < p; j++) acc -= A[j][i] * z[j];
      z[i] = acc / A[i][i];
    }
    var coef = new Array(p);
    for (i = 0; i < p; i++) coef[perm[i]] = z[i] / norms[perm[i]];
    var Rinv = [];
    for (i = 0; i < p; i++) Rinv.push(new Float64Array(p));
    for (j = 0; j < p; j++) {
      Rinv[j][j] = 1 / A[j][j];
      for (i = j - 1; i >= 0; i--) {
        var sum = 0;
        for (k = i + 1; k <= j; k++) sum += A[k][i] * Rinv[k][j];
        Rinv[i][j] = -sum / A[i][i];
      }
    }
    var xtx = [];
    for (i = 0; i < p; i++) xtx.push(new Array(p));
    for (i = 0; i < p; i++) {
      for (j = 0; j < p; j++) {
        var m = 0;
        for (k = Math.max(i, j); k < p; k++) m += Rinv[i][k] * Rinv[j][k];
        xtx[perm[i]][perm[j]] = m / (norms[perm[i]] * norms[perm[j]]);
      }
    }
    for (i = 0; i < p; i++) {
      for (j = i + 1; j < p; j++) { var avg = (xtx[i][j] + xtx[j][i]) / 2; xtx[i][j] = avg; xtx[j][i] = avg; }
    }
    var sse = 0, mean = 0;
    for (i = 0; i < n; i++) mean += y[i];
    mean /= n;
    var sst = 0;
    for (i = 0; i < n; i++) {
      var e = y[i] - dot(D[i], coef);
      sse += e * e;
      sst += (y[i] - mean) * (y[i] - mean);
    }
    var r2 = sst > 0 ? 1 - sse / sst : null;
    return {
      ok: true, n: n, n_columns: p, rank: rank, df_resid: dfResid, coef: coef, xtx_inv: xtx,
      s2: sse / dfResid, r2: r2, adj_r2: r2 === null ? null : 1 - (1 - r2) * (n - 1) / dfResid,
      t_crit: tQuantile(0.5 + PI_LEVEL / 2, dfResid)
    };
  }

  function dot(a, b) {
    var s = 0;
    for (var i = 0; i < a.length; i++) s += a[i] * b[i];
    return s;
  }

  /* y_hat and the 95% PI for one design row x (intercept first). */
  function interval(fit, x) {
    var yhat = dot(x, fit.coef), q = 0;
    for (var i = 0; i < x.length; i++) q += x[i] * dot(fit.xtx_inv[i], x);
    var half = fit.t_crit * Math.sqrt(fit.s2 * (1 + q));
    return { predicted: yhat, lower: yhat - half, upper: yhat + half };
  }

  function metricsOf(actual, predicted) {
    var n = actual.length, se = 0, ae = 0, mean = 0, sst = 0, i;
    for (i = 0; i < n; i++) mean += actual[i];
    mean /= n;
    for (i = 0; i < n; i++) {
      var e = predicted[i] - actual[i];
      se += e * e; ae += Math.abs(e);
      sst += (actual[i] - mean) * (actual[i] - mean);
    }
    var mse = se / n;
    return { mae: ae / n, mse: mse, rmse: Math.sqrt(mse), r2: sst > 0 ? 1 - se / sst : null };
  }

  /* ---- one candidate: CV on the folds and the canonical fit ------------------------------------ */
  function levelsOf(enc) {
    var out = {};
    enc.groups.forEach(function (g) { if (g.type === 'categorical') out[g.name] = { levels: g.levels.slice(), baseline: g.baseline }; });
    return out;
  }

  function median(values) {
    var s = values.slice().sort(ascending), n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }

  function inputsOf(load, enc, rows) {
    var out = {};
    enc.groups.forEach(function (g) {
      if (g.type !== 'numeric') return;
      var v = rows.map(function (r) { return load.rows[r][g.index]; });
      out[g.name] = { min: Math.min.apply(null, v), max: Math.max.apply(null, v), median: median(v) };
    });
    return out;
  }

  function fitRecord(load, enc, rows, fit) {
    return {
      n_train: fit.n, n_columns: fit.n_columns, rank: fit.rank, df_resid: fit.df_resid,
      s2: fit.s2, r2_train: fit.r2, adj_r2_train: fit.adj_r2, t_crit: fit.t_crit, pi_level: PI_LEVEL,
      groups: enc.groups.map(function (g) { return g.name; }),
      encoded_columns: enc.columns.map(function (c) { return { group: c.group, level: c.level }; }),
      coef: fit.coef.slice(), xtx_inv: fit.xtx_inv.map(function (r) { return r.slice(); }),
      levels: levelsOf(enc), inputs: inputsOf(load, enc, rows),
      encoding: enc
    };
  }

  function evaluateCandidate(load, groups, split, method, k) {
    var folds = [], reasons = [];
    var key = method === 'allin' ? 'allin' : method + '_k' + (k < 10 ? '0' : '') + k;
    var names = groups.map(function (g) { return g.name; });
    if (!groups.length) {
      return { key: key, method: method, k: 0, status: 'INVALID_MODEL',
        reasons: [{ rule: 'no_feature_groups', scope: 'training_set', fold: null }],
        folds: [], cv: null, canonical_groups: [], fit: null };
    }
    for (var f = 0; f < N_FOLDS; f++) {
      var trainRows = [], validRows = [];
      split.train.forEach(function (r, i) { (split.folds[i] === f ? validRows : trainRows).push(r); });
      var enc = fitEncoding(load, groups, trainRows);
      var fit = fitOls(encodeRows(load, enc, trainRows).X, targetOf(load, trainRows));
      var rec = { fold: f, n_train: trainRows.length, n_valid: validRows.length, groups: names.slice(),
        levels: levelsOf(enc), n_columns: fit.n_columns, rank: fit.rank, df_resid: fit.df_resid };
      if (!fit.ok) {
        rec.status = 'invalid'; rec.rule = fit.rule; rec.metrics = null;
        reasons.push({ rule: fit.rule, scope: 'fold', fold: f, rank: fit.rank, n_columns: fit.n_columns, df_resid: fit.df_resid });
      } else {
        var valid = encodeRows(load, enc, validRows);
        var pred = valid.X.map(function (x) { return dot([1].concat(x), fit.coef); });
        rec.status = 'ok'; rec.rule = null; rec.coef = fit.coef.slice();
        rec.metrics = metricsOf(targetOf(load, validRows), pred);
        rec.n_valid_unseen = valid.unseenRows;
      }
      folds.push(rec);
    }
    var cEnc = fitEncoding(load, groups, split.train);
    var cFit = fitOls(encodeRows(load, cEnc, split.train).X, targetOf(load, split.train));
    if (!cFit.ok) {
      reasons.push({ rule: cFit.rule, scope: 'training_set', fold: null, rank: cFit.rank, n_columns: cFit.n_columns, df_resid: cFit.df_resid });
    }
    var cv = null, status = reasons.length ? 'INVALID_MODEL' : 'VALID';
    if (status === 'VALID') {
      cv = { n_folds: N_FOLDS, std_ddof: CV_STD_DDOF, mean: {}, std: {} };
      METRICS.forEach(function (m) {
        var vals = folds.map(function (r) { return r.metrics[m]; });
        if (vals.some(function (v) { return v === null; })) { cv.mean[m] = null; cv.std[m] = null; return; }
        var mu = vals.reduce(function (a, v) { return a + v; }, 0) / vals.length;
        var ss = vals.reduce(function (a, v) { return a + (v - mu) * (v - mu); }, 0);
        cv.mean[m] = mu;
        cv.std[m] = Math.sqrt(ss / (vals.length - CV_STD_DDOF));
      });
    }
    return { key: key, method: method, k: groups.length, status: status, reasons: reasons, folds: folds, cv: cv,
      canonical_groups: names.slice(),
      fit: status === 'VALID' ? fitRecord(load, cEnc, split.train, cFit) : null };
  }

  /* ---- test: only for the frozen winners' canonical fits --------------------------------------- */
  function evaluateTest(load, candidate, testRows) {
    var fit = candidate.fit;
    var enc = encodeRows(load, fit.encoding, testRows);
    var actual = targetOf(load, testRows);
    var predicted = [], lower = [], upper = [], covered = [];
    enc.X.forEach(function (x, i) {
      var pi = interval(fit, [1].concat(x));
      predicted.push(pi.predicted); lower.push(pi.lower); upper.push(pi.upper);
      covered.push(pi.lower <= actual[i] && actual[i] <= pi.upper);
    });
    var nCovered = covered.filter(Boolean).length;
    return { key: candidate.key, rows: testRows.slice(), n_test: testRows.length, actual: actual,
      predicted: predicted, lower: lower, upper: upper, covered: covered,
      n_covered: nCovered, coverage: nCovered / testRows.length,
      metrics: metricsOf(actual, predicted), n_unseen_rows: enc.unseenRows, n_unseen_by_group: enc.unseenByGroup };
  }

  /* ---- the run ---------------------------------------------------------------------------------- */
  function now(options) {
    if (options && options.now) return options.now();
    return typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now();
  }

  function publicCandidate(c) {
    var out = Object.assign({}, c);
    if (out.fit) { out.fit = Object.assign({}, out.fit); delete out.fit.encoding; }
    return out;
  }

  function run(load, options) {
    options = options || {};
    var t0 = now(options);
    if (!load || !load.ok) throw new Error('run: needs an accepted LoadResult');
    var seed = options.seed === undefined ? SEED : options.seed;
    var n = load.rows.length;
    var split = options.split ? { train: options.split.train.slice(), test: options.split.test.slice(), folds: options.split.folds.slice() }
      : makeSplit(n, seed);
    checkSplit(split, n);
    var meta = {
      engine_version: ENGINE_VERSION, problem: options.problem || null, source: options.source || null,
      sha256: load.sha256, target: load.target.name, n_rows_read: load.n_rows_read, n_rows: n,
      n_rows_dropped_missing: load.n_rows_dropped_missing, seed: seed, split_injected: !!options.split,
      pi_level: PI_LEVEL, max_levels: MAX_LEVELS, min_df_resid: MIN_DF_RESID, cv_std_ddof: CV_STD_DDOF,
      timing_ms: {}
    };
    var decided = trainDecisions(load, split.train);
    var t1 = now(options);
    var allin = evaluateCandidate(load, decided.groups, split, 'allin');
    var t2 = now(options);
    meta.timing_ms.decisions = t1 - t0;
    meta.timing_ms.allin = t2 - t1;
    var result = {
      meta: meta,
      columns: decided.columns,
      groups: decided.groups.map(function (g) { return { name: g.name, index: g.index, type: g.type }; }),
      split: { train: split.train, test: split.test, folds: split.folds, n_folds: N_FOLDS,
        prng: 'mulberry32 + Fisher-Yates (split seed, folds seed + 1)' }
    };
    var candidates = [allin];
    var valid = candidates.filter(function (c) { return c.status === 'VALID'; });
    if (!valid.length) {
      result.run = { status: 'REJECTED', reason: 'ALL_CANDIDATES_INVALID',
        invalid_candidates: candidates.map(function (c) { return { key: c.key, status: c.status, reasons: c.reasons }; }) };
      meta.timing_ms.total = now(options) - t0;
      return result;
    }
    /* winners are fixed here (#74: the All-in baseline is the only candidate and so the overall
     * CV winner); the test rows are read only after this point. */
    var winners = { method_winners: {}, overall: { method: 'allin', key: allin.key, k: allin.k }, test_keys: [allin.key] };
    var test = {};
    winners.test_keys.forEach(function (key) {
      var c = candidates.filter(function (x) { return x.key === key; })[0];
      test[key] = evaluateTest(load, c, split.test);
    });
    meta.timing_ms.test = now(options) - t2;
    meta.timing_ms.total = now(options) - t0;
    result.run = { status: 'COMPLETED', reason: null };
    result.candidates = candidates.map(publicCandidate);
    result.winners = winners;
    result.test = test;
    return result;
  }

  /* ---- live predictor ---------------------------------------------------------------------------- */
  function canPredict(candidate) {
    return !!(candidate && candidate.status === 'VALID' && candidate.fit && candidate.fit.coef && candidate.fit.xtx_inv);
  }

  /* Inputs the predictor asks for: one per feature group of the fit (training-set values only). */
  function inputSpec(fit) {
    return fit.groups.map(function (name) {
      var lv = fit.levels[name];
      if (lv) return { name: name, type: 'categorical', levels: lv.levels.slice(), baseline: lv.baseline, default: lv.baseline };
      var info = fit.inputs[name];
      return { name: name, type: 'numeric', min: info.min, max: info.max, median: info.median, default: info.median };
    });
  }

  /* Point prediction and 95% PI for raw source values {group: value}. Out-of-range numbers are still
   * computed (warning); an unseen category is computed as the baseline (warning). */
  function predict(candidate, raw) {
    if (!canPredict(candidate)) throw new Error('this candidate is not VALID: no prediction');
    var fit = candidate.fit, x = [1], warnings = [];
    inputSpec(fit).forEach(function (spec) {
      var v = raw[spec.name];
      if (spec.type === 'numeric') {
        var num = typeof v === 'number' ? v : Number(String(v).trim());
        if (v === null || v === undefined || String(v).trim() === '' || !isFinite(num)) throw new Error('input ' + spec.name + ' is not a number');
        if (num < spec.min || num > spec.max) warnings.push({ type: 'out_of_range', group: spec.name, value: num, min: spec.min, max: spec.max });
        x.push(num);
        return;
      }
      var s = String(v);
      if (spec.levels.indexOf(s) < 0) warnings.push({ type: 'unseen_level', group: spec.name, value: s, baseline: spec.baseline });
      for (var l = 1; l < spec.levels.length; l++) x.push(s === spec.levels[l] ? 1 : 0);
    });
    var pi = interval(fit, x);
    return { predicted: pi.predicted, lower: pi.lower, upper: pi.upper, warnings: warnings, design: x };
  }

  return {
    ENGINE_VERSION: ENGINE_VERSION, SEED: SEED, TEST_FRACTION: TEST_FRACTION, N_FOLDS: N_FOLDS,
    MAX_LEVELS: MAX_LEVELS, MIN_DF_RESID: MIN_DF_RESID, PI_LEVEL: PI_LEVEL, CV_STD_DDOF: CV_STD_DDOF,
    mulberry32: mulberry32, shuffledIndices: shuffledIndices, makeSplit: makeSplit,
    trainDecisions: trainDecisions, fitEncoding: fitEncoding, encodeRows: encodeRows,
    fitOls: fitOls, tQuantile: tQuantile, metricsOf: metricsOf, interval: interval,
    evaluateCandidate: evaluateCandidate, run: run,
    canPredict: canPredict, inputSpec: inputSpec, predict: predict
  };
});
