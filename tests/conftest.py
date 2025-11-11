import pytest
from app import create_app, db
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.product import Product


@pytest.fixture
def app():
    """Créer une instance de l'application pour les tests"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Headers d'authentification pour les tests"""
    # Créer un utilisateur admin pour les tests
    admin = User(
        email='admin@test.com',
        first_name='Admin',
        last_name='Test',
        role=UserRole.ADMIN
    )
    admin.set_password('test123')
    db.session.add(admin)
    
    # Créer un utilisateur client pour les tests
    client_user = User(
        email='client@test.com',
        first_name='Client',
        last_name='Test',
        role=UserRole.CLIENT
    )
    client_user.set_password('test123')
    db.session.add(client_user)
    db.session.commit()
    
    # Connexion admin
    admin_login_data = {
        'email': 'admin@test.com',
        'password': 'test123'
    }
    admin_response = client.post('/api/auth/login', json=admin_login_data)
    admin_token = admin_response.json['access_token']
    
    # Connexion client
    client_login_data = {
        'email': 'client@test.com',
        'password': 'test123'
    }
    client_response = client.post('/api/auth/login', json=client_login_data)
    client_token = client_response.json['access_token']
    
    return {
        'admin': {'Authorization': f'Bearer {admin_token}'},
        'client': {'Authorization': f'Bearer {client_token}'}
    }


@pytest.fixture
def sample_category():
    """Catégorie d'exemple pour les tests"""
    category = Category(
        name='Test Category',
        description='Category for testing'
    )
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture
def sample_product(sample_category):
    """Produit d'exemple pour les tests"""
    product = Product(
        name='Test Product',
        description='Product for testing',
        price=99.99,
        stock_quantity=10,
        category_id=sample_category.id,
        sku='TEST-001'
    )
    db.session.add(product)
    db.session.commit()
    return product