import os
import pandas as pd

def load_all_sources(input_dir: str) -> dict:
    """
    Load all CSV/Excel files from input_dir.
    Return dict mapping basename->DataFrame.
    """
    dfs = {}
    for fname in os.listdir(input_dir):
        path = os.path.join(input_dir, fname)
        name, ext = os.path.splitext(fname)
        if ext.lower() in ['.csv', '.xls', '.xlsx']:
            try:
                if ext.lower() == '.csv':
                    dfs[name] = pd.read_csv(path, dtype=str)
                else:
                    dfs[name] = pd.read_excel(path, dtype=str)
            except Exception as e:
                print(f"Skipping {fname}: {e}")
    if not dfs:
        raise FileNotFoundError(f"No CSV/XLS files found in {input_dir}")
    return dfs