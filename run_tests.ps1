# Script PowerShell pour lancer les tests pytest avec l'environnement correct
Write-Host "🧪 Lancement des tests DigiMarket" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Se déplacer dans le répertoire du projet
Set-Location "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1"

# Activer l'environnement virtuel
Write-Host "📦 Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\\.venv\\Scripts\\Activate.ps1"

# Ajouter le répertoire racine au PYTHONPATH
$env:PYTHONPATH = "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1;$env:PYTHONPATH"

# Vérifier que le module app est accessible
Write-Host "🔍 Vérification du module app..." -ForegroundColor Yellow
try {
    python -c "import app; print('✅ Module app trouvé')"
    Write-Host ""
    Write-Host "🚀 Exécution des tests..." -ForegroundColor Green
    Write-Host ""
    
    # Lancer pytest avec les arguments passés au script
    pytest tests/ @args
}
catch {
    Write-Host "❌ Erreur: Module app non trouvé" -ForegroundColor Red
    exit 1
}