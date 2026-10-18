"""USD-scale metrics and prediction-interval coverage (Spec rev 5 「指標與推論」「預測區間」).

- MAE, MSE, RMSE and R² are computed in USD on the back-transformed predictions exp(ŷ_log);
  R² = 1 − SSE/SST with SST around the mean of the scored rows.
- Coverage uses the closed interval: covered ⇔ lower ≤ actual ≤ upper. coverage = covered / n.
  Mean width is the mean of (upper − lower) in USD.
- The sampling uncertainty of the coverage is reported as 1.96·√(p(1−p)/n), **a binomial
  approximation that assumes independent coverage events** (SR-08, SR-12). The test set contains
  repeat sales of the same house, so the events are not guaranteed to be independent and the
  accuracy of this approximation is not estimated; no direction or size of its error is stated.
"""
import numpy as np

Z_95 = 1.96
BINOMIAL_NOTE = ("binomial approximation 1.96*sqrt(p(1-p)/n_test) that assumes independent "
                 "coverage events; the test set contains repeat sales of the same house, so the "
                 "events are not guaranteed to be independent and the accuracy of this "
                 "approximation is not estimated (no direction or size of its error is stated)")


def usd_metrics(actual, predicted) -> dict:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if actual.shape != predicted.shape or actual.size == 0:
        raise ValueError("actual and predicted must be non-empty and of the same shape")
    err = predicted - actual
    mse = float(np.mean(err ** 2))
    sst = float(np.sum((actual - actual.mean()) ** 2))
    return {
        "mae": float(np.mean(np.abs(err))),
        "mse": mse,
        "rmse": float(np.sqrt(mse)),
        "r2": float(1.0 - np.sum(err ** 2) / sst) if sst > 0 else None,
    }


def coverage_stats(actual, lower, upper) -> dict:
    actual = np.asarray(actual, dtype=float)
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    covered = (lower <= actual) & (actual <= upper)
    n = int(actual.size)
    p = float(covered.mean())
    half = Z_95 * float(np.sqrt(p * (1.0 - p) / n))
    return {
        "covered": covered,
        "n_covered": int(covered.sum()),
        "coverage": p,
        "mean_width": float(np.mean(upper - lower)),
        "coverage_uncertainty": {
            "half_width_95": half,
            "interval": [p - half, p + half],
            "method": BINOMIAL_NOTE,
        },
    }
