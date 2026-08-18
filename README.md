# Global Coffee & Living Index

An econometric analysis, statistical modeling framework, and data pipeline examining real purchasing power, price elasticities, and agricultural commodity trade dynamics across 251 global entities ($n = 198$ matched observations)[cite: 8, 9].

---

## Executive Summary

* **Penn Effect Validation:** Confirms that the Price Level Index ($PLI$) scales inelastically relative to GNI per capita ($\epsilon = 0.2252, R^2 = 0.572$)[cite: 8, 9]. Domestic price levels rise at less than one-quarter the rate of nominal national income growth, driving a non-linear acceleration in real living affordability in developed economies ($R^2 = 0.777$)[cite: 8, 9].
* **The Coffee Commodity Paradox:** Green coffee-producing nations exhibit a mean Living Affordability Score ($LAS$) of 9.35 compared to 29.29 for non-producing entities ($p < 10^{-13}$)[cite: 8, 9]. Controlling for national income, coffee production volume yields no statistically significant contribution to local purchasing power ($\beta = 0.1812, p = 0.348$)[cite: 8, 9].
* **Pipeline Remediation:** Fixed silent API timeout errors using automated multi-year retry loops (2022 $\rightarrow$ 2021 $\rightarrow$ 2020) and implemented dynamic filtering to prevent 48 regional aggregate entities from contaminating country-level cross-sections[cite: 8, 9].

---

## Key Methodology & Formulas

### 1. Purchasing Power Ratio ($PPR$)
$$PPR_i = \frac{GNI_i}{PLI_i}$$
Quantifies real local income per unit of domestic price intensity relative to the US baseline ($US = 100$)[cite: 8, 9].

### 2. Living Affordability Score ($LAS$)
$$LAS_i = \left( \frac{PPR_i - \min(PPR)}{\max(PPR) - \min(PPR)} \right) \times 100$$
Projects $PPR$ onto a normalized $[0, 100]$ scale for global cross-country benchmarking[cite: 8, 9]. Baseline boundary values range from 12.86 (Burundi) to 1,277.93 (Qatar)[cite: 8, 9].

---

## Data Schema

| Field Variable Name | Data Type | Description |
| :--- | :--- | :--- |
| `iso3_code` | String | Primary Key; ISO 3166-1 alpha-3 international code[cite: 8, 9] |
| `country_name` | String | Standardized official country identifier[cite: 8, 9] |
| `gni_per_capita_usd` | Float64 | Gross National Income per capita (Atlas method, current US$)[cite: 8, 9] |
| `price_level_index` | Float64 | Price Level Index relative to US baseline ($US = 100$)[cite: 8, 9] |
| `ppp_conversion_factor` | Float64 | PPP conversion factor (Local Currency Units per Intl $)[cite: 8, 9] |
| `representative_city` | String | Capital city name used for spatial mapping[cite: 8, 9] |
| `coffee_production_qty` | Float64 | Annual green coffee production volume (Metric tonnes, $t$)[cite: 8, 9] |
| `purchasing_power_ratio` | Float64 | Price-adjusted real income metric ($GNI / PLI$)[cite: 8, 9] |
| `living_affordability_score` | Float64 | Min-max normalized purchasing power score $[0, 100]$[cite: 8, 9] |

---

## Pipeline Execution Roadmap

1. **`01_ingest_worldbank.py`**: Queries World Bank API for GNI per capita and Price Level Index indicators[cite: 8, 9].
2. **`02_ingest_faostat.py`**: Queries FAOSTAT API for green coffee production and export metrics, using offline CSV fallback parsers upon API timeout[cite: 8, 9].
3. **`03_clean_transform.py`**: Filters regional aggregate ISO codes (e.g., `WLD`, `EUU`), normalizes country names, and calculates $PPR$ and $LAS$[cite: 8, 9].
4. **`04_econometric_models.py`**: Runs log-log and multivariate OLS regressions, evaluating Penn Effect elasticity and commodity trade impacts[cite: 8, 9].

---

## Citation & Metadata

* **Author:** Rahman Aliyev[cite: 8, 9]
* **Data Vintage:** World Bank Indicators (2018–2023) & FAOSTAT Coffee Statistics (2020–2022)[cite: 8, 9]
* **Publication Date:** August 2026[cite: 8, 9]
