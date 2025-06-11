import os
import pandas as pd
import matplotlib.pyplot as plt
from src.config import INPUT_DIR, OUTPUT_DIR, REMAP, THRESH
from src.loader import load_all_sources

# 1. Load all input files
datasets = load_all_sources('inputs')
ts = datasets.get('ts_technologies')
bd = datasets.get('bd_technologies')

# 2. Display basic info
print("=== ts_technologies INFO ===")
print(ts.info())
print(ts.describe(include='all').T)

print("=== bd_technologies INFO ===")
print(bd.info())
print(bd.describe(include='all').T)

# 3. Missing values check
print("Missing in ts:" , ts.isna().sum().to_dict())
print("Missing in bd:" , bd.isna().sum().to_dict())

# 4. Unique and duplicate counts
print("Unique ts names:", ts['name'].nunique())
print("Duplicate ts names:", ts['name'].duplicated().sum())
print("Unique bd names:", bd['product_name'].nunique())
print("Duplicate bd names:", bd['product_name'].duplicated().sum())

# 5. Description length distributions
ts['desc_len'] = ts['description'].fillna('').str.len()
bd['desc_len'] = bd['description'].fillna('').str.len()

plt.figure(figsize=(10,4))
plt.hist(ts['desc_len'], bins=40, alpha=0.5, label='TS')
plt.hist(bd['desc_len'], bins=40, alpha=0.5, label='BD')
plt.legend(); plt.title('Description Length Distribution')
plt.show()

# 6. Top categories
print("Top TS categories:\n", ts['category'].value_counts().head(10))
print("Top BD main categories:\n", bd['main_category'].value_counts().head(10))

# 7. URL coverage
print("TS URL coverage:", ts['url'].notna().mean())
print("BD URL coverage:", bd['seller_website'].notna().mean())

# 8. Exact name overlap examples
ts_names = set(ts['name'].str.lower().str.strip())
bd_names = set(bd['product_name'].str.lower().str.strip())
overlap = ts_names & bd_names
print(f"Exact overlap count: {len(overlap)}; Examples: {list(overlap)[:5]}")