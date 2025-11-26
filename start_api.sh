#!/bin/bash
# Script de démarrage de l'API DigiMarket

cd /workspaces/Blent-Api-Rest-Projet-1
source .venv/bin/activate

echo "🚀 Démarrage de l'API DigiMarket sur le port 5001..."
python -c "from app import create_app; app = create_app(); app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)"
