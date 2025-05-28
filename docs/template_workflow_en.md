# Template Workflow – Detailed Process Description (English)

## Overview

This document outlines the complete workflow for template validation, evaluation, and approval within the Level-1 prompt system.

## Process Description

1. **Prompt Validation #1**
   - Validation targets: grammar, structure, tone, idiomatic usage
   - Tools used:
     - `validate_prompt_quality_cli.py`
     - `validate_metadata_files.py`
     - `validate_prompt_quality_de.py`, `validate_prompt_quality_en.py`
     - `lang_de.py`, `lang_en.py`

2. **Execution**
   - Applying the prompt to real-world input
   - Generates `determined_features.json`

3. **Validation #2**
   - Output schema validation
   - Checks: JSON validity, required keys, structural conformity

4. **Scoring**
   - Weighted assessment of structural quality
   - Highlighting deviations and deficiencies

5. **Prompt Update**
   - Iterative refinement based on scoring results

6. **Approval**
   - Promotion to `02-products` layer
   - Saved as `feature_determination_latest.yaml`

7. **Next Prompts**
   - Apply same workflow to:
     - `use_case_determination_template.yaml`
     - `industry_classification_template.yaml`
     - ...

## Goal

This process ensures that prompts are both high-quality and structurally sound for reliable evaluation and automation.