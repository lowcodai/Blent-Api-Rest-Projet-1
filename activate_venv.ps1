# 1. Activer l'environnement virtuel
& "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1\.venv\Scripts\Activate.ps1"

# 2. Configurer PYTHONPATH
$env:PYTHONPATH = "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1;$env:PYTHONPATH"

# 3. Lancer les tests
pytest tests/ -v

# 4. lancer le serveur
.\start_server.ps1

# 5. Lancer les tests
python test_api.py

# 6. sortir de l'environnement virtuel
deactivate

# 7. Message de fin
Write-Host "✅ Tests terminés" -ForegroundColor Green