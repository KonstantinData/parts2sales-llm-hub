# PowerShell Script: run_generate_sample_data.ps1
# Run this from the project root (where pyproject.toml is)

Write-Host "=== Excel to JSON Extraction via Python & Rye ===`n"

# Eingabe: Excel-Datei auswählen
$excelPath = Read-Host "Enter path to Excel file (e.g. data/raw/products.xlsx)"

# Eingabe: JSON-Output-Datei wählen
$outputPath = Read-Host "Enter path for output JSON file (e.g. data/processed/products.json)"

# Optional: Check, ob Excel-Datei existiert
if (!(Test-Path $excelPath)) {
    Write-Host "`nERROR: Input file does not exist!`n" -ForegroundColor Red
    exit 1
}

# Construct Python command
$pycmd = "rye run python scripts/generate_sample_data.py --file `"$excelPath`" --out `"$outputPath`""

Write-Host "`nRunning:"
Write-Host $pycmd -ForegroundColor Yellow

# Ausführen
Invoke-Expression $pycmd

Write-Host "`nFertig! (Siehe Output above.)"
