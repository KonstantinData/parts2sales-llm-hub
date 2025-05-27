"""
validate_output.py

Validates the structure of the final combined evaluation output file.

Usage:
    python scripts/validate_output.py evals/evaluation_output_YYYYMMDD_HHMMSS.json

Checks:
- Required top-level keys: feature_determination, use_case_determination, industry_classification
- Ensures each section is a list of dicts with required subfields
- Generates a summary report with error counts and samples
"""

import sys
import json
from pathlib import Path
from datetime import datetime

SECTIONS = [
    "feature_determination",
    "use_case_determination",
    "industry_classification",
]
REQUIRED_FIELDS = ["input", "actual"]


def validate_entry(entry: dict) -> list:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"missing field: {field}")
        elif entry[field] in (None, "", [], {}):
            errors.append(f"empty content: {field}")
    return errors


def validate_section(name: str, entries: list) -> dict:
    section_errors = []
    for i, entry in enumerate(entries):
        entry_errors = validate_entry(entry)
        if entry_errors:
            section_errors.append({"index": i, "errors": entry_errors})
    return {
        "section": name,
        "total": len(entries),
        "invalid": len(section_errors),
        "errors": section_errors[:5],
    }


def validate_file(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Top-level structure must be a dictionary.")

    reports = []
    for section in SECTIONS:
        entries = data.get(section, [])
        if not isinstance(entries, list):
            raise ValueError(f"{section} must be a list.")
        reports.append(validate_section(section, entries))

    return {
        "source_file": path.name,
        "timestamp": datetime.utcnow().isoformat(),
        "reports": reports,
    }


def save_report(report: dict, output_dir: Path):
    suffix = report["source_file"].replace("evaluation_output_", "")
    out_path = output_dir / f"validation_report_{suffix}"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"🧾 Validation report written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_output.py path/to/evaluation_output_*.json")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    try:
        report = validate_file(path)
        for r in report["reports"]:
            print(
                f"{r['section']}: {r['total'] - r['invalid']} valid / {r['total']} total"
            )
            if r["invalid"]:
                print(f"❌ {r['invalid']} invalid entries in {r['section']}")
        save_report(report, path.parent)
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)
