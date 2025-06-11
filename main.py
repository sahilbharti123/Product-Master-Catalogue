import os
import pandas as pd

from src.config import INPUT_DIR, OUTPUT_DIR, REMAP, THRESH
from src.loader import load_all_sources
from src.cleaner import clean, normalize
from src.deduper import dedupe, find_internal_duplicates

def main():
    # 1. Load
    raw = load_all_sources(INPUT_DIR)
    # 2. Clean & normalize
    stores = {}
    for name, df in raw.items():
        stores[name] = normalize(clean(df, REMAP.get(name, {})))
    # 3. Build master
    keys = list(stores)
    master = stores[keys[0]]
    for k in keys[1:]:
        master = dedupe(master, stores[k], threshold=THRESH)
    # 4. Export master
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    master_path = os.path.join(OUTPUT_DIR, 'master_catalogue.csv')
    master.to_csv(master_path, index=False)
    print(f"Master contains {len(master):,} products and saved to {master_path}.")
    # 5. Internal duplicate review
    candidates = find_internal_duplicates(master, threshold=THRESH)
    dup_path = os.path.join(OUTPUT_DIR, 'internal_duplicates.csv')
    pd.DataFrame(candidates).to_csv(dup_path, index=False)
    print(f"{len(candidates)} internal duplicate pairs written to {dup_path}")

if __name__ == "__main__":
    main()
