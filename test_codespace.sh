#!/bin/bash

# Script de test spécialement conçu pour GitHub Codespace
echo "🌐 Test API DigiMarket sur GitHub Codespace"
echo "==========================================="

# Détecter l'URL du Codespace
if [ -n "$CODESPACE_NAME" ]; then
    API_URL="https://$CODESPACE_NAME-5001.app.github.dev"
    echo "✅ Codespace détecté"
    echo "🔗 URL API: $API_URL"
else
    API_URL="http://localhost:5001"
    echo "ℹ️  Mode local détecté"
    echo "🔗 URL API: $API_URL"
fi

echo ""

# Fonction de test
test_endpoint() {
    local endpoint=$1
    local description=$2
    local method=${3:-GET}
    local data=$4
    
    echo -n "🔍 $description... "
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -w "%{http_code}" -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" -o /dev/null)
    else
        response=$(curl -s -w "%{http_code}" "$API_URL$endpoint" -o /dev/null)
    fi
    
    if [ "$response" -eq 200 ] || [ "$response" -eq 201 ]; then
        echo "✅ OK ($response)"
    else
        echo "❌ ÉCHEC ($response)"
    fi
}

echo "1. Tests de base"
echo "================"

test_endpoint "" "Endpoint racine"
test_endpoint "/api/health" "API Health"

echo ""
echo "2. Tests des données"
echo "==================="

test_endpoint "/api/categories" "Catégories"
test_endpoint "/api/produits" "Produits" 
test_endpoint "/api/produits/search?q=MacBook" "Recherche produits"

echo ""
echo "3. Test d'authentification"
echo "=========================="

echo -n "🔍 Connexion admin... "
login_response=$(curl -s -X POST "$API_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@digimarket.com","password":"admin123"}')

if echo "$login_response" | grep -q "access_token"; then
    echo "✅ OK"
    
    # Extraire le token
    admin_token=$(echo "$login_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$admin_token" ]; then
        echo "📱 Token obtenu: ${admin_token:0:20}..."
        
        echo -n "🔍 Test accès admin... "
        admin_test=$(curl -s -w "%{http_code}" \
            -H "Authorization: Bearer $admin_token" \
            "$API_URL/api/auth/users" -o /dev/null)
        
        if [ "$admin_test" -eq 200 ]; then
            echo "✅ OK"
        else
            echo "❌ ÉCHEC"
        fi
    fi
else
    echo "❌ ÉCHEC"
fi

echo ""
echo "4. Informations utiles"
echo "====================="

echo "🔗 Endpoints principaux:"
echo "  • Santé API: $API_URL/api/health"
echo "  • Produits: $API_URL/api/produits"
echo "  • Catégories: $API_URL/api/categories"
echo "  • Connexion: POST $API_URL/api/auth/login"
echo ""

echo "📱 Comptes de test:"
echo "  • Admin: admin@digimarket.com / admin123"
echo "  • Client: jean.dupont@email.com / client123"
echo ""

echo "🧪 Commande de test rapide:"
echo "curl $API_URL/api/health"
echo ""

if [ -n "$CODESPACE_NAME" ]; then
    echo "💡 Dans Codespace:"
    echo "  • Le port 5001 devrait être automatiquement forwardé"
    echo "  • Vérifiez l'onglet PORTS dans VS Code"
    echo "  • Changez la visibilité en 'Public' si nécessaire"
fi

echo ""
echo "✨ Test terminé!"