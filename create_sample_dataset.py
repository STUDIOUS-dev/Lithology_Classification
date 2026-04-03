"""
Creates a clean 500-row sample from hidden_test.csv for deployment.
Keeps only the key columns users care about.
"""
import pandas as pd
from pathlib import Path
import random

random.seed(42)

src = Path("litho_data/test/hidden_test.csv")
df = pd.read_csv(src, sep=";", on_bad_lines="skip")

print(f"Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")

# Core ML features + metadata columns
keep_cols = [
    "WELL", "DEPTH_MD",
    "GR", "RHOB", "NPHI", "RDEP", "DTC", "PEF",
    "FORMATION", "GROUP"
]
keep_cols = [c for c in keep_cols if c in df.columns]

df_sample = df[keep_cols].copy()

# Remove rows missing ALL core features
feature_cols = [c for c in ["GR", "RHOB", "NPHI", "RDEP", "DTC", "PEF"] if c in df_sample.columns]
df_sample = df_sample.dropna(subset=feature_cols, how="all")

# Sample 500 rows evenly across wells if multiple wells exist
if "WELL" in df_sample.columns and df_sample["WELL"].nunique() > 1:
    wells = df_sample["WELL"].unique()
    per_well = max(1, 500 // len(wells))
    parts = [df_sample[df_sample["WELL"] == w].sample(min(per_well, len(df_sample[df_sample["WELL"] == w])), random_state=42) for w in wells]
    df_out = pd.concat(parts).head(500).reset_index(drop=True)
else:
    df_out = df_sample.sample(min(500, len(df_sample)), random_state=42).sort_values("DEPTH_MD").reset_index(drop=True)

# Round numeric columns for readability
for col in feature_cols + ["DEPTH_MD"]:
    if col in df_out.columns:
        df_out[col] = df_out[col].round(4)

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "hidden_test_sample.csv"
df_out.to_csv(out_path, index=False)

print(f"\nSaved sample: {df_out.shape[0]} rows x {df_out.shape[1]} cols -> {out_path}")
print(f"File size: {out_path.stat().st_size / 1024:.1f} KB")
print(f"Feature completeness:")
for col in feature_cols:
    valid = df_out[col].notna().sum()
    print(f"  {col}: {valid}/{len(df_out)} ({valid/len(df_out)*100:.1f}%)")
