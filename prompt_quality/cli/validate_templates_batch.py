import os
import yaml
from validate_prompt_quality_cli import validate_prompt, detect_language, log_results

TEMPLATE_DIR = "prompts/00-templates"


def run_template_validation():
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith("template.yaml"):
            filepath = os.path.join(TEMPLATE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                prompt = data.get("prompt", "")
                if not prompt:
                    print(f"⚠️ No 'prompt' field in {filename}")
                    continue
                language = detect_language(prompt)
                results, explanation_map = validate_prompt(prompt, language)
                log_results(prompt, language, results, explanation_map, show_score=True)


if __name__ == "__main__":
    print("🔍 Validating prompt in template.yaml...")
    run_template_validation()
