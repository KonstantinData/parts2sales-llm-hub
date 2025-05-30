# prompt_validation_workflow_live.py

import os
import argparse
import subprocess
import shutil
import json
import sys
from pathlib import Path
from typing import List
from datetime import datetime
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Load API key and initialize client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set in environment.")
client = OpenAI(api_key=api_key)

# Setup logging
logging.basicConfig(
    filename="prompt_validation_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

OUTPUT_DIR = Path("prompt_quality/output_prompt_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def validate_prompt_quality(prompt_path: Path) -> float:
    print(f"📊 Starting quality check #1 for {prompt_path.name} via prompt_quality_cli")
    validate_script = (
        Path(__file__).parent
        / "prompt_quality"
        / "cli"
        / "validate_prompt_quality_cli.py"
    )

    if not validate_script.exists():
        raise FileNotFoundError(f"CLI-Script nicht gefunden: {validate_script}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent)

    result = subprocess.run(
        [
            sys.executable,
            str(validate_script.resolve()),
            "--file",
            str(prompt_path),
            "--json",
        ],
        capture_output=True,
        text=True,
        env=env,
    )

    logging.debug("Validation stdout: %s", result.stdout)
    logging.debug("Validation stderr: %s", result.stderr)

    if result.returncode != 0:
        print("❌ Error during execution of prompt_quality_cli")
        print(result.stderr)
        logging.error("Subprocess failed with return code %d", result.returncode)
        return 0.0, None

    try:
        data = json.loads(result.stdout)
        score = data.get("score", 0.0)
        print(f"➡️ Quality score: {score}")

        timestamp = datetime.now().strftime("%y%m%d_%I-%M_%p")
        file_stem = prompt_path.stem
        out_name = f"{file_stem}.{timestamp}.json"
        feedback_path = OUTPUT_DIR / out_name
        feedback_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        return score, feedback_path
    except Exception as e:
        print(f"❌ Error parsing output: {e}")
        logging.exception("Failed to parse JSON output")
        return 0.0, None


def generate_new_prompt_version(
    old_prompt: Path, feedback_json: Path, new_version: Path
):
    if feedback_json is None or not feedback_json.exists():
        print("❌ No feedback file available – skipping OpenAI prompt generation.")
        logging.warning("Feedback file missing or invalid: %s", feedback_json)
        return

    print(f"🨭 Improving via OpenAI → {new_version.name}")
    feedback = feedback_json.read_text()
    prompt_text = old_prompt.read_text()

    improvement_prompt = f"""
You are an expert prompt engineer.

Your task is to revise and improve the following YAML prompt based on the quality assessment feedback.

🔍 Requirements:
- Fix any issues reported in the feedback
- Improve clarity, structural logic, and consistency
- Enhance LLM compatibility (avoid idioms, ambiguities, vague slots)
- Ensure formal and precise tone
- Keep the original prompt intention intact

🗓 Feedback (JSON format):
{feedback}

📄 Original YAML prompt:
{prompt_text}

Please return only the improved YAML prompt – no explanations or comments.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an experienced prompt engineer."},
            {"role": "user", "content": improvement_prompt},
        ],
    )

    improved_yaml = response.choices[0].message.content.strip()
    new_version.write_text(improved_yaml)
    print(f"📁 New version saved: {new_version}")
    logging.info("New prompt version saved to %s", new_version)


def execute_prompt(prompt_path: Path) -> Path:
    print(f"⚙️ Executing prompt {prompt_path.name} (placeholder)")
    return Path("evals/output_example.json")


def validate_output(result_path: Path) -> bool:
    print(f"🔍 Validating results in {result_path.name}")
    return True


def score_output(result_path: Path) -> float:
    print(f"📈 Calculating score for {result_path.name} (placeholder) → 0.85")
    return 0.85


def workflow_for_prompt(prompt_path: Path, score_threshold: float = 0.9):
    version = 1
    max_iterations = 3
    base_name = prompt_path.stem.replace("_v1", "")
    parent_dir = prompt_path.parent

    while version <= max_iterations:
        print(f"\n--- Iteration v{version} for {prompt_path.name} ---")

        score, feedback_path = validate_prompt_quality(prompt_path)
        if score >= score_threshold:
            print(f"✅ Score target reached (Score: {score})")
            final_path = parent_dir / f"{base_name}_final.yaml"
            shutil.copyfile(prompt_path, final_path)
            print(f"📂 Saved as final version: {final_path.name}")
            break

        if version == max_iterations:
            print("⛔️ Maximum number of iterations reached. Process aborted.")
            break

        new_version = parent_dir / f"{base_name}_v{version+1}.yaml"
        generate_new_prompt_version(prompt_path, feedback_path, new_version)

        prompt_path = new_version
        version += 1


def main():
    parser = argparse.ArgumentParser(description="Prompt Validation Workflow")
    parser.add_argument("--file", type=str, help="Path to the prompt file")
    parser.add_argument(
        "--all", action="store_true", help="Check all prompts sequentially"
    )
    args = parser.parse_args()

    if args.all:
        prompts = [
            "feature_determination_v1.yaml",
            "use_case_determination_v1.yaml",
            "industry_classification_v1.yaml",
            "company_assignment_v1.yaml",
            "contact_assignment_v1.yaml",
        ]
        base_path = Path("prompts/00-templates")

        for prompt_file in prompts:
            prompt_path = base_path / prompt_file
            workflow_for_prompt(prompt_path)

    elif args.file:
        prompt_path = Path(args.file)
        if not prompt_path.exists():
            print(f"❌ File not found: {prompt_path}")
            return
        workflow_for_prompt(prompt_path)
    else:
        print("⚠️ Please provide either --file or --all.")


if __name__ == "__main__":
    main()
