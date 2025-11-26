from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.category import Category
from app.auth import admin_required, optional_auth, validate_request_data
from app.utils.error_handlers import ValidationError, BusinessLogicError


products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=['GET'])
@optional_auth
def get_products(current_user=None):
    """Récupérer la liste des produits avec pagination et recherche"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # Limite à 50 par page
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', type=int)
    
    # Construire la requête de base
    query = Product.query
    
    # Filtrer par catégorie si spécifiée
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Recherche par nom si spécifiée
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    # Filtrer les produits actifs pour les non-admins
    if not current_user or not current_user.is_admin():
        query = query.filter_by(is_active=True)
    
    # Pagination
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'pagination': {
            'page': products.page,
            'pages': products.pages,
            'per_page': products.per_page,
            'total': products.total
        }
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
@optional_auth
def get_product(product_id, current_user=None):
    """Récupérer un produit spécifique"""
    product = db.session.get(Product, product_id)
    
    if not product:
        return jsonify({
            'error': 'Produit introuvable'
        }), 404
    
    # Vérifier si le produit est actif pour les non-admins
    if not product.is_active and (not current_user or not current_user.is_admin()):
        return jsonify({
            'error': 'Produit introuvable'
        }), 404
    
    return jsonify({
        'product': product.to_dict()
    }), 200


@products_bp.route('', methods=['POST'])
@admin_required
@validate_request_data(['name', 'price', 'category_id'])
def create_product(current_user, data):
    """Créer un nouveau produit (Admin uniquement)"""
    try:
        # Vérifier que la catégorie existe
        category = db.session.get(Category, data['category_id'])
        if not category:
            raise ValidationError("Catégorie introuvable", "category_id")
        
        # Vérifier si le SKU existe déjà (si fourni)
        if 'sku' in data and data['sku']:
            existing_sku = Product.query.filter_by(sku=data['sku']).first()
            if existing_sku:
                raise ValidationError("Ce SKU existe déjà", "sku")
        
        product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            stock_quantity=data.get('stock_quantity', 0),
            category_id=data['category_id'],
            sku=data.get('sku'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Produit créé avec succès',
            'product': product.to_dict()
        }), 201
        
    except ValidationError:
        raise
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la création du produit: {str(e)}")


@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
@validate_request_data(['name', 'price', 'category_id'])
def update_product(product_id, current_user, data):
    """Mettre à jour un produit (Admin uniquement)"""
    product = db.session.get(Product, product_id)
    
    if not product:
        return jsonify({
            'error': 'Produit introuvable'
        }), 404
    
    try:
        # Vérifier que la catégorie existe
        category = db.session.get(Category, data['category_id'])
        if not category:
            raise ValidationError("Catégorie introuvable", "category_id")
        
        # Vérifier si le nouveau SKU existe déjà (si fourni et différent de l'actuel)
        if 'sku' in data and data['sku'] and data['sku'] != product.sku:
            existing_sku = Product.query.filter_by(sku=data['sku']).first()
            if existing_sku:
                raise ValidationError("Ce SKU existe déjà", "sku")
        
        # Mise à jour des champs
        product.name = data['name']
        product.description = data.get('description', product.description)
        product.price = data['price']
        product.category_id = data['category_id']
        
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'sku' in data:
            product.sku = data['sku']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Produit mis à jour avec succès',
            'product': product.to_dict()
        }), 200
        
    except ValidationError:
        raise
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la mise à jour du produit: {str(e)}")


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id, current_user):
    """Supprimer un produit (Admin uniquement)"""
    product = db.session.get(Product, product_id)
    
    if not product:
        return jsonify({
            'error': 'Produit introuvable'
        }), 404
    
    try:
        # Vérifier s'il y a des commandes avec ce produit
        if product.order_lines:
            # Au lieu de supprimer, désactiver le produit
            product.is_active = False
            db.session.commit()
            
            return jsonify({
                'message': 'Produit désactivé car il est associé à des commandes'
            }), 200
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Produit supprimé avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la suppression du produit: {str(e)}")


@products_bp.route('/<int:product_id>/stock', methods=['PATCH'])
@admin_required
@validate_request_data(['stock_quantity'])
def update_stock(product_id, current_user, data):
    """Mettre à jour le stock d'un produit (Admin uniquement)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'error': 'Produit introuvable'
        }), 404
    
    try:
        product.stock_quantity = data['stock_quantity']
        db.session.commit()
        
        return jsonify({
            'message': 'Stock mis à jour avec succès',
            'product': {
                'id': product.id,
                'name': product.name,
                'stock_quantity': product.stock_quantity,
                'is_available': product.is_available()
            }
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la mise à jour du stock: {str(e)}")


@products_bp.route('/search', methods=['GET'])
@optional_auth
def search_products(current_user=None):
    """Recherche de produits par nom ou caractéristiques"""
    search_term = request.args.get('q', '', type=str)
    
    if not search_term:
        return jsonify({
            'error': 'Terme de recherche requis',
            'message': 'Utilisez le paramètre "q" pour spécifier votre recherche'
        }), 400
    
    # Recherche dans le nom et la description
    query = Product.query.filter(
        db.or_(
            Product.name.ilike(f'%{search_term}%'),
            Product.description.ilike(f'%{search_term}%')
        )
    )
    
    # Filtrer les produits actifs pour les non-admins
    if not current_user or not current_user.is_admin():
        query = query.filter_by(is_active=True)
    
    products = query.limit(20).all()  # Limite à 20 résultats
    
    return jsonify({
        'search_term': search_term,
        'results_count': len(products),
        'products': [product.to_dict() for product in products]
    }), 200