# Template Workflow – Detaillierte Prozessbeschreibung (Deutsch)

## Übersicht

Dieses Dokument beschreibt den vollständigen Ablauf der Template-Validierung, Evaluation und Freigabe des Promptsystems auf Level-1.

## Ablaufbeschreibung

1. **Prompt Validierung #1**
   - Validierungsziele: Grammatik, Struktur, Stil, Idiomatik
   - Eingesetzte Tools:
     - `validate_prompt_quality_cli.py`
     - `validate_metadata_files.py`
     - `validate_prompt_quality_de.py`, `validate_prompt_quality_en.py`
     - `lang_de.py`, `lang_en.py`

2. **Execution**
   - Anwendung des Templates auf echte Eingabedaten
   - Generierung eines `determined_features.json`

3. **Validierung #2**
   - Schema-Validierung der generierten Outputs
   - Prüfung: JSON-Gültigkeit, Schlüssel vorhanden, Struktur korrekt

4. **Scoring**
   - Gewichtete Bewertung der Strukturqualität
   - Markierung von Abweichungen

5. **Prompt Update**
   - Iteratives Refactoring auf Basis der Scoring-Ergebnisse

6. **Freigabe**
   - Promotion in Layer `02-products`
   - Speichern als `feature_determination_latest.yaml`

7. **Weiterverarbeitung**
   - Anwendung des gleichen Prozesses auf weitere Templates:
     - `use_case_determination_template.yaml`
     - `industry_classification_template.yaml`
     - ...

## Ziel

Der Prozess stellt sicher, dass Prompts sowohl qualitativ hochwertig als auch strukturell robust und evaluierbar sind.