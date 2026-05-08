#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "smoke_data"
OUT = ROOT / "tests" / "smoke_output"
DATA.mkdir(parents=True, exist_ok=True)

years = list(range(1965, 2024))
E = np.linspace(100, 300, len(years))
GDP_PPP = 7.5 * (E ** 1.5)
GDP_MARKET = 0.85 * GDP_PPP
GDP_PER_E = GDP_PPP / E

def wb_csv(path, indicator_name, indicator_code, values):
    cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + [str(y) for y in years]
    row = ["World", "WLD", indicator_name, indicator_code] + list(values)
    # Add four dummy rows to mimic the World Bank API export.
    with open(path, "w", encoding="utf-8") as f:
        f.write("dummy,dummy,dummy,dummy\n")
        f.write("dummy,dummy,dummy,dummy\n")
        f.write("dummy,dummy,dummy,dummy\n")
        f.write("dummy,dummy,dummy,dummy\n")
        pd.DataFrame([row], columns=cols).to_csv(f, index=False)

wb_csv(DATA / "gdp_market.csv", "GDP constant", "NY.GDP.MKTP.KD", GDP_MARKET)
wb_csv(DATA / "gdp_ppp.csv", "GDP PPP constant", "NY.GDP.MKTP.PP.KD", GDP_PPP)
wb_csv(DATA / "gdp_per_energy.csv", "GDP per unit energy", "EG.GDP.PUSE.KO.PP.KD", GDP_PER_E)

cmd = [
    sys.executable,
    str(ROOT / "src" / "energy_gdp_analysis.py"),
    "--gdp-file", str(DATA / "gdp_market.csv"),
    "--gdp-ppp-file", str(DATA / "gdp_ppp.csv"),
    "--gdp-per-energy-file", str(DATA / "gdp_per_energy.csv"),
    "--countries", "WLD",
    "--start-year", "1965",
    "--end-year", "2023",
    "--out", str(OUT),
]

subprocess.run(cmd, check=True)

summary = pd.read_csv(OUT / "regression_summary.csv")
loglog = summary[summary["model"] == "loglog"].iloc[0]
assert abs(loglog["beta"] - 1.5) < 1e-10, loglog
assert loglog["r2"] > 0.999999, loglog

print("[OK] Smoke test passed")
print(summary.to_string(index=False))
print(f"Outputs written to: {OUT}")
