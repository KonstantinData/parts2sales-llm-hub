# Testreport-Arten und ihre Bedeutung (Deutsch)

Dieser Überblick richtet sich an technische wie nicht-technische Leser:innen und erklärt, welche Arten von Testberichten im Projektkontext sinnvoll sind, wie sie erzeugt werden und welchen Nutzen sie im CI/CD-Prozess haben.

## 📄 1. JUnit XML Report

**Art:** Strukturierter XML-Testbericht
**Erzeugung:** `pytest --junitxml=tests/workflow/junit.xml`
**Zweck:** Standardformat zur automatisierten Auswertung in CI-Systemen (z. B. GitHub Actions, Jenkins)
**Nutzen:**
- CI-Systeme erkennen sofort, welche Tests fehlgeschlagen sind
- Grundlage für visuelle Dashboards oder Testabzeichen
- Ermöglicht automatische Regressionserkennung

---

## 📈 2. Coverage Report

**Art:** Testabdeckungsbericht
**Erzeugung:** `pytest --cov=src --cov-report=xml:coverage.xml`
**Zweck:** Zeigt, wie viel des Codes durch Tests abgedeckt ist
**Nutzen:**
- Identifikation von „blinden Flecken“ im Testset
- Messgröße für Testqualität
- Entscheidungsgrundlage bei Refactorings

---

## 📊 3. HTML Coverage Report

**Art:** Menschlich lesbarer HTML-Report zur Codeabdeckung
**Erzeugung:** `pytest --cov=src --cov-report=html`
**Zweck:** Grafische Darstellung der Abdeckung pro Datei, Funktion, Zeile
**Nutzen:**
- Leicht verständlich für Entwickler:innen
- Gute Grundlage für Pair Reviews oder Audits

---

## 📁 Speicherort & Upload via CI

Alle Berichte sollten unter `tests/workflow/` gespeichert werden.

In `.github/workflows/ci.yml`:

```yaml
- name: 📊 Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: tests/workflow/
```

**Hinweis:** Reports werden nur dann hochgeladen, wenn sie existieren – das muss durch vorherige Testläufe sichergestellt sein.