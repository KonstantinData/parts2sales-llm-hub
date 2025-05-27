# PowerShell Setup Script for LLM Hub Environment

Write-Host "🔍 Checking Rye installation..."
$ryeVersion = rye --version 2>$null
if (-not $ryeVersion) {
    Write-Host "❌ Rye is not installed. Please install it from https://rye.astral.sh/"
    exit 1
} else {
    Write-Host "✅ Rye found: $ryeVersion"
}

Write-Host "🔄 Syncing dependencies with Rye..."
rye sync

Write-Host "🐍 Checking Python version from Rye..."
$pythonVersion = rye run python --version
Write-Host "✅ Python version: $pythonVersion"

Write-Host "📦 Listing installed packages:"
rye show

Write-Host "✅ Environment setup complete."
