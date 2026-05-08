#!/usr/bin/env python3
"""
Download World Bank World Development Indicators CSV sources used by the
GDP-energy coupling analysis.

The script downloads the official World Bank CSV ZIP export for each indicator,
extracts the main API_*.csv file, and renames it to a stable local filename.

No third-party dependency is required.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


INDICATORS = {
    "NY.GDP.MKTP.KD": {
        "label": "Real GDP, constant US$",
        "filename": "API_NY.GDP.MKTP.KD.csv",
        "url": "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD?downloadformat=csv",
    },
    "NY.GDP.MKTP.PP.KD": {
        "label": "Real GDP, PPP constant 2021 international $ or latest WB base",
        "filename": "API_NY.GDP.MKTP.PP.KD.csv",
        "url": "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.PP.KD?downloadformat=csv",
    },
    "EG.GDP.PUSE.KO.PP.KD": {
        "label": "GDP per unit of energy use, PPP constant international $ per kg oil equivalent",
        "filename": "API_EG.GDP.PUSE.KO.PP.KD.csv",
        "url": "https://api.worldbank.org/v2/en/indicator/EG.GDP.PUSE.KO.PP.KD?downloadformat=csv",
    },
}


def download_file(url: str, target: Path) -> None:
    print(f"[download] {url}")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 campergue-energy-gdp-reproducibility-script"
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        with target.open("wb") as f:
            shutil.copyfileobj(response, f)
    print(f"[ok] wrote {target} ({target.stat().st_size} bytes)")


def extract_main_csv(zip_path: Path, indicator_code: str, out_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()

        candidates = [
            n for n in names
            if n.lower().endswith(".csv")
            and Path(n).name.startswith("API_")
            and indicator_code in Path(n).name
            and "Metadata_" not in Path(n).name
        ]

        if not candidates:
            candidates = [
                n for n in names
                if n.lower().endswith(".csv")
                and Path(n).name.startswith("API_")
                and "Metadata_" not in Path(n).name
            ]

        if len(candidates) != 1:
            raise RuntimeError(
                f"Could not identify unique main CSV for {indicator_code} in {zip_path}. "
                f"Candidates: {candidates}. ZIP entries: {names}"
            )

        member = candidates[0]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with z.open(member) as src, out_path.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    print(f"[extract] {indicator_code} -> {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download World Bank CSV sources for the GDP-energy analysis.")
    parser.add_argument("--out", type=Path, default=Path("data/code"), help="Output directory for stable CSV filenames.")
    parser.add_argument("--raw", type=Path, default=Path("data/raw"), help="Output directory for downloaded ZIP files.")
    parser.add_argument("--force", action="store_true", help="Re-download even if local files already exist.")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    args.raw.mkdir(parents=True, exist_ok=True)

    print("[info] Downloading World Bank sources")
    print(f"[info] CSV output: {args.out}")
    print(f"[info] ZIP output: {args.raw}")

    for indicator_code, meta in INDICATORS.items():
        final_csv = args.out / meta["filename"]
        zip_file = args.raw / f"{indicator_code}.zip"

        print()
        print(f"[indicator] {indicator_code} — {meta['label']}")

        if final_csv.exists() and not args.force:
            print(f"[skip] {final_csv} already exists. Use --force to replace it.")
            continue

        if not zip_file.exists() or args.force:
            download_file(meta["url"], zip_file)
        else:
            print(f"[reuse] {zip_file}")

        extract_main_csv(zip_file, indicator_code, final_csv)

    print()
    print("[OK] Sources ready.")
    print()
    print("Run the analysis with:")
    print("python src/energy_gdp_analysis.py \\")
    print("  --gdp-file data/code/API_NY.GDP.MKTP.KD.csv \\")
    print("  --gdp-ppp-file data/code/API_NY.GDP.MKTP.PP.KD.csv \\")
    print("  --gdp-per-energy-file data/code/API_EG.GDP.PUSE.KO.PP.KD.csv \\")
    print("  --countries WLD,USA,FRA,DEU,CHN,IND \\")
    print("  --start-year 1965 \\")
    print("  --end-year 2023 \\")
    print("  --out output_macro")


if __name__ == "__main__":
    main()
