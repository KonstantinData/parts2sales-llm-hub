
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
