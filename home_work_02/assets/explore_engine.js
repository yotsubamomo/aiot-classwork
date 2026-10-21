/* HW2 V2 Exploratory run engine (Spec V2 「前處理與洩漏邊界」「切分與交叉驗證」「候選有效性、狀態與運算預算」
 * 「評估、預測區間與即時預測器」「Exploratory run 結果契約」「可重現性」). Pure functions: no page, no network, no
 * storage; the same file runs in the browser (window.HW2ExploreEngine) and in Node (module.exports).
 *
 * #74 (V2-T1) built the All-in candidate; #75 (V2-T2) added the four path methods, the candidate states,
 * the winners, the Lasso degeneracy (A-2) and the dependency diagnostic (A-3); #77 (V2-T4) adds the
 * per-method computing budget, failure isolation, the stepwise run that can be cancelled at the next
 * candidate boundary, progress events, and target-unit independent path criteria (DA
 * decision-20261022-issue75-lasso-early-stop R4-2, R4-3, R4-4). The chain, in this order (Brief V2 §5.5, E-1):
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
 * Path methods (#75; the criteria of hw2/selection.py, on each fold's training rows and once on the
 * whole training set; one feature group per step; k = 1..p):
 *   - Forward / Backward SFS: the RSS of the OLS on the given rows, from the Gram matrix of the centred,
 *     unit-norm encoded columns with minimum-norm solutions (hw2.selection.GroupGram).
 *   - RFE: remove the group with the smallest sd(X_g b_g) over the given rows.
 *   - Lasso path: exact LARS with the Lasso modification (a port of sklearn's lars_path, method "lasso",
 *     which the formal analysis uses) on the formal standardization (numeric columns centred and scaled
 *     by the population sd, one-hot columns 0/1, then every column centred) of the given rows; a group
 *     enters at the knot alpha before its first non-zero coefficient; order by entry alpha, largest
 *     first. A-2 (R4-1): when the path stops with groups that never entered -- for any reason -- the
 *     entered groups are the actual path, the others are shown after them in CSV order only, and every
 *     k beyond is INVALID_MODEL / lasso_path_degenerate with the true stop cause (R4-2):
 *     'active_set_degenerate' (an entering column whose residual on the active columns is <= 1e-6 of its
 *     norm, or below sklearn's pivot limit 1e-7), 'path_ended' (the path reached its end: the other
 *     groups' correlation with the residual is numerically zero), the numerical stops 'alpha_increasing',
 *     'max_iter' and 'multiple_drops', or 'target_constant' (no variation of the target on those rows).
 *   - Target units (R4-3, R4-4): every path criterion is computed on the target of the given rows
 *     centred and divided by its root mean square on the same rows (the scale s; 0 when the target is
 *     constant there, and then nothing is divided). Exact LARS, the RSS and sd(X_g b_g) are equivariant
 *     to that scaling, so the orders are unchanged, but every numerical threshold (sklearn's equality
 *     tolerance, the TIE_RTOL floors) becomes unit free: multiplying the target by any c > 0 gives the
 *     same paths, stops, causes and states. Entry alphas are reported on the original scale (the scaled
 *     alpha times s), i.e. sklearn's alpha of the path on the centred original target.
 *   - Ties (relative 1e-12, hw2.selection.TIE_RTOL) follow CSV order: forward and Lasso take the
 *     earlier group first, backward and RFE remove the later group first.
 * Winners (hw2/models.py determine_winners): a method's CV winner is its VALID candidate with the lowest
 * CV RMSE, ties to the smaller k (All-in is its own winner); the overall CV winner is the lowest CV RMSE
 * among them, ties in the order All-in, Forward SFS, Backward SFS, RFE, Lasso path. Winners with the
 * same canonical subset are one model and are scored once.
 * A-3: the All-in design of the whole training set (intercept, then the encoded columns), equilibrated,
 * is scanned in that order; a column within max(n, p) * eps of the span of the earlier independent
 * columns closes one linear relation, reported with all its columns and their feature groups.
 *
 * #77 (V2-T4; Spec V2 「候選有效性、狀態與運算預算」 SR-V2-03, 「可重現性」 SR-V2-04; Tickets Review adjustment B):
 *   - Budget: before a path method runs, its cost is estimated as (estimated OLS solves) x (training rows)
 *     x (encoded columns)^2, from the training-set encoding only: Forward / Backward / RFE count
 *     p(p+1)/2 solves per row set (O(p^2)), Lasso p steps per row set (O(p)), plus one fit per candidate
 *     and row set, on the five folds and the training set. A method whose estimate exceeds its budget
 *     constant (BUDGETS) is SKIPPED_RESOURCE_LIMIT as a whole: none of its paths or candidates is computed,
 *     its candidates carry the estimate and the budget. The decision uses the estimate only, never a
 *     clock, so it is part of the deterministic result. All-in is always attempted first, never skipped.
 *   - Resources: every matrix the run allocates is a design of a subset of the training (or test) rows by
 *     a subset of the training-set encoded columns (plus the intercept), its Gram or (X'X)^-1, so its
 *     size is known before the run (meta.budget); matrices are typed arrays, so a failed allocation is
 *     an ordinary exception. Any exception inside a method (All-in or a path method) makes that whole
 *     method FAILED, with the message and environment information; the other methods go on. FAILED and
 *     SKIPPED_RESOURCE_LIMIT candidates have no CV metrics, no fit and no canonical subset, and are never
 *     winners. A failure of the dependency diagnostic is reported in `dependencies.error`.
 *   - Steps and cancellation: createRun() returns a stepper; step() runs to the next yield point (after
 *     every fold fit, path step, LARS run, predictor-default column and, on larger data, every QR column
 *     step, Gram row, LARS iteration, diagnostic column and block of test rows: about YIELD_CELLS
 *     multiply-adds at most between two yields), so a page can keep its controls operable between steps. cancel() is honoured at the next candidate boundary
 *     (before the first candidate, and after each candidate or skipped method): the run then ends as
 *     CANCELLED, with no candidates, winners, test or other partial result -- only the counts of finished
 *     methods and candidates. A candidate in progress is never cut in the middle. run() drives the same
 *     stepper to the end synchronously.
 *   - Progress: options.onProgress(event) at the start and at every candidate boundary: the method, k,
 *     finished / total candidates and methods, the fraction and the elapsed time (non-deterministic);
 *     phase 'diagnostic' after the last candidate (the A-3 diagnostic runs then, after every boundary).
 *   - Deterministic part: everything but meta.timing_ms (per-method timings and the start time) and the
 *     environment information of a FAILED reason. Same content, target, seed, engine version and budget
 *     constants give the same values, bit for bit in the same engine.
 *   - options.hooks (tests only): candidate(method, k), fold(method, k, f) and path(method, rowSet) are
 *     called as the work starts; they count work and may throw to inject a failure.
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

  var ENGINE_VERSION = 'explore-engine 3.0 (V2-T4: budgets, cancellation, unit-free paths)';
  var SEED = 42;
  var TEST_FRACTION = 0.2;
  var N_FOLDS = 5;
  var MAX_LEVELS = 20;
  var MIN_DF_RESID = 3;
  var PI_LEVEL = 0.95;
  var CV_STD_DDOF = 1;
  var EPS = 2.220446049250313e-16;
  var METRICS = ['mae', 'mse', 'rmse', 'r2'];
  var PATH_METHODS = ['forward_sfs', 'backward_sfs', 'rfe', 'lasso_path'];
  var METHOD_ORDER = ['allin'].concat(PATH_METHODS);
  var TIE_RTOL = 1e-12;                       /* hw2.selection.TIE_RTOL */
  var LARS_MAX_ITER = 500;                    /* sklearn lars_path default */
  var LARS_DEGENERATE_RTOL = 1e-6;
  var LARS_PIVOT_ATOL = 1e-7;                 /* sklearn's own Cholesky pivot limit */
  var TINY32 = 1.1754943508222875e-38;        /* numpy float32 tiny */
  var EQ_TOL = 1.1920928955078125e-7;         /* numpy float32 eps (sklearn's equality_tolerance) */
  var RELATION_ZERO = 1e-9;
  /* #77: the per-method computing budget, in BUDGET_UNIT (measured; see doc/acceptance/ACCEPTANCE.md V2-27). */
  var BUDGET_UNIT = 'estimated OLS solves x training rows x encoded columns^2';
  var BUDGETS = { forward_sfs: 2e11, backward_sfs: 2e11, rfe: 2e11, lasso_path: 8e10 };
  /* Work between two yield points, in multiply-adds: a QR column step, a Gram row, a LARS iteration, a
   * diagnostic column or a block of test rows larger than this yields after itself (each yield is a step of
   * the run, never a cancellation point), so that one step stays well under a frame on the reference
   * machine. Small problems (50 Startups) never yield inside a fit. */
  var YIELD_CELLS = 2e5;

  /* Objects keyed by column names (fit.levels, fit.inputs, n_unseen_by_group, predictor inputs) get
   * their keys as own data properties and are read through own properties only, so that a name such as
   * `__proto__`, `constructor` or `toString` is an ordinary key (#74 R1-F2), not the prototype or an
   * inherited member. The objects stay plain, so the result contract serializes them as before. */
  function putOwn(obj, key, value) {
    Object.defineProperty(obj, key, { value: value, enumerable: true, writable: true, configurable: true });
    return obj;
  }
  function getOwn(obj, key) {
    return obj && Object.prototype.hasOwnProperty.call(obj, key) ? obj[key] : undefined;
  }

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

  /* Rows -> encoded columns (no intercept), one Float64Array per encoded column. Unseen levels are the
   * baseline (all zeros), counted. */
  function encodeCols(load, enc, rows) {
    var n = rows.length, cols = [], unseenRows = 0, unseenByGroup = {};
    enc.columns.forEach(function () { cols.push(new Float64Array(n)); });
    for (var i = 0; i < n; i++) {
      var src = load.rows[rows[i]], c = 0, unseen = false;
      for (var gi = 0; gi < enc.groups.length; gi++) {
        var g = enc.groups[gi], v = src[g.index];
        if (g.type === 'numeric') { cols[c++][i] = v; continue; }
        if (g.levels.indexOf(v) < 0) {
          unseen = true;
          putOwn(unseenByGroup, g.name, (getOwn(unseenByGroup, g.name) || 0) + 1);
        }
        for (var l = 1; l < g.levels.length; l++) cols[c++][i] = v === g.levels[l] ? 1 : 0;
      }
      if (unseen) unseenRows++;
    }
    return { cols: cols, n: n, unseenRows: unseenRows, unseenByGroup: unseenByGroup };
  }

  /* The design row of row i (intercept first). */
  function designRow(cols, i) {
    var x = [1];
    for (var j = 0; j < cols.length; j++) x.push(cols[j][i]);
    return x;
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

  /* ---- driving generators -------------------------------------------------------------------------- */
  function drive(gen) {
    var r = gen.next();
    while (!r.done) r = gen.next();
    return r.value;
  }

  /* ---- OLS with the actual rank (pivoted Householder QR on the equilibrated design) ----------- */
  /* cols: encoded columns (Float64Array each, no intercept), y: the target. A large QR yields between
   * its column steps (a step of the run, never a cancellation point). */
  function* olsSteps(cols, y) {
    var n = y.length, p = cols.length + 1, j, i, k;
    var colOf = function (jj) { return jj === 0 ? null : cols[jj - 1]; };
    var norms = new Float64Array(p);
    for (j = 0; j < p; j++) {
      var s = 0, src = colOf(j);
      for (i = 0; i < n; i++) { var dv = src === null ? 1 : src[i]; s += dv * dv; }
      norms[j] = s > 0 ? Math.sqrt(s) : 1;
    }
    var A = [];
    for (j = 0; j < p; j++) {
      var col = new Float64Array(n), sj = colOf(j);
      for (i = 0; i < n; i++) col[i] = (sj === null ? 1 : sj[i]) / norms[j];
      A.push(col);
    }
    var b = Float64Array.from(y);
    var perm = [];
    for (j = 0; j < p; j++) perm.push(j);
    var kmax = Math.min(n, p), rdiag = new Float64Array(kmax);
    for (k = 0; k < kmax; k++) {
      if (n * (p - k) > YIELD_CELLS) yield null;
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
        var d = v0 * c[k];
        for (var ii = k + 1; ii < n; ii++) d += x[ii] * c[ii];
        var f = 2 * d / vtv;
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
      var e = y[i] - rowDot(cols, i, coef);
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
  function fitOls(cols, y) { return drive(olsSteps(cols, y)); }

  /* x_i' coef with x_i = [1, cols[0][i], ...], summed in that order (the design row's dot product). */
  function rowDot(cols, i, coef) {
    var s = 0;
    s += 1 * coef[0];
    for (var j = 0; j < cols.length; j++) s += cols[j][i] * coef[j + 1];
    return s;
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
    enc.groups.forEach(function (g) { if (g.type === 'categorical') putOwn(out, g.name, { levels: g.levels.slice(), baseline: g.baseline }); });
    return out;
  }

  function median(values) {
    var s = values.slice().sort(ascending), n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }

  /* The predictor's numeric defaults are statistics of the whole training set: the same for every candidate
   * of a run, so they are computed once per (training rows, column) and reused (a sort per column). */
  var inputCache = typeof WeakMap === 'function' ? new WeakMap() : null;
  function numericInput(load, rows, index) {
    var byIndex = inputCache ? inputCache.get(rows) : null;
    if (inputCache && !byIndex) { byIndex = new Map(); inputCache.set(rows, byIndex); }
    if (byIndex && byIndex.has(index)) return byIndex.get(index);
    var v = rows.map(function (r) { return load.rows[r][index]; }), lo = Infinity, hi = -Infinity;
    for (var i = 0; i < v.length; i++) { if (v[i] < lo) lo = v[i]; if (v[i] > hi) hi = v[i]; }
    var info = { min: lo, max: hi, median: median(v) };
    if (byIndex) byIndex.set(index, info);
    return info;
  }
  function inputsOf(load, enc, rows) {
    var out = {};
    enc.groups.forEach(function (g) {
      if (g.type !== 'numeric') return;
      var info = numericInput(load, rows, g.index);
      putOwn(out, g.name, { min: info.min, max: info.max, median: info.median });
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

  function modelKey(method, k) { return method === 'allin' ? 'allin' : method + '_k' + (k < 10 ? '0' : '') + k; }

  function subsetGroups(groups, names) {
    return groups.filter(function (g) { return names.indexOf(g.name) >= 0; });
  }

  function foldRows(split, f) {
    var trainRows = [], validRows = [];
    split.train.forEach(function (r, i) { (split.folds[i] === f ? validRows : trainRows).push(r); });
    return { train: trainRows, valid: validRows };
  }

  /* The Lasso path of these rows stopped before reaching k groups (A-2, R4-1): the true stop cause. */
  function missingReason(scope, fold, info) {
    return { rule: 'lasso_path_degenerate', scope: scope, fold: fold, n_groups_entered: info.n_entered, cause: info.cause };
  }

  function callHook(hooks, name, a, b, c) { if (hooks && typeof hooks[name] === 'function') hooks[name](a, b, c); }

  /* Candidate (method, k): fold f is fitted on its training rows with foldSubsets[f] (null: that fold's
   * Lasso path stopped before k groups), the canonical fit on the whole training set with
   * canonicalSubset. A-1 and A-2 decide the status; every reason is kept. Yields after every fit. */
  function* candidateSteps(load, groups, split, method, k, foldSubsets, canonicalSubset, foldLasso, canonicalLasso, hooks) {
    var folds = [], reasons = [], key = modelKey(method, k);
    callHook(hooks, 'candidate', method, k);
    for (var f = 0; f < N_FOLDS; f++) {
      callHook(hooks, 'fold', method, k, f);
      var rows = foldRows(split, f), subset = foldSubsets[f];
      if (subset === null) {
        folds.push({ fold: f, n_train: rows.train.length, n_valid: rows.valid.length, groups: null, levels: null,
          n_columns: null, rank: null, df_resid: null, status: 'invalid', rule: 'lasso_path_degenerate', metrics: null });
        reasons.push(missingReason('fold', f, foldLasso[f]));
        continue;
      }
      var enc = fitEncoding(load, subsetGroups(groups, subset), rows.train);
      var fit = yield* olsSteps(encodeCols(load, enc, rows.train).cols, targetOf(load, rows.train));
      var rec = { fold: f, n_train: rows.train.length, n_valid: rows.valid.length, groups: subset.slice(),
        levels: levelsOf(enc), n_columns: fit.n_columns, rank: fit.rank, df_resid: fit.df_resid };
      if (!fit.ok) {
        rec.status = 'invalid'; rec.rule = fit.rule; rec.metrics = null;
        reasons.push({ rule: fit.rule, scope: 'fold', fold: f, rank: fit.rank, n_columns: fit.n_columns, df_resid: fit.df_resid });
      } else {
        var valid = encodeCols(load, enc, rows.valid), pred = [];
        for (var i = 0; i < valid.n; i++) pred.push(rowDot(valid.cols, i, fit.coef));
        rec.status = 'ok'; rec.rule = null; rec.coef = fit.coef.slice();
        rec.metrics = metricsOf(targetOf(load, rows.valid), pred);
        rec.n_valid_unseen = valid.unseenRows;
      }
      folds.push(rec);
      yield null;
    }
    callHook(hooks, 'fold', method, k, 'training_set');
    var cEnc = null, cFit = null;
    if (canonicalSubset === null) {
      reasons.push(missingReason('training_set', null, canonicalLasso));
    } else {
      cEnc = fitEncoding(load, subsetGroups(groups, canonicalSubset), split.train);
      cFit = yield* olsSteps(encodeCols(load, cEnc, split.train).cols, targetOf(load, split.train));
      yield null;
      if (!cFit.ok) {
        reasons.push({ rule: cFit.rule, scope: 'training_set', fold: null, rank: cFit.rank, n_columns: cFit.n_columns, df_resid: cFit.df_resid });
      }
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
    return { key: key, method: method, k: k, status: status, reasons: reasons, folds: folds, cv: cv,
      canonical_groups: canonicalSubset === null ? null : canonicalSubset.slice(),
      fit: status === 'VALID' ? fitRecord(load, cEnc, split.train, cFit) : null };
  }

  /* The All-in baseline: every feature group in every fold and on the training set. */
  function* allinSteps(load, groups, split, hooks) {
    if (!groups.length) {
      callHook(hooks, 'candidate', 'allin', 0);
      return { key: 'allin', method: 'allin', k: 0, status: 'INVALID_MODEL',
        reasons: [{ rule: 'no_feature_groups', scope: 'training_set', fold: null }],
        folds: [], cv: null, canonical_groups: [], fit: null };
    }
    var names = groups.map(function (g) { return g.name; });
    var all = [];
    for (var f = 0; f < N_FOLDS; f++) all.push(names);
    return yield* candidateSteps(load, groups, split, 'allin', groups.length, all, names, null, null, hooks);
  }

  /* SKIPPED_RESOURCE_LIMIT / FAILED: the whole method, every k; no CV metrics, fit or canonical subset. */
  function methodCandidate(method, k, status, reason) {
    return { key: modelKey(method, k), method: method, k: k, status: status, reasons: [reason], folds: [], cv: null,
      canonical_groups: null, fit: null };
  }

  function environmentInfo() {
    var env = { engine_version: ENGINE_VERSION };
    try {
      if (typeof navigator !== 'undefined' && navigator && navigator.userAgent) {
        env.user_agent = String(navigator.userAgent);
        if (navigator.hardwareConcurrency) env.hardware_concurrency = navigator.hardwareConcurrency;
        if (navigator.deviceMemory) env.device_memory_gb = navigator.deviceMemory;
      } else if (typeof process !== 'undefined' && process.versions && process.versions.node) {
        env.runtime = 'node ' + process.versions.node;
      }
    } catch (e) { /* environment information is best effort */ }
    return env;
  }

  function failureReason(error, k) {
    var name = error && error.name ? String(error.name) : 'Error';
    var text = error && error.message !== undefined ? String(error.message) : String(error);
    return { rule: 'unexpected_error', scope: 'method', fold: null, k: k, error: name, message: text,
      environment: environmentInfo() };
  }

  /* ---- the computing budget (#77) --------------------------------------------------------------- */
  /* Estimated OLS solves of a method: on the N_FOLDS fold training sets and the whole training set, the
   * path (Forward / Backward / RFE: p(p+1)/2 solves, O(p^2); Lasso: p steps, O(p)) and one fit per k. */
  function estimateSolves(method, p) {
    var sets = N_FOLDS + 1, fits = sets * p;
    if (method === 'allin') return sets;
    if (method === 'lasso_path') return sets * p + fits;
    return sets * p * (p + 1) / 2 + fits;
  }
  function resourceEstimates(nTrain, q, p) {
    var out = {};
    METHOD_ORDER.forEach(function (m) {
      out[m] = m !== 'allin' && p === 0 ? 0 : estimateSolves(m, p) * nTrain * q * q;
    });
    return out;
  }

  /* ---- selection paths: Gram criteria (hw2.selection.GroupGram) ---------------------------------- */
  function meanOf(v) { var s = 0; for (var i = 0; i < v.length; i++) s += v[i]; return s / v.length; }

  /* Centred, unit-norm columns and centred target: G = Z'Z, b = Z'y, yy = y'y (formal constructor). */
  function* gramSteps(cols, y, colGroup, nGroups) {
    var n = y.length, q = cols.length, Z = [], j, i;
    for (j = 0; j < q; j++) {
      var m = meanOf(cols[j]), c = new Float64Array(n), ss = 0;
      for (i = 0; i < n; i++) { c[i] = cols[j][i] - m; ss += c[i] * c[i]; }
      var nrm = Math.sqrt(ss) || 1;
      for (i = 0; i < n; i++) c[i] /= nrm;
      Z.push(c);
    }
    var my = meanOf(y), yc = new Float64Array(n), yy = 0;
    for (i = 0; i < n; i++) { yc[i] = y[i] - my; yy += yc[i] * yc[i]; }
    var G = [], b = new Float64Array(q);
    for (j = 0; j < q; j++) {
      G.push(new Float64Array(q));
      b[j] = dot(Z[j], yc);
    }
    for (j = 0; j < q; j++) {
      for (var l = j; l < q; l++) { var v = dot(Z[j], Z[l]); G[j][l] = v; G[l][j] = v; }
      if (n * (q - j) > YIELD_CELLS) yield null;
    }
    var members = [];
    for (var g = 0; g < nGroups; g++) members.push([]);
    for (j = 0; j < q; j++) members[colGroup[j]].push(j);
    return { n: n, G: G, b: b, yy: yy, members: members };
  }

  /* Cyclic Jacobi eigen-decomposition of a symmetric matrix (array of rows). */
  function jacobiEigen(A) {
    var m = A.length, a = A.map(function (r) { return Array.from(r); }), V = [], i, j, k;
    for (i = 0; i < m; i++) { V.push(new Array(m).fill(0)); V[i][i] = 1; }
    for (var sweep = 0; sweep < 100; sweep++) {
      var off = 0;
      for (i = 0; i < m; i++) for (j = i + 1; j < m; j++) off += a[i][j] * a[i][j];
      if (off === 0) break;
      for (i = 0; i < m - 1; i++) {
        for (j = i + 1; j < m; j++) {
          if (a[i][j] === 0) continue;
          var theta = (a[j][j] - a[i][i]) / (2 * a[i][j]);
          var t = (theta >= 0 ? 1 : -1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
          var c = 1 / Math.sqrt(t * t + 1), s = t * c;
          for (k = 0; k < m; k++) {
            var aki = a[k][i], akj = a[k][j];
            a[k][i] = c * aki - s * akj; a[k][j] = s * aki + c * akj;
          }
          for (k = 0; k < m; k++) {
            var aik = a[i][k], ajk = a[j][k];
            a[i][k] = c * aik - s * ajk; a[j][k] = s * aik + c * ajk;
          }
          for (k = 0; k < m; k++) {
            var vki = V[k][i], vkj = V[k][j];
            V[k][i] = c * vki - s * vkj; V[k][j] = s * vki + c * vkj;
          }
        }
      }
    }
    var values = [];
    for (i = 0; i < m; i++) values.push(a[i][i]);
    return { values: values, vectors: V };
  }

  /* Minimum-norm least-squares solution of the symmetric system A x = b, as numpy.linalg.lstsq with
   * rcond = eps * m: a Cholesky solve when the pivots are clearly positive, else the pseudo-inverse. */
  function minNormSolve(A, b) {
    var m = A.length, i, j, k, maxDiag = 0, ok = true;
    for (i = 0; i < m; i++) maxDiag = Math.max(maxDiag, Math.abs(A[i][i]));
    var L = [];
    for (i = 0; i < m && ok; i++) {
      L.push(new Float64Array(m));
      for (j = 0; j <= i; j++) {
        var s = A[i][j];
        for (k = 0; k < j; k++) s -= L[i][k] * L[j][k];
        if (i === j) {
          if (!(s > 1e-8 * maxDiag)) { ok = false; break; }
          L[i][i] = Math.sqrt(s);
        } else L[i][j] = s / L[j][j];
      }
    }
    var x = new Float64Array(m);
    if (ok) {
      var w = new Float64Array(m);
      for (i = 0; i < m; i++) { var t = b[i]; for (k = 0; k < i; k++) t -= L[i][k] * w[k]; w[i] = t / L[i][i]; }
      for (i = m - 1; i >= 0; i--) { var u = w[i]; for (k = i + 1; k < m; k++) u -= L[k][i] * x[k]; x[i] = u / L[i][i]; }
      return x;
    }
    var e = jacobiEigen(A), smax = 0;
    e.values.forEach(function (v) { smax = Math.max(smax, Math.abs(v)); });
    var cut = EPS * m * smax;
    for (var r = 0; r < m; r++) {
      var lam = e.values[r];
      if (!(Math.abs(lam) > cut)) continue;
      var proj = 0;
      for (i = 0; i < m; i++) proj += e.vectors[i][r] * b[i];
      for (i = 0; i < m; i++) x[i] += e.vectors[i][r] * proj / lam;
    }
    return x;
  }

  function gramSolve(gram, groupIdx) {
    var idx = [];
    groupIdx.forEach(function (g) { idx = idx.concat(gram.members[g]); });
    var A = idx.map(function (r) { return idx.map(function (c) { return gram.G[r][c]; }); });
    var b = idx.map(function (r) { return gram.b[r]; });
    return { idx: idx, beta: idx.length ? minNormSolve(A, b) : new Float64Array(0) };
  }
  function gramRss(gram, groupIdx) {
    var s = gramSolve(gram, groupIdx);
    if (!s.idx.length) return gram.yy;
    var fit = 0;
    for (var i = 0; i < s.idx.length; i++) fit += gram.b[s.idx[i]] * s.beta[i];
    return Math.max(gram.yy - fit, 0);
  }
  /* sd over the rows of each group's contribution to the fitted values (RFE's group importance). */
  function gramImportance(gram, groupIdx) {
    var s = gramSolve(gram, groupIdx), out = [], start = 0;
    groupIdx.forEach(function (g) {
      var cols = gram.members[g], w = cols.length, v = 0;
      for (var a = 0; a < w; a++) for (var c = 0; c < w; c++) v += s.beta[start + a] * gram.G[cols[a]][cols[c]] * s.beta[start + c];
      out.push(w ? Math.sqrt(Math.max(v / gram.n, 0)) : 0);
      start += w;
    });
    return out;
  }

  /* The group with the smallest score; ties (TIE_RTOL) by canonical (CSV) order, the later one when
   * removing. scores: [{v, g}] with g the canonical index. The scores are computed on the scaled target
   * (R4-4), so the floor max(|best|, 1) is unit free. */
  function pick(scores, preferLate) {
    var best = Infinity;
    scores.forEach(function (s) { if (s.v < best) best = s.v; });
    var tol = TIE_RTOL * Math.max(Math.abs(best), 1);
    var tied = scores.filter(function (s) { return s.v <= best + tol; }).map(function (s) { return s.g; });
    return preferLate ? Math.max.apply(null, tied) : Math.min.apply(null, tied);
  }
  function sortedIdx(list) { return list.slice().sort(ascending); }

  function* forwardSteps(gram, p) {
    var selected = [], remaining = [], subsets = [];
    for (var g = 0; g < p; g++) remaining.push(g);
    while (remaining.length) {
      var scores = remaining.map(function (h) { return { v: gramRss(gram, sortedIdx(selected.concat([h]))), g: h }; });
      var pickG = pick(scores, false);
      selected.push(pickG);
      remaining.splice(remaining.indexOf(pickG), 1);
      subsets.push(sortedIdx(selected));
      yield null;
    }
    return subsets;
  }
  function* backwardSteps(gram, p) {
    var current = [], subsets = new Array(p);
    for (var g = 0; g < p; g++) current.push(g);
    subsets[p - 1] = current.slice();
    while (current.length > 1) {
      var scores = current.map(function (h) { return { v: gramRss(gram, current.filter(function (x) { return x !== h; })), g: h }; });
      var pickG = pick(scores, true);
      current.splice(current.indexOf(pickG), 1);
      subsets[current.length - 1] = current.slice();
      yield null;
    }
    return subsets;
  }
  function* rfeSteps(gram, p) {
    var current = [], subsets = new Array(p);
    for (var g = 0; g < p; g++) current.push(g);
    subsets[p - 1] = current.slice();
    while (current.length > 1) {
      var imp = gramImportance(gram, current);
      var pickG = pick(current.map(function (h, i) { return { v: imp[i], g: h }; }), true);
      current.splice(current.indexOf(pickG), 1);
      subsets[current.length - 1] = current.slice();
      yield null;
    }
    return subsets;
  }

  /* ---- Lasso path: exact LARS (port of sklearn's lars_path, method "lasso", Gram=None) ----------- */
  /* The formal Ridge/Lasso standardization on these rows, then every column centred. */
  function lassoDesign(cols, dummy) {
    return cols.map(function (c, j) {
      var n = c.length, center = 0, scale = 1, i, out = new Float64Array(n);
      if (!dummy[j]) {
        center = meanOf(c);
        var ss = 0;
        for (i = 0; i < n; i++) ss += (c[i] - center) * (c[i] - center);
        scale = Math.sqrt(ss / n);
        if (scale === 0) scale = 1;
      }
      for (i = 0; i < n; i++) out[i] = (c[i] - center) / scale;
      var m = meanOf(out);
      for (i = 0; i < n; i++) out[i] -= m;
      return out;
    });
  }

  function minPos(values) {
    var best = Number.MAX_VALUE;
    for (var i = 0; i < values.length; i++) if (values[i] > 0 && values[i] < best) best = values[i];
    return best;
  }
  function rint(v) {
    var f = Math.floor(v), d = v - f;
    if (d < 0.5) return f;
    if (d > 0.5) return f + 1;
    return f % 2 === 0 ? f : f + 1;
  }
  function round15(v) { return rint(v * 1e15) / 1e15; }      /* numpy around(v, 15) */
  function sign(v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }
  /* L L' x = b for the leading m x m block of the lower-triangular L (LAPACK potrs). */
  function cholSolve(L, m, b) {
    var w = new Float64Array(m), x = new Float64Array(m), i, k;
    for (i = 0; i < m; i++) { var t = b[i]; for (k = 0; k < i; k++) t -= L[i][k] * w[k]; w[i] = t / L[i][i]; }
    for (i = m - 1; i >= 0; i--) { var u = w[i]; for (k = i + 1; k < m; k++) u -= L[k][i] * x[k]; x[i] = u / L[i][i]; }
    return x;
  }
  /* BLAS drotg (reference implementation). */
  function rotg(a, b) {
    var roe = Math.abs(a) > Math.abs(b) ? a : b, scale = Math.abs(a) + Math.abs(b);
    if (scale === 0) return { r: 0, z: 0, c: 1, s: 0 };
    var r = scale * Math.sqrt((a / scale) * (a / scale) + (b / scale) * (b / scale));
    if (roe < 0) r = -r;
    var c = a / r, s = b / r, z = 1;
    if (Math.abs(a) > Math.abs(b)) z = s;
    if (Math.abs(b) >= Math.abs(a) && c !== 0) z = 1 / c;
    return { r: r, z: z, c: c, s: s };
  }
  /* sklearn.utils.arrayfuncs.cholesky_delete on the leading n x n block. */
  function choleskyDelete(L, n, goOut) {
    var i, k, r;
    for (i = goOut; i < n - 1; i++) for (k = 0; k < i + 2; k++) L[i][k] = L[i + 1][k];
    for (i = goOut; i < n - 1; i++) {
      var g = rotg(L[i][i], L[i][i + 1]), c = g.c, s = g.s;
      L[i][i] = g.r; L[i][i + 1] = g.z;
      if (L[i][i] < 0) { L[i][i] = Math.abs(L[i][i]); c = -c; s = -s; }
      L[i][i + 1] = 0;
      for (r = i + 1; r < n - 1; r++) {
        var x = L[r][i], yv = L[r][i + 1];
        L[r][i] = c * x + s * yv; L[r][i + 1] = c * yv - s * x;
      }
    }
  }

  /* Exact Lasso path by LARS on centred columns X (Float64Array each) and centred y. Returns the knot
   * alphas and coefficients (original column order) up to the stop, and why it stopped:
   * 'completed' (alpha reached sklearn's equality tolerance, or every column active), 'alpha_increasing'
   * (sklearn's early stop), 'max_iter', 'active_set_degenerate' (A-2) or 'multiple_drops'. */
  function* larsSteps(cols, y) {
    var n = y.length, p = cols.length, X = cols.slice(), i, j, k;
    var maxFeatures = Math.min(LARS_MAX_ITER, p);
    var Cov = [];
    for (j = 0; j < p; j++) Cov.push(dot(X[j], y));
    var indices = [];
    for (j = 0; j < p; j++) indices.push(j);
    var alphas = [], coefs = [], nIter = 0, nActive = 0, active = [], signActive = [], drop = false, idx = [];
    var L = [];
    for (i = 0; i < maxFeatures; i++) L.push(new Float64Array(maxFeatures));
    var stop = { cause: 'completed', iteration: null, attempted: null };
    while (true) {
      if (n * p > YIELD_CELLS) yield null;
      var cIdx = -1, cRaw = 0, C = 0;
      for (j = 0; j < Cov.length; j++) if (cIdx < 0 || Math.abs(Cov[j]) > C) { cIdx = j; C = Math.abs(Cov[j]); }
      /* Ties (TIE_RTOL) go to the earliest column in CSV order (Spec: Lasso adds the earlier group first);
       * sklearn takes the first in its internal order, which only differs for exactly tied columns. */
      for (j = 0; j < Cov.length; j++) {
        if (C - Math.abs(Cov[j]) <= TIE_RTOL * Math.max(C, 1) && indices[nActive + j] < indices[nActive + cIdx]) cIdx = j;
      }
      if (cIdx >= 0) { cRaw = Cov[cIdx]; C = Math.abs(cRaw); }
      if (coefs.length <= nIter) coefs.push(new Float64Array(p));
      var coef = coefs[nIter], alpha = C / n;
      alphas[nIter] = alpha;
      if (alpha <= EQ_TOL) break;                                 /* sklearn's early stop (alpha_min 0) */
      if (nIter >= LARS_MAX_ITER || nActive >= p) { if (nIter >= LARS_MAX_ITER) stop.cause = 'max_iter'; break; }
      if (!drop) {
        signActive[nActive] = sign(cRaw);
        var m = nActive, nn = cIdx + nActive, tmp;
        tmp = Cov[cIdx]; Cov[cIdx] = Cov[0]; Cov[0] = tmp;
        tmp = indices[nn]; indices[nn] = indices[m]; indices[m] = tmp;
        Cov = Cov.slice(1);
        tmp = X[nn]; X[nn] = X[m]; X[m] = tmp;
        var c = dot(X[nActive], X[nActive]);
        for (i = 0; i < nActive; i++) L[nActive][i] = dot(X[nActive], X[i]);
        for (i = 0; i < nActive; i++) {                          /* L[:m, :m] w = L[m, :m] */
          var t = L[nActive][i];
          for (k = 0; k < i; k++) t -= L[i][k] * L[nActive][k];
          L[nActive][i] = t / L[i][i];
        }
        var v = 0;
        for (i = 0; i < nActive; i++) v += L[nActive][i] * L[nActive][i];
        var diag = Math.max(Math.sqrt(Math.abs(c - v)), EPS);
        L[nActive][nActive] = diag;
        if (diag < LARS_PIVOT_ATOL || diag <= LARS_DEGENERATE_RTOL * Math.sqrt(c)) {
          stop = { cause: 'active_set_degenerate', iteration: nIter, attempted: indices[nActive] };
          break;
        }
        active.push(indices[nActive]);
        nActive++;
      }
      if (nIter > 0 && alphas[nIter - 1] < alpha) { stop.cause = 'alpha_increasing'; break; }
      var ls = cholSolve(L, nActive, signActive), AA, sum;
      if (nActive === 1 && ls[0] === 0) { ls[0] = 1; AA = 1; }
      else {
        sum = 0;
        for (i = 0; i < nActive; i++) sum += ls[i] * signActive[i];
        AA = 1 / Math.sqrt(sum);
        if (!isFinite(AA)) {
          var reg = 0;
          while (!isFinite(AA)) {
            var Lr = L.map(function (row) { return Float64Array.from(row); });
            for (i = 0; i < nActive; i++) Lr[i][i] += Math.pow(2, reg) * EPS;
            ls = cholSolve(Lr, nActive, signActive);
            sum = 0;
            for (i = 0; i < nActive; i++) sum += ls[i] * signActive[i];
            AA = 1 / Math.sqrt(Math.max(sum, EPS));
            reg++;
          }
        }
        for (i = 0; i < nActive; i++) ls[i] *= AA;
      }
      var eq = new Float64Array(n);
      for (i = 0; i < nActive; i++) for (var r = 0; r < n; r++) eq[r] += X[i][r] * ls[i];
      var corr = [];
      for (j = nActive; j < p; j++) corr.push(round15(dot(X[j], eq)));
      var r1 = [], r2 = [];
      for (j = 0; j < Cov.length; j++) {
        r1.push((C - Cov[j]) / (AA - corr[j] + TINY32));
        r2.push((C + Cov[j]) / (AA + corr[j] + TINY32));
      }
      var gamma = Math.min(minPos(r1), minPos(r2), C / AA);
      drop = false;
      var z = active.map(function (orig, a) { return -coef[orig] / (ls[a] + TINY32); });
      var zPos = minPos(z);
      idx = [];
      if (zPos < gamma) {
        for (i = z.length - 1; i >= 0; i--) if (z[i] === zPos) idx.push(i);
        idx.forEach(function (a) { signActive[a] = -signActive[a]; });
        gamma = zPos;
        drop = true;
      }
      nIter++;
      var next = new Float64Array(p);
      for (i = 0; i < active.length; i++) next[active[i]] = coef[active[i]] + gamma * ls[i];
      coefs[nIter] = next;
      for (j = 0; j < Cov.length; j++) Cov[j] -= gamma * corr[j];
      if (drop) {
        if (idx.length > 1) {                                    /* sklearn's state is undefined here: stop before */
          nIter--;
          stop = { cause: 'multiple_drops', iteration: nIter, attempted: null };
          break;
        }
        var ii = idx[0];
        choleskyDelete(L, nActive, ii);
        nActive--;
        active.splice(ii, 1);
        for (i = ii; i < nActive; i++) {
          tmp = X[i]; X[i] = X[i + 1]; X[i + 1] = tmp;
          tmp = indices[i]; indices[i] = indices[i + 1]; indices[i + 1] = tmp;
        }
        var resid = Float64Array.from(y);
        for (i = 0; i < nActive; i++) for (r = 0; r < n; r++) resid[r] -= X[i][r] * next[active[i]];
        Cov = [dot(X[nActive], resid)].concat(Cov);
        signActive.splice(ii, 1);
        signActive.push(0);
      }
    }
    return { alphas: alphas.slice(0, nIter + 1), coefs: coefs.slice(0, nIter + 1), stop: stop };
  }
  function larsLasso(cols, y) { return drive(larsSteps(cols, y)); }

  /* Groups by Lasso entry on these rows (A-2 applied): entry alpha descending, ties in CSV order. LARS
   * runs on the scaled target (R4-3), so its stop does not depend on the target's unit; the tie clusters
   * use the scaled alphas, and the reported entry alphas are scaled back (times s). */
  function* lassoOrderSteps(setup, p) {
    var scaled = new Array(p).fill(null), stopCause = null, g;
    if (setup.scale > 0) {
      var my = meanOf(setup.ys), yc = new Float64Array(setup.ys.length);
      for (var i = 0; i < yc.length; i++) yc[i] = setup.ys[i] - my;
      var path = yield* larsSteps(lassoDesign(setup.cols, setup.dummy), yc), K = path.coefs.length;
      for (g = 0; g < p; g++) {
        var first = Infinity;
        for (var j = 0; j < setup.cols.length; j++) {
          if (setup.colGroup[j] !== g) continue;
          for (var kk = 1; kk < K; kk++) if (path.coefs[kk][j] !== 0) { first = Math.min(first, kk); break; }
        }
        if (first !== Infinity) scaled[g] = path.alphas[first - 1];
      }
      stopCause = path.stop.cause;
    }
    var order = [];
    for (g = 0; g < p; g++) if (scaled[g] !== null) order.push(g);
    order.sort(function (a, b) { return scaled[b] - scaled[a] || a - b; });
    var clustered = [], s = 0;
    while (s < order.length) {
      var e = s + 1;
      while (e < order.length && scaled[order[e - 1]] - scaled[order[e]] <= TIE_RTOL * Math.max(Math.abs(scaled[order[e - 1]]), 1)) e++;
      clustered = clustered.concat(order.slice(s, e).sort(ascending));
      s = e;
    }
    var alpha = scaled.map(function (a) { return a === null ? null : a * setup.scale; });
    var nEntered = clustered.length, notEntered = [];
    for (g = 0; g < p; g++) if (scaled[g] === null) notEntered.push(g);
    var cause = null;
    if (nEntered < p) cause = setup.scale > 0 ? (stopCause === 'completed' ? 'path_ended' : stopCause) : 'target_constant';
    var subsets = [];
    for (var k = 1; k <= p; k++) subsets.push(k <= nEntered ? sortedIdx(clustered.slice(0, k)) : null);
    return { order: clustered, alpha: alpha, notEntered: notEntered, nEntered: nEntered, cause: cause, subsets: subsets };
  }

  /* The rows of one path computation: encoded columns, and the target centred and divided by its root
   * mean square on these rows (scale; 0 for a constant target, nothing divided) -- R4-3, R4-4. */
  function rowSetup(load, groups, rows) {
    var enc = fitEncoding(load, groups, rows);
    var cols = encodeCols(load, enc, rows).cols, y = targetOf(load, rows), n = y.length, i;
    var nameIdx = new Map();
    groups.forEach(function (g, gi) { nameIdx.set(g.name, gi); });
    var my = meanOf(y), yc = new Float64Array(n), ss = 0;
    for (i = 0; i < n; i++) { yc[i] = y[i] - my; ss += yc[i] * yc[i]; }
    var scale = Math.sqrt(ss / n);
    if (!(scale > 0) || !isFinite(scale)) scale = 0;
    var ys = new Float64Array(n);
    for (i = 0; i < n; i++) ys[i] = scale > 0 ? yc[i] / scale : yc[i];
    return { cols: cols, ys: ys, scale: scale,
      colGroup: enc.columns.map(function (c) { return nameIdx.get(c.group); }),
      dummy: enc.columns.map(function (c) { return c.level !== null; }) };
  }

  function lassoInfo(groups, lasso, p) {
    return {
      entries: lasso.order.map(function (g) { return { group: groups[g].name, entry_alpha: lasso.alpha[g] }; }),
      not_entered: lasso.notEntered.map(function (g) { return groups[g].name; }),
      n_entered: lasso.nEntered, degenerate: lasso.nEntered < p,
      first_invalid_k: lasso.nEntered < p ? lasso.nEntered + 1 : null, cause: lasso.cause
    };
  }

  /* One path method on the five fold training sets and the training set: subsets[k - 1] (canonical group
   * names) for k = 1..p per row set, and the Lasso information. Yields after every path step. */
  function* methodPathSteps(load, groups, split, method, hooks, gramCache) {
    var p = groups.length, sets = [], out = { folds: [], canonical: null, lasso: null };
    for (var f = 0; f < N_FOLDS; f++) sets.push(foldRows(split, f).train);
    sets.push(split.train);
    var names = function (sub) { return sub === null ? null : sub.map(function (g) { return groups[g].name; }); };
    var lassoInfos = [];
    for (var s = 0; s < sets.length; s++) {
      callHook(hooks, 'path', method, s === N_FOLDS ? 'training_set' : s);
      var subsets;
      if (method === 'lasso_path') {
        var lasso = yield* lassoOrderSteps(rowSetup(load, groups, sets[s]), p);
        lassoInfos.push(lassoInfo(groups, lasso, p));
        subsets = lasso.subsets;
        yield null;
      } else {
        if (!gramCache[s]) {
          var setup = rowSetup(load, groups, sets[s]);
          gramCache[s] = yield* gramSteps(setup.cols, setup.ys, setup.colGroup, p);
          yield null;
        }
        var steps = method === 'forward_sfs' ? forwardSteps : method === 'backward_sfs' ? backwardSteps : rfeSteps;
        subsets = yield* steps(gramCache[s], p);
      }
      if (s === N_FOLDS) out.canonical = subsets.map(names);
      else out.folds.push(subsets.map(names));
    }
    if (method === 'lasso_path') out.lasso = { canonical: lassoInfos[N_FOLDS], folds: lassoInfos.slice(0, N_FOLDS) };
    return out;
  }

  /* ---- winners (hw2/models.py determine_winners rules) ----------------------------------------- */
  function determineWinners(candidates) {
    var methodWinners = {}, byKey = new Map();
    candidates.forEach(function (c) { byKey.set(c.key, c); });
    METHOD_ORDER.forEach(function (m) {
      var best = null;
      candidates.forEach(function (c) {
        if (c.method !== m || c.status !== 'VALID') return;
        if (best === null || c.cv.mean.rmse < best.cv.mean.rmse || (c.cv.mean.rmse === best.cv.mean.rmse && c.k < best.k)) best = c;
      });
      methodWinners[m] = best === null ? null : { key: best.key, k: best.k };
    });
    var pool = METHOD_ORDER.filter(function (m) { return methodWinners[m] !== null; });
    if (!pool.length) return null;
    var om = pool[0];
    pool.forEach(function (m) {
      if (byKey.get(methodWinners[m].key).cv.mean.rmse < byKey.get(methodWinners[om].key).cv.mean.rmse) om = m;
    });
    var overall = { method: om, key: methodWinners[om].key, k: methodWinners[om].k };
    var order = pool.map(function (m) { return methodWinners[m].key; }).concat([overall.key]);
    var reps = [], testKeys = [], testKeyOf = {};
    function repOf(key) {
      var sub = JSON.stringify(byKey.get(key).canonical_groups);
      for (var i = 0; i < reps.length; i++) if (reps[i].sub === sub) return reps[i].key;
      reps.push({ sub: sub, key: key });
      return key;
    }
    order.forEach(function (key) {
      var rep = repOf(key);
      if (testKeys.indexOf(rep) < 0) testKeys.push(rep);
      testKeyOf[key] = rep;
    });
    return { method_winners: methodWinners, overall: overall, test_keys: testKeys, test_key_of: testKeyOf };
  }

  /* ---- A-3: linear relations among the All-in design columns on the training set ---------------- */
  function* dependencySteps(load, groups, rows) {
    var enc = fitEncoding(load, groups, rows), X = encodeCols(load, enc, rows).cols;
    var n = rows.length, q = enc.columns.length, p = q + 1, i, j, l;
    var cols = [{ intercept: true, group: null, level: null }].concat(enc.columns.map(function (c) {
      return { intercept: false, group: c.group, level: c.level };
    }));
    var D = [new Float64Array(n).fill(1)].concat(X);
    var safe = D.map(function (c) { var s = Math.sqrt(dot(c, c)); return s > 0 ? s : 1; });
    var tol = Math.max(n, p) * EPS, Q = [], R = [], basis = [], relations = [];
    for (j = 0; j < p; j++) {
      if (n * Q.length > YIELD_CELLS) yield null;
      var v = new Float64Array(n), rj = new Array(Q.length).fill(0);
      for (i = 0; i < n; i++) v[i] = D[j][i] / safe[j];
      for (var pass = 0; pass < 2; pass++) {
        for (l = 0; l < Q.length; l++) {
          var d = dot(Q[l], v);
          for (i = 0; i < n; i++) v[i] -= d * Q[l][i];
          rj[l] += d;
        }
      }
      var r = Math.sqrt(dot(v, v));
      if (r > tol) {
        for (i = 0; i < n; i++) v[i] /= r;
        Q.push(v); R.push(rj.concat([r])); basis.push(j);
        continue;
      }
      var m = basis.length, a = new Array(m).fill(0);
      for (l = m - 1; l >= 0; l--) {                              /* R_B a = r_j (upper triangular) */
        var t = rj[l];
        for (var u = l + 1; u < m; u++) t -= R[u][l] * a[u];
        a[l] = t / R[l][l];
      }
      var coef = new Array(p).fill(0);
      for (l = 0; l < m; l++) coef[basis[l]] = -a[l] * safe[j] / safe[basis[l]];
      coef[j] = 1;
      var big = 0;
      coef.forEach(function (x) { big = Math.max(big, Math.abs(x)); });
      coef = coef.map(function (x) { var y = x / big; return Math.abs(y) <= RELATION_ZERO ? 0 : y; });
      var nz = [];
      coef.forEach(function (x, k) { if (x !== 0) nz.push(k); });
      if (coef[nz[0]] < 0) coef = coef.map(function (x) { return x === 0 ? 0 : -x; });
      var members = nz.map(function (k) { return { intercept: cols[k].intercept, group: cols[k].group, level: cols[k].level, coef: coef[k] }; });
      relations.push({ columns: members,
        feature_groups: groups.filter(function (g) { return members.some(function (c) { return c.group === g.name; }); })
          .map(function (g) { return g.name; }),
        includes_intercept: cols[nz[0]].intercept });
    }
    return { n_columns: p, rank: basis.length, relations: relations };
  }
  function dependencyGroups(load, groups, rows) { return drive(dependencySteps(load, groups, rows)); }

  /* ---- test: only for the frozen winners' canonical fits --------------------------------------- */
  function* testSteps(load, candidate, testRows) {
    var fit = candidate.fit;
    var enc = encodeCols(load, fit.encoding, testRows);
    var actual = targetOf(load, testRows);
    var predicted = [], lower = [], upper = [], covered = [];
    var block = Math.max(1, Math.floor(YIELD_CELLS / (fit.coef.length * fit.coef.length)));
    for (var i = 0; i < enc.n; i++) {
      if (i > 0 && i % block === 0) yield null;
      var pi = interval(fit, designRow(enc.cols, i));
      predicted.push(pi.predicted); lower.push(pi.lower); upper.push(pi.upper);
      covered.push(pi.lower <= actual[i] && actual[i] <= pi.upper);
    }
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

  function budgetsOf(options) {
    var b = {};
    PATH_METHODS.forEach(function (m) {
      var given = options.budgets && options.budgets[m];
      b[m] = typeof given === 'number' ? given : BUDGETS[m];
    });
    return b;
  }

  function* runSteps(load, options, control) {
    var t0 = now(options);
    if (!load || !load.ok) throw new Error('run: needs an accepted LoadResult');
    var seed = options.seed === undefined ? SEED : options.seed;
    var n = load.rows.length, hooks = options.hooks || null;
    var split = options.split ? { train: options.split.train.slice(), test: options.split.test.slice(), folds: options.split.folds.slice() }
      : makeSplit(n, seed);
    checkSplit(split, n);
    var meta = {
      engine_version: ENGINE_VERSION, problem: options.problem || null, source: options.source || null,
      sha256: load.sha256, target: load.target.name, n_rows_read: load.n_rows_read, n_rows: n,
      n_rows_dropped_missing: load.n_rows_dropped_missing, seed: seed, split_injected: !!options.split,
      pi_level: PI_LEVEL, max_levels: MAX_LEVELS, min_df_resid: MIN_DF_RESID, cv_std_ddof: CV_STD_DDOF,
      timing_ms: { started_at_epoch_ms: Date.now() }
    };
    var decided = trainDecisions(load, split.train), groups = decided.groups, p = groups.length;
    var q = fitEncoding(load, groups, split.train).columns.length, budgets = budgetsOf(options);
    meta.budget = { unit: BUDGET_UNIT, constants: budgets, estimates: resourceEstimates(split.train.length, q, p),
      n_train: split.train.length, encoded_columns: q, feature_groups: p };
    var methods = p ? METHOD_ORDER : ['allin'];
    var progress = { candidatesDone: 0, candidatesTotal: 1 + 4 * p, methodsDone: 0, methodsTotal: methods.length };
    function emit(phase, method, k) {
      if (typeof options.onProgress !== 'function') return;
      options.onProgress({ phase: phase, method: method, k: k, candidates_done: progress.candidatesDone,
        candidates_total: progress.candidatesTotal, methods_done: progress.methodsDone, methods_total: progress.methodsTotal,
        fraction: progress.candidatesDone / progress.candidatesTotal, elapsed_ms: now(options) - t0 });
    }
    function cancelled() {
      meta.timing_ms.total = now(options) - t0;
      return { meta: meta, run: { status: 'CANCELLED', reason: null, methods_completed: progress.methodsDone,
        methods_total: progress.methodsTotal, candidates_completed: progress.candidatesDone,
        candidates_total: progress.candidatesTotal } };
    }
    var t1 = now(options);
    meta.timing_ms.decisions = t1 - t0;
    var result = {
      meta: meta,
      columns: decided.columns,
      groups: groups.map(function (g) { return { name: g.name, index: g.index, type: g.type }; }),
      split: { train: split.train, test: split.test, folds: split.folds, n_folds: N_FOLDS,
        prng: 'mulberry32 + Fisher-Yates (split seed, folds seed + 1)' },
      dependencies: null,
      lasso_path: null
    };
    for (var gi = 0; gi < groups.length; gi++) {                 /* the predictor's defaults, one column per step */
      if (groups[gi].type === 'numeric') { numericInput(load, split.train, groups[gi].index); yield null; }
    }
    emit('start', null, null);
    if (control.cancel) return cancelled();                       /* the boundary before the first candidate */

    var candidates = [];
    var tm = now(options), allin;
    try {
      allin = yield* allinSteps(load, groups, split, hooks);
    } catch (e) {
      allin = methodCandidate('allin', p, 'FAILED', failureReason(e, p));
    }
    meta.timing_ms.allin = now(options) - tm;
    candidates.push(allin);
    progress.candidatesDone++; progress.methodsDone++;
    emit(allin.status === 'FAILED' ? 'failed' : 'candidate', 'allin', allin.k);
    if (control.cancel) return cancelled();

    var gramCache = [];
    for (var mi = 0; mi < (p ? PATH_METHODS.length : 0); mi++) {
      var method = PATH_METHODS[mi], base = progress.candidatesDone, k;
      tm = now(options);
      if (meta.budget.estimates[method] > budgets[method]) {
        for (k = 1; k <= p; k++) {
          candidates.push(methodCandidate(method, k, 'SKIPPED_RESOURCE_LIMIT', { rule: 'resource_limit', scope: 'method',
            fold: null, estimate: meta.budget.estimates[method], budget: budgets[method] }));
        }
        progress.candidatesDone = base + p; progress.methodsDone++;
        meta.timing_ms[method] = now(options) - tm;
        emit('skipped', method, null);
        if (control.cancel) return cancelled();
        continue;
      }
      var list = [], paths = null, failure = null;
      for (k = 1; k <= p; k++) {
        var cand;
        try {
          if (!paths) paths = yield* methodPathSteps(load, groups, split, method, hooks, gramCache);
          cand = yield* candidateSteps(load, groups, split, method, k,
            paths.folds.map(function (fp) { return fp[k - 1]; }), paths.canonical[k - 1],
            paths.lasso ? paths.lasso.folds : null, paths.lasso ? paths.lasso.canonical : null, hooks);
        } catch (e) {
          failure = failureReason(e, k);
          break;
        }
        list.push(cand);
        progress.candidatesDone++;
        if (k === p) progress.methodsDone++;
        emit('candidate', method, k);
        if (control.cancel) return cancelled();
      }
      if (failure) {
        list = [];
        for (k = 1; k <= p; k++) list.push(methodCandidate(method, k, 'FAILED', failure));
        progress.candidatesDone = base + p; progress.methodsDone++;
      } else if (method === 'lasso_path') {
        result.lasso_path = paths.lasso;
      }
      candidates = candidates.concat(list);
      meta.timing_ms[method] = now(options) - tm;
      if (failure) {
        emit('failed', method, failure.k);
        if (control.cancel) return cancelled();
      }
    }
    /* A-3 after the last candidate boundary (it does not delay a cancellation). */
    var td = now(options);
    emit('diagnostic', null, null);
    try {
      result.dependencies = yield* dependencySteps(load, groups, split.train);
    } catch (e) {
      result.dependencies = { n_columns: q + 1, rank: null, relations: [], error: failureReason(e, null) };
    }
    meta.timing_ms.dependencies = now(options) - td;
    var valid = candidates.filter(function (c) { return c.status === 'VALID'; });
    if (!valid.length) {
      result.run = { status: 'REJECTED', reason: 'ALL_CANDIDATES_INVALID',
        invalid_candidates: candidates.map(function (c) { return { key: c.key, status: c.status, reasons: c.reasons }; }) };
      meta.timing_ms.total = now(options) - t0;
      return result;
    }
    /* winners are fixed here; the test rows are read only after this point, and only for them. */
    var winners = determineWinners(candidates);
    var test = {}, t4 = now(options);
    for (var ti = 0; ti < winners.test_keys.length; ti++) {
      var tkey = winners.test_keys[ti];
      test[tkey] = yield* testSteps(load, candidates.filter(function (x) { return x.key === tkey; })[0], split.test);
    }
    meta.timing_ms.test = now(options) - t4;
    meta.timing_ms.total = now(options) - t0;
    result.run = { status: 'COMPLETED', reason: null };
    result.candidates = candidates.map(publicCandidate);
    result.winners = winners;
    result.test = test;
    return result;
  }

  /* A run as a stepper: step() advances to the next yield point and returns { done, result }; cancel()
   * is honoured at the next candidate boundary. Steps are synchronous; the caller decides when to take
   * the next one (e.g. after letting the page handle its events). */
  function createRun(load, options) {
    options = options || {};
    var control = { cancel: false }, gen = runSteps(load, options, control), state = { done: false, result: null, steps: 0 };
    return {
      step: function () {
        if (state.done) return state;
        var r = gen.next();
        state.steps++;
        if (r.done) { state.done = true; state.result = r.value; }
        return state;
      },
      cancel: function () { control.cancel = true; },
      cancelRequested: function () { return control.cancel; },
      isDone: function () { return state.done; },
      result: function () { return state.result; },
      steps: function () { return state.steps; }
    };
  }

  function run(load, options) {
    var r = createRun(load, options);
    while (!r.step().done) { /* every step */ }
    return r.result();
  }

  /* ---- live predictor ---------------------------------------------------------------------------- */
  function canPredict(candidate) {
    return !!(candidate && candidate.status === 'VALID' && candidate.fit && candidate.fit.coef && candidate.fit.xtx_inv);
  }

  /* Inputs the predictor asks for: one per feature group of the fit (training-set values only). */
  function inputSpec(fit) {
    return fit.groups.map(function (name) {
      var lv = getOwn(fit.levels, name);
      if (lv) return { name: name, type: 'categorical', levels: lv.levels.slice(), baseline: lv.baseline, default: lv.baseline };
      var info = getOwn(fit.inputs, name);
      return { name: name, type: 'numeric', min: info.min, max: info.max, median: info.median, default: info.median };
    });
  }

  /* Point prediction and 95% PI for raw source values {group: value} (own properties, or a Map). Out-of-range
   * numbers are still computed (warning); an unseen category is computed as the baseline (warning). */
  function predict(candidate, raw) {
    if (!canPredict(candidate)) throw new Error('this candidate is not VALID: no prediction');
    var fit = candidate.fit, x = [1], warnings = [];
    inputSpec(fit).forEach(function (spec) {
      var v = raw instanceof Map ? raw.get(spec.name) : getOwn(raw, spec.name);
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
    METHOD_ORDER: METHOD_ORDER, PATH_METHODS: PATH_METHODS, TIE_RTOL: TIE_RTOL,
    BUDGETS: BUDGETS, BUDGET_UNIT: BUDGET_UNIT, estimateSolves: estimateSolves, resourceEstimates: resourceEstimates,
    mulberry32: mulberry32, shuffledIndices: shuffledIndices, makeSplit: makeSplit,
    trainDecisions: trainDecisions, fitEncoding: fitEncoding, encodeCols: encodeCols,
    fitOls: fitOls, tQuantile: tQuantile, metricsOf: metricsOf, interval: interval,
    modelKey: modelKey, determineWinners: determineWinners,
    larsLasso: larsLasso, dependencyGroups: dependencyGroups,
    createRun: createRun, run: run,
    canPredict: canPredict, inputSpec: inputSpec, predict: predict, putOwn: putOwn, getOwn: getOwn
  };
});
