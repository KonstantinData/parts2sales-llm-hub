
# 🔁 Iterativer Prompt-Validierungsprozess (ausführlich)

Diese Dokumentation beschreibt den vollständigen Workflow zur schrittweisen Validierung von LLM-Prompts. Ziel ist es, stabile und evaluierte Prompt-Vorlagen für den Produktionseinsatz zu generieren.

---

## 📋 Ablaufübersicht mit Stationserläuterung

### 1. Start: `feature_determination_v1.yaml`
Der erste Prompt zur Bestimmung von Merkmalen wird getestet. Die Datei befindet sich in `prompts/00-templates/`.

- **Qualitätsprüfung #1:** Es wird geprüft, ob der Prompt strukturell korrekt, sprachlich sauber und formal vollständig ist.
- **Ausführung:** Der Prompt wird mit Testdaten (z. B. Produktbeschreibungen) ausgeführt.
- **Qualitätsprüfung #2:** Die JSON-Ergebnisse werden hinsichtlich Schema, Inhalt, Vollständigkeit und Quellen geprüft.
- **Iteration:** Falls das Ergebnis nicht den Score-Vorgaben entspricht, wird ein neuer Prompt (v2, v3, ...) erstellt und erneut validiert.
- **Abschluss:** Erfolgreiche Version wird als `feature_determination_final.yaml` markiert.

### 2. Nächster Prompt: `use_case_determination_v1.yaml`
- Identisch strukturierter Prozess zur Erkennung von Anwendungsfällen.
- Ziel: Robust validierte Erkennung von Use Cases pro Input-Einheit.

### 3. Dritter Prompt: `industry_classification_v1.yaml`
- Fokus auf Branchenzuordnung.
- Ergebnisse müssen klar, standardisiert und in validem JSON-Format vorliegen.

### 4. Vierter Prompt: `company_assignment_v1.yaml`
- Firmenzuordnung anhand von Kontextdaten.
- Hohe Präzision erforderlich (validierte Zuweisung durch externe Referenz oder Matching).

### 5. Letzter Prompt: `contact_assignment_v1.yaml`
- Ziel: Extraktion und Zuordnung von Kontaktpersonen.
- Hier ist oft ein Multi-Step Prompt erforderlich (z. B. Kontextverarbeitung + Rollenidentifikation).

---

## 🔁 Iterationslogik

- Jeder Prompt folgt diesem Ablauf:
  - **Qualitätsprüfung #1**: YAML-Validierung + Sprachprüfung
  - **Prompt-Ausführung**: Mit realen Beispieldaten
  - **Qualitätsprüfung #2**: Ergebnisprüfung + JSON-Schema-Abgleich
  - **Feedback & Iteration**: Scoring-basierte Prompt-Optimierung
  - **Finalisierung**: `*_final.yaml` bei Zielerreichung

---

## 💾 Ergebnisformate

- **Input:** `.csv`, `.xlsx`, Google Sheets
- **Output:** JSON-Dateien (`*_vX.json`)
- **Scoring & Logs:** `evals/`, `prompt_quality/logs/`, `reference_examples/`

---

## 🏁 Ziel

Ein wiederholbarer, versionierter Prompt-Workflow mit klarer Freigabeentscheidung nach objektiven Evaluierungskriterien.
