import pandas as pd
from rapidfuzz import process, fuzz
from difflib import SequenceMatcher

def dedupe(master, new, threshold=85):
    """
    Fuzzy-merge 'new' into 'master' on 'key', within 'block'.
    """
    rows = []
    for r in new.itertuples():
        candidates = master.loc[master.block == r.block, 'key']
        best = process.extractOne(r.key, candidates, scorer=fuzz.token_sort_ratio)
        if not best or best[1] < threshold:
            rows.append(r._asdict())
    extra = pd.DataFrame(rows)
    out = pd.concat([master, extra], ignore_index=True)
    return out.drop_duplicates(subset='product_name').reset_index(drop=True)

def find_internal_duplicates(df, threshold=85):
    """
    Find internally similar product name pairs for manual review.
    """
    candidates = []
    names = df['product_name'].tolist()
    for i in range(len(names) - 1):
        a, b = names[i], names[i + 1]
        score = SequenceMatcher(None, a, b).ratio() * 100
        if score >= threshold:
            candidates.append({'name_a': a, 'name_b': b, 'score': round(score, 2)})
    return candidates