def test_app_creation(app):
    """Test que l'application se crée correctement"""
    assert app is not None
    assert app.config['TESTING'] is True


def test_health_endpoint(client):
    """Test du endpoint de santé"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'OK'


def test_index_endpoint(client):
    """Test de l'endpoint racine"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['message'] == 'API DigiMarket E-commerce'
    assert response.json['version'] == '1.0.0'