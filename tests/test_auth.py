def test_user_registration(client):
    """Test l'inscription d'un nouvel utilisateur"""
    data = {
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert 'user' in response.json
    assert response.json['user']['email'] == data['email']


def test_user_registration_duplicate_email(client):
    """Test l'inscription avec un email déjà utilisé"""
    data = {
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    
    # Première inscription
    client.post('/api/auth/register', json=data)
    
    # Tentative de seconde inscription avec le même email
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 400
    assert 'email' in response.json.get('field', '')


def test_user_login(client, auth_headers):
    """Test la connexion d'un utilisateur"""
    data = {
        'email': 'admin@test.com',
        'password': 'test123'
    }
    
    response = client.post('/api/auth/login', json=data)
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'user' in response.json


def test_user_login_invalid_credentials(client):
    """Test la connexion avec des identifiants invalides"""
    data = {
        'email': 'invalid@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/auth/login', json=data)
    assert response.status_code == 401


def test_get_profile(client, auth_headers):
    """Test la récupération du profil utilisateur"""
    response = client.get('/api/auth/profile', headers=auth_headers['admin'])
    assert response.status_code == 200
    assert 'user' in response.json
    assert response.json['user']['email'] == 'admin@test.com'


def test_get_profile_without_auth(client):
    """Test la récupération du profil sans authentification"""
    response = client.get('/api/auth/profile')
    assert response.status_code == 401