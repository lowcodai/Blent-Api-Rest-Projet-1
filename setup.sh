#!/bin/bash

# Script de démarrage pour l'API DigiMarket
echo "🚀 Initialisation de l'API DigiMarket E-commerce"
echo "==============================================="

# Vérification de l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Veuillez d'abord l'installer:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Vérification que nous sommes dans l'environnement virtuel
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activation de l'environnement virtuel..."
    source .venv/bin/activate
fi

echo "✅ Environnement virtuel actif: $VIRTUAL_ENV"

# Vérification des dépendances
echo "📦 Vérification des dépendances..."
python -c "import flask, flask_sqlalchemy, flask_jwt_extended" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dépendances manquantes. Installation..."
    pip install -r requirements.txt
fi

# Configuration de l'environnement
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
fi

echo "🗄️  Initialisation de la base de données..."

# Initialisation de la base de données avec gestion d'erreur
python -c "
import os
import sys
sys.path.insert(0, '.')

try:
    from app import create_app, db
    from app.utils.seed_data import create_sample_data
    
    app = create_app()
    with app.app_context():
        # Créer les tables
        db.create_all()
        print('✅ Tables créées avec succès')
        
        # Ajouter des données de test
        create_sample_data()
        print('✅ Données de test ajoutées')
        
except Exception as e:
    print(f'❌ Erreur lors de l\'initialisation: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Base de données initialisée avec succès!"
    echo ""
    echo "🎯 Application prête! Vous pouvez maintenant:"
    echo "   1. Lancer le serveur: python run.py"
    echo "   2. Tester l'API: ./test_api.sh"
    echo "   3. Consulter la doc: cat API_DOCUMENTATION.md"
    echo ""
    echo "📱 Comptes de test disponibles:"
    echo "   Admin: admin@digimarket.com / admin123"
    echo "   Client: jean.dupont@email.com / client123"
else
    echo "❌ Échec de l'initialisation de la base de données"
    exit 1
fi