# init_rye.ps1
# Initializes a new rye-based Python environment in the current project directory

# Step 1: Initialize rye project
rye init --name parts2sales-llm-hub

# Step 2: Add core dependencies
rye add fastapi pytest ruff mypy typer jinja2 uvicorn

# Step 3: Optional dev tools
rye add --dev black pre-commit

# Step 4: Create .gitignore if not already present
if (-not (Test-Path ".gitignore")) {
    Set-Content -Path ".gitignore" -Value @"
__pycache__/
.venv/
rye.lock
.pytest_cache/
.mypy_cache/
.env
*.log
"@
    Write-Host "Created .gitignore"
}

# Step 5: Initialize Git repo if not already
if (-not (Test-Path ".git")) {
    git init
    git add .
    git commit -m "Initialize parts2sales-llm-hub structure with rye"
    Write-Host "Initialized new Git repository"
}

# Step 6: Setup pre-commit if available
if (Test-Path ".git") {
    pre-commit sample-config > .pre-commit-config.yaml
    pre-commit install
    Write-Host "Pre-commit hooks installed"
}

Write-Host "✅ Rye environment initialized and ready."
