"""VED spike, step 2: can trip features explain ICE/HEV fuel use, and is the cold effect visible?

Usage: python -I model.py <trips_csv> <out_json>
"""
import json
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold

COLD_REF, HOT_REF = 20.0, 25.0  # hinge points (°C) for the piecewise temperature terms


def load(path: str) -> pd.DataFrame:
    t = pd.read_csv(path)
    t["vtype"] = t["Vehicle Type"].fillna(t["EngineType"])
    t = t[t.vtype.isin(["ICE", "HEV"])]
    t = t[(t.maf_cov >= 0.9) & t.oat_mean.notna() & (t.dist_km >= 2) & (t.duration_s >= 120)].copy()
    # OAT readings above 40 °C or below -30 °C are implausible for Ann Arbor air (sensor heat soak)
    t = t[t.oat_mean.between(-30, 40)].copy()
    t["l100"] = t.fuel_l_maf / t.dist_km * 100
    n_before = len(t)
    t = t[(t.l100 >= 2) & (t.l100 <= 30)].copy()
    t.attrs["dropped_l100"] = n_before - len(t)

    t["disp_l"] = t["Engine Configuration & Displacement"].astype(str).str.extract(r"(\d+(?:\.\d+)?)L")[0].astype(float)
    t["weight_lb"] = pd.to_numeric(t["Generalized_Weight"], errors="coerce")
    t["is_hev"] = (t.vtype == "HEV").astype(int)
    t["cold"] = np.maximum(0, COLD_REF - t.oat_mean)
    t["hot"] = np.maximum(0, t.oat_mean - HOT_REF)
    t["speed2"] = t.mean_speed_kmh ** 2 / 100
    t["stops_per_km"] = t.stops / t.dist_km
    t["log_dist"] = np.log(t.dist_km)
    t["disp_l"] = t.disp_l.fillna(t.disp_l.median())
    t["weight_lb"] = t.weight_lb.fillna(t.weight_lb.median())
    return t


FEATURES = ["cold", "hot", "mean_speed_kmh", "speed2", "idle_frac", "stops_per_km", "pke",
            "log_dist", "disp_l", "weight_lb", "is_hev"]


def cv_eval(t: pd.DataFrame) -> dict:
    X, y, groups = t[FEATURES].to_numpy(), t.l100.to_numpy(), t.veh.to_numpy()
    models = {
        "mean_baseline": None,
        "mlr": LinearRegression(),
        "hgb": HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0),
    }
    out = {}
    for name, m in models.items():
        pred = np.empty_like(y)
        for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
            if m is None:
                pred[te] = y[tr].mean()
            else:
                m.fit(X[tr], y[tr])
                pred[te] = m.predict(X[te])
        out[name] = {
            "MAE": round(mean_absolute_error(y, pred), 3),
            "RMSE": round(float(np.sqrt(mean_squared_error(y, pred))), 3),
            "R2": round(r2_score(y, pred), 3),
            "MAPE_%": round(float(np.mean(np.abs(pred - y) / y) * 100), 1),
        }
    return out


def temp_bins(t: pd.DataFrame) -> dict:
    bins = [-30, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40]
    g = t.groupby(pd.cut(t.oat_mean, bins), observed=True).l100.agg(["median", "count"])
    return {str(k): {"median_l100": round(v["median"], 2), "trips": int(v["count"])} for k, v in g.iterrows()}


def fixed_effects(t: pd.DataFrame) -> dict:
    """Within-vehicle model: vehicle fixed effects absorb car identity, so the temperature
    coefficient compares the same car on cold vs mild days. SEs clustered by vehicle."""
    formula = "l100 ~ cold + hot + mean_speed_kmh + speed2 + idle_frac + stops_per_km + pke + log_dist + C(veh)"
    fit = smf.ols(formula, data=t).fit(cov_type="cluster", cov_kwds={"groups": t.veh})
    keep = ["cold", "hot", "mean_speed_kmh", "speed2", "idle_frac", "stops_per_km", "pke", "log_dist"]
    coefs = {k: {"coef": round(fit.params[k], 4), "ci95": [round(x, 4) for x in fit.conf_int().loc[k]],
                 "p": float(f"{fit.pvalues[k]:.2g}")} for k in keep}

    # cold effect at -8 °C vs 20 °C for a typical trip, same car (VED paper reports ~46% for MPG)
    typical = t.l100.median()
    delta = fit.params["cold"] * (COLD_REF - (-8.0))
    return {
        "coefs": coefs,
        "r2_within_insample": round(fit.rsquared, 3),
        "typical_l100": round(typical, 2),
        "cold_minus8_vs_20_extra_l100": round(delta, 2),
        "cold_minus8_vs_20_pct_of_typical": round(delta / typical * 100, 1),
    }


def decomposition_example(t: pd.DataFrame) -> dict:
    """For the coldest-quartile trips, how much of the fuel is attributed to cold
    (predicted at actual OAT minus predicted with OAT set to 20 °C)?"""
    m = LinearRegression().fit(t[FEATURES], t.l100)
    cold_trips = t[t.oat_mean <= t.oat_mean.quantile(0.25)]
    base = cold_trips[FEATURES].copy()
    warm = base.copy()
    warm["cold"] = 0.0
    warm["hot"] = 0.0
    share = (m.predict(base) - m.predict(warm)) / m.predict(base)
    return {
        "cold_quartile_oat_max": round(t.oat_mean.quantile(0.25), 1),
        "trips": len(cold_trips),
        "median_cold_share_%": round(float(np.median(share) * 100), 1),
        "p10_p90_cold_share_%": [round(float(np.percentile(share, q) * 100), 1) for q in (10, 90)],
    }


def main(trips_csv: str, out_json: str) -> None:
    t = load(trips_csv)
    summary = {
        "trips_used": len(t),
        "vehicles": int(t.veh.nunique()),
        "by_type": t.vtype.value_counts().to_dict(),
        "dropped_implausible_l100": t.attrs["dropped_l100"],
        "oat_range": [round(t.oat_mean.min(), 1), round(t.oat_mean.max(), 1)],
        "l100_quartiles": [round(x, 2) for x in t.l100.quantile([0.25, 0.5, 0.75])],
        "cv_grouped_by_vehicle": cv_eval(t),
        "median_l100_by_oat_bin": temp_bins(t),
        "within_vehicle_fixed_effects": fixed_effects(t),
        "cold_attribution_example": decomposition_example(t),
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:3])
