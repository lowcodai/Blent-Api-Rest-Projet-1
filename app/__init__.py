from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.config import config
import os


# Initialisation des extensions
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None):
    """Factory pattern pour créer l'application Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Import des modèles pour s'assurer qu'ils sont enregistrés
    from app.models import user, product, category, order
    
    # Enregistrement des Blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.categories import categories_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/produits')
    app.register_blueprint(orders_bp, url_prefix='/api/commandes')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    
    # Route de base pour vérifier le fonctionnement
    @app.route('/')
    def index():
        return {
            'message': 'API DigiMarket E-commerce',
            'version': '1.0.0',
            'status': 'active'
        }
    
    @app.route('/api/health')
    def health():
        return {'status': 'OK', 'message': 'API is running'}
    
    # Gestion globale des erreurs
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app