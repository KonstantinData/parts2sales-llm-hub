# generate_prompt_from_feedback.py

"""
Single-use script to generate an improved prompt YAML using OpenAI,
based on an original YAML prompt and a JSON-format feedback report.
"""

import argparse
import openai
import os
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_improved_prompt(prompt_file: Path, feedback_file: Path, output_file: Path):
    prompt_text = prompt_file.read_text(encoding="utf-8")
    feedback_text = feedback_file.read_text(encoding="utf-8")

    improvement_prompt = f"""
Please improve the following YAML prompt based on the feedback below.
Focus on clarity, structure, robustness, LLM suitability, and include concrete examples where appropriate.

# Feedback (JSON):
{feedback_text}

# Original Prompt:
{prompt_text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an experienced prompt engineer."},
            {"role": "user", "content": improvement_prompt},
        ],
    )

    improved_prompt = response.choices[0].message.content.strip()
    output_file.write_text(improved_prompt, encoding="utf-8")
    print(f"✅ Improved prompt saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate improved prompt file from feedback"
    )
    parser.add_argument(
        "--prompt", type=str, required=True, help="Path to the original YAML file"
    )
    parser.add_argument(
        "--feedback", type=str, required=True, help="Path to the JSON feedback file"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Destination path for the new YAML file",
    )
    args = parser.parse_args()

    generate_improved_prompt(Path(args.prompt), Path(args.feedback), Path(args.output))


if __name__ == "__main__":
    main()
