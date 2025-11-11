def test_get_products(client, sample_product):
    """Test la récupération de la liste des produits"""
    response = client.get('/api/produits')
    assert response.status_code == 200
    assert 'products' in response.json
    assert len(response.json['products']) >= 1


def test_get_product_by_id(client, sample_product):
    """Test la récupération d'un produit par ID"""
    response = client.get(f'/api/produits/{sample_product.id}')
    assert response.status_code == 200
    assert response.json['product']['id'] == sample_product.id
    assert response.json['product']['name'] == sample_product.name


def test_get_nonexistent_product(client):
    """Test la récupération d'un produit inexistant"""
    response = client.get('/api/produits/9999')
    assert response.status_code == 404


def test_create_product_as_admin(client, auth_headers, sample_category):
    """Test la création d'un produit en tant qu'admin"""
    data = {
        'name': 'New Test Product',
        'description': 'A new product for testing',
        'price': 199.99,
        'stock_quantity': 5,
        'category_id': sample_category.id,
        'sku': 'NEW-001'
    }
    
    response = client.post('/api/produits', json=data, headers=auth_headers['admin'])
    assert response.status_code == 201
    assert response.json['product']['name'] == data['name']


def test_create_product_as_client(client, auth_headers, sample_category):
    """Test la création d'un produit en tant que client (doit échouer)"""
    data = {
        'name': 'New Test Product',
        'description': 'A new product for testing',
        'price': 199.99,
        'stock_quantity': 5,
        'category_id': sample_category.id
    }
    
    response = client.post('/api/produits', json=data, headers=auth_headers['client'])
    assert response.status_code == 403


def test_update_product_as_admin(client, auth_headers, sample_product):
    """Test la mise à jour d'un produit en tant qu'admin"""
    data = {
        'name': 'Updated Product Name',
        'description': 'Updated description',
        'price': 149.99,
        'category_id': sample_product.category_id
    }
    
    response = client.put(f'/api/produits/{sample_product.id}', json=data, headers=auth_headers['admin'])
    assert response.status_code == 200
    assert response.json['product']['name'] == data['name']


def test_delete_product_as_admin(client, auth_headers, sample_product):
    """Test la suppression d'un produit en tant qu'admin"""
    response = client.delete(f'/api/produits/{sample_product.id}', headers=auth_headers['admin'])
    assert response.status_code == 200


def test_search_products(client, sample_product):
    """Test la recherche de produits"""
    response = client.get('/api/produits/search?q=Test')
    assert response.status_code == 200
    assert 'products' in response.json
    assert len(response.json['products']) >= 1