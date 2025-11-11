from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.order import Order, OrderLine, OrderStatus
from app.models.product import Product
from app.models.user import User
from app.auth import admin_required, customer_or_admin_required, validate_request_data
from app.utils.error_handlers import ValidationError, BusinessLogicError


orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
@customer_or_admin_required
def get_orders(current_user):
    """Récupérer les commandes (toutes pour admin, seulement les siennes pour client)"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    status_filter = request.args.get('status', type=str)
    
    # Construire la requête
    query = Order.query
    
    # Filtrer par utilisateur si ce n'est pas un admin
    if not current_user.is_admin():
        query = query.filter_by(user_id=current_user.id)
    
    # Filtrer par statut si spécifié
    if status_filter:
        try:
            status_enum = OrderStatus(status_filter)
            query = query.filter_by(status=status_enum)
        except ValueError:
            return jsonify({
                'error': 'Statut invalide',
                'valid_statuses': [status.value for status in OrderStatus]
            }), 400
    
    # Pagination
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'orders': [order.to_dict() for order in orders.items],
        'pagination': {
            'page': orders.page,
            'pages': orders.pages,
            'per_page': orders.per_page,
            'total': orders.total
        }
    }), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@customer_or_admin_required
def get_order(order_id, current_user):
    """Récupérer une commande spécifique"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'error': 'Commande introuvable'
        }), 404
    
    # Vérifier les permissions (client ne peut voir que ses commandes)
    if not current_user.is_admin() and order.user_id != current_user.id:
        return jsonify({
            'error': 'Accès refusé',
            'message': 'Vous ne pouvez consulter que vos propres commandes'
        }), 403
    
    return jsonify({
        'order': order.to_dict(include_lines=True)
    }), 200


@orders_bp.route('', methods=['POST'])
@customer_or_admin_required
@validate_request_data(['shipping_address', 'order_lines'])
def create_order(current_user, data):
    """Créer une nouvelle commande"""
    if not data['order_lines']:
        raise ValidationError("La commande doit contenir au moins une ligne", "order_lines")
    
    try:
        # Créer la commande
        order = Order(
            user_id=current_user.id,
            shipping_address=data['shipping_address'],
            status=OrderStatus.PENDING
        )
        
        db.session.add(order)
        db.session.flush()  # Pour obtenir l'ID de la commande
        
        total_amount = 0
        
        # Traiter chaque ligne de commande
        for line_data in data['order_lines']:
            if 'product_id' not in line_data or 'quantity' not in line_data:
                raise ValidationError("Chaque ligne doit contenir product_id et quantity")
            
            product_id = line_data['product_id']
            quantity = line_data['quantity']
            
            if quantity <= 0:
                raise ValidationError(f"Quantité invalide pour le produit {product_id}")
            
            # Vérifier le produit
            product = Product.query.get(product_id)
            if not product:
                raise ValidationError(f"Produit {product_id} introuvable")
            
            if not product.is_active:
                raise ValidationError(f"Le produit {product.name} n'est plus disponible")
            
            if not product.can_fulfill_quantity(quantity):
                raise ValidationError(
                    f"Stock insuffisant pour {product.name}. "
                    f"Disponible: {product.stock_quantity}, Demandé: {quantity}"
                )
            
            # Créer la ligne de commande
            order_line = OrderLine(
                order_id=order.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price
            )
            
            db.session.add(order_line)
            
            # Réduire le stock
            product.reduce_stock(quantity)
            
            total_amount += order_line.get_subtotal()
        
        # Mettre à jour le total de la commande
        order.total_amount = total_amount
        
        db.session.commit()
        
        return jsonify({
            'message': 'Commande créée avec succès',
            'order': order.to_dict(include_lines=True)
        }), 201
        
    except ValidationError:
        db.session.rollback()
        raise
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la création de la commande: {str(e)}")


@orders_bp.route('/<int:order_id>', methods=['PATCH'])
@admin_required
@validate_request_data(['status'])
def update_order_status(order_id, current_user, data):
    """Mettre à jour le statut d'une commande (Admin uniquement)"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'error': 'Commande introuvable'
        }), 404
    
    try:
        # Valider le nouveau statut
        try:
            new_status = OrderStatus(data['status'])
        except ValueError:
            return jsonify({
                'error': 'Statut invalide',
                'valid_statuses': [status.value for status in OrderStatus]
            }), 400
        
        # Mettre à jour le statut (avec validation des transitions)
        order.update_status(new_status)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Statut de la commande mis à jour: {new_status.value}',
            'order': order.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de la mise à jour du statut: {str(e)}")


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@customer_or_admin_required
def cancel_order(order_id, current_user):
    """Annuler une commande"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'error': 'Commande introuvable'
        }), 404
    
    # Vérifier les permissions (client ne peut annuler que ses commandes)
    if not current_user.is_admin() and order.user_id != current_user.id:
        return jsonify({
            'error': 'Accès refusé',
            'message': 'Vous ne pouvez annuler que vos propres commandes'
        }), 403
    
    if not order.can_be_cancelled():
        return jsonify({
            'error': 'Impossible d\'annuler',
            'message': f'Cette commande ne peut pas être annulée (statut: {order.status.value})'
        }), 409
    
    try:
        # Remettre les produits en stock
        for line in order.order_lines:
            product = Product.query.get(line.product_id)
            if product:
                product.increase_stock(line.quantity)
        
        # Mettre à jour le statut
        order.update_status(OrderStatus.CANCELLED)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Commande annulée avec succès',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Erreur lors de l'annulation de la commande: {str(e)}")


@orders_bp.route('/<int:order_id>/lignes', methods=['GET'])
@customer_or_admin_required
def get_order_lines(order_id, current_user):
    """Consulter les lignes d'une commande"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'error': 'Commande introuvable'
        }), 404
    
    # Vérifier les permissions (client ne peut voir que ses commandes)
    if not current_user.is_admin() and order.user_id != current_user.id:
        return jsonify({
            'error': 'Accès refusé',
            'message': 'Vous ne pouvez consulter que vos propres commandes'
        }), 403
    
    return jsonify({
        'order_id': order.id,
        'order_lines': [line.to_dict() for line in order.order_lines],
        'total_amount': float(order.total_amount)
    }), 200


@orders_bp.route('/stats', methods=['GET'])
@admin_required
def get_order_stats(current_user):
    """Statistiques des commandes (Admin uniquement)"""
    try:
        # Compter par statut
        stats = {}
        for status in OrderStatus:
            count = Order.query.filter_by(status=status).count()
            stats[status.value] = count
        
        # Total des commandes
        total_orders = Order.query.count()
        
        # Chiffre d'affaires total (commandes validées et expédiées)
        revenue_statuses = [OrderStatus.CONFIRMED, OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.status.in_(revenue_statuses)
        ).scalar() or 0
        
        return jsonify({
            'total_orders': total_orders,
            'orders_by_status': stats,
            'total_revenue': float(total_revenue)
        }), 200
        
    except Exception as e:
        raise BusinessLogicError(f"Erreur lors du calcul des statistiques: {str(e)}")