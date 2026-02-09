#!/bin/bash

# Script pour configurer et tester l'API dans Codespace
echo "🚀 Configuration automatique pour GitHub Codespace"
echo "=================================================="

# Détecter si nous sommes dans un Codespace
if [ -n "$CODESPACE_NAME" ]; then
    echo "✅ Codespace détecté: $CODESPACE_NAME"
    
    # Construire l'URL de base du Codespace
    CODESPACE_URL="https://$CODESPACE_NAME-5001.app.github.dev"
    echo "🌐 URL de votre API: $CODESPACE_URL"
    
    # Exporter l'URL pour les autres scripts
    export API_URL="$CODESPACE_URL"
    echo "export API_URL=\"$CODESPACE_URL\"" >> ~/.bashrc
    
    echo ""
    echo "📝 Configuration terminée!"
    echo "Votre API sera accessible sur: $CODESPACE_URL"
    echo ""
    echo "🔗 Liens utiles:"
    echo "  • API Health: $CODESPACE_URL/api/health"
    echo "  • API Root: $CODESPACE_URL/"
    echo "  • Produits: $CODESPACE_URL/api/produits"
    echo "  • Documentation: Consultez API_DOCUMENTATION.md"
    echo ""
    echo "🧪 Pour tester votre API:"
    echo "  1. Lancez le serveur: python run.py"
    echo "  2. Dans un autre terminal: ./test_codespace.sh"
    
else
    echo "ℹ️  Pas de Codespace détecté - configuration locale"
    export API_URL="http://localhost:5001"
    echo "🌐 URL locale: $API_URL"
fi

echo ""
echo "✨ Prêt à commencer!"