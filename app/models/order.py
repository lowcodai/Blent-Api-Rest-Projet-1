from datetime import datetime
from app import db
from enum import Enum


class OrderStatus(Enum):
    """Enumération pour les statuts de commande"""
    PENDING = "en_attente"
    CONFIRMED = "validee"
    SHIPPED = "expediee"
    DELIVERED = "livree"
    CANCELLED = "annulee"


class Order(db.Model):
    """Modèle pour les commandes"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    order_lines = db.relationship('OrderLine', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        """Calcule le montant total de la commande"""
        total = sum(line.get_subtotal() for line in self.order_lines)
        self.total_amount = total
        return total
    
    def can_be_modified(self):
        """Vérifie si la commande peut être modifiée"""
        return self.status in [OrderStatus.PENDING]
    
    def can_be_cancelled(self):
        """Vérifie si la commande peut être annulée"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def update_status(self, new_status):
        """Met à jour le statut de la commande avec validation"""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: []
        }
        
        if new_status not in valid_transitions.get(self.status, []):
            raise ValueError(f"Transition invalide de {self.status.value} vers {new_status.value}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_lines=False):
        """Conversion en dictionnaire pour JSON"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': f"{self.customer.first_name} {self.customer.last_name}" if self.customer else None,
            'status': self.status.value,
            'total_amount': float(self.total_amount),
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'lines_count': len(self.order_lines)
        }
        
        if include_lines:
            data['order_lines'] = [line.to_dict() for line in self.order_lines]
        
        return data
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status.value}>'


class OrderLine(db.Model):
    """Modèle pour les lignes de commande"""
    __tablename__ = 'order_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Prix au moment de la commande
    
    def get_subtotal(self):
        """Calcule le sous-total de la ligne"""
        return self.quantity * self.unit_price
    
    def to_dict(self):
        """Conversion en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.get_subtotal())
        }
    
    def __repr__(self):
        return f'<OrderLine {self.id} - Qty: {self.quantity}>'