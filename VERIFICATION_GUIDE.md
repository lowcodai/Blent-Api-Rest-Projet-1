# 🔍 Guide de Vérification de l'API DigiMarket

Ce guide vous explique comment vérifier que l'API DigiMarket fonctionne correctement.

## 🌐 Configuration Codespace (GitHub Codespaces)

**Si vous utilisez GitHub Codespaces :**

1. **IMPORTANT : Activer l'environnement virtuel d'abord :**
   ```bash
   source .venv/bin/activate
   ```
   
2. **Lancer le serveur :**
   ```bash
   python run.py
   ```

2. **VS Code détectera automatiquement le port 5001** et affichera une notification
3. **Cliquer sur "Make Public"** ou configurer la visibilité dans l'onglet PORTS
4. **Votre API sera accessible via une URL comme :**
   ```
   https://CODESPACE-NAME-5001.app.github.dev
   ```

5. **Pour les tests, remplacer localhost par votre URL Codespace :**
   ```bash
   export API_URL="https://VOTRE-CODESPACE-5001.app.github.dev"
   # Puis utiliser $API_URL dans vos commandes curl
   ```

## 🚀 Étapes de vérification

### 1. Préparation de l'environnement

```bash
# 1. Naviguer vers le dossier du projet
cd /workspaces/Blent-Api-Rest-Projet-1

# 2. Activer l'environnement virtuel
source .venv/bin/activate

# 3. Vérifier que toutes les dépendances sont installées
pip list | grep -E "(Flask|SQLAlchemy|JWT)"
```

### 2. Initialisation de la base de données

```bash
# Exécuter le script d'initialisation automatique
./setup.sh
```

**✅ Résultat attendu :**
- Messages de création des tables
- Génération de données de test (4 utilisateurs, 6 catégories, 16 produits, 3 commandes)
- Affichage des comptes de test

### 3. Lancement du serveur

```bash
# Lancer le serveur Flask
python run.py
```

**✅ Résultat attendu :**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://10.0.0.5:5001
```

## 🔧 Tests de vérification

### 1. Tests automatiques

```bash
# Dans un nouveau terminal (garder le serveur actif)
cd /workspaces/Blent-Api-Rest-Projet-1
./verify_api.sh
```

### 2. Tests manuels rapides

#### A. Test de base
```bash
# Vérifier que l'API répond (local)
curl http://localhost:5001/api/health

# Ou si vous êtes sur Codespace:
curl https://VOTRE-CODESPACE-5001.app.github.dev/api/health

# Réponse attendue:
{"status": "OK", "message": "API is running"}
```

#### B. Test de catalogue (public)
```bash
# Lister les produits
curl http://localhost:5001/api/produits

# Rechercher des produits
curl "http://localhost:5001/api/produits/search?q=MacBook"

# Lister les catégories
curl http://localhost:5001/api/categories
```

#### C. Test d'authentification
```bash
# Connexion admin
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@digimarket.com","password":"admin123"}'

# Inscription nouveau client
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nouveau@client.com",
    "password": "motdepasse123",
    "first_name": "Nouveau",
    "last_name": "Client"
  }'
```

#### D. Test avec authentification
```bash
# 1. Se connecter et récupérer le token
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jean.dupont@email.com","password":"client123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 2. Consulter son profil
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/auth/profile

# 3. Voir ses commandes
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/commandes

# 4. Créer une nouvelle commande
curl -X POST http://localhost:5001/api/commandes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "shipping_address": "123 Nouvelle Adresse, Paris",
    "order_lines": [
      {"product_id": 1, "quantity": 1}
    ]
  }'
```

### 3. Tests unitaires

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_auth.py -v
pytest tests/test_products.py -v
```

## ✅ Critères de validation

### Fonctionnalités de base ✅
- [ ] API répond sur port 5001
- [ ] Endpoint de santé accessible
- [ ] Base de données initialisée avec données de test

### Authentification ✅
- [ ] Inscription utilisateur fonctionne
- [ ] Connexion admin fonctionne  
- [ ] Tokens JWT générés correctement
- [ ] Accès protégé pour endpoints sécurisés

### Catalogue produits ✅
- [ ] Liste des produits accessible publiquement
- [ ] Recherche de produits fonctionne
- [ ] CRUD produits réservé aux admins
- [ ] Gestion des catégories

### Gestion des commandes ✅
- [ ] Création de commandes pour clients connectés
- [ ] Calcul automatique des totaux
- [ ] Vérification des stocks
- [ ] Historique des commandes par client
- [ ] Gestion des statuts (admin)

### Sécurité ✅
- [ ] Authentification JWT obligatoire pour endpoints protégés
- [ ] Permissions par rôle (client/admin)
- [ ] Validation des données d'entrée
- [ ] Gestion d'erreurs appropriée

## 🐛 Dépannage

### Problème : Serveur ne démarre pas
```bash
# Vérifier l'environnement virtuel
which python
pip list | grep Flask

# Vérifier les erreurs de syntaxe
python -m py_compile run.py
python -c "from app import create_app; print('OK')"
```

### Problème : Base de données vide
```bash
# Réinitialiser la base
rm -f digimarket.db
./setup.sh
```

### Problème : Erreur 401/403
- Vérifier que le token est valide
- S'assurer d'utiliser le bon compte (admin vs client)
- Vérifier la syntaxe de l'en-tête Authorization

### Problème : Tests échouent
```bash
# Vérifier que le serveur est lancé
curl http://localhost:5001/api/health

# Relancer les tests
pytest tests/ -v
```

## 📊 Données de test disponibles

### Comptes utilisateurs
```
Admin:
- Email: admin@digimarket.com
- Password: admin123

Clients:
- jean.dupont@email.com / client123
- marie.martin@email.com / client123  
- pierre.bernard@email.com / client123
```

### Produits d'exemple
- MacBook Pro M2 13" (ID: 1)
- Dell XPS 15 (ID: 2)
- PC Gaming Custom RTX 4070 (ID: 5)
- iPhone 15 Pro 256GB (ID: 12)
- Et 12 autres produits...

### Commandes d'exemple
- Commande 1: Jean Dupont (Livrée)
- Commande 2: Marie Martin (Expédiée)  
- Commande 3: Pierre Bernard (En attente)

## 🎯 Tests de performance

```bash
# Test de charge simple (nécessite Apache Bench)
ab -n 100 -c 10 http://localhost:5001/api/produits

# Test de stress sur authentification
for i in {1..10}; do
  curl -X POST http://localhost:5001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@digimarket.com","password":"admin123"}' &
done
wait
```

## 📝 Checklist finale

- [ ] ✅ Serveur démarre sans erreur
- [ ] ✅ Base de données initialisée avec données de test  
- [ ] ✅ Tous les endpoints répondent correctement
- [ ] ✅ Authentification JWT fonctionne
- [ ] ✅ Permissions admin/client respectées
- [ ] ✅ CRUD produits opérationnel
- [ ] ✅ Système de commandes complet
- [ ] ✅ Gestion d'erreurs appropriée
- [ ] ✅ Tests unitaires passent
- [ ] ✅ Documentation accessible

**🎉 Si tous les points sont validés, votre API DigiMarket fonctionne parfaitement !**