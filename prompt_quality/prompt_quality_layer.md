# Layer: prompt_quality/

## Purpose
Provides CLI tools and validation logic to assess the linguistic and structural quality of prompts before they move into production.

## Responsibilities

- Run quality checks on prompt grammar, tone, structure, idiomatic phrasing, and task clarity.
- Validate that templates meet internal linguistic standards (e.g. using `language_tool_python`).
- Support English (`lang_en`) and German (`lang_de`) quality benchmarks.
- Log validation results for traceability and improvement.

## Structure

```
prompt_quality/
├── lang_en.py                   # English-specific phrase/style rules
├── lang_de.py                   # German-specific phrase/style rules
├── validate_prompt_quality_en.py # Full validation logic for English prompts
├── validate_prompt_quality_de.py # Full validation logic for German prompts
├── validate_prompt_quality_cli.py # CLI tool for user-driven prompt validation
├── render_and_validate_template.py # Combines template + example → validation
├── validate_metadata_files.py   # Validates metadata against schema
├── logs/                        # Timestamped log files of validation runs
```

## Observations to Make

- Are quality failures due to prompt structure, language, or missing task cues?
- Do logs consistently show the same failed criteria across variants?
- Are the rules in `lang_en.py` and `lang_de.py` aligned with user tone and brand?

## Quality Control

- Output from CLI shows ✅/❌ per quality criterion.
- Logs are saved to `prompt_quality/logs/` with timestamps.
- Common quality flags: missing idioms, weak structure, unclear tasks.
- Use outputs to inform iterations at the template level.

## Additional Best Practices

- Ensure logs are readable and timestamped for reproducibility.
- Update `lang_*.py` modules if tone, terminology, or prompt patterns evolve.
- Use validation as part of pre-merge CI before moving templates to production.

## Strategic Relevance

This layer enforces prompt quality across the lifecycle, reducing risk of unclear LLM output and ensuring consistent tone and format across all Liquisto prompts.
