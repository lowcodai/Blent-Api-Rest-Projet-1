#!/bin/bash

# Script de démarrage simple pour l'API DigiMarket
echo "🚀 Démarrage de l'API DigiMarket"
echo "================================"

cd /workspaces/Blent-Api-Rest-Projet-1

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python -m venv .venv
fi

# Activer l'environnement virtuel
echo "📦 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier et installer les dépendances
echo "🔍 Vérification des dépendances..."
pip install -r requirements.txt

# Vérifier que Flask est disponible
python -c "import flask; print('✅ Flask disponible')" || exit 1

# Initialiser la base de données si nécessaire
if [ ! -f "digimarket.db" ]; then
    echo "🗄️ Initialisation de la base de données..."
    python -c "
from app import create_app, db
from app.utils.seed_data import create_sample_data
app = create_app()
with app.app_context():
    db.create_all()
    create_sample_data()
    print('✅ Base de données initialisée')
"
fi

# Vérifier et libérer le port 5001 si nécessaire
echo "🔍 Vérification du port 5001..."
PROCESSES=$(lsof -ti :5001 2>/dev/null)
if [ ! -z "$PROCESSES" ]; then
    echo "⚠️  Port 5001 occupé par les processus: $PROCESSES"
    echo "🔧 Libération du port..."
    kill -9 $PROCESSES 2>/dev/null
    sleep 1
fi

# Lancer le serveur
echo ""
echo "🌐 Démarrage du serveur sur le port 5001..."
echo "   URL locale: http://localhost:5001"
if [ -n "$CODESPACE_NAME" ]; then
    echo "   URL Codespace: https://$CODESPACE_NAME-5001.app.github.dev"
fi
echo ""
echo "🛑 Pour arrêter le serveur, utilisez Ctrl+C"
echo ""

python run.py