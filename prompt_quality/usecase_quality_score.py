# usecase\_quality\_score.py

# ------------------------------------------

# Purpose:

# Compute a numeric quality score for prompts based on the number of violations.

# Goals:

# - Translate qualitative prompt feedback into a quantifiable score (0–100)

# - Provide consistent, automatable scoring for CI checks and dashboards

# Use Cases:

# - CLI or automated pipelines that require simple numeric pass/fail metrics

# Score calculator based on number of rule violations

# ---------------------------------------------------

def score\_validated\_row(row: dict) -> int:
violations = row\.get("violations", \[])
num\_checks = 7  # total expected keys in validation output
failed = len(violations)
score = round((1 - failed / num\_checks) \* 100)
return max(score, 0)
