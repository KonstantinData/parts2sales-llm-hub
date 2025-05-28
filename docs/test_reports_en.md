# Types of Test Reports and Their Meaning (English)

This overview is aimed at both technical and non-technical readers and explains which types of test reports make sense in the project context, how they are generated, and what their benefits are in the CI/CD process.

## 📄 1. JUnit XML Report

**Type:** Structured XML test report
**Generated via:** `pytest --junitxml=tests/workflow/junit.xml`
**Purpose:** Standard format for automated evaluation in CI systems (e.g., GitHub Actions, Jenkins)
**Benefits:**
- CI systems immediately detect which tests failed
- Base for visual dashboards or test badges
- Enables automatic regression detection

---

## 📈 2. Coverage Report

**Type:** Code coverage report
**Generated via:** `pytest --cov=src --cov-report=xml:coverage.xml`
**Purpose:** Shows how much of the code is covered by tests
**Benefits:**
- Identifies blind spots in the test suite
- Metric for test quality
- Decision basis for refactorings

---

## 📊 3. HTML Coverage Report

**Type:** Human-readable HTML report of code coverage
**Generated via:** `pytest --cov=src --cov-report=html`
**Purpose:** Graphical display of coverage per file, function, and line
**Benefits:**
- Easily understandable by developers
- Useful for pair reviews or audits

---

## 📁 Storage Location & Upload via CI

All reports should be stored under `tests/workflow/`.

In `.github/workflows/ci.yml`:

```yaml
- name: 📊 Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: tests/workflow/
```

**Note:** Reports are only uploaded if they exist — this must be ensured through prior test runs.