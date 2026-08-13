"""
01_extract_worldbank_indicators.py

Pulls real, free, CC BY-4.0 licensed country-level economic indicators from
the World Bank Indicators API. No API key required.

Indicators pulled:
  - NY.GNP.PCAP.CD : GNI per capita, Atlas method (current US$)
  - PA.NUS.GDP.PLI : Price level index (GDP) - price levels relative to a
                      world-average benchmark; this is the real "cost of
                      living" proxy for this project
  - PA.NUS.PPP     : PPP conversion factor, GDP (LCU per international $)

API docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/898599
Response shape (confirmed from official docs):
  [ {"page": 1, "pages": N, "per_page": "...", "total": N},
    [ {"indicator": {"id":...}, "country": {"id":..., "value":...},
       "countryiso3code": "...", "date": "2023", "value": 1234.5, ...}, ... ] ]
"""

import requests
import pandas as pd
import time

INDICATORS = {
    "NY.GNP.PCAP.CD": "gni_per_capita_usd",
    "PA.NUS.GDP.PLI": "price_level_index",
    "PA.NUS.PPP": "ppp_conversion_factor",
}

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/{indicator}"


def fetch_indicator(indicator_code, column_name, year_range="2018:2023"):
    """
    Pull one indicator for all countries. World Bank data has gaps by year,
    so we pull a range and keep, per country, the most recent non-null value
    rather than a single fixed year (avoids losing countries that just
    happen to be missing the latest year).
    """
    rows = []
    page = 1
    while True:
        params = {
            "format": "json",
            "date": year_range,
            "per_page": 1000,
            "page": page,
        }
        resp = requests.get(BASE_URL.format(indicator=indicator_code), params=params)
        resp.raise_for_status()
        payload = resp.json()

        # payload[0] = pagination metadata, payload[1] = actual records
        if len(payload) < 2 or payload[1] is None:
            break

        for rec in payload[1]:
            if rec["value"] is None:
                continue
            rows.append({
                "country_name": rec["country"]["value"],
                "iso3_code": rec["countryiso3code"],
                "year": rec["date"],
                column_name: rec["value"],
            })

        total_pages = payload[0]["pages"]
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # Keep most recent year per country
    df = df.sort_values("year", ascending=False).drop_duplicates(subset="iso3_code")
    return df[["country_name", "iso3_code", column_name]]


def main():
    merged = None
    for code, column in INDICATORS.items():
        print(f"Fetching {code} -> {column}")
        df = fetch_indicator(code, column)
        print(f"  {len(df)} countries with data")
        if merged is None:
            merged = df
        else:
            merged = merged.merge(df.drop(columns=["country_name"]), on="iso3_code", how="outer")

    merged = merged[merged["iso3_code"].str.len() == 3]  # drop aggregate regions (e.g. "WLD", "EUU")
    merged.to_csv("worldbank_indicators_raw.csv", index=False)
    print(f"\nSaved -> worldbank_indicators_raw.csv ({len(merged)} countries)")


if __name__ == "__main__":
    main()
