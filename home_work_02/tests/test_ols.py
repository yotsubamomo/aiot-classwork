"""OLS, Adjusted R² with the actual rank, the parametric PI and coverage
(Spec rev 5 次 seam「模型與推論」: PI 公式以手算的小例子核對；coverage 以已知的上下界核對)."""
import numpy as np
import pytest
from scipy import stats

from hw2 import metrics, ols

# A small example small enough to check by hand: y on [1, x], n = 5.
X5 = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
Y5 = np.array([1.0, 3.0, 2.0, 5.0, 4.0])


def test_fit_matches_the_hand_computed_example():
    fit = ols.fit_ols(X5, Y5, ["x"])
    # x̄ = 3, ȳ = 3, Sxx = 10, Sxy = 8 -> slope 0.8, intercept 0.6
    np.testing.assert_allclose(fit.coef, [0.6, 0.8], atol=1e-12)
    # residuals -0.4, 0.8, -1.0, 1.2, -0.6 -> SSE = 3.6; SST = 10
    assert fit.n == 5 and fit.rank == 2 and fit.df_resid == 3
    assert fit.s2 == pytest.approx(3.6 / 3)
    assert fit.r2 == pytest.approx(0.64)
    assert fit.adj_r2 == pytest.approx(1 - (1 - 0.64) * 4 / 3)
    # (XᵀX)⁻¹ for [1, x]: 1/(n Sxx) * [[Σx², −Σx], [−Σx, n]] = 1/50 * [[55, −15], [−15, 5]]
    np.testing.assert_allclose(fit.xtx_inv, np.array([[55, -15], [-15, 5]]) / 50, atol=1e-12)
    assert fit.t_crit == pytest.approx(stats.t.ppf(0.975, 3))


def test_prediction_interval_matches_the_textbook_formula():
    fit = ols.fit_ols(X5, Y5, ["x"])
    x0 = 6.0
    yhat, lo, hi = ols.log_interval(fit, np.array([[x0]]))
    # se_pred = sqrt(s² (1 + 1/n + (x0 − x̄)² / Sxx))
    se = np.sqrt(3.6 / 3 * (1 + 1 / 5 + (x0 - 3) ** 2 / 10))
    t = stats.t.ppf(0.975, 3)
    assert yhat[0] == pytest.approx(0.6 + 0.8 * x0)
    assert lo[0] == pytest.approx(0.6 + 0.8 * x0 - t * se)
    assert hi[0] == pytest.approx(0.6 + 0.8 * x0 + t * se)
    point, ulo, uhi = ols.usd_interval(fit, np.array([[x0]]))
    assert (point[0], ulo[0], uhi[0]) == pytest.approx((np.exp(yhat[0]), np.exp(lo[0]), np.exp(hi[0])))
    assert ulo[0] < point[0] < uhi[0]
    assert point[0] - ulo[0] < uhi[0] - point[0]          # asymmetric in USD


def test_adjusted_r2_uses_the_actual_rank_not_the_column_count():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(40, 3))
    y = X @ [1.0, -2.0, 0.5] + rng.normal(size=40)
    fit = ols.fit_ols(X, y, ["a", "b", "c"])
    assert fit.rank == 4 and fit.df_resid == 36
    assert fit.adj_r2 == pytest.approx(1 - (1 - fit.r2) * 39 / 36)


@pytest.mark.parametrize("make, needle", [
    (lambda X: np.column_stack([X, np.full(len(X), 7.0)]), "constant"),       # collinear with 1
    (lambda X: np.column_stack([X, X[:, 0] * 3.0]), "rank"),                    # duplicate column
    (lambda X: np.column_stack([X, X[:, 0] + X[:, 1]]), "rank"),                # linear combination
    (lambda X: np.column_stack([X, np.zeros(len(X))]), "rank"),                 # all-zero column
])
def test_rank_deficient_designs_raise_and_never_drop_a_column(make, needle):
    rng = np.random.default_rng(2)
    X = make(rng.normal(size=(30, 2)) * [1e5, 1.0])     # very different scales on purpose
    names = [f"c{j}" for j in range(X.shape[1])]
    with pytest.raises(ols.RankDeficientError, match=needle) as err:
        ols.fit_ols(X, rng.normal(size=30), names)
    assert err.value.n_columns == X.shape[1] + 1 and err.value.rank < err.value.n_columns


def test_raw_scale_columns_of_very_different_magnitude_keep_full_rank():
    rng = np.random.default_rng(3)
    X = np.column_stack([rng.uniform(1e5, 2e6, 200), rng.uniform(47.1, 47.8, 200),
                         rng.integers(0, 2, 200)])
    fit = ols.fit_ols(X, rng.normal(size=200), ["lot", "lat", "flag"])
    assert fit.rank == 4
    D = ols.design(X)
    np.testing.assert_allclose(fit.xtx_inv, np.linalg.inv(D.T @ D), rtol=1e-6)


def test_usd_metrics_by_hand():
    m = metrics.usd_metrics([100.0, 200.0, 300.0], [110.0, 190.0, 330.0])
    assert m["mae"] == pytest.approx(50 / 3)
    assert m["mse"] == pytest.approx((100 + 100 + 900) / 3)
    assert m["rmse"] == pytest.approx(np.sqrt(1100 / 3))
    assert m["r2"] == pytest.approx(1 - 1100 / 20000)


def test_coverage_with_known_bounds_uses_the_closed_interval():
    actual = [10.0, 20.0, 30.0, 40.0]
    lower = [10.0, 21.0, 25.0, 30.0]          # row 0 sits on the lower bound (covered)
    upper = [12.0, 25.0, 30.0, 39.0]          # row 2 sits on the upper bound (covered)
    c = metrics.coverage_stats(actual, lower, upper)
    assert c["covered"].tolist() == [True, False, True, False]
    assert c["n_covered"] == 2 and c["coverage"] == 0.5
    assert c["mean_width"] == pytest.approx((2 + 4 + 5 + 9) / 4)
    half = 1.96 * np.sqrt(0.5 * 0.5 / 4)
    assert c["coverage_uncertainty"]["half_width_95"] == pytest.approx(half)
    assert c["coverage_uncertainty"]["interval"] == pytest.approx([0.5 - half, 0.5 + half])
    assert "independent" in c["coverage_uncertainty"]["method"]
