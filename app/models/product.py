from datetime import datetime
from app import db
from sqlalchemy.orm import validates
from decimal import Decimal


class Product(db.Model):
    """Modèle pour les produits"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    sku = db.Column(db.String(50), unique=True)  # Stock Keeping Unit
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    order_lines = db.relationship('OrderLine', backref='product', lazy=True)
    
    @validates('price')
    def validate_price(self, key, price):
        """Validation du prix"""
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        return price
    
    @validates('stock_quantity')
    def validate_stock(self, key, quantity):
        """Validation du stock"""
        if quantity < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        return quantity
    
    def is_available(self):
        """Vérifie si le produit est disponible"""
        return self.is_active and self.stock_quantity > 0
    
    def can_fulfill_quantity(self, requested_quantity):
        """Vérifie si on peut satisfaire la quantité demandée"""
        return self.stock_quantity >= requested_quantity
    
    def reduce_stock(self, quantity):
        """Réduit le stock du produit"""
        if not self.can_fulfill_quantity(quantity):
            raise ValueError(f"Stock insuffisant. Disponible: {self.stock_quantity}, Demandé: {quantity}")
        self.stock_quantity -= quantity
    
    def increase_stock(self, quantity):
        """Augmente le stock du produit"""
        self.stock_quantity += quantity
    
    def to_dict(self):
        """Conversion en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'sku': self.sku,
            'is_active': self.is_active,
            'is_available': self.is_available(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def search_by_name(search_term):
        """Recherche de produits par nom"""
        return Product.query.filter(
            Product.name.ilike(f'%{search_term}%'),
            Product.is_active == True
        ).all()
    
    def __repr__(self):
        return f'<Product {self.name}>'