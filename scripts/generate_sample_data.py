"""
generate_sample_data.py

Extracts columns (even with various spellings/capitalizations) from an Excel file to a normalized JSON file.
- Uses both mapping-lists (hard mapping) and fuzzy matching for maximum robustness.

USAGE:
    rye run python src/scripts/generate_sample_data.py --file "data/raw/sample.xlsx" --out "data/processed/sample_data.json"

REQUIREMENTS:
    pip install pandas openpyxl rapidfuzz

Author: Liquisto LLM Prompt Engineering, 2024
"""

import argparse
import pandas as pd
import json
import sys
from rapidfuzz import fuzz

# ---- Configuration ----

PART_NUMBER_KEYS = [
    "manufacturer part number",
    "part number",
    "part_number",
    "partnumber",
    "manufacturer number",
    "manufacturer_number",
    "manufacturer no",
    "artikelnummer",
]
TITLE_KEYS = ["title", "product title", "name", "product name"]
MANUFACTURER_KEYS = ["manufacturer", "brand", "maker", "produzent", "hersteller"]
FUZZY_THRESHOLD = 85  # similarity threshold (0-100)

# ---- Core Logic ----


def find_column_robust(df_columns, possible_keys, fuzzy_threshold=FUZZY_THRESHOLD):
    # 1. Hard mapping
    for key in possible_keys:
        for col in df_columns:
            if col.strip().lower() == key.strip().lower():
                return col
    # 2. Fuzzy matching
    for key in possible_keys:
        for col in df_columns:
            if fuzz.ratio(col.lower(), key.lower()) >= fuzzy_threshold:
                return col
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Extract columns from Excel and output as normalized JSON."
    )
    parser.add_argument("--file", required=True, help="Input Excel file path")
    parser.add_argument("--out", default="output.json", help="Output JSON file path")
    args = parser.parse_args()

    try:
        df = pd.read_excel(args.file)
    except Exception as e:
        print(f"ERROR: Could not read Excel file: {e}")
        sys.exit(1)

    cols = list(df.columns)
    col_part = find_column_robust(cols, PART_NUMBER_KEYS)
    col_title = find_column_robust(cols, TITLE_KEYS)
    col_manuf = find_column_robust(cols, MANUFACTURER_KEYS)

    # Logging for missing columns
    print("COLUMN MATCHING RESULT:")
    print(f"  part_number:    {col_part if col_part else 'MISSING!'}")
    print(f"  title:          {col_title if col_title else 'MISSING!'}")
    print(f"  manufacturer:   {col_manuf if col_manuf else 'MISSING!'}")

    if not all([col_part, col_title, col_manuf]):
        print(
            "\nERROR: One or more required columns were not found! Check your input file and column names."
        )
        sys.exit(2)

    records = []
    for idx, row in df.iterrows():
        record = {
            "part_number": (
                str(row[col_part]).strip() if pd.notna(row[col_part]) else ""
            ),
            "title": str(row[col_title]).strip() if pd.notna(row[col_title]) else "",
            "manufacturer": (
                str(row[col_manuf]).strip() if pd.notna(row[col_manuf]) else ""
            ),
        }
        records.append(record)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"\nSUCCESS: Extracted {len(records)} records to '{args.out}'")


if __name__ == "__main__":
    main()
