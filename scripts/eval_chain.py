"""
eval_chain.py

Purpose:
    Executes a sequence of evaluation tasks, estimates token costs, generates summaries,
    validates outputs, and uploads results to S3.

Key Functions:
    - run_eval: Executes evaluation scripts for specified tasks.
    - load_latest_result: Loads the most recent evaluation result for a given task.
    - estimate_cost: Calculates token usage and associated costs.
    - upload_to_s3: Uploads evaluation outputs to an S3 bucket.

Design Objectives:
    - Ensure modularity and clarity in processing evaluation tasks.
    - Maintain accurate tracking of token usage and costs.
    - Facilitate easy integration with cloud storage solutions.

Notable Features:
    - Dynamic file naming based on UTC timestamps.
    - Robust error handling during S3 uploads.
    - Comprehensive logging for process tracking.
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
import boto3

EVAL_DIR = Path("evals")
TOKEN_COST_FILE = EVAL_DIR / "token_costs.json"

MODEL_PRICING = {"gpt-4.1": {"input": 0.01, "output": 0.03}}


def load_latest_result(task_id: str) -> list:
    """
    Loads the most recent evaluation result for the specified task.

    Args:
        task_id (str): Identifier for the evaluation task.

    Returns:
        list: Parsed JSON data from the latest evaluation result file.

    Raises:
        FileNotFoundError: If no matching evaluation result files are found.
    """
    matching = sorted(EVAL_DIR.glob(f"{task_id}_*.json"), reverse=True)
    if not matching:
        raise FileNotFoundError(f"No evaluation result found for: {task_id}")
    selected_file = matching[0]
    print(f"📄 Selected latest result: {selected_file.name}")
    with open(selected_file, encoding="utf-8") as f:
        return json.load(f)


def run_eval(task_id: str):
    """
    Executes the evaluation script for the specified task.

    Args:
        task_id (str): Identifier for the evaluation task.
    """
    print(f"🚀 Running: {task_id}")
    subprocess.run(["python", "scripts/eval_runner.py", task_id], check=True)


def estimate_cost(results: list, model: str) -> dict:
    """
    Estimates token usage and associated costs for the evaluation results.

    Args:
        results (list): Evaluation results data.
        model (str): Model identifier used for pricing.

    Returns:
        dict: Dictionary containing token counts and cost estimations.
    """
    input_tokens = sum(len(json.dumps(x.get("input", {}))) // 4 for x in results)
    output_tokens = sum(
        len(x.get("actual", {}).get("result", "")) // 4 for x in results
    )
    pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round((input_tokens / 1000) * pricing["input"], 4),
        "output_cost": round((output_tokens / 1000) * pricing["output"], 4),
        "total_cost": round(
            (input_tokens / 1000) * pricing["input"]
            + (output_tokens / 1000) * pricing["output"],
            4,
        ),
    }


def upload_to_s3(file_path: Path, bucket: str, prefix: str = "outputs/"):
    """
    Uploads the specified file to an S3 bucket.

    Args:
        file_path (Path): Path to the file to be uploaded.
        bucket (str): S3 bucket name.
        prefix (str, optional): S3 key prefix. Defaults to "outputs/".
    """
    try:
        s3 = boto3.client("s3")
        key = f"{prefix}{file_path.name}"
        s3.upload_file(str(file_path), bucket, key)
        print(f"✅ Uploaded to S3: s3://{bucket}/{key}")
    except Exception as e:
        print(f"❌ S3 upload failed: {e}")


def main():
    """
    Main function to execute the evaluation pipeline.
    """
    cost_log = {}

    run_eval("feature_determination_latest")
    features = load_latest_result("feature_determination_latest")
    cost_log["feature_determination"] = estimate_cost(features, "gpt-4.1")

    run_eval("use_case_determination_latest")
    use_cases = load_latest_result("use_case_determination_latest")
    cost_log["use_case_determination"] = estimate_cost(use_cases, "gpt-4.1")

    run_eval("industry_classification_latest")
    industries = load_latest_result("industry_classification_latest")
    cost_log["industry_classification"] = estimate_cost(industries, "gpt-4.1")

    summary = {
        "feature_count": len(features),
        "use_case_count": len(use_cases),
        "industry_count": len(industries),
        "company_count": "skipped",
        "new_company_count": "skipped",
        "timestamp": datetime.utcnow().isoformat(),
        "total_cost_usd": round(sum(x["total_cost"] for x in cost_log.values()), 4),
    }

    summary_path = EVAL_DIR / "pipeline_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with open(TOKEN_COST_FILE, "w", encoding="utf-8") as f:
        json.dump(cost_log, f, indent=2)

    # Write final evaluation output for download
    output_filename = (
        f"evaluation_output_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_path = EVAL_DIR / output_filename

    evaluation_output = {
        "feature_determination": features,
        "use_case_determination": use_cases,
        "industry_classification": industries,
        "summary": summary,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_output, f, indent=2)
    print(f"📁 Evaluation written to {output_path.name}")

    # Validate and upload to S3
    try:
        subprocess.run(
            ["python", "scripts/validate_output.py", str(output_path)], check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Validation failed: {e}")
        return

    bucket = os.getenv("S3_OUTPUT_BUCKET", "gpt-eval-results")
    upload_to_s3(output_path, bucket)

    # Optional: run post-summary script
    try:
        print("INFO:main:✅ Running token_cost_summary.py...")
        subprocess.run(["python", "token_cost_summary.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(
            f"WARNING:main:⚠️ token_cost_summary.py failed but pipeline continues: {e}"
        )

    print("✅ Full evaluation pipeline complete.")
    print(f"📊 Summary written to {summary_path}")
    print(f"💰 Token cost breakdown written to {TOKEN_COST_FILE}")


if __name__ == "__main__":
    main()
