# Global Coffee & Living Index

An econometric analysis, statistical modeling framework, and data pipeline examining real purchasing power, price elasticities, and agricultural commodity trade dynamics across 251 global entities ($n = 198$ matched observations).

---

## Executive Summary

* **Penn Effect Validation:** Confirms that the Price Level Index ($PLI$) scales inelastically relative to GNI per capita ($\epsilon = 0.2252, R^2 = 0.572$). Domestic price levels rise at less than one-quarter the rate of nominal national income growth, driving a non-linear acceleration in real living affordability in developed economies ($R^2 = 0.777$).
* **The Coffee Commodity Paradox:** Green coffee-producing nations exhibit a mean Living Affordability Score ($LAS$) of 9.35 compared to 29.29 for non-producing entities ($p < 10^{-13}$). Controlling for national income, coffee production volume yields no statistically significant contribution to local purchasing power ($\beta = 0.1812, p = 0.348$).
* **Pipeline Remediation:** Fixed silent API timeout errors using automated multi-year retry loops (2022 $\rightarrow$ 2021 $\rightarrow$ 2020) and implemented dynamic filtering to prevent 48 regional aggregate entities from contaminating country-level cross-sections.

---

## Key Methodology & Formulas

### 1. Purchasing Power Ratio ($PPR$)
$$PPR_i = \frac{GNI_i}{PLI_i}$$
Quantifies real local income per unit of domestic price intensity relative to the US baseline ($US = 100$).

### 2. Living Affordability Score ($LAS$)
$$LAS_i = \left( \frac{PPR_i - \min(PPR)}{\max(PPR) - \min(PPR)} \right) \times 100$$
Projects $PPR$ onto a normalized $[0, 100]$ scale for global cross-country benchmarking. Baseline boundary values range from 12.86 (Burundi) to 1,277.93 (Qatar).

---

## Data Schema

| Field Variable Name | Data Type | Description |
| :--- | :--- | :--- |
| `iso3_code` | String | Primary Key; ISO 3166-1 alpha-3 international code |
| `country_name` | String | Standardized official country identifier |
| `gni_per_capita_usd` | Float64 | Gross National Income per capita (Atlas method, current US$) |
| `price_level_index` | Float64 | Price Level Index relative to US baseline ($US = 100$) |
| `ppp_conversion_factor` | Float64 | PPP conversion factor (Local Currency Units per Intl $) |
| `representative_city` | String | Capital city name used for spatial mapping |
| `coffee_production_qty` | Float64 | Annual green coffee production volume (Metric tonnes, $t$) |
| `purchasing_power_ratio` | Float64 | Price-adjusted real income metric ($GNI / PLI$) |
| `living_affordability_score` | Float64 | Min-max normalized purchasing power score $[0, 100]$ |

---

## Pipeline Execution Roadmap

1. **`01_ingest_worldbank.py`**: Queries World Bank API for GNI per capita and Price Level Index indicators.
2. **`02_ingest_faostat.py`**: Queries FAOSTAT API for green coffee production and export metrics, using offline CSV fallback parsers upon API timeout.
3. **`03_clean_transform.py`**: Filters regional aggregate ISO codes (e.g., `WLD`, `EUU`), normalizes country names, and calculates $PPR$ and $LAS$.
4. **`04_econometric_models.py`**: Runs log-log and multivariate OLS regressions, evaluating Penn Effect elasticity and commodity trade impacts.

---

## Citation & Metadata

* **Author:** Rahman Aliyev
* **Data Vintage:** World Bank Indicators (2018–2023) & FAOSTAT Coffee Statistics (2020–2022)
* **Publication Date:** August 2026

---

>  **Kaggle Release:** The complete dataset, processed metrics, and analytical notebooks are published on [Kaggle](https://www.kaggle.com/datasets/rahman4li/global-coffee-and-living-index-2026) for interactive exploration, visualization, and reproducible research.

---

##  Kaggle Resources

* **Kaggle Dataset:** [Global Coffee & Living Index Dataset](https://www.kaggle.com/datasets/rahman4li/global-coffee-and-living-index-2026)
* **Kaggle Notebook / EDA:** [View Interactive Analysis](https://www.kaggle.com/code/rahman4li/global-coffee-and-living-index)
