
# 🔁 Iterative Prompt Validation Process (Detailed)

This document outlines the full workflow for validating LLM prompts step-by-step. The goal is to develop robust, production-ready prompt templates through repeatable evaluations.

---

## 📋 Process Overview with Station Descriptions

### 1. Start: `feature_determination_v1.yaml`
The first prompt focuses on feature extraction. Located in `prompts/00-templates/`.

- **Quality Check #1:** Structure, metadata, and language are validated.
- **Execution:** The prompt is run using realistic input data (e.g. product specs).
- **Quality Check #2:** Output is validated against JSON schema, content checks, completeness, and source traceability.
- **Iteration:** If the result fails the scoring threshold, new versions (v2, v3...) are created and revalidated.
- **Completion:** The approved version is marked as `feature_determination_final.yaml`.

### 2. Next Prompt: `use_case_determination_v1.yaml`
- Structured identically, targeting use case recognition.
- Must meet output standards and scoring goals.

### 3. Third Prompt: `industry_classification_v1.yaml`
- Classifies into industries.
- Standardized and schema-compliant outputs expected.

### 4. Fourth Prompt: `company_assignment_v1.yaml`
- Assigns inputs to known companies.
- Requires precision and verification.

### 5. Final Prompt: `contact_assignment_v1.yaml`
- Extracts and links contact persons to the case.
- Often requires multistep prompting (context + role inference).

---

## 🔁 Iteration Logic

Each prompt follows this loop:
- **Quality Check #1:** YAML & language checks
- **Prompt Execution:** With actual sample data
- **Quality Check #2:** Schema and content validation
- **Feedback & Iteration:** Based on scoring logic
- **Finalization:** When target score is reached → `_final.yaml`

---

## 💾 Output Formats

- **Input:** `.csv`, `.xlsx`, Google Sheets
- **Output:** JSON files (`*_vX.json`)
- **Scoring & Logs:** `evals/`, `prompt_quality/logs/`, `reference_examples/`

---

## 🏁 Goal

A reproducible, versioned prompt engineering process with automated approval based on objective evaluation.
