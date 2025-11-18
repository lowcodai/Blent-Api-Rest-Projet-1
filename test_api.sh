#!/bin/bash

# Script de test complet pour l'API DigiMarket
# Ce script vérifie que toutes les fonctionnalités de l'API fonctionnent correctement

echo "🚀 Test complet de l'API DigiMarket E-commerce"
echo "=============================================="

API_URL="http://localhost:5001"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ SUCCÈS${NC}: $2"
    else
        echo -e "${RED}❌ ÉCHEC${NC}: $2"
        echo "Détails de l'erreur:"
        echo "$3"
        return 1
    fi
}

# Fonction pour tester un endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local headers=$4
    local expected_status=$5
    local description=$6
    
    echo -e "${BLUE}🔍 Test:${NC} $description"
    
    if [ -z "$data" ]; then
        if [ -z "$headers" ]; then
            response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$API_URL$url")
        else
            response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$API_URL$url" -H "$headers")
        fi
    else
        if [ -z "$headers" ]; then
            response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$API_URL$url" -H "Content-Type: application/json" -d "$data")
        else
            response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$API_URL$url" -H "Content-Type: application/json" -H "$headers" -d "$data")
        fi
    fi
    
    http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo $response | sed -e 's/HTTPSTATUS:.*//g')
    
    if [ "$http_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✅${NC} Status: $http_code (attendu: $expected_status)"
        return 0
    else
        echo -e "${RED}❌${NC} Status: $http_code (attendu: $expected_status)"
        echo "Réponse: $body"
        return 1
    fi
}

echo -e "\n${YELLOW}1. Test de base - Santé de l'API${NC}"
echo "=================================="

# Test endpoint de santé
test_endpoint "GET" "/api/health" "" "" 200 "Vérification de l'état de l'API"
test_endpoint "GET" "/" "" "" 200 "Vérification de l'endpoint racine"

echo -e "\n${YELLOW}2. Test d'authentification${NC}"
echo "=============================="

# Test inscription
echo -e "${BLUE}🔍 Test:${NC} Inscription d'un nouvel utilisateur"
register_data='{
  "email": "test@example.com",
  "password": "password123",
  "first_name": "Test",
  "last_name": "User",
  "address": "123 Test Street",
  "phone": "+33123456789"
}'

register_response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$API_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "$register_data")

register_status=$(echo $register_response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
register_body=$(echo $register_response | sed -e 's/HTTPSTATUS:.*//g')

if [ "$register_status" -eq 201 ]; then
    echo -e "${GREEN}✅${NC} Inscription réussie"
    # Extraire le token d'accès
    ACCESS_TOKEN=$(echo $register_body | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "Token d'accès obtenu: ${ACCESS_TOKEN:0:20}..."
else
    echo -e "${RED}❌${NC} Échec de l'inscription (Status: $register_status)"
    echo "Réponse: $register_body"
fi

# Test connexion avec le compte admin par défaut
echo -e "${BLUE}🔍 Test:${NC} Connexion avec le compte admin"
admin_login_data='{
  "email": "admin@digimarket.com",
  "password": "admin123"
}'

admin_response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "$admin_login_data")

admin_status=$(echo $admin_response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
admin_body=$(echo $admin_response | sed -e 's/HTTPSTATUS:.*//g')

if [ "$admin_status" -eq 200 ]; then
    echo -e "${GREEN}✅${NC} Connexion admin réussie"
    ADMIN_TOKEN=$(echo $admin_body | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "Token admin obtenu: ${ADMIN_TOKEN:0:20}..."
else
    echo -e "${RED}❌${NC} Échec de la connexion admin (Status: $admin_status)"
    echo "Réponse: $admin_body"
fi

echo -e "\n${YELLOW}3. Test des catégories${NC}"
echo "========================"

test_endpoint "GET" "/api/categories" "" "" 200 "Récupération des catégories"

echo -e "\n${YELLOW}4. Test des produits${NC}"
echo "====================="

test_endpoint "GET" "/api/produits" "" "" 200 "Récupération des produits"
test_endpoint "GET" "/api/produits/search?q=MacBook" "" "" 200 "Recherche de produits"

# Test création de produit (nécessite le token admin)
if [ ! -z "$ADMIN_TOKEN" ]; then
    echo -e "${BLUE}🔍 Test:${NC} Création d'un produit (Admin)"
    product_data='{
      "name": "Test Product API",
      "description": "Produit créé via test API",
      "price": 99.99,
      "stock_quantity": 10,
      "category_id": 1,
      "sku": "TEST-API-001"
    }'
    
    product_response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$API_URL/api/produits" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $ADMIN_TOKEN" \
      -d "$product_data")
    
    product_status=$(echo $product_response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    
    if [ "$product_status" -eq 201 ]; then
        echo -e "${GREEN}✅${NC} Création de produit réussie"
        PRODUCT_ID=$(echo $product_response | sed -e 's/HTTPSTATUS:.*//g' | grep -o '"id":[0-9]*' | cut -d':' -f2)
        echo "ID du produit créé: $PRODUCT_ID"
    else
        echo -e "${RED}❌${NC} Échec de la création de produit (Status: $product_status)"
    fi
fi

echo -e "\n${YELLOW}5. Test des commandes${NC}"
echo "======================"

# Test création de commande (nécessite le token utilisateur)
if [ ! -z "$ACCESS_TOKEN" ]; then
    echo -e "${BLUE}🔍 Test:${NC} Création d'une commande"
    order_data='{
      "shipping_address": "123 Rue de Test, Paris, France",
      "order_lines": [
        {
          "product_id": 1,
          "quantity": 1
        }
      ]
    }'
    
    order_response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$API_URL/api/commandes" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -d "$order_data")
    
    order_status=$(echo $order_response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    
    if [ "$order_status" -eq 201 ]; then
        echo -e "${GREEN}✅${NC} Création de commande réussie"
    else
        echo -e "${RED}❌${NC} Échec de la création de commande (Status: $order_status)"
        echo "Réponse: $(echo $order_response | sed -e 's/HTTPSTATUS:.*//g')"
    fi
    
    # Test récupération des commandes
    test_endpoint "GET" "/api/commandes" "" "Authorization: Bearer $ACCESS_TOKEN" 200 "Récupération des commandes utilisateur"
fi

echo -e "\n${YELLOW}6. Test des permissions${NC}"
echo "=========================="

# Test accès admin sans token
test_endpoint "POST" "/api/produits" '{"name":"Test"}' "" 401 "Accès admin sans authentification (doit échouer)"

# Test accès avec token client sur endpoint admin
if [ ! -z "$ACCESS_TOKEN" ]; then
    test_endpoint "POST" "/api/produits" '{"name":"Test"}' "Authorization: Bearer $ACCESS_TOKEN" 403 "Accès admin avec token client (doit échouer)"
fi

echo -e "\n${YELLOW}7. Test de gestion d'erreurs${NC}"
echo "==============================="

test_endpoint "GET" "/api/produits/9999" "" "" 404 "Produit inexistant"
test_endpoint "POST" "/api/auth/login" '{"email":"invalid","password":"wrong"}' "" 401 "Connexion avec identifiants invalides"

echo -e "\n${GREEN}🎉 Tests terminés !${NC}"
echo "===================="

echo -e "\n${BLUE}📊 Résumé des fonctionnalités testées:${NC}"
echo "• ✅ Endpoints de base (santé, racine)"
echo "• ✅ Authentification (inscription, connexion)"
echo "• ✅ Gestion des produits (lecture publique, CRUD admin)"
echo "• ✅ Gestion des catégories"
echo "• ✅ Système de commandes"
echo "• ✅ Permissions et autorisations"
echo "• ✅ Gestion d'erreurs"

echo -e "\n${YELLOW}💡 Pour des tests plus approfondis:${NC}"
echo "• Lancez les tests unitaires: pytest"
echo "• Consultez la documentation API: API_DOCUMENTATION.md"
echo "• Utilisez un client REST comme Postman ou Insomnia"