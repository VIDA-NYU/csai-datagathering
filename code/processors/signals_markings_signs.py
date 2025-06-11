#!/usr/bin/env python3
"""
Processor: Merge NYC traffic signals, signs, and markings into one geospatial dataset.
Only merges APS, street signs, and traffic signals — excluding speed limits.
Removes duplicates **within each source** by its unique ID (SIGNID, F_id, etc.).
"""

import pandas as pd
import geopandas as gpd
import os

# === Constants ===
DATA_DIR = "data/signals_markings_signs"
OUTPUT_PATH = os.path.join(DATA_DIR, "signals_signs_markings_combined.csv")
WGS84 = "EPSG:4326"

# === Helper: Convert df with X/Y columns to GeoDataFrame and deduplicate
def to_gdf_from_xy(df, x_col, y_col, source_name, id_cols):
    df = df.dropna(subset=[x_col, y_col]).copy()
    df["geometry"] = gpd.points_from_xy(df[x_col], df[y_col])
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=WGS84)
    gdf["source"] = source_name

    # Try deduplicating using one of the provided ID columns
    for col in id_cols:
        if col in gdf.columns and gdf[col].nunique() > 100:
            gdf["unique_id"] = gdf[col].astype(str).str.strip()
            gdf = gdf.drop_duplicates(subset="unique_id", keep="first")
            break

    return gdf.drop(columns=["unique_id"], errors="ignore")

# === Load and deduplicate each dataset ===
datasets = []

# 1. Accessible pedestrian signals
df_aps = pd.read_csv(os.path.join(DATA_DIR, "accessible_pedestrian_signals.csv"))
gdf_aps = to_gdf_from_xy(df_aps, "POINT_X", "POINT_Y", "accessible_ped_signal", ["F_id", "OBJECTID"])
datasets.append(gdf_aps)

# 2. Street sign work orders
df_ss = pd.read_csv(os.path.join(DATA_DIR, "street_sign_work_orders.csv"))
gdf_ss = to_gdf_from_xy(df_ss, "sign_x_coord", "sign_y_coord", "street_sign", ["SIGNID", "sign_id"])
datasets.append(gdf_ss)

# 3. Traffic signals
df_ts = pd.read_csv(os.path.join(DATA_DIR, "traffic_signals.csv"))
gdf_ts = to_gdf_from_xy(df_ts, "X", "Y", "traffic_signal", ["F_id"])
datasets.append(gdf_ts)

# === Log counts before merging
print("\nLoaded datasets:")
for gdf in datasets:
    print(f" - {gdf['source'].iloc[0]:<25} → {len(gdf):,} rows")

# === Merge all datasets
combined = pd.concat(datasets, ignore_index=True)

# === Save CSV
combined.drop(columns=["geometry"], errors="ignore").to_csv(OUTPUT_PATH, index=False)
print(f"\nFinal merged dataset saved: {OUTPUT_PATH} ({len(combined):,} rows)")