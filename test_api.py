#!/usr/bin/env python3
"""
Script de test simple pour vérifier que l'API DigiMarket fonctionne correctement.
Ce script teste les principales fonctionnalités de l'API.
"""

import requests
import json
import sys
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5001"
API_URL = f"{API_BASE_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200, description=""):
    """Teste un endpoint de l'API"""
    url = f"{API_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=data, headers=headers, timeout=10)
        else:
            print_error(f"Méthode HTTP non supportée: {method}")
            return False, None
        
        if response.status_code == expected_status:
            print_success(f"{description} - Status: {response.status_code}")
            try:
                return True, response.json()
            except:
                return True, response.text
        else:
            print_error(f"{description} - Status: {response.status_code} (attendu: {expected_status})")
            try:
                error_details = response.json()
                print(f"   Détails: {error_details.get('message', 'Pas de message')}")
            except:
                print(f"   Réponse: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print_error(f"{description} - Impossible de se connecter à l'API")
        print_warning("Assurez-vous que le serveur Flask est lancé avec: python run.py")
        return False, None
    except requests.exceptions.Timeout:
        print_error(f"{description} - Timeout de connexion")
        return False, None
    except Exception as e:
        print_error(f"{description} - Erreur: {str(e)}")
        return False, None

def main():
    print(f"{Colors.BOLD}🚀 Test de l'API DigiMarket E-commerce{Colors.ENDC}")
    print("=" * 50)
    
    # Variables pour stocker les tokens
    user_token = None
    admin_token = None
    
    print(f"\n{Colors.YELLOW}1. Tests de base{Colors.ENDC}")
    print("-" * 20)
    
    # Test de l'endpoint racine (utilise API_BASE_URL directement)
    try:
        response = requests.get(API_BASE_URL, timeout=10)
        if response.status_code == 200:
            print_success("Endpoint racine - Status: 200")
        else:
            print_error(f"Endpoint racine - Status: {response.status_code} (attendu: 200)")
            print_error("L'API ne répond pas. Vérifiez que le serveur est lancé.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print_error("Endpoint racine - Impossible de se connecter à l'API")
        print_error("L'API ne répond pas. Vérifiez que le serveur est lancé.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Endpoint racine - Erreur: {str(e)}")
        sys.exit(1)
    
    # Test de l'endpoint de santé
    test_endpoint("GET", "/health", description="Endpoint de santé")
    
    print(f"\n{Colors.YELLOW}2. Test d'authentification{Colors.ENDC}")
    print("-" * 30)
    
    # Test d'inscription
    register_data = {
        "email": f"test_{int(time.time())}@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "address": "123 Test Street",
        "phone": "+33123456789"
    }
    
    success, response = test_endpoint(
        "POST", "/auth/register", 
        data=register_data, 
        expected_status=201,
        description="Inscription d'un utilisateur"
    )
    
    if success and response:
        user_token = response.get('access_token')
        print_info(f"Token utilisateur obtenu: {user_token[:20]}...")
    
    # Test de connexion admin
    admin_login_data = {
        "email": "admin@digimarket.com",
        "password": "admin123"
    }
    
    success, response = test_endpoint(
        "POST", "/auth/login",
        data=admin_login_data,
        description="Connexion administrateur"
    )
    
    if success and response:
        admin_token = response.get('access_token')
        print_info(f"Token admin obtenu: {admin_token[:20]}...")
    
    print(f"\n{Colors.YELLOW}3. Test des catégories{Colors.ENDC}")
    print("-" * 25)
    
    test_endpoint("GET", "/categories", description="Récupération des catégories")
    
    print(f"\n{Colors.YELLOW}4. Test des produits{Colors.ENDC}")
    print("-" * 23)
    
    test_endpoint("GET", "/produits", description="Récupération des produits")
    test_endpoint("GET", "/produits/search?q=MacBook", description="Recherche de produits")
    
    # Test création de produit (admin requis)
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        product_data = {
            "name": "Test Product API",
            "description": "Produit créé via test API",
            "price": 99.99,
            "stock_quantity": 10,
            "category_id": 1,
            "sku": f"TEST-API-{int(time.time())}"
        }
        
        test_endpoint(
            "POST", "/produits",
            data=product_data,
            headers=headers,
            expected_status=201,
            description="Création d'un produit (admin)"
        )
    
    print(f"\n{Colors.YELLOW}5. Test des commandes{Colors.ENDC}")
    print("-" * 23)
    
    if user_token:
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Test création de commande
        order_data = {
            "shipping_address": "123 Rue de Test, Paris, France",
            "order_lines": [
                {
                    "product_id": 1,
                    "quantity": 1
                }
            ]
        }
        
        test_endpoint(
            "POST", "/commandes",
            data=order_data,
            headers=headers,
            expected_status=201,
            description="Création d'une commande"
        )
        
        # Test récupération des commandes
        test_endpoint(
            "GET", "/commandes",
            headers=headers,
            description="Récupération des commandes"
        )
    
    print(f"\n{Colors.YELLOW}6. Test des permissions{Colors.ENDC}")
    print("-" * 26)
    
    # Test accès admin sans authentification
    test_endpoint(
        "POST", "/produits",
        data={"name": "Test"},
        expected_status=401,
        description="Accès admin sans auth (doit échouer)"
    )
    
    # Test accès client à endpoint admin
    if user_token:
        headers = {"Authorization": f"Bearer {user_token}"}
        test_endpoint(
            "POST", "/produits",
            data={"name": "Test"},
            headers=headers,
            expected_status=403,
            description="Accès admin avec token client (doit échouer)"
        )
    
    print(f"\n{Colors.YELLOW}7. Test de gestion d'erreurs{Colors.ENDC}")
    print("-" * 32)
    
    test_endpoint("GET", "/produits/9999", expected_status=404, description="Produit inexistant")
    test_endpoint(
        "POST", "/auth/login",
        data={"email": "invalid@example.com", "password": "wrong"},
        expected_status=401,
        description="Connexion avec identifiants invalides"
    )
    
    print(f"\n{Colors.GREEN}🎉 Tests terminés !{Colors.ENDC}")
    print("=" * 20)
    
    print(f"\n{Colors.BLUE}📊 Fonctionnalités testées:{Colors.ENDC}")
    print("• ✅ Endpoints de base")
    print("• ✅ Authentification (inscription/connexion)")
    print("• ✅ Gestion des produits")
    print("• ✅ Gestion des catégories")
    print("• ✅ Système de commandes")
    print("• ✅ Permissions et autorisations")
    print("• ✅ Gestion d'erreurs")
    
    print(f"\n{Colors.YELLOW}💡 Prochaines étapes:{Colors.ENDC}")
    print("• Lancez les tests unitaires: pytest")
    print("• Consultez la documentation: API_DOCUMENTATION.md")
    print("• Testez avec Postman ou Insomnia pour plus de détails")

if __name__ == "__main__":
    main()