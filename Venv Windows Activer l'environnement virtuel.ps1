# 1. Activer l'environnement virtuel
& "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1\.venv\Scripts\Activate.ps1"

# Configurer PYTHONPATH
$env:PYTHONPATH = "C:\Users\COSTE\OneDrive - itshaker\VS Code projects\Blent-Api-Rest-Projet-1;$env:PYTHONPATH"

# Lancer les tests
pytest tests/ -v


# 2. Lancer les tests
python test_api.py