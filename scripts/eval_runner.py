# eval_runner.py
# ------------------------------------------
# Purpose:
#   Evaluate a filled prompt template against sample inputs using OpenAI
# Goals:
#   - Load production prompt and input data
#   - Use OpenAI's API to execute and store results
#   - Support evaluation from uploaded_input.json for _latest tasks

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import yaml
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables for OpenAI API key
load_dotenv()
client = OpenAI()

# Define folders for production prompts and examples
PROMPT_DIR = Path("prompts/02-production")
EXAMPLES_DIR = Path("prompts/01-examples")


# Load YAML-based prompt configuration
def load_prompt_yaml(task_id: str) -> dict:
    """
    Loads a YAML file for the specified task from the production prompt folder.
    E.g., task_id="usecase_extraction" loads prompts/02-production/usecase_extraction.yaml
    """
    path = PROMPT_DIR / f"{task_id}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# Load example input data
def load_json_examples(task_id: str) -> List[Dict]:
    """
    Loads evaluation inputs. If task_id ends with '_latest', pull from uploaded_input.json.
    Otherwise, load example files from prompts/01-examples/{task_id}/
    """
    if task_id.endswith("_latest"):
        uploaded_path = Path("evals") / "uploaded_input.json"
        with open(uploaded_path, encoding="utf-8") as f:
            records = json.load(f)
        return [{"input": record, "expected": {}} for record in records]

    # Default: load example files
    dir_path = EXAMPLES_DIR / task_id
    examples = []
    for file in dir_path.glob("*.json"):
        with open(file, encoding="utf-8") as f:
            examples.append(json.load(f))
    return examples


# Call OpenAI using client.responses.create()
def call_model(prompt: dict, input_data: dict) -> dict:
    """
    Combines instruction + input, sends to OpenAI, returns the model result.
    """
    instruction = prompt.get("instruction", "")
    combined = f"{instruction}\n\n{json.dumps(input_data)}"
    response = client.responses.create(model="gpt-4.1", input=combined)
    return {"result": response.output_text.strip()}


# Evaluate all examples and save result
def evaluate(task_id: str) -> None:
    """
    Runs all input samples for the given task prompt.
    Collects and stores actual model outputs with expected results.
    """
    prompt_def = load_prompt_yaml(task_id)
    examples = load_json_examples(task_id)

    results = []
    for ex in examples:
        input_data = ex["input"]
        expected = ex.get("expected", {})
        actual = call_model(prompt_def, input_data)

        results.append({"input": input_data, "expected": expected, "actual": actual})

    timestamp = datetime.utcnow().isoformat()
    out_path = Path("evals") / f"{task_id}_{timestamp}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Evaluation saved to {out_path}")


# CLI entry point
def main():
    """
    Parses command-line input (task_id) and runs the evaluation for that prompt.
    """
    parser = argparse.ArgumentParser(
        description="Evaluate a prompt against input examples using OpenAI"
    )
    parser.add_argument("task_id", help="Name of the task prompt (without extension)")
    args = parser.parse_args()
    evaluate(args.task_id)


# Run main() if script is executed directly
if __name__ == "__main__":
    main()
