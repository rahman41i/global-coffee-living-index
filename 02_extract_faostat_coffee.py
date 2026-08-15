import os
import pandas as pd

def load_faostat_data():
    raw_file = "faostat_coffee_raw.csv"
    manual_export = "FAOSTAT_data_en_8-15-2026.csv"
    
    if os.path.exists(raw_file):
        print(f"Loading cached FAOSTAT data from {raw_file}...")
        return pd.read_csv(raw_file)
    elif os.path.exists(manual_export):
        print(f"Parsing manual FAOSTAT export file {manual_export}...")
        df = pd.read_csv(manual_export)
        m49_to_iso3 = {
            24: 'AGO', 84: 'BLZ', 204: 'BEN', 68: 'BOL', 76: 'BRA', 108: 'BDI', 132: 'CPV',
            116: 'KHM', 120: 'CMR', 140: 'CAF', 159: 'CHN', 158: 'TWN', 156: 'CHN', 170: 'COL',
            174: 'COM', 178: 'COG', 184: 'COK', 188: 'CRI', 192: 'CUB', 384: 'CIV', 180: 'COD',
            212: 'DMA', 214: 'DOM', 218: 'ECU', 222: 'SLV', 226: 'GNQ', 231: 'ETH', 242: 'FJI',
            258: 'PYF', 266: 'GAB', 288: 'GHA', 320: 'GTM', 324: 'GIN', 328: 'GUY', 332: 'HTI',
            340: 'HND', 356: 'IND', 360: 'IDN', 388: 'JAM', 404: 'KEN', 418: 'LAO', 430: 'LBR',
            450: 'MDG', 454: 'MWI', 458: 'MYS', 480: 'MUS', 484: 'MEX', 508: 'MOZ', 104: 'MMR',
            524: 'NPL', 540: 'NCL', 558: 'NIC', 566: 'NGA', 591: 'PAN', 598: 'PNG', 600: 'PRY',
            604: 'PER', 608: 'PHL', 630: 'PRI', 646: 'RWA', 662: 'LCA', 670: 'VCT', 882: 'WSM',
            678: 'STP', 682: 'SAU', 694: 'SLE', 144: 'LKA', 740: 'SUR', 764: 'THA', 626: 'TLS',
            768: 'TGO', 776: 'TON', 780: 'TTO', 800: 'UGA', 834: 'TZA', 840: 'USA', 548: 'VUT',
            862: 'VEN', 704: 'VNM', 887: 'YEM', 894: 'ZMB', 716: 'ZWE'
        }
        df['iso3_code'] = df['Area Code (M49)'].map(m49_to_iso3)
        df_out = pd.DataFrame({
            'iso3_code': df['iso3_code'],
            'country_name': df['Area'],
            'coffee_production_qty': df['Value'],
            'production_unit': df['Unit'],
            'coffee_export_value_usd1000': None,
            'export_unit': None
        })
        df_out.to_csv(raw_file, index=False)
        print(f"Successfully processed and saved {raw_file}")
        return df_out
    else:
        raise FileNotFoundError("Neither API response nor local FAOSTAT export CSV found.")
