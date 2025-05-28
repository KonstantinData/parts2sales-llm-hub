import json
from pathlib import Path


def load_latest_output(base_path: Path) -> dict:
    files = sorted(base_path.glob("evaluation_output_*.json"), reverse=True)
    if not files:
        raise FileNotFoundError("No evaluation_output_*.json files found.")
    with open(files[0], encoding="utf-8") as f:
        return json.load(f)
