"""DIC-02: 50 Startups multiple linear regression - feature-selection comparison (CRISP-DM).

Five schemes x k = 1..5 features, each scored by training-only nested cross-validation:
  outer 5-fold CV (evaluation) -> inside every outer-training fold, feature selection and
  hyperparameter tuning use an inner 5-fold CV -> the selected subset is refit with plain
  OLS (LinearRegression) and scored on the outer validation fold.
The held-out test set is used only once per scheme, after the best k is fixed by CV RMSE.

Run from the repository root:  python week06/analysis/nested_cv_comparison.py
Outputs: results/nested_cv/ and assets/model_data.js (+ .json) for index.html.
"""
from itertools import combinations
import hashlib
import json
import warnings

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy
import sklearn
from scipy import stats
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_selection import RFE, RFECV, SequentialFeatureSelector
from sklearn.linear_model import ElasticNetCV, LassoCV, LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import DATA_CSV, SEED, WEB_DATA_JS, load_data, results_dir, split

KS = range(1, 6)
OUTER_CV = KFold(n_splits=5, shuffle=True, random_state=SEED)
INNER_CV = KFold(n_splits=5, shuffle=True, random_state=SEED)
L1_RATIOS = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]


# ---- CRISP-DM 1-3: business understanding, data understanding, data preparation ----
# Shared with the other DIC-02 scripts: see common.load_data() and common.split().


# ---- CRISP-DM 4: modeling - five selectors; each sees only the data it is given ----
def rank_top_k(coefs, columns, k):
    """Top-k by |coefficient|; ties (e.g. several zeros) keep the original column order."""
    order = sorted(range(len(columns)), key=lambda i: (-abs(coefs[i]), i))
    return [columns[i] for i in order[:k]]


def inner_rmse(X, y, cols):
    """Inner 5-fold CV RMSE of OLS on the given (outer-training) data."""
    return -cross_val_score(LinearRegression(), X[list(cols)], y, cv=INNER_CV,
                            scoring='neg_root_mean_squared_error').mean()


def select_exhaustive(X, y, k):
    """Every size-k subset; keep the one with the lowest inner-CV RMSE."""
    return list(min(combinations(X.columns, k), key=lambda c: inner_rmse(X, y, c)))


def select_sfs(X, y, k):
    """Forward sequential selection scored by inner-CV RMSE (k = all features is trivial)."""
    if k == X.shape[1]:
        return list(X.columns)
    sfs = SequentialFeatureSelector(LinearRegression(), n_features_to_select=k,
                                    direction='forward', cv=INNER_CV,
                                    scoring='neg_root_mean_squared_error')
    return list(X.columns[sfs.fit(X, y).get_support()])


def select_lasso(X, y, k):
    """LassoCV (alpha tuned by inner CV) on standardized features; top-k |coef|."""
    model = make_pipeline(StandardScaler(), LassoCV(cv=INNER_CV, random_state=SEED,
                                                    max_iter=200000))
    return rank_top_k(model.fit(X, y)[-1].coef_, list(X.columns), k)


def select_rfe(X, y, k):
    """RFE with OLS on standardized features, fixed k (no hyperparameter to tune)."""
    model = make_pipeline(StandardScaler(), RFE(LinearRegression(), n_features_to_select=k))
    return list(X.columns[model.fit(X, y)[-1].get_support()])


def select_enet(X, y, k):
    """ElasticNetCV (alpha and l1_ratio tuned by inner CV) on standardized features; top-k |coef|."""
    model = make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=L1_RATIOS, cv=INNER_CV,
                                                         random_state=SEED, max_iter=200000))
    return rank_top_k(model.fit(X, y)[-1].coef_, list(X.columns), k)


SCHEMES = {
    'Exhaustive Search': select_exhaustive,
    'Forward SFS': select_sfs,
    'Lasso (L1) Top-k': select_lasso,
    'RFE': select_rfe,
    'Elastic Net Top-k': select_enet,
}
STYLE = {  # one fixed colour and marker per scheme, reused in every plot and in the web page
    # Colours: the dataviz reference categorical palette, slots 1-5 (light mode), validated
    # for colour-vision deficiency; the distinct markers are the secondary encoding.
    'Exhaustive Search': ('#2a78d6', 'o'),
    'Forward SFS': ('#eb6834', 's'),
    'Lasso (L1) Top-k': ('#1baf7a', '^'),
    'RFE': ('#eda100', 'D'),
    'Elastic Net Top-k': ('#e87ba4', 'v'),
}


# ---- CRISP-DM 5: evaluation ----
def nested_cv(select, X, y, k):
    """Outer 5-fold: select on the outer-training fold, refit OLS, score the outer validation fold."""
    rmses, r2s, subsets = [], [], []
    for tr, va in OUTER_CV.split(X):
        cols = select(X.iloc[tr], y.iloc[tr], k)
        pred = LinearRegression().fit(X.iloc[tr][cols], y.iloc[tr]).predict(X.iloc[va][cols])
        rmses.append(np.sqrt(mean_squared_error(y.iloc[va], pred)))
        r2s.append(r2_score(y.iloc[va], pred))
        subsets.append(tuple(sorted(cols)))
    return np.mean(rmses), np.mean(r2s), subsets, rmses


def test_metrics(cols, X_train, y_train, X_test, y_test):
    pred = LinearRegression().fit(X_train[cols], y_train).predict(X_test[cols])
    mse = mean_squared_error(y_test, pred)
    return {'Test MAE': mean_absolute_error(y_test, pred), 'Test MSE': mse,
            'Test RMSE': np.sqrt(mse), 'Test R2': r2_score(y_test, pred)}


def ols_details(cols, X_train, y_train):
    """OLS with intercept on the full training set: inference table, fit statistics and
    the pieces a browser needs for a 95% prediction interval."""
    A = np.column_stack([np.ones(len(X_train)), X_train[cols].to_numpy()])
    yv = y_train.to_numpy()
    beta, *_ = np.linalg.lstsq(A, yv, rcond=None)
    resid = yv - A @ beta
    n, p = A.shape
    df_resid = n - p
    s2 = resid @ resid / df_resid
    xtx_inv = np.linalg.inv(A.T @ A)
    se = np.sqrt(np.diag(s2 * xtx_inv))
    tstat = beta / se
    t_crit = stats.t.ppf(0.975, df_resid)
    r2 = 1 - resid @ resid / np.sum((yv - yv.mean()) ** 2)
    f_stat = (r2 / (p - 1)) / ((1 - r2) / df_resid)

    def vif(j):
        if len(cols) == 1:
            return 1.0
        others = [c for c in cols if c != cols[j]]
        B = np.column_stack([np.ones(n), X_train[others].to_numpy()])
        target = X_train[cols[j]].to_numpy()
        fit, *_ = np.linalg.lstsq(B, target, rcond=None)
        r2_j = 1 - np.sum((target - B @ fit) ** 2) / np.sum((target - target.mean()) ** 2)
        return 1 / (1 - r2_j)

    names = ['Intercept'] + list(cols)
    coefficients = [{'feature': names[i], 'coef': beta[i], 'stderr': se[i], 'tstat': tstat[i],
                     'pvalue': 2 * stats.t.sf(abs(tstat[i]), df_resid),
                     'ci_lower': beta[i] - t_crit * se[i], 'ci_upper': beta[i] + t_crit * se[i],
                     'vif': None if i == 0 else vif(i - 1)} for i in range(p)]
    return {'coefficients': coefficients, 'train_r2': r2,
            'train_adj_r2': 1 - (1 - r2) * (n - 1) / df_resid,
            'f_stat': f_stat, 'f_pvalue': stats.f.sf(f_stat, p - 1, df_resid),
            'df_resid': df_resid, 's2': s2, 't_crit': t_crit, 'xtx_inv': xtx_inv.tolist()}


def prediction_interval(details, x_row):
    """95% OLS prediction interval for one observation (x_row without the intercept)."""
    x0 = np.concatenate([[1.0], x_row])
    beta = np.array([c['coef'] for c in details['coefficients']])
    half = details['t_crit'] * np.sqrt(details['s2'] * (1 + x0 @ np.array(details['xtx_inv']) @ x0))
    pred = x0 @ beta
    return pred, pred - half, pred + half


def export_web_data(results, summary, stability, fold_rmses, rfecv_cols, data, path_js):
    """Write everything the web page shows into model_data.js (window.MODEL_DATA) and .json."""
    X, y, X_train, y_train, X_test, y_test = data
    models = {}
    for _, row in results.iterrows():
        cols = row['Selected Features'].split(', ')
        details = ols_details(cols, X_train, y_train)
        models.setdefault(row['Method'], []).append({
            'k': int(row['k']), 'features': cols, 'cv_rmse': row['CV RMSE'], 'cv_r2': row['CV R2'],
            'fold_rmse': fold_rmses[(row['Method'], int(row['k']))],
            'folds_agree': stability[(row['Method'], int(row['k']))], **details})
    best = []
    for _, row in summary.iterrows():
        cols = row['Selected Features'].split(', ')
        details = ols_details(cols, X_train, y_train)
        preds = []
        for idx in X_test.index:
            pred, lo, hi = prediction_interval(details, X_test.loc[idx, cols].to_numpy())
            actual = float(y_test.loc[idx])
            preds.append({'row': int(idx), 'actual': actual, 'predicted': pred,
                          'residual': actual - pred, 'pi_lower': lo, 'pi_upper': hi,
                          'covered': bool(lo <= actual <= hi)})
        best.append({'method': row['Method'], 'best_k': int(row['Best k']), 'features': cols,
                     'cv_rmse': row['CV RMSE'], 'cv_r2': row['CV R2'],
                     'test_mae': row['Test MAE'], 'test_mse': row['Test MSE'],
                     'test_rmse': row['Test RMSE'], 'test_r2': row['Test R2'],
                     'test_predictions': preds})
    csv_bytes = DATA_CSV.read_bytes()
    payload = {
        'meta': {'dataset': '50 Startups (Kaggle), 50 rows', 'csv_sha256': hashlib.sha256(csv_bytes).hexdigest(),
                 'features': list(X.columns), 'target': 'Profit', 'reference_state': 'California',
                 'n_train': len(X_train), 'n_test': len(X_test), 'random_state': SEED,
                 'cv': 'nested: outer 5-fold (evaluation) x inner 5-fold (selection / tuning), training set only',
                 'versions': {'numpy': np.__version__, 'pandas': pd.__version__,
                              'scikit-learn': sklearn.__version__, 'scipy': scipy.__version__,
                              'matplotlib': matplotlib.__version__}},
        'schemes': [{'name': n, 'color': STYLE[n][0]} for n in SCHEMES],
        'models': models, 'best': best,
        'rfecv': {'k': len(rfecv_cols), 'features': rfecv_cols},
        'test_rows': [{'row': int(i), 'R&D Spend': float(X_test.loc[i, 'R&D Spend']),
                       'Administration': float(X_test.loc[i, 'Administration']),
                       'Marketing Spend': float(X_test.loc[i, 'Marketing Spend']),
                       'State': ('Florida' if X_test.loc[i, 'State_Florida'] else
                                 'New York' if X_test.loc[i, 'State_New York'] else 'California')}
                      for i in X_test.index],
        'input_ranges': {c: {'min': float(X_train[c].min()), 'max': float(X_train[c].max()),
                             'median': float(X_train[c].median())}
                         for c in ['R&D Spend', 'Administration', 'Marketing Spend']},
    }
    text = json.dumps(payload, indent=1, default=float)
    path_js.with_suffix('.json').write_text(text, encoding='utf-8')
    path_js.write_text('// Generated by analysis/nested_cv_comparison.py - do not edit by hand.\n'
                       f'window.MODEL_DATA = {text};\n', encoding='utf-8')


def plot_comparison(results, path):
    """Two side-by-side panels: CV RMSE and CV R2 vs number of features, one line per scheme."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    offsets = dict(zip(SCHEMES, np.linspace(-0.12, 0.12, len(SCHEMES))))
    for ax, metric, label in [(axes[0], 'CV RMSE', 'CV RMSE (USD)'), (axes[1], 'CV R2', 'CV R-squared')]:
        for name, block in results.groupby('Method', sort=False):
            colour, marker = STYLE[name]
            ax.plot(block['k'] + offsets[name], block[metric], color=colour, marker=marker,
                    linewidth=1.8, markersize=7, label=name)
        ax.set(title=f'{label} vs. Number of Features', xlabel='Number of Features (k)', ylabel=label)
        ax.set_xticks(list(KS))
        ax.grid(True, linestyle=':', alpha=0.6)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=5, frameon=False)
    fig.suptitle('50 Startups: nested 5x5-fold CV on the training set (points offset horizontally for visibility)',
                 fontsize=11)
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    warnings.filterwarnings('ignore', category=ConvergenceWarning)
    X, y = load_data()
    X_train, X_test, y_train, y_test = split(X, y)
    print(f'Data: {len(X)} rows, features {list(X.columns)}')
    print(f'Train {len(X_train)} / test {len(X_test)} (random_state={SEED}); '
          'nested CV: outer 5-fold, inner 5-fold, training set only.\n')

    rows, stability, fold_rmses = [], {}, {}
    for name, select in SCHEMES.items():
        for k in KS:
            cv_rmse, cv_r2, fold_subsets, rmses = nested_cv(select, X_train, y_train, k)
            final = select(X_train, y_train, k)          # same procedure on the full training set
            rows.append({'Method': name, 'k': k, 'Selected Features': ', '.join(final),
                         'CV RMSE': cv_rmse, 'CV R2': cv_r2})
            stability[(name, k)] = sum(s == tuple(sorted(final)) for s in fold_subsets)
            fold_rmses[(name, k)] = [float(r) for r in rmses]
    results = pd.DataFrame(rows)

    summary = []
    for name, block in results.groupby('Method', sort=False):
        best = block.loc[block['CV RMSE'].idxmin()]          # model selection: CV RMSE only
        cols = best['Selected Features'].split(', ')
        summary.append({'Method': name, 'Best k': int(best['k']),
                        'Selected Features': best['Selected Features'],
                        'CV RMSE': best['CV RMSE'], 'CV R2': best['CV R2'],
                        **test_metrics(cols, X_train, y_train, X_test, y_test)})
    summary = pd.DataFrame(summary)

    rfecv = make_pipeline(StandardScaler(), RFECV(LinearRegression(), cv=INNER_CV,
                                                  scoring='neg_root_mean_squared_error'))
    rfecv.fit(X_train, y_train)
    rfecv_cols = list(X_train.columns[rfecv[-1].get_support()])

    out = results_dir('nested_cv')
    results.round({'CV RMSE': 2, 'CV R2': 4}).to_csv(out / 'all_25_results.csv', index=False)
    summary.round({'CV RMSE': 2, 'CV R2': 4, 'Test MAE': 2, 'Test MSE': 2,
                   'Test RMSE': 2, 'Test R2': 4}).to_csv(out / 'best_models_summary.csv', index=False)
    plot_comparison(results, out / 'cv_rmse_r2_comparison.png')
    export_web_data(results, summary, stability, fold_rmses, rfecv_cols,
                    (X, y, X_train, y_train, X_test, y_test),
                    WEB_DATA_JS)

    pd.set_option('display.width', 240, 'display.max_columns', None, 'display.max_colwidth', 80)
    print('All 25 (method, k) results - nested CV on the training set:')
    print(results.round({'CV RMSE': 2, 'CV R2': 4}).to_string(index=False))
    print('\nBest k per method (lowest CV RMSE), then scored once on the held-out test set:')
    print(summary.round(4).to_string(index=False))
    print('\nSelection stability across outer folds (folds whose subset equals the final one):')
    for (name, k), agree in stability.items():
        print(f'{name:<18} k={k}: {agree}/5')
    print(f'\nRFECV reference (automatic k by inner CV on the full training set): '
          f'k={len(rfecv_cols)} -> {rfecv_cols}')
    print(f'\nOutputs written to {out} and {WEB_DATA_JS.parent}')


if __name__ == '__main__':
    main()
