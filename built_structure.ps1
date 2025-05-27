# built_structure.ps1 (safe version for root-level execution)
# Run this only inside your target Git repo folder (e.g. parts2sales-llm-hub)

$folders = @(
    ".github/workflows",
    "cli",
    "data",
    "docs",
    "evals",
    "infra",
    "prompts",
    "prompt_quality",
    "scripts",
    "static",
    "templates",
    "tests"
)

$files = @(
    "README.md",
    "LICENSE.txt",
    "pyproject.toml",
    "prompt_registry.yaml"
)

# Create folders and .gitkeep
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    New-Item -ItemType File -Path (Join-Path $folder ".gitkeep") -Force | Out-Null
}

# Create top-level files
foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force | Out-Null
}

# Write basic README content
Set-Content -Path "README.md" -Value "# parts2sales-llm-hub`nModular LLM hub for Parts2Sales applications."

Write-Host "Project structure created in current directory."
