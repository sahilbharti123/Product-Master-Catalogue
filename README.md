# Product Master Catalogue Deduplication Pipeline

This repository contains a modular, reproducible pipeline for merging and deduplicating product catalogues from multiple data sources. It is designed for efficient entity resolution and can be extended to handle more sources easily.

---

## Project Structure

```
Product-Master-Catalogue/
├── inputs/
│   ├── ts_technologies.xlsx
│   └── bd_technologies.csv
├── output/
│   ├── master_catalogue.csv
│   └── internal_duplicates.csv
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── cleaner.py
│   ├── deduper.py
│   ├── config.py
│   └── exploration.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Approach & Deduplication Strategy

### 1. Data Loading

- All input files in the `inputs/` directory are automatically loaded.
- Supports both `.csv` and `.xlsx` formats.

### 2. Cleaning & Standardization

- Column names are renamed to a consistent schema for merging.
- Text fields are normalized:
  - Lowercased
  - Trimmed
  - Non-ASCII characters removed
- Product names are cleaned by removing model numbers and trailing codes.
- Only relevant columns are retained:
  - `product_name`
  - `description`
  - `category`
  - `source_url`

### 3. Normalization & Blocking

#### String Normalization

- Product names are transformed into normalized “keys”:
  - Alphanumeric only
  - Lowercase
  - Punctuation removed

#### Blocking

- Products are grouped by the **first letter** of their normalized key.
- This drastically reduces the number of comparisons by filtering out irrelevant matches.
- **Performance Impact**: Blocking roughly halves the processing time for large datasets.

### 4. Fuzzy Deduplication

#### Matching Strategy

- Within each block, new records are compared to the master catalogue using `RapidFuzz`'s `token_sort_ratio`.

#### Threshold Tuning

- Thresholds between `80–90` were tested.
- **Final threshold: 85**, chosen for the best trade-off between:
  - False positives (wrong merges)
  - False negatives (missed matches)
- The threshold can be adjusted in `src/config.py` via the `THRESH` variable.

### 5. Merging

- Only non-duplicates are added to the master catalogue.
- Each product appears only once to maintain uniqueness.

---

## Blocking & Performance

- **Without blocking**: Deduplication has quadratic complexity (very slow for large data).
- **With blocking**: Runtime improved by ~50% on real datasets.
- The pipeline is now suitable for **tens of thousands** of records on standard hardware.

---

### 6. Outputs

When you run `main.py`, the pipeline generates two output files in the `output/` directory:

- `output/master_catalogue.csv`  
  A deduplicated, merged catalogue containing all unique product entries from all sources.

- `output/internal_duplicates.csv`  
  A list of possible internal duplicates — product name pairs that appear highly similar.

### Internal Duplicate Detection

- After the primary deduplication process, the pipeline performs a **secondary scan** using Python’s `SequenceMatcher`.
- This identifies **residual duplicates** that may not have been caught through fuzzy matching.
- The results are saved to:
  
  ```
  output/internal_duplicates.csv
  ```

- This file is intended for **manual review**, allowing human validation of:
  - Near-duplicates missed by automated matching
  - Inconsistencies in product naming

---

## Assumptions and Limitations

### Assumptions

- Primary matching is based on **normalized product names**.
- Metadata fields like description, category, and source URL are used for merging but not for deduplication.
- Blocking by the first character is sufficient to balance speed and accuracy.
- Input files are only in ```.csv``` and ```.xlsx``` format

### Limitations

- The current strategy uses only **one blocking method** (first-letter); more advanced methods (e.g., multi-character, phonetic blocking) can be implemented.
- Incomplete or poorly formatted product names can affect accuracy.
- The approach relies on **string similarity**, not semantic understanding.
- Very large files (**>100MB**) are not tracked by Git due to GitHub limitations.

---

## Handling Large Files

- Files such as: inputs/bd_technologies.csv (>100MB) are not committed to the repository.
- These files are **excluded via `.gitignore`** to comply with GitHub’s file size policies.
