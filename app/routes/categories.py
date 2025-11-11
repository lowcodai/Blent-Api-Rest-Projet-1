from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from app.auth import admin_required, optional_auth, validate_request_data
from app.utils.error_handlers import ValidationError, BusinessLogicError


categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
@optional_auth
def get_categories(current_user=None):
    """Récupérer la liste des catégories"""
    # Filtrer les catégories actives pour les non-admins
    if not current_user or not current_user.is_admin():
        categories = Category.query.filter_by(is_active=True).all()
    else:
        categories = Category.query.all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200


@categories_bp.route('/<int:category_id>', methods=['GET'])
@optional_auth
def get_category(category_id, current_user=None):
    """Récupérer une catégorie spécifique"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'error': 'Catégorie introuvable'
        }), 404
    
    # Vérifier si la catégorie est active pour les non-admins
    if not category.is_active and (not current_user or not current_user.is_admin()):
        return jsonify({
            'error': 'Catégorie introuvable'
        }), 404
    
    return jsonify({
        'category': category.to_dict()
    }), 200


@categories_bp.route('', methods=['POST'])
@admin_required
@validate_request_data(['name'])
def create_category(current_user, data):
    """Créer une nouvelle catégorie (Admin uniquement)"""
    try:
        # Vérifier si la catégorie existe déjà
        if Category.query.filter_by(name=data['name']).first():
            raise ValidationError("Une catégorie avec ce nom existe déjà", "name")
        
        category = Category(
            name=data['name'],
            description=data.get('description'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Catégorie créée avec succès',
            'category': category.to_dict()
        }), 201
        
    except ValidationError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la création de la catégorie: {str(e)}")


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
@validate_request_data(['name'])
def update_category(category_id, current_user, data):
    """Mettre à jour une catégorie (Admin uniquement)"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'error': 'Catégorie introuvable'
        }), 404
    
    try:
        # Vérifier si le nouveau nom existe déjà (sauf pour la catégorie actuelle)
        existing = Category.query.filter(
            Category.name == data['name'],
            Category.id != category_id
        ).first()
        
        if existing:
            raise ValidationError("Une catégorie avec ce nom existe déjà", "name")
        
        category.name = data['name']
        category.description = data.get('description', category.description)
        category.is_active = data.get('is_active', category.is_active)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Catégorie mise à jour avec succès',
            'category': category.to_dict()
        }), 200
        
    except ValidationError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la mise à jour de la catégorie: {str(e)}")


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id, current_user):
    """Supprimer une catégorie (Admin uniquement)"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'error': 'Catégorie introuvable'
        }), 404
    
    try:
        # Vérifier s'il y a des produits dans cette catégorie
        if category.products:
            return jsonify({
                'error': 'Impossible de supprimer',
                'message': f'Cette catégorie contient {len(category.products)} produit(s)'
            }), 409
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Catégorie supprimée avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la suppression de la catégorie: {str(e)}")