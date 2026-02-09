#!/bin/bash
# Script de démarrage de l'API DigiMarket

cd /workspaces/Blent-Api-Rest-Projet-1
source .venv/bin/activate

SSL_ARGS=""
if [ "$HTTPS" = "1" ]; then
	echo "🔐 Mode HTTPS active"
	if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
		echo "🧾 Generation d'un certificat auto-signe (cert.pem/key.pem)..."
		openssl req -x509 -newkey rsa:2048 -nodes \
			-keyout key.pem -out cert.pem -days 365 \
			-subj "/CN=localhost"
	fi
	SSL_ARGS=", ssl_context=('cert.pem','key.pem')"
fi

echo "🚀 Démarrage de l'API DigiMarket sur le port 5001..."
python -c "from app import create_app; app = create_app(); app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False$SSL_ARGS)"
