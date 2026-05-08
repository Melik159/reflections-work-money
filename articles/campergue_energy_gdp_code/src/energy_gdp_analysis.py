#!/usr/bin/env python3
"""
Energy-GDP coupling analysis.

This script replaces the earlier one-off scripts with a single reproducible workflow.

Preferred methods:
  1. Use an independent energy-consumption series with --energy-file.
  2. Or reconstruct energy dimensionally as:
       Energy = GDP_PPP_constant / GDP_per_unit_of_energy_PPP_constant
     requiring --gdp-ppp-file and --gdp-per-energy-file.

Avoid, except as an explicitly marked fallback:
       Energy = GDP_market_constant / GDP_per_unit_of_energy_PPP_constant
because the units are mixed.
"""

from __future__ import annotations

import argparse
import json
import math
import warnings
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


WB_ID_COLS = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]


def load_wb_indicator(
    path: Path,
    *,
    country_codes: list[str],
    indicator_code: str | None = None,
    value_name: str = "value",
    start_year: int | None = None,
    end_year: int | None = None,
) -> pd.DataFrame:
    """Load a World Bank CSV exported from the API, usually with four metadata rows."""
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    # World Bank API CSVs usually require skiprows=4.
    # If that fails, retry without skipping.
    try:
        df = pd.read_csv(path, skiprows=4)
        if "Country Code" not in df.columns:
            raise ValueError("not a WB table after skiprows=4")
    except Exception:
        df = pd.read_csv(path)

    required = {"Country Name", "Country Code"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required World Bank columns: {sorted(missing)}")

    if indicator_code is not None and "Indicator Code" in df.columns:
        df = df[df["Indicator Code"] == indicator_code].copy()

    df = df[df["Country Code"].isin(country_codes)].copy()

    id_vars = [c for c in WB_ID_COLS if c in df.columns]
    year_cols = [c for c in df.columns if str(c).isdigit()]

    if not year_cols:
        raise ValueError(f"No year columns found in {path}")

    long = df.melt(id_vars=id_vars, value_vars=year_cols, var_name="year", value_name=value_name)
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    long[value_name] = pd.to_numeric(long[value_name], errors="coerce")
    long = long.dropna(subset=["year", value_name])
    long["year"] = long["year"].astype(int)

    if start_year is not None:
        long = long[long["year"] >= start_year]
    if end_year is not None:
        long = long[long["year"] <= end_year]

    return long[["Country Name", "Country Code", "year", value_name]].copy()


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """Small dependency-free OLS with intercept: y = a + b*x."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 3:
        return {"n": int(len(x)), "intercept": np.nan, "beta": np.nan, "r2": np.nan}

    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    y_hat = X @ coef
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = np.nan if ss_tot == 0 else 1.0 - ss_res / ss_tot
    return {
        "n": int(len(x)),
        "intercept": float(coef[0]),
        "beta": float(coef[1]),
        "r2": float(r2),
    }


def safe_log(s: pd.Series) -> pd.Series:
    return np.log(s.where(s > 0))


def prepare_dataset(args: argparse.Namespace) -> tuple[pd.DataFrame, dict]:
    country_codes = [c.strip().upper() for c in args.countries.split(",") if c.strip()]
    meta: dict = {
        "countries": country_codes,
        "start_year": args.start_year,
        "end_year": args.end_year,
        "energy_method": None,
        "warnings": [],
    }

    gdp = load_wb_indicator(
        args.gdp_file,
        country_codes=country_codes,
        indicator_code=args.gdp_indicator,
        value_name="gdp_real",
        start_year=args.start_year,
        end_year=args.end_year,
    )

    df = gdp

    if args.energy_file:
        energy = load_wb_indicator(
            args.energy_file,
            country_codes=country_codes,
            indicator_code=args.energy_indicator,
            value_name="energy",
            start_year=args.start_year,
            end_year=args.end_year,
        )
        df = df.merge(energy, on=["Country Name", "Country Code", "year"], how="inner")
        meta["energy_method"] = "independent_energy_series"
        meta["energy_source"] = str(args.energy_file)
        meta["energy_indicator"] = args.energy_indicator

    elif args.gdp_ppp_file and args.gdp_per_energy_file:
        gdp_ppp = load_wb_indicator(
            args.gdp_ppp_file,
            country_codes=country_codes,
            indicator_code=args.gdp_ppp_indicator,
            value_name="gdp_ppp_real",
            start_year=args.start_year,
            end_year=args.end_year,
        )
        gdp_per_e = load_wb_indicator(
            args.gdp_per_energy_file,
            country_codes=country_codes,
            indicator_code=args.gdp_per_energy_indicator,
            value_name="gdp_per_energy",
            start_year=args.start_year,
            end_year=args.end_year,
        )
        df = df.merge(gdp_ppp, on=["Country Name", "Country Code", "year"], how="inner")
        df = df.merge(gdp_per_e, on=["Country Name", "Country Code", "year"], how="inner")
        df["energy"] = df["gdp_ppp_real"] / df["gdp_per_energy"]
        meta["energy_method"] = "reconstructed_dimensionally"
        meta["energy_formula"] = "energy = gdp_ppp_real / gdp_per_energy"
        meta["gdp_ppp_source"] = str(args.gdp_ppp_file)
        meta["gdp_per_energy_source"] = str(args.gdp_per_energy_file)

    elif args.gdp_per_energy_file and args.allow_dimensional_fallback:
        gdp_per_e = load_wb_indicator(
            args.gdp_per_energy_file,
            country_codes=country_codes,
            indicator_code=args.gdp_per_energy_indicator,
            value_name="gdp_per_energy",
            start_year=args.start_year,
            end_year=args.end_year,
        )
        df = df.merge(gdp_per_e, on=["Country Name", "Country Code", "year"], how="inner")
        df["energy"] = df["gdp_real"] / df["gdp_per_energy"]
        msg = (
            "Dimensional fallback used: energy = market GDP / PPP GDP-per-energy. "
            "This is not recommended for final claims."
        )
        warnings.warn(msg)
        meta["warnings"].append(msg)
        meta["energy_method"] = "reconstructed_dimensional_fallback_not_recommended"
        meta["energy_formula"] = "energy = gdp_real / gdp_per_energy"

    else:
        raise SystemExit(
            "No valid energy source provided.\n"
            "Use either:\n"
            "  --energy-file PATH [--energy-indicator CODE]\n"
            "or:\n"
            "  --gdp-ppp-file PATH --gdp-per-energy-file PATH\n"
            "or, only for legacy comparison:\n"
            "  --gdp-per-energy-file PATH --allow-dimensional-fallback"
        )

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["gdp_real", "energy"])
    df = df[(df["gdp_real"] > 0) & (df["energy"] > 0)].copy()

    if df.empty:
        raise SystemExit("No overlapping positive GDP/energy observations after cleaning.")

    return df, meta


def add_transformations(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values(["Country Code", "year"]).copy()
    out["log_gdp"] = safe_log(out["gdp_real"])
    out["log_energy"] = safe_log(out["energy"])
    out["dlog_gdp"] = out.groupby("Country Code")["log_gdp"].diff()
    out["dlog_energy"] = out.groupby("Country Code")["log_energy"].diff()
    return out


def summarize_country(d: pd.DataFrame) -> list[dict]:
    rows = []
    country_name = str(d["Country Name"].iloc[0])
    country_code = str(d["Country Code"].iloc[0])

    specs = [
        ("level", "energy", "gdp_real", "GDP_real ~ Energy"),
        ("loglog", "log_energy", "log_gdp", "log(GDP_real) ~ log(Energy)"),
        ("dlog", "dlog_energy", "dlog_gdp", "Δlog(GDP_real) ~ Δlog(Energy)"),
    ]

    for model_name, xcol, ycol, formula in specs:
        fit = ols_fit(d[xcol].to_numpy(), d[ycol].to_numpy())
        rows.append({
            "country": country_name,
            "country_code": country_code,
            "model": model_name,
            "formula": formula,
            **fit,
        })

    return rows


def plot_scatter_with_fit(d: pd.DataFrame, xcol: str, ycol: str, title: str, xlabel: str, ylabel: str, out_path: Path) -> None:
    plot_df = d[[xcol, ycol]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(plot_df) < 3:
        return

    fit = ols_fit(plot_df[xcol].to_numpy(), plot_df[ycol].to_numpy())
    x_grid = np.linspace(plot_df[xcol].min(), plot_df[xcol].max(), 100)
    y_hat = fit["intercept"] + fit["beta"] * x_grid

    plt.figure(figsize=(7, 5))
    plt.scatter(plot_df[xcol], plot_df[ycol], alpha=0.65)
    plt.plot(x_grid, y_hat, linewidth=2, label=f"beta={fit['beta']:.4g}, R²={fit['r2']:.4f}, n={fit['n']}")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def plot_country_series(d: pd.DataFrame, out_path: Path) -> None:
    if len(d) < 3:
        return

    dd = d.sort_values("year").copy()

    # Index both series to 100 at first common observation to compare trajectories.
    first_gdp = dd["gdp_real"].iloc[0]
    first_e = dd["energy"].iloc[0]
    dd["gdp_index"] = 100.0 * dd["gdp_real"] / first_gdp
    dd["energy_index"] = 100.0 * dd["energy"] / first_e

    plt.figure(figsize=(8, 5))
    plt.plot(dd["year"], dd["gdp_index"], linewidth=2, label="GDP index")
    plt.plot(dd["year"], dd["energy_index"], linewidth=2, label="Energy index")
    plt.title(f"{dd['Country Name'].iloc[0]}: GDP and energy indexed to first year")
    plt.xlabel("Year")
    plt.ylabel("Index, first year = 100")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def rolling_loglog_elasticity(d: pd.DataFrame, window: int) -> pd.DataFrame:
    rows = []
    dd = d.sort_values("year").copy()
    for i in range(0, len(dd) - window + 1):
        w = dd.iloc[i:i + window]
        fit = ols_fit(w["log_energy"].to_numpy(), w["log_gdp"].to_numpy())
        rows.append({
            "country": str(w["Country Name"].iloc[0]),
            "country_code": str(w["Country Code"].iloc[0]),
            "start_year": int(w["year"].iloc[0]),
            "end_year": int(w["year"].iloc[-1]),
            "window": int(window),
            "beta_loglog": fit["beta"],
            "r2_loglog": fit["r2"],
            "n": fit["n"],
        })
    return pd.DataFrame(rows)


def plot_rolling(roll: pd.DataFrame, out_path: Path) -> None:
    if roll.empty:
        return
    plt.figure(figsize=(8, 5))
    for code, d in roll.groupby("country_code"):
        x = (d["start_year"] + d["end_year"]) / 2
        plt.plot(x, d["beta_loglog"], linewidth=2, label=code)
    plt.title("Rolling log-log GDP-energy elasticity")
    plt.xlabel("Window midpoint year")
    plt.ylabel("Elasticity beta")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze GDP-energy coupling from World Bank-style CSVs.")
    parser.add_argument("--gdp-file", type=Path, required=True, help="Real GDP CSV. Default indicator: NY.GDP.MKTP.KD.")
    parser.add_argument("--gdp-indicator", default="NY.GDP.MKTP.KD")

    parser.add_argument("--energy-file", type=Path, default=None, help="Preferred: independent total energy-consumption CSV.")
    parser.add_argument("--energy-indicator", default=None, help="Indicator code for --energy-file, if needed.")

    parser.add_argument("--gdp-ppp-file", type=Path, default=None, help="PPP real GDP CSV used to reconstruct energy.")
    parser.add_argument("--gdp-ppp-indicator", default="NY.GDP.MKTP.PP.KD")

    parser.add_argument("--gdp-per-energy-file", type=Path, default=None, help="GDP per unit of energy CSV.")
    parser.add_argument("--gdp-per-energy-indicator", default="EG.GDP.PUSE.KO.PP.KD")

    parser.add_argument("--allow-dimensional-fallback", action="store_true", help="Legacy comparison only; mixes GDP units.")
    parser.add_argument("--countries", default="WLD", help="Comma-separated World Bank country codes, e.g. WLD,USA,FRA,DEU,CHN,IND.")
    parser.add_argument("--start-year", type=int, default=1965)
    parser.add_argument("--end-year", type=int, default=2023)
    parser.add_argument("--rolling-window", type=int, default=15)
    parser.add_argument("--out", type=Path, default=Path("output_macro"))

    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    df, meta = prepare_dataset(args)
    df = add_transformations(df)

    df.to_csv(args.out / "merged_energy_gdp.csv", index=False)

    summaries = []
    for _, d in df.groupby("Country Code"):
        summaries.extend(summarize_country(d))

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(args.out / "regression_summary.csv", index=False)

    roll_all = []
    for _, d in df.groupby("Country Code"):
        roll = rolling_loglog_elasticity(d, args.rolling_window)
        if not roll.empty:
            roll_all.append(roll)

    if roll_all:
        roll_df = pd.concat(roll_all, ignore_index=True)
    else:
        roll_df = pd.DataFrame()
    roll_df.to_csv(args.out / "rolling_loglog_elasticity.csv", index=False)

    for code, d in df.groupby("Country Code"):
        safe_code = str(code).lower()
        name = str(d["Country Name"].iloc[0])

        plot_scatter_with_fit(
            d, "energy", "gdp_real",
            f"{name}: real GDP vs energy",
            "Energy",
            "Real GDP",
            args.out / f"{safe_code}_energy_gdp_level.png",
        )
        plot_scatter_with_fit(
            d, "log_energy", "log_gdp",
            f"{name}: log(real GDP) vs log(energy)",
            "log(Energy)",
            "log(Real GDP)",
            args.out / f"{safe_code}_energy_gdp_loglog.png",
        )
        plot_scatter_with_fit(
            d, "dlog_energy", "dlog_gdp",
            f"{name}: annual log changes",
            "Δlog(Energy)",
            "Δlog(Real GDP)",
            args.out / f"{safe_code}_energy_gdp_dlog.png",
        )
        plot_country_series(d, args.out / f"{safe_code}_indexed_series.png")

    if not roll_df.empty:
        plot_rolling(roll_df, args.out / "rolling_loglog_elasticity.png")

    meta["n_observations"] = int(len(df))
    meta["year_min"] = int(df["year"].min())
    meta["year_max"] = int(df["year"].max())
    meta["outputs"] = [
        "merged_energy_gdp.csv",
        "regression_summary.csv",
        "rolling_loglog_elasticity.csv",
        "*_energy_gdp_level.png",
        "*_energy_gdp_loglog.png",
        "*_energy_gdp_dlog.png",
        "*_indexed_series.png",
        "rolling_loglog_elasticity.png",
    ]

    (args.out / "run_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("\n[OK] Analysis complete")
    print(f"Output directory: {args.out}")
    print("\nRegression summary:")
    print(summary_df.to_string(index=False))
    if meta.get("warnings"):
        print("\nWarnings:")
        for w in meta["warnings"]:
            print(f"- {w}")


if __name__ == "__main__":
    main()
