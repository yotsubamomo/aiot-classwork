"""VED spike, step 1: aggregate the weekly dynamic CSVs into one row per trip.

Usage: python -I build_trips.py <dyn_dir> <static_dir> <out_csv>

Fuel for ICE/HEV is estimated from MAF and fuel trims (VED paper, Algorithm 1 idea):
    fuel[g/s] = MAF[g/s] * (1 + (STFT + LTFT)/100) / AFR
with AFR = 14.7 (gasoline stoichiometric) and density 745 g/L. Where the logged
Fuel Rate[L/hr] exists it is used instead.
"""
import glob
import os
import sys

import numpy as np
import pandas as pd

AFR = 14.7
DENSITY_G_PER_L = 745.0
MAX_DT_S = 5.0  # cap gaps so a logging dropout is not integrated as driving

COLS = {
    "DayNum": "day",
    "VehId": "veh",
    "Trip": "trip",
    "Timestamp(ms)": "t_ms",
    "Vehicle Speed[km/h]": "speed",
    "MAF[g/sec]": "maf",
    "OAT[DegC]": "oat",
    "Fuel Rate[L/hr]": "fuel_rate",
    "Short Term Fuel Trim Bank 1[%]": "stft1",
    "Short Term Fuel Trim Bank 2[%]": "stft2",
    "Long Term Fuel Trim Bank 1[%]": "ltft1",
    "Long Term Fuel Trim Bank 2[%]": "ltft2",
}


def trip_features(g: pd.DataFrame) -> dict:
    g = g.sort_values("t_ms")
    t = g["t_ms"].to_numpy() / 1000.0
    dt = np.clip(np.diff(t, append=t[-1]), 0, MAX_DT_S)

    speed = g["speed"].ffill().fillna(0).to_numpy()  # km/h
    v = speed / 3.6  # m/s
    dist_m = float(np.sum(v * dt))
    duration_s = float(np.sum(dt))

    maf = g["maf"].ffill().to_numpy()
    stft = g[["stft1", "stft2"]].mean(axis=1).ffill().fillna(0).to_numpy()
    ltft = g[["ltft1", "ltft2"]].mean(axis=1).ffill().fillna(0).to_numpy()
    fuel_gps = maf * (1 + (stft + ltft) / 100.0) / AFR
    maf_cov = float(np.sum(dt[~np.isnan(maf)]) / duration_s) if duration_s > 0 else 0.0
    fuel_l_maf = float(np.nansum(fuel_gps * dt) / DENSITY_G_PER_L)

    fr = g["fuel_rate"].ffill().to_numpy()
    fr_cov = float(np.sum(dt[~np.isnan(fr)]) / duration_s) if duration_s > 0 else 0.0
    fuel_l_logged = float(np.nansum(fr * dt) / 3600.0)

    # positive kinetic energy per metre: sum of positive (v_{i+1}^2 - v_i^2) / distance
    dv2 = np.diff(v ** 2)
    pke = float(np.sum(dv2[dv2 > 0]) / dist_m) if dist_m > 0 else np.nan

    stopped = speed < 1
    # a stop = entering "stopped" (<1 km/h) after having been "moving" (>5 km/h);
    # speeds in between keep the previous state so slow creeping is not double counted
    state = pd.Series(np.where(speed > 5, 1.0, np.where(stopped, 0.0, np.nan))).ffill().to_numpy()
    stops = int(np.sum((state[1:] == 0) & (state[:-1] == 1)))

    return {
        "day": float(g["day"].iloc[0]),
        "duration_s": duration_s,
        "dist_km": dist_m / 1000.0,
        "mean_speed_kmh": (dist_m / duration_s * 3.6) if duration_s > 0 else np.nan,
        "max_speed_kmh": float(speed.max()),
        "idle_frac": float(np.sum(dt[stopped]) / duration_s) if duration_s > 0 else np.nan,
        "stops": stops,
        "pke": pke,
        "oat_mean": float(g["oat"].mean()),
        "oat_cov": float(g["oat"].notna().mean()),
        "maf_cov": maf_cov,
        "fuel_l_maf": fuel_l_maf,
        "fr_cov": fr_cov,
        "fuel_l_logged": fuel_l_logged,
        "n_rows": len(g),
    }


def main(dyn_dir: str, static_dir: str, out_csv: str) -> None:
    rows = []
    files = sorted(glob.glob(os.path.join(dyn_dir, "*.csv")))
    for i, f in enumerate(files, 1):
        df = pd.read_csv(f, usecols=list(COLS)).rename(columns=COLS)
        for (veh, trip), g in df.groupby(["veh", "trip"], sort=False):
            r = trip_features(g)
            r.update(veh=int(veh), trip=int(trip))
            rows.append(r)
        print(f"[{i}/{len(files)}] {os.path.basename(f)} trips so far: {len(rows)}", flush=True)

    trips = pd.DataFrame(rows)
    static = pd.concat(
        [
            pd.read_excel(os.path.join(static_dir, "VED_Static_Data_ICE&HEV.xlsx")),
            pd.read_excel(os.path.join(static_dir, "VED_Static_Data_PHEV&EV.xlsx")),
        ],
        ignore_index=True,
    )
    static = static.rename(columns={"VehId": "veh"})
    trips = trips.merge(static, on="veh", how="left")
    trips.to_csv(out_csv, index=False)
    print("wrote", out_csv, trips.shape)


if __name__ == "__main__":
    main(*sys.argv[1:4])
