import pandas as pd

def clean(df, renames, keep=None):
    """
    - Rename via 'renames'
    - Normalize column names
    - Keep listed fields
    - Fill/trim text, strip model numbers, drop exact duplicates
    """
    df = df.rename(columns={c: c.strip().lower().replace(' ', '_') for c in df.columns})
    df = df.rename(columns={k: v for k, v in renames.items() if k in df.columns})
    keep = keep or ['product_name','description','category','source_url']
    df = df[[c for c in keep if c in df.columns]].copy()
    for c in df.columns:
        df[c] = df[c].fillna('').astype(str).str.strip()
    if 'product_name' in df:
        df['product_name'] = df['product_name'].str.replace(
            r"\s+\d[\w-]*$", '', regex=True
        ).str.strip()
    return df.drop_duplicates().reset_index(drop=True)

def normalize(df):
    """Add 'key' (normalized name) and 'block' (first char)"""
    d = df.copy()
    d['key'] = (
        d['product_name']
         .str.lower()
         .str.replace(r'[^a-z0-9]+', ' ', regex=True)
         .str.strip()
    )
    d['block'] = d['key'].str[:1]
    return d
