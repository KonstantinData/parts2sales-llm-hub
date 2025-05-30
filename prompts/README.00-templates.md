# 🧱 Prompt Templates

This folder defines **abstract, reusable YAML prompt templates** for each supported task. Templates act as design-time blueprints — not executable prompts.

## Purpose
- Enable consistent structure across prompt development
- Enforce common formatting and constraint conventions
- Serve as base layer for deriving production-ready prompts

## Structure
Each template includes:
- `id`: logical task identifier
- `description`: explanation of template use
- `role`: a role-based system prompt (with instruction placeholder)
- `objective`: explanation of the extraction/classification goal
- `input_format`: string or JSON schema description of expected input
- `output_format`: output JSON schema or example
- `constraints`: hard logic and formatting rules to follow

## Rules
- No hardcoded product, brand, or model data
- No inline examples inside the `role` or `objective` fields
- No use of model-specific tokens (e.g. ChatGPT formatting)

## Notes
This layer is **CI-skipped** — it does not run in pipelines until promoted to `02-production/`.