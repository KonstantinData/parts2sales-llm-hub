# built_structure_workflow.ps1
# Ergänzt das Projektverzeichnis um eine modulare Struktur für Workflow-spezifische Komponenten

$folders = @(
    "core",            # Zentrale Steuerlogik (z. B. eval_runner, pipeline controller)
    "generators",      # Datengenerierung & PDF-Ausgabe
    "validators",      # Prompt- und Output-Validierungen
    "uploads",         # Zwischenablage für Web-Uploads
    "outputs",         # Ergebnisse als JSON, CSV, PDF
    "s3",              # optional: upload.py mit boto3
    "pdf",             # (optional) spezialisierte PDF-Renderer, Templates, Assets
    "tests/workflow"   # Unit- oder Integrationstests für Workflowteile
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        New-Item -ItemType File -Path "$folder\.gitkeep" -Force | Out-Null
    }
}

Write-Host "Workflow-specific structure has been added to the current directory."
