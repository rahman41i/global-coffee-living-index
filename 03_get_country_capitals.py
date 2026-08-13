"""
03_get_country_capitals.py

Pulls real capital-city names per country from restcountries.com (free,
no API key). Used ONLY as a readability label ("representative city") on
top of country-level data - not a claim that price/coffee data is specific
to that city. This should be documented clearly in the final dataset's
README/data dictionary.
"""

import requests
import pandas as pd

URL = "http://api.worldbank.org/v2/country?format=json&per_page=300"


def main():
    print("Fetching country capitals from World Bank API...")
    rows = []
    try:
        resp = requests.get(URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if len(data) > 1 and isinstance(data[1], list):
            for item in data[1]:
                iso3 = item.get("id", "")
                capital = item.get("capitalCity", "")
                if iso3:
                    rows.append({"iso3_code": iso3, "capital_city": capital})
    except Exception as e:
        print(f"[Warning] Failed to fetch country capitals: {e}")

    df = pd.DataFrame(rows)
    if df.empty:
        df = pd.DataFrame(columns=["iso3_code", "capital_city"])

    df.to_csv("country_capitals_raw.csv", index=False)
    print(f"Saved -> country_capitals_raw.csv ({len(df)} countries)")


if __name__ == "__main__":
    main()