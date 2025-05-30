# generate_prompt_improvement.py

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_improved_prompt(prompt_path: Path, feedback_path: Path, output_path: Path):
    prompt_text = prompt_path.read_text()
    feedback_json = feedback_path.read_text()

    meta_instruction = f"""
You are an experienced prompt engineer.

Your task: Improve the YAML prompt below based on the structured feedback from a quality validation tool.

🧾 Feedback:
{feedback_json}

🧱 Original Prompt:
{prompt_text}

🎯 Your goal is to improve:
- Clarity: use precise, unambiguous wording
- Structure: ensure logical flow, steps, or blocks
- Robustness: prevent edge case failures
- LLM-compatibility: avoid idioms, vague terms, or ambiguous slots
- Formal tone and grammar: correct stylistic issues

📌 Constraints:
- Do not change the core intent of the original prompt.
- Return **only** the improved YAML content – no prose or explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an experienced prompt engineer."},
            {"role": "user", "content": meta_instruction},
        ],
    )

    improved_yaml = response.choices[0].message.content.strip()
    output_path.write_text(improved_yaml)
    print(f"✅ Improved prompt saved to: {output_path}")
