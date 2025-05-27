# validate\_prompt\_quality\_cli.py

# ---------------------------------

# Purpose:

# This script provides a command-line interface (CLI) to validate LLM prompts

# for linguistic and structural quality in English or German.

# Goals:

# - Evaluate prompts based on grammar, idiomatic use, tone, structure, etc.

# - Output clear pass/fail criteria and detailed explanations

# - Optionally compute a numeric quality score (0–100) based on violations

# Use Cases:

# - Manual or automated prompt audits before moving to production

# - CI pipelines, editor integrations, or developer-side checks

import os
from datetime import datetime
from langdetect import detect
from colorama import init, Fore, Style
import argparse
import sys

# Ensure parent module paths are available

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(**file**), "..")))

from validate\_prompt\_quality\_en import validate\_prompt\_en
from validate\_prompt\_quality\_de import validate\_prompt\_de
import lang\_en
import lang\_de
from usecase\_quality\_score import score\_validated\_row

# Initialize color formatting for console output

init(autoreset=True)

LOG\_DIR = os.path.join("prompt\_quality", "logs")
os.makedirs(LOG\_DIR, exist\_ok=True)

# Detects language using langdetect or defaults to English

# --------------------------------------------------------

def detect\_language(text):
try:
lang = detect(text)
return "de" if lang.startswith("de") else "en"
except Exception:
return "en"

# Executes quality checks using language-specific logic

# -----------------------------------------------------

def validate\_prompt(prompt, language):
if language == "en":
results = validate\_prompt\_en(prompt)
explanation\_map = lang\_en.explanations()
else:
results = validate\_prompt\_de(prompt)
explanation\_map = lang\_de.explanations()
return results, explanation\_map

# Outputs results to console and logs them to file

# ------------------------------------------------

def log\_results(prompt, language, results, explanation\_map, show\_score):
timestamp = datetime.now().strftime("%Y-%m-%d\_%H-%M-%S")
log\_path = os.path.join(LOG\_DIR, f"prompt\_check\_{language}\_{timestamp}.txt")

```
with open(log_path, "w", encoding="utf-8") as log:
    log.write(f"Prompt: {prompt}\n\n")
    print(f"\n{Style.BRIGHT}Prompt: {prompt}\n")
    violations = []
    for check, passed in results.items():
        status = f"{Fore.GREEN}✅" if passed else f"{Fore.RED}❌"
        explanation = explanation_map.get(check, "No explanation available.")
        line = f"{check}: {status}"
        print(line)
        log.write(f"{check}: {'PASS' if passed else 'FAIL'}\n")
        if not passed:
            print(f"  → {explanation}")
            log.write(f"  → {explanation}\n")
            violations.append(check)

    if show_score:
        score = score_validated_row({"violations": violations})
        print(f"\n🔢 Score: {score}/100")
        log.write(f"\nScore: {score}/100\n")
```

# CLI entry point

# ---------------

def main():
parser = argparse.ArgumentParser(description="Prompt Quality Checker (EN/DE)")
parser.add\_argument("--lang", help="Language code: en or de")
parser.add\_argument("--prompt", help="Prompt string to validate")
parser.add\_argument("--score", action="store\_true", help="Display numerical score based on violations")
args = parser.parse\_args()

```
print("\n🧪 Prompt Quality Checker (EN/DE)")
print("----------------------------------")

prompt = args.prompt or input("\nEnter the prompt text:\n> ").strip()
language = args.lang or detect_language(prompt)

if language not in ["en", "de"]:
    print(f"{Fore.RED}❌ Unsupported language.")
    return

results, explanation_map = validate_prompt(prompt, language)
log_results(prompt, language, results, explanation_map, args.score)
```

if **name** == "**main**":
main()
