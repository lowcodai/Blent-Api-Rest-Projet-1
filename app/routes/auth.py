from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User, UserRole
from app.auth import generate_tokens, validate_request_data
from app.utils.error_handlers import ValidationError, BusinessLogicError


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@validate_request_data(['email', 'password', 'first_name', 'last_name'])
def register(data):
    """Inscription d'un nouvel utilisateur"""
    try:
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError("Cette adresse email est déjà utilisée", "email")
        
        # Créer le nouvel utilisateur
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=UserRole.ADMIN if data.get('is_admin', False) else UserRole.CLIENT,
            address=data.get('address'),
            phone=data.get('phone')
        )
        
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Générer les tokens
        tokens = generate_tokens(user)
        
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            **tokens
        }), 201
        
    except ValidationError:
        raise
    except ValueError as e:
        raise ValidationError(str(e))
    except IntegrityError:
        db.session.rollback()
        raise ValidationError("Cette adresse email est déjà utilisée", "email")
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la création de l'utilisateur: {str(e)}")


@auth_bp.route('/login', methods=['POST'])
@validate_request_data(['email', 'password'])
def login(data):
    """Connexion d'un utilisateur"""
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({
            'error': 'Identifiants invalides',
            'message': 'Email ou mot de passe incorrect'
        }), 401
    
    if not user.is_active:
        return jsonify({
            'error': 'Compte désactivé',
            'message': 'Votre compte a été désactivé'
        }), 403
    
    # Générer les tokens
    tokens = generate_tokens(user)
    
    return jsonify({
        'message': 'Connexion réussie',
        **tokens
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Récupérer le profil de l'utilisateur connecté"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'error': 'Utilisateur introuvable'
        }), 404
    
    return jsonify({
        'user': user.to_dict()
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@validate_request_data(['first_name', 'last_name'])
def update_profile(data):
    """Mettre à jour le profil de l'utilisateur connecté"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'error': 'Utilisateur introuvable'
        }), 404
    
    try:
        # Mise à jour des champs autorisés
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        
        if 'address' in data:
            user.address = data['address']
        if 'phone' in data:
            user.phone = data['phone']
        
        # Changement de mot de passe si fourni
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profil mis à jour avec succès',
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la mise à jour: {str(e)}")


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@validate_request_data(['current_password', 'new_password'])
def change_password(data):
    """Changer le mot de passe de l'utilisateur connecté"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'error': 'Utilisateur introuvable'
        }), 404
    
    # Vérifier le mot de passe actuel
    if not user.check_password(data['current_password']):
        return jsonify({
            'error': 'Mot de passe incorrect',
            'message': 'Le mot de passe actuel est incorrect'
        }), 400
    
    try:
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({
            'message': 'Mot de passe modifié avec succès'
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors du changement de mot de passe: {str(e)}")


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """Lister tous les utilisateurs (Admin uniquement)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin():
        return jsonify({
            'error': 'Accès refusé',
            'message': 'Droits administrateur requis'
        }), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    users = User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'pagination': {
            'page': users.page,
            'pages': users.pages,
            'per_page': users.per_page,
            'total': users.total
        }
    }), 200