"""Ordinary least squares on ln(price) with the actual model rank, and the parametric 95% PI.

Spec rev 5 「指標與推論」「預測區間」:

- The design matrix is the intercept column followed by the encoded columns (raw scale for OLS).
- **Model rank** is the number of linearly independent columns of the actual design matrix
  (intercept included). It is computed by a column-pivoted (rank-revealing) QR of the
  column-equilibrated matrix (every column divided by its Euclidean norm; rank does not change
  under column scaling, and the scaled matrix is far better conditioned than the raw one). A
  matrix with rank < number of columns is **rank deficient**: :func:`fit_ols` raises
  :class:`RankDeficientError` and never drops a column.
- With full rank: coefficients from the same QR; ``(XᵀX)⁻¹ = N⁻¹ P R⁻¹ R⁻ᵀ Pᵀ N⁻¹``
  (``N`` the column norms, ``P`` the pivoting); ``df_resid = n − rank``; ``s² = SSE / df_resid``; log-scale ``R²`` and
  Adjusted ``R² = 1 − (1 − R²)(n − 1)/(n − rank)``; ``t = t(0.975, df_resid)``.
- PI on the log scale: ``ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))``, then ``exp`` back to USD (asymmetric).
  :func:`log_interval` evaluates exactly this formula with the exported ``(XᵀX)⁻¹`` so that the
  dashboard and an independent recomputation can reproduce it from the exported numbers.
"""
from dataclasses import dataclass

import numpy as np
from scipy import linalg, stats

PI_LEVEL = 0.95
INTERCEPT = "(intercept)"


class RankDeficientError(ValueError):
    """The design matrix (intercept included) has rank < number of columns."""

    def __init__(self, message: str, rank: int, n_columns: int, dependent_columns: list):
        super().__init__(message)
        self.rank = rank
        self.n_columns = n_columns
        self.dependent_columns = dependent_columns


@dataclass(frozen=True)
class OLSFit:
    column_names: tuple[str, ...]     # INTERCEPT first, then the encoded columns
    coef: np.ndarray                  # raw scale, intercept first
    xtx_inv: np.ndarray               # (XᵀX)⁻¹ of the raw design (intercept included)
    n: int
    rank: int
    df_resid: int
    s2: float
    r2: float                         # log scale
    adj_r2: float                     # log scale, with the actual rank
    t_crit: float                     # t(0.975, df_resid)

    @property
    def n_columns(self) -> int:
        return len(self.column_names)


def design(X: np.ndarray) -> np.ndarray:
    """Prepend the intercept column."""
    X = np.asarray(X, dtype=float)
    return np.hstack([np.ones((X.shape[0], 1)), X])


def _equilibrated_qr(D: np.ndarray):
    """Column-pivoted QR of the column-equilibrated design: (q, r, perm, norms, rank).

    Every column is divided by its Euclidean norm (an all-zero column keeps norm 1 and stays
    zero). The rank is the number of diagonal entries of R with |r_ii| > |r_00|·max(n, p)·eps,
    the same tolerance rule as numpy's matrix_rank."""
    norms = np.linalg.norm(D, axis=0)
    safe = np.where(norms > 0, norms, 1.0)
    q, r, perm = linalg.qr(D / safe, mode="economic", pivoting=True)
    diag = np.abs(np.diag(r))
    tol = (diag[0] if diag.size else 0.0) * max(D.shape) * np.finfo(float).eps
    rank = int((diag > tol).sum())
    return q, r, perm, safe, rank


def matrix_rank(D: np.ndarray) -> int:
    """Rank of a design matrix (intercept included), as used by :func:`fit_ols`."""
    return _equilibrated_qr(np.asarray(D, dtype=float))[4]


def _dependent_columns(D: np.ndarray, names) -> list:
    """Columns other than the intercept that are constant on the rows (for the message only)."""
    return [f"{name} (constant on these rows)" for j, name in enumerate(names)
            if j > 0 and np.ptp(D[:, j]) == 0]


def fit_ols(X: np.ndarray, y: np.ndarray, column_names, level: float = PI_LEVEL) -> OLSFit:
    """Fit y on [1, X]. Raises RankDeficientError when the design is rank deficient."""
    D = design(X)
    y = np.asarray(y, dtype=float)
    names = (INTERCEPT, *column_names)
    n, p = D.shape
    if len(names) != p:
        raise ValueError("column_names does not match X")
    q, r, perm, norms, rank = _equilibrated_qr(D)
    if rank < p:
        dependent = _dependent_columns(D, names)
        raise RankDeficientError(
            f"design matrix rank {rank} < {p} columns"
            + (f"; e.g. {', '.join(dependent[:5])}" if dependent else ""),
            rank=rank, n_columns=p, dependent_columns=dependent)
    df_resid = n - rank
    if df_resid <= 0:
        raise RankDeficientError(f"no residual degrees of freedom (n={n}, rank={rank})",
                                 rank=rank, n_columns=p, dependent_columns=[])
    beta_scaled = np.empty(p)
    beta_scaled[perm] = linalg.solve_triangular(r, q.T @ y)
    coef = beta_scaled / norms
    r_inv = linalg.solve_triangular(r, np.eye(p))
    inv_scaled = np.empty((p, p))
    inv_scaled[np.ix_(perm, perm)] = r_inv @ r_inv.T
    xtx_inv = inv_scaled / np.outer(norms, norms)
    xtx_inv = (xtx_inv + xtx_inv.T) / 2.0
    resid = y - D @ coef
    sse = float(resid @ resid)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / df_resid
    return OLSFit(column_names=names, coef=coef, xtx_inv=xtx_inv, n=n, rank=rank,
                  df_resid=df_resid, s2=sse / df_resid, r2=r2, adj_r2=adj_r2,
                  t_crit=float(stats.t.ppf(0.5 + level / 2.0, df_resid)))


def predict_log(fit: OLSFit, X: np.ndarray) -> np.ndarray:
    return design(X) @ fit.coef


def log_interval(fit: OLSFit, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(ŷ_log, lower_log, upper_log) with ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))."""
    D = design(X)
    yhat = D @ fit.coef
    leverage = np.einsum("ij,jk,ik->i", D, fit.xtx_inv, D)
    half = fit.t_crit * np.sqrt(fit.s2 * (1.0 + leverage))
    return yhat, yhat - half, yhat + half


def usd_interval(fit: OLSFit, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(point, lower, upper) in USD: exp of the log-scale values (no bias correction; the point is
    a conditional-median estimate, not the conditional mean)."""
    yhat, lo, hi = log_interval(fit, X)
    return np.exp(yhat), np.exp(lo), np.exp(hi)
