"""DIC-02: 50 Startups feature selection - five schemes, performance for k = 1..5 (CRISP-DM).

Each scheme produces one feature subset per k (its selection path). Every subset is
refit with OLS and scored by 5-fold CV on the training set and once on the test set.
All selection decisions use the training set only; the test set is only reported.

Run from the repository root:  python week06/analysis/selection_paths.py
"""
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LassoCV, LinearRegression, lasso_path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import FEATURES, SEED, load_data, results_dir, split

# 1-3. Business / data understanding and preparation (shared, see common.py)
X, y = load_data()
X_train, X_test, y_train, y_test = split(X, y)
KS = range(1, len(FEATURES) + 1)
CV = KFold(n_splits=5, shuffle=True, random_state=SEED)


def cv_score(cols, scoring):
    return cross_val_score(LinearRegression(), X_train[list(cols)], y_train,
                           cv=CV, scoring=scoring).mean()


def cv_rmse(cols):
    """Mean 5-fold CV RMSE of OLS on the training set."""
    return -cv_score(cols, 'neg_root_mean_squared_error')


def ols_stats(cols):
    """OLS with intercept on the training set: p-values (t-test) and BIC."""
    A = np.column_stack([np.ones(len(X_train)), X_train[list(cols)].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(A, y_train.to_numpy(float), rcond=None)
    resid = y_train.to_numpy(float) - A @ beta
    n, p = A.shape
    rss = resid @ resid
    se = np.sqrt(np.diag(rss / (n - p) * np.linalg.inv(A.T @ A)))
    pvalues = 2 * stats.t.sf(np.abs(beta / se), df=n - p)
    bic = n * np.log(rss / n) + p * np.log(n)
    return pd.Series(pvalues[1:], index=list(cols)), bic


# 4. Modeling: each scheme returns (subsets for k = 1..5, the k chosen by its own rule)
def exhaustive_cv():
    """Best subset of each size by 5-fold CV RMSE; chosen k = lowest CV RMSE overall."""
    path = [list(min(combinations(FEATURES, k), key=cv_rmse)) for k in KS]
    return path, 1 + int(np.argmin([cv_rmse(s) for s in path]))


def forward_stepwise():
    """Add the feature that lowers CV RMSE most; chosen k = last step that still improved."""
    path, scores = [], []
    for _ in KS:
        prev = path[-1] if path else []
        score, feat = min((cv_rmse(prev + [f]), f) for f in FEATURES if f not in prev)
        path.append(prev + [feat])
        scores.append(score)
    chosen = next((k for k in KS[1:] if scores[k - 1] >= scores[k - 2]), len(KS) + 1) - 1
    return path, chosen


def backward_pvalue(alpha=0.05):
    """Drop the largest-p-value feature each step; chosen k = first subset with all p <= alpha."""
    path, cols = {}, FEATURES.copy()
    while cols:
        path[len(cols)] = cols.copy()
        cols.remove(ols_stats(cols)[0].idxmax())
    path = [path[k] for k in KS]
    chosen = next(k for k in reversed(KS) if ols_stats(path[k - 1])[0].max() <= alpha)
    return path, chosen


def lasso_l1():
    """Order features by when they enter the Lasso path; chosen k = non-zero coefs of LassoCV."""
    Xs = StandardScaler().fit_transform(X_train)
    alphas, coefs, _ = lasso_path(Xs, y_train - y_train.mean(), alphas=500)
    active = coefs != 0                                   # alphas are in decreasing order
    entry = [np.argmax(row) if row.any() else len(alphas) for row in active]
    order = [FEATURES[i] for i in np.argsort(entry, kind='stable')]
    lasso = make_pipeline(StandardScaler(), LassoCV(cv=CV, random_state=SEED, max_iter=100000))
    lasso.fit(X_train, y_train)
    return [order[:k] for k in KS], int(np.sum(np.abs(lasso[-1].coef_) > 1e-8))


def best_bic():
    """Best subset of each size by BIC on train; chosen k = lowest BIC overall."""
    path = [list(min(combinations(FEATURES, k), key=lambda c: ols_stats(c)[1])) for k in KS]
    return path, 1 + int(np.argmin([ols_stats(s)[1] for s in path]))


SCHEMES = {
    'Exhaustive best subset (CV)': exhaustive_cv,
    'Forward stepwise (CV)': forward_stepwise,
    'Backward elimination (p-value)': backward_pvalue,
    'Lasso (L1 path)': lasso_l1,
    'Best subset (BIC)': best_bic,
}

# 5. Evaluation: every (scheme, k) subset refit with OLS; CV on train, one score on test
rows = []
for name, scheme in SCHEMES.items():
    path, chosen_k = scheme()
    for k, cols in zip(KS, path):
        pred = LinearRegression().fit(X_train[cols], y_train).predict(X_test[cols])
        mse = mean_squared_error(y_test, pred)
        rows.append({'Scheme': name, 'k': k, 'Chosen': 'yes' if k == chosen_k else '',
                     'Features': ', '.join(cols),
                     'CV_RMSE': round(cv_rmse(cols), 2), 'CV_R2': round(cv_score(cols, 'r2'), 4),
                     'Test_MAE': round(mean_absolute_error(y_test, pred), 2),
                     'Test_MSE': round(mse, 2), 'Test_RMSE': round(np.sqrt(mse), 2),
                     'Test_R2': round(r2_score(y_test, pred), 4)})
results = pd.DataFrame(rows)

pd.set_option('display.width', 220, 'display.max_columns', None, 'display.max_colwidth', 75)
print(f'Train n={len(X_train)}, test n={len(X_test)}; selection uses train only (5-fold CV, seed {SEED}).')
for name, block in results.groupby('Scheme', sort=False):
    print(f'\n===== {name} =====')
    print(block.drop(columns='Scheme').to_string(index=False))
print('\nEach scheme\'s own choice ("Chosen" = its stopping rule):')
print(results[results['Chosen'] == 'yes'].drop(columns='Chosen').to_string(index=False))

out = results_dir('selection_paths')
results.to_csv(out / 'all_schemes_progression.csv', index=False)


def slug(name):
    return ''.join(c if c.isalnum() else '_' for c in name.lower()).strip('_').replace('__', '_')


# Per-scheme figure: RMSE and R-squared by number of features (CV on train vs test)
for name, block in results.groupby('Scheme', sort=False):
    chosen_k = int(block.loc[block['Chosen'] == 'yes', 'k'].iloc[0])
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, cv_col, test_col, label in [(axes[0], 'CV_RMSE', 'Test_RMSE', 'RMSE'),
                                        (axes[1], 'CV_R2', 'Test_R2', 'R-squared')]:
        ax.plot(block['k'], block[cv_col], marker='o', label='CV (train)')
        ax.plot(block['k'], block[test_col], marker='s', linestyle='--', label='Test')
        ax.axvline(chosen_k, color='grey', linestyle=':', label=f'Chosen k = {chosen_k}')
        ax.set(title=f'{label} by Number of Features', xlabel='Number of Features', ylabel=label)
        ax.set_xticks(list(KS))
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
    fig.suptitle(name)
    fig.tight_layout()
    fig.savefig(out / f'progression_{slug(name)}.png', dpi=160)
    plt.close(fig)

# Combined figure: all five schemes, CV (top) and test (bottom)
fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)
for row, prefix, where in [(0, 'CV', 'CV on train'), (1, 'Test', 'test set')]:
    for col, metric, label in [(0, 'RMSE', 'RMSE'), (1, 'R2', 'R-squared')]:
        ax = axes[row, col]
        for i, (name, block) in enumerate(results.groupby('Scheme', sort=False)):
            ax.plot(block['k'] + (i - 2) * 0.03, block[f'{prefix}_{metric}'], marker='o', label=name)
        ax.set(title=f'{label} by Number of Features ({where})', ylabel=label)
        ax.set_xticks(list(KS))
        ax.grid(True, linestyle=':', alpha=0.6)
for ax in axes[1]:
    ax.set_xlabel('Number of Features')
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, frameon=False)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(out / 'all_schemes_progression.png', dpi=160)
plt.close(fig)
print('\nOutputs:', out)
