from datetime import datetime
from app import db


class Category(db.Model):
    """Modèle pour les catégories de produits"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        """Conversion en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'products_count': len(self.products) if self.products else 0
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'