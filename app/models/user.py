from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from enum import Enum


class UserRole(Enum):
    """Enumération pour les rôles utilisateurs"""
    CLIENT = "client"
    ADMIN = "admin"


class User(db.Model):
    """Modèle pour les utilisateurs (clients et administrateurs)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    @validates('email')
    def validate_email(self, key, email):
        """Validation de l'email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Format d'email invalide")
        return email.lower()
    
    def set_password(self, password):
        """Hash et stocke le mot de passe"""
        if len(password) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caractères")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == UserRole.ADMIN
    
    def to_dict(self, include_sensitive=False):
        """Conversion en dictionnaire pour JSON"""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role.value,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'