from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import InvalidTokenError


class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(message)


class BusinessLogicError(Exception):
    """Exception personnalisée pour les erreurs de logique métier"""
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(message)


def register_error_handlers(app):
    """Enregistre les gestionnaires d'erreurs globaux"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            'error': 'Erreur de validation',
            'message': e.message,
            'field': e.field
        }), 400
    
    @app.errorhandler(BusinessLogicError)
    def handle_business_logic_error(e):
        return jsonify({
            'error': 'Erreur métier',
            'message': e.message,
            'code': e.code
        }), 422
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        app.logger.error(f"Database integrity error: {str(e)}")
        return jsonify({
            'error': 'Erreur de données',
            'message': 'Une contrainte de base de données a été violée'
        }), 409
    
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(e):
        return jsonify({
            'error': 'Token invalide',
            'message': 'Le token d\'authentification est invalide ou a expiré'
        }), 401
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'error': 'Ressource introuvable',
            'message': 'La ressource demandée n\'existe pas'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            'error': 'Méthode non autorisée',
            'message': 'Cette méthode HTTP n\'est pas autorisée pour cette URL'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        app.logger.error(f"Internal server error: {str(e)}")
        return jsonify({
            'error': 'Erreur interne du serveur',
            'message': 'Une erreur inattendue s\'est produite'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            'error': e.name,
            'message': e.description,
            'code': e.code
        }), e.code