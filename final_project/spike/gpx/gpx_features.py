"""Check whether a BMW Motorrad Connected GPX can produce the same trip features as the VED spike.

Usage: python -I gpx_features.py <file.gpx>
Prints sampling statistics and derived features only (no coordinates).
"""
import sys
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

NS = {"g": "http://www.topografix.com/GPX/1/1"}


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi, dlmb = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def main(path: str) -> None:
    root = ET.parse(path).getroot()
    rows = []
    for si, seg in enumerate(root.iterfind(".//g:trkseg", NS)):
        for pt in seg.iterfind("g:trkpt", NS):
            rows.append({
                "seg": si,
                "lat": float(pt.get("lat")),
                "lon": float(pt.get("lon")),
                "ele": float(pt.findtext("g:ele", namespaces=NS)),
                "time": pd.Timestamp(pt.findtext("g:time", namespaces=NS)),
            })
    df = pd.DataFrame(rows).sort_values("time").reset_index(drop=True)

    dt = df.time.diff().dt.total_seconds()
    step = haversine_m(df.lat.shift(), df.lon.shift(), df.lat, df.lon)
    df["dt"], df["step_m"] = dt, step

    print("points", len(df), "segments", df.seg.nunique())
    print("start (UTC)", df.time.iloc[0], "end", df.time.iloc[-1],
          "span_min", round((df.time.iloc[-1] - df.time.iloc[0]).total_seconds() / 60, 1))
    print("sampling interval s: median", dt.median(), "p90", dt.quantile(0.9), "max", dt.max())
    print("intervals: 1s", int((dt == 1).sum()), "2s", int((dt == 2).sum()), ">5s", int((dt > 5).sum()), ">60s", int((dt > 60).sum()))

    # derived speed only over normal sampling gaps; long gaps are logging pauses (e.g. engine off)
    ok = df.dt.between(0.5, 5)
    df["speed_kmh"] = np.where(ok, df.step_m / df.dt * 3.6, np.nan)
    moving_time = df.loc[ok, "dt"].sum()
    dist_km = df.loc[ok, "step_m"].sum() / 1000
    print("distance_km (within normal gaps)", round(dist_km, 2), "moving-log time min", round(moving_time / 60, 1))
    s = df.speed_kmh.dropna()
    print("speed km/h: median", round(s.median(), 1), "p95", round(s.quantile(0.95), 1), "max", round(s.max(), 1))
    print("implausible speed points (>200 km/h):", int((s > 200).sum()))

    # smoothed speed for behaviour features (GPS speed from position differences is noisy)
    sm = df.speed_kmh.rolling(3, center=True, min_periods=1).median()
    v = sm / 3.6
    dtt = df.dt.where(ok, 0).fillna(0)
    idle = dtt[sm < 3].sum() / moving_time if moving_time else np.nan
    dv2 = (v ** 2).diff()
    pke = dv2[(dv2 > 0) & ok].sum() / (dist_km * 1000) if dist_km else np.nan
    state = pd.Series(np.where(sm > 10, 1.0, np.where(sm < 3, 0.0, np.nan))).ffill()
    stops = int(((state == 0) & (state.shift() == 1)).sum())
    climb = df.ele.diff().clip(lower=0)[ok].sum()
    print("idle_frac", round(idle, 3), "stops", stops, "stops_per_km", round(stops / dist_km, 2) if dist_km else None,
          "pke", round(pke, 3), "elevation_gain_m", round(climb, 0))

    seg_stats = df.groupby("seg").agg(n=("time", "size"), start=("time", "min"), end=("time", "max"))
    seg_stats["min"] = ((seg_stats.end - seg_stats.start).dt.total_seconds() / 60).round(1)
    print(seg_stats[["n", "min"]].to_string())


if __name__ == "__main__":
    main(sys.argv[1])
