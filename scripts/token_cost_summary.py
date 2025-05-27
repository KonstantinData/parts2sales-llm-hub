# token_cost_summary.py
# ------------------------------------------
# Purpose:
#   Aggregate and summarize token usage and costs across evaluation stages
# Output:
#   Writes evals/token_costs_summary.json with total token counts and cost breakdown

import json
from pathlib import Path

# Input and output file paths
TOKEN_COST_FILE = Path("evals/token_costs.json")
SUMMARY_FILE = Path("evals/token_costs_summary.json")


# Function to read and summarize token data
def summarize_token_costs():
    if not TOKEN_COST_FILE.exists():
        raise FileNotFoundError("token_costs.json not found.")

    # Load token cost data
    with open(TOKEN_COST_FILE, encoding="utf-8") as f:
        costs = json.load(f)

    # Aggregate total token counts and cost
    total_input = sum(x["input_tokens"] for x in costs.values())
    total_output = sum(x["output_tokens"] for x in costs.values())
    total_cost = round(sum(x["total_cost"] for x in costs.values()), 4)

    # Build summary structure
    summary = {
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost_usd": total_cost,
    }

    # Write summary to file
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"📊 Token summary written to {SUMMARY_FILE}")


# Entry point for script execution
if __name__ == "__main__":
    summarize_token_costs()
