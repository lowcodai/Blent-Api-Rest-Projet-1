# Script PowerShell pour lancer les tests API DigiMarket
Write-Host "🧪 Lancement des tests API DigiMarket" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Se déplacer dans le répertoire du projet
Set-Location "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1"

# Activer l'environnement virtuel .venv (Python 3.12)
Write-Host "📦 Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\\.venv\\Scripts\\Activate.ps1"

# Vérifier que l'API est disponible
Write-Host "🔍 Vérification de la disponibilité de l'API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API disponible sur http://localhost:5001" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ API non disponible. Lancez d'abord le serveur avec:" -ForegroundColor Red
    Write-Host "   .\start_server.ps1" -ForegroundColor Yellow
    Write-Host "   ou: python run.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🚀 Lancement des tests API..." -ForegroundColor Green
Write-Host ""

# Lancer les tests
python test_api.py