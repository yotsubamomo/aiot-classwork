"""DIC-02: 50 Startups full five-feature OLS regression (CRISP-DM).

Run from the repository root:  python week06/analysis/full_model.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from common import FEATURES, load_data, load_raw, results_dir, split

# 1. Business understanding: predict startup profit.
# 2. Data understanding
raw = load_raw()
print('Shape:', raw.shape)
print('Missing values:\n', raw.isna().sum())

# 3. Data preparation: California is the reference category (see common.py).
X, y = load_data()
X_train, X_test, y_train, y_test = split(X, y)

# 4. Modeling: use all five features, no feature selection.
model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('\nIntercept:', round(model.intercept_, 4))
print('Coefficients:\n', pd.Series(model.coef_, index=X.columns).round(6))

# 5. Evaluation: held-out test set.
print('\nTest MAE:', round(mean_absolute_error(y_test, pred), 2))
print('Test RMSE:', round(np.sqrt(mean_squared_error(y_test, pred)), 2))
print('Test R2:', round(r2_score(y_test, pred), 4))   # ASCII label: Windows cp950 consoles cannot print "²"
residual = y_test.to_numpy() - pred
out = results_dir('full_model')
pd.DataFrame({'Actual': y_test.to_numpy(), 'Predicted': pred, 'Residual': residual},
             index=y_test.index).to_csv(out / 'predictions.csv', index_label='Row')

fig, ax = plt.subplots()
ax.scatter(y_test, pred)
lo, hi = min(y_test.min(), pred.min()), max(y_test.max(), pred.max())
ax.plot([lo, hi], [lo, hi], 'r--')
ax.set(xlabel='Actual Profit', ylabel='Predicted Profit', title='Actual vs Predicted')
fig.tight_layout()
fig.savefig(out / 'actual_vs_predicted.png', dpi=160)
plt.close(fig)

fig, ax = plt.subplots()
ax.scatter(pred, residual)
ax.axhline(0, color='red', linestyle='--')
ax.set(xlabel='Predicted Profit', ylabel='Residual', title='Residual Plot')
fig.tight_layout()
fig.savefig(out / 'residuals.png', dpi=160)
plt.close(fig)

# 6. Deployment: inference example (California reference state).
new_startup = pd.DataFrame([{'R&D Spend': 100000, 'Administration': 120000, 'Marketing Spend': 150000,
                             'State_Florida': 0, 'State_New York': 0}])[FEATURES]
print('Example predicted profit:', round(model.predict(new_startup)[0], 2))
print('Outputs:', out)
