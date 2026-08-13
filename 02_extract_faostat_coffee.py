"""
02_extract_faostat_coffee.py

Pulls real, free, openly-licensed coffee production and export data from
FAOSTAT (UN Food and Agriculture Organization).

Features:
  - Multi-year fallback loop (2022 -> 2021 -> 2020 -> 2019)
  - Retry logic with exponential backoff for network resilience
  - Loud failure policy (raises Exception if dataset remains 100% empty)
"""

import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://fenixservices.fao.org/faostat/api/v1/en"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get_session():
    session = requests.Session()
    retries = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=[500, 502, 503, 504, 521],
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def fetch_domain_year_fallback(session, domain_code, item_code, element_code, years=[2022, 2021, 2020, 2019]):
    url = f"{BASE}/data/{domain_code}"
    
    for yr in years:
        params = {
            "item": item_code,
            "element": element_code,
            "year": yr,
            "area_cs": "ISO3",
            "show_code": 1,
            "show_unit": 1,
            "show_flags": 0,
            "null_values": 0,
            "limit": -1,
            "output_type": "objects",
        }
        try:
            print(f"  Attempting domain {domain_code} for year {yr}...")
            resp = session.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                if data:
                    print(f"  Success! Year {yr} -> {len(data)} records found.")
                    return data
            else:
                print(f"  Year {yr} returned status code {resp.status_code}")
        except Exception as e:
            print(f"  Request failed for year {yr}: {e}")
        time.sleep(1)
        
    return []


def main():
    session = get_session()
    coffee_item_code = 656
    production_element_code = 5510
    export_value_element_code = 5922

    print("Fetching coffee production (domain QCL)...")
    production = fetch_domain_year_fallback(session, "QCL", coffee_item_code, production_element_code)

    print("Fetching coffee export value (domain TCL)...")
    exports = fetch_domain_year_fallback(session, "TCL", coffee_item_code, export_value_element_code)

    if not production and not exports:
        raise RuntimeError(
            "CRITICAL: FAOSTAT API call failed for all fallback years and retries! "
            "No coffee data retrieved. Check network connectivity or FAOSTAT service status."
        )

    if production:
        prod_df = pd.DataFrame(production)[["Area Code (ISO3)", "Area", "Value", "Unit"]].rename(
            columns={
                "Area Code (ISO3)": "iso3_code",
                "Area": "country_name",
                "Value": "coffee_production_qty",
                "Unit": "production_unit",
            }
        )
    else:
        prod_df = pd.DataFrame(columns=["iso3_code", "country_name", "coffee_production_qty", "production_unit"])

    if exports:
        exp_df = pd.DataFrame(exports)[["Area Code (ISO3)", "Value", "Unit"]].rename(
            columns={
                "Area Code (ISO3)": "iso3_code",
                "Value": "coffee_export_value_usd1000",
                "Unit": "export_unit",
            }
        )
    else:
        exp_df = pd.DataFrame(columns=["iso3_code", "coffee_export_value_usd1000", "export_unit"])

    merged = prod_df.merge(exp_df, on="iso3_code", how="outer")
    merged.to_csv("faostat_coffee_raw.csv", index=False)
    print(f"\nSaved -> faostat_coffee_raw.csv ({len(merged)} countries with coffee data)")


if __name__ == "__main__":
    main()