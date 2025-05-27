# Erstelle ein korrektes PowerShell-Skript mit ASCII-Baumstruktur-Ausgabe in eine Datei
script_content = '''
$basePath = Get-Location
$outputFile = "project_structure.txt"

Function Get-Tree {
    param (
        [string]$path,
        [int]$indent = 0
    )

    $entries = Get-ChildItem -Path $path | Where-Object { $_.Name -ne ".git" -and $_.Name -ne ".venv" }

    foreach ($entry in $entries) {
        $prefix = "│  " * $indent + "├─ " + $entry.Name
        Add-Content -Path $outputFile -Value $prefix

        if ($entry.PSIsContainer) {
            Get-Tree -path $entry.FullName -indent ($indent + 1)
        }
    }
}

# Schreibe Überschrift und leere vorherige Datei
"Project Structure:" | Set-Content -Path $outputFile
"" | Add-Content -Path $outputFile

# Starte mit dem aktuellen Verzeichnis
Get-Tree -path $basePath
'''

script_path = "/mnt/data/print_structure_ascii.ps1"
with open(script_path, "w", encoding="utf-8") as f:
    f.write(script_content)

script_path
