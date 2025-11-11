#!/usr/bin/env python3
"""
Point d'entrée principal de l'application DigiMarket API
"""

from app import create_app, db
from flask import current_app
import os


app = create_app()


@app.cli.command()
def init_db():
    """Initialise la base de données avec les tables"""
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès!")


@app.cli.command()
def seed_db():
    """Peuple la base de données avec des données de test"""
    from app.utils.seed_data import create_sample_data
    with app.app_context():
        create_sample_data()
        print("Données de test ajoutées avec succès!")


if __name__ == '__main__':
    # En développement, on peut lancer directement avec python app.py
    import os
    port = int(os.environ.get('PORT', 5001))  # Port 5001 par défaut
    app.run(debug=True, host='0.0.0.0', port=port)