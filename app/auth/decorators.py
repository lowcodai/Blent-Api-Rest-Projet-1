from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, 
    create_access_token, create_refresh_token,
    get_jwt
)
from app.models.user import User, UserRole


def admin_required(f):
    """Décorateur pour les routes nécessitant les droits administrateur"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin():
            return jsonify({
                'error': 'Accès refusé',
                'message': 'Droits administrateur requis'
            }), 403
        
        return f(current_user=user, *args, **kwargs)
    return decorated


def customer_or_admin_required(f):
    """Décorateur pour les routes accessibles aux clients et admins"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'error': 'Accès refusé',
                'message': 'Utilisateur inactif ou introuvable'
            }), 403
        
        return f(current_user=user, *args, **kwargs)
    return decorated


def optional_auth(f):
    """Décorateur pour les routes avec authentification optionnelle"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Tenter de récupérer le token
            if 'Authorization' in request.headers:
                from flask_jwt_extended import verify_jwt_in_request
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                return f(current_user=user, *args, **kwargs)
        except Exception:
            # Si pas de token ou token invalide, continuer sans user
            pass
        
        return f(current_user=None, *args, **kwargs)
    return decorated


def generate_tokens(user):
    """Génère les tokens d'accès et de rafraîchissement pour un utilisateur"""
    access_token = create_access_token(
        identity=user.id,
        additional_claims={
            'role': user.role.value,
            'email': user.email
        }
    )
    
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }


def validate_request_data(required_fields):
    """Valide que les champs requis sont présents dans la requête"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'error': 'Données JSON requises'
                }), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    'error': 'Champs manquants',
                    'missing_fields': missing_fields
                }), 400
            
            return f(data=data, *args, **kwargs)
        return decorated
    return decorator