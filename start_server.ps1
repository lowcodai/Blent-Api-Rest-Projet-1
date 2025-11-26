# Script PowerShell pour lancer l'application DigiMarket API
Write-Host "🚀 Lancement de l'application DigiMarket API" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Se déplacer dans le répertoire du projet
Set-Location "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1"

# Activer l'environnement virtuel .venv (Python 3.12)
Write-Host "📦 Activation de l'environnement virtuel Python 3.12..." -ForegroundColor Yellow
& ".\\.venv\\Scripts\\Activate.ps1"

# Configurer PYTHONPATH
$env:PYTHONPATH = "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1;$env:PYTHONPATH"

Write-Host "🌐 Lancement du serveur Flask..." -ForegroundColor Green
Write-Host "API sera disponible sur : http://127.0.0.1:5001" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Lancer l'application
python run.py