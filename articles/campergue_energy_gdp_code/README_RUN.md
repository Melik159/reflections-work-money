# Energy-GDP Coupling Code

## Download World Bank sources

The repository does not vendor the World Bank datasets by default. Download them with:

```bash
python scripts/download_wb_sources.py --out data/code --raw data/raw
```

This creates stable local CSV filenames:

```text
data/code/API_NY.GDP.MKTP.KD.csv
data/code/API_NY.GDP.MKTP.PP.KD.csv
data/code/API_EG.GDP.PUSE.KO.PP.KD.csv
```

Then run the dimensionally coherent reconstruction:

```bash
python src/energy_gdp_analysis.py \
  --gdp-file data/code/API_NY.GDP.MKTP.KD.csv \
  --gdp-ppp-file data/code/API_NY.GDP.MKTP.PP.KD.csv \
  --gdp-per-energy-file data/code/API_EG.GDP.PUSE.KO.PP.KD.csv \
  --countries WLD,USA,FRA,DEU,CHN,IND \
  --start-year 1965 \
  --end-year 2023 \
  --out output_macro
```

The download script uses the official World Bank API CSV export endpoints:

```text
https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD?downloadformat=csv
https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.PP.KD?downloadformat=csv
https://api.worldbank.org/v2/en/indicator/EG.GDP.PUSE.KO.PP.KD?downloadformat=csv
```



This folder contains the updated Python workflow for the GDP-energy coupling analysis.

## Preferred run: independent energy series

Use this if you have a World Bank-style or compatible total energy-consumption CSV:

```bash
python src/energy_gdp_analysis.py \
  --gdp-file data/API_NY.GDP.MKTP.KD_DS2_en_csv_v2_320397.csv \
  --energy-file data/YOUR_TOTAL_ENERGY_FILE.csv \
  --energy-indicator YOUR.ENERGY.INDICATOR \
  --countries WLD,USA,FRA,DEU,CHN,IND \
  --start-year 1965 \
  --end-year 2023 \
  --out output_macro
```

## Dimensionally coherent reconstruction

Use this with:

- real GDP, market USD: `NY.GDP.MKTP.KD`
- real GDP, PPP constant international dollars: `NY.GDP.MKTP.PP.KD`
- GDP per unit of energy, PPP constant dollars per kg oil equivalent: `EG.GDP.PUSE.KO.PP.KD`

```bash
python src/energy_gdp_analysis.py \
  --gdp-file data/API_NY.GDP.MKTP.KD_DS2_en_csv_v2_320397.csv \
  --gdp-ppp-file data/API_NY.GDP.MKTP.PP.KD_DS2_en_csv.csv \
  --gdp-per-energy-file data/API_EG.GDP.PUSE.KO.PP.KD_DS2_en_csv_v2_304872.csv \
  --countries WLD,USA,FRA,DEU,CHN,IND \
  --start-year 1965 \
  --end-year 2023 \
  --out output_macro
```

## Legacy fallback

This reproduces the old logic, but marks it as a methodological fallback because it mixes market GDP and PPP GDP-per-energy units.

```bash
python src/energy_gdp_analysis.py \
  --gdp-file data/API_NY.GDP.MKTP.KD_DS2_en_csv_v2_320397.csv \
  --gdp-per-energy-file data/API_EG.GDP.PUSE.KO.PP.KD_DS2_en_csv_v2_304872.csv \
  --allow-dimensional-fallback \
  --countries WLD,USA,FRA,DEU,CHN,IND \
  --out output_macro_legacy
```

## Outputs

The script writes:

- `merged_energy_gdp.csv`
- `regression_summary.csv`
- `rolling_loglog_elasticity.csv`
- `run_metadata.json`
- level, log-log, annual log-change, indexed-series plots for each country
- rolling log-log elasticity plot

## Interpretation

The level and log-log regressions describe long-run co-movement.

The annual log-change regression is more demanding because it tests whether yearly changes in GDP and energy move together, rather than only showing that both series trend upward over time.

The scripts provide empirical support for a limited claim: GDP and energy remain historically coupled in the tested data. They do not, by themselves, validate the entire theoretical corpus.
