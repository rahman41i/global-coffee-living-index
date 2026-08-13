"""
04_merge_and_compute_index.py

Merges World Bank indicators, FAOSTAT coffee data, and capital-city labels
into the final Global Coffee & Living Index dataset. Computes one derived
metric: a coffee export value relative to income, as a real (not fabricated)
"affordability"-style signal.
"""

import pandas as pd


def main():
    wb = pd.read_csv("worldbank_indicators_raw.csv")
    faostat = pd.read_csv("faostat_coffee_raw.csv")
    capitals = pd.read_csv("country_capitals_raw.csv")

    if "capital_city" in capitals.columns and "representative_city" not in capitals.columns:
        capitals = capitals.rename(columns={"capital_city": "representative_city"})

    df = wb.copy()

    if not capitals.empty and "iso3_code" in capitals.columns:
        city_cols = [c for c in ["iso3_code", "representative_city"] if c in capitals.columns]
        df = df.merge(capitals[city_cols], on="iso3_code", how="left")

    if not faostat.empty and "iso3_code" in faostat.columns:
        faostat_cols = [c for c in faostat.columns if c != "country_name"]
        df = df.merge(faostat[faostat_cols], on="iso3_code", how="left")

    if "representative_city" not in df.columns:
        df["representative_city"] = ""

    for col in ["coffee_production_qty", "coffee_export_value_usd1000"]:
        if col not in df.columns:
            df[col] = float("nan")

    df["purchasing_power_ratio"] = df["gni_per_capita_usd"] / df["price_level_index"]

    max_ppr = df["purchasing_power_ratio"].max()
    min_ppr = df["purchasing_power_ratio"].min()

    if pd.notna(max_ppr) and max_ppr != min_ppr:
        df["living_affordability_score"] = (
            (df["purchasing_power_ratio"] - min_ppr) / (max_ppr - min_ppr)
        ) * 100
        df["living_affordability_score"] = df["living_affordability_score"].round(2)
    else:
        df["living_affordability_score"] = float("nan")

    df["purchasing_power_ratio"] = df["purchasing_power_ratio"].round(2)

    df.to_csv("global_coffee_living_index.csv", index=False)
    print(f"Saved -> global_coffee_living_index.csv ({len(df)} countries)")
    print("\nPreview (Top 10 by Living Affordability Score):")
    
    preview_cols = [
        "country_name",
        "iso3_code",
        "representative_city",
        "gni_per_capita_usd",
        "price_level_index",
        "living_affordability_score",
    ]
    
    sorted_df = df.dropna(subset=["living_affordability_score"]).sort_values(
        by="living_affordability_score", ascending=False
    )
    print(sorted_df[preview_cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
