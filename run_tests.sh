#!/bin/bash

# Script pour lancer les tests pytest avec l'environnement correct
echo "🧪 Lancement des tests DigiMarket"
echo "================================"

cd /workspaces/Blent-Api-Rest-Projet-1

# Activer l'environnement virtuel
echo "📦 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Ajouter le répertoire racine au PYTHONPATH pour que Python trouve le module 'app'
export PYTHONPATH="/workspaces/Blent-Api-Rest-Projet-1:$PYTHONPATH"

# Vérifier que le module app est accessible
echo "🔍 Vérification du module app..."
python -c "import app; print('✅ Module app trouvé')" || {
    echo "❌ Erreur: Module app non trouvé"
    exit 1
}

echo ""
echo "🚀 Exécution des tests..."
echo ""

# Lancer pytest avec les arguments passés au script
pytest tests/ "$@"