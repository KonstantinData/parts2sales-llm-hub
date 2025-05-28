# validate_prompt_quality_de.py

# ------------------------------------------

# Purpose:
# Perform detailed quality checks on German LLM prompts.

# Goals:
# - Use grammar validation (language_tool_python)
# - Apply idiomatic, lexical, structural and tone checks

# Use Cases:
# - Used by CLI tools and test scripts to validate prompt quality

import language_tool_python
from prompt_quality.languages import lang_de


# Validate German prompt using grammar and heuristics
# ---------------------------------------------------
def validate_prompt_de(prompt_text: str) -> dict:
    tool = language_tool_python.LanguageTool("de")

    # Grammar check via LanguageTool
    def grammar_is_valid(text):
        return len(tool.check(text)) == 0

    # Combined check: grammar + clarity
    def no_structural_drift(text):
        return grammar_is_valid(text) and lang_de.is_actionable(text)

    # Quality evaluation result structure
    results = {
        "grammar_check": grammar_is_valid(prompt_text),
        "idiomatic_check": lang_de.has_idiom(prompt_text),
        "task_clarity": lang_de.is_actionable(prompt_text),
        "structure_check": lang_de.has_structure(prompt_text),
        "lexical_fit": not lang_de.violates_lexical_rules(prompt_text),
        "tone_check": not lang_de.has_tone_issue(prompt_text),
        "translation_integrity": no_structural_drift(prompt_text),
    }

    tool.close()
    return results
