# 🛒 DigiMarket API REST - E-commerce

**API REST Flask pour plateforme e-commerce de matériel informatique**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-red.svg)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentification-orange.svg)](https://jwt.io)

## 📋 Description du projet

L'entreprise DigiMarket, spécialisée dans la vente de matériel informatique, souhaite diversifier son activité en proposant une boutique en ligne. Cette API REST permet la gestion complète de produits, catégories, commandes et utilisateurs avec un système d'authentification JWT sécurisé.

### 🎯 Objectifs
- Gestion des utilisateurs (clients et administrateurs)
- Catalogue produits avec catégories
- Système de commandes complet
- Authentification et autorisation JWT
- API RESTful suivant les bonnes pratiques

## 🚀 Installation et Configuration

### Prérequis
- Python 3.12+
- pip
- Git

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/Blent-Api-Rest-Projet-1.git
cd Blent-Api-Rest-Projet-1
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
```bash
# Copier le fichier d'environnement d'exemple
cp .env.example .env

# Modifier .env avec vos valeurs si nécessaire
```

### 5. Initialiser la base de données
```bash
# Créer les tables
flask --app run.py init-db

# Ajouter des données de test
flask --app run.py seed-db
```

### 6. Lancer l'application
```bash
python run.py
```

L'API sera disponible sur `http://localhost:5001`

## 📚 Structure du projet

```
Blent-Api-Rest-Projet-1/
├── app/
│   ├── __init__.py          # Factory pattern Flask
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── user.py         # Modèle utilisateur
│   │   ├── product.py      # Modèle produit
│   │   ├── category.py     # Modèle catégorie
│   │   └── order.py        # Modèles commande
│   ├── routes/              # Routes API (Blueprints)
│   │   ├── auth.py         # Authentification
│   │   ├── products.py     # Gestion produits
│   │   ├── categories.py   # Gestion catégories
│   │   └── orders.py       # Gestion commandes
│   ├── auth/                # Système d'authentification
│   │   └── decorators.py   # Décorateurs JWT
│   └── utils/               # Utilitaires
│       ├── error_handlers.py  # Gestion d'erreurs
│       └── seed_data.py       # Données de test
├── config/
│   └── config.py           # Configuration application
├── tests/                  # Tests unitaires
├── run.py                  # Point d'entrée principal
├── requirements.txt        # Dépendances Python
└── API_DOCUMENTATION.md    # Documentation API complète
```

## ⚡ Démarrage rapide

### Comptes de test
```bash
# Administrateur
Email: admin@digimarket.com
Mot de passe: admin123

# Clients
Email: jean.dupont@email.com
Mot de passe: client123

Email: marie.martin@email.com  
Mot de passe: client123

Email: pierre.bernard@email.com
Mot de passe: client123
```

### Test rapide de l'API
```bash
# Vérifier que l'API fonctionne
curl http://localhost:5001/api/health

# Connexion admin
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@digimarket.com","password":"admin123"}'

# Lister les produits
curl http://localhost:5001/api/produits
    ```

    ## 🔧 Technologies utilisées

    - **Backend**: Flask 2.3.3
    - **ORM**: SQLAlchemy 2.0.23  
    - **Base de données**: SQLite
    - **Authentification**: JWT (Flask-JWT-Extended)
    - **Sécurité**: bcrypt pour hash des mots de passe
    - **Tests**: pytest
    - **CORS**: Flask-CORS

    ## 📖 Fonctionnalités

    ### 🔐 Gestion des utilisateurs
    - ✅ Inscription et connexion avec JWT
    - ✅ Deux types de profils : Clients et Administrateurs
    - ✅ Gestion de profil (mise à jour, changement mot de passe)
    - ✅ Authentification sécurisée avec hash bcrypt

    ### 📦 Catalogue produits  
    - ✅ CRUD complet des produits (admin)
    - ✅ Consultation publique des produits actifs
    - ✅ Recherche par nom et caractéristiques
    - ✅ Gestion des stocks automatique
    - ✅ Organisation par catégories
    - ✅ Pagination et filtrage

    ### 🛒 Gestion des commandes
    - ✅ Création de commandes avec panier
    - ✅ Suivi des statuts (en attente → validée → expédiée → livrée)
    - ✅ Historique des commandes par client
    - ✅ Gestion administrative des commandes
    - ✅ Calcul automatique des totaux
    - ✅ Vérification des stocks avant validation
    - ✅ Annulation avec remise en stock

    ### 🏷️ Catégories
    - ✅ Gestion des catégories de produits
    - ✅ Organisation hiérarchique du catalogue

    ## 🛡️ Sécurité

    - **Authentification JWT** avec tokens d'accès et de rafraîchissement
    - **Hachage bcrypt** des mots de passe  
    - **Validation stricte** des données d'entrée
    - **Autorisations par rôles** (client/admin)
    - **Protection CORS** configurée
    - **Gestion d'erreurs** sécurisée sans exposition de données sensibles

    ## 📡 API Endpoints

    ### 🔐 Authentification (`/api/auth`)
    | Méthode | Endpoint | Description | Auth |
    |---------|----------|-------------|------|
    | POST | `/register` | Inscription utilisateur | - |
    | POST | `/login` | Connexion | - |
    | GET | `/profile` | Profil utilisateur | ✅ |
    | PUT | `/profile` | Mise à jour profil | ✅ |
    | POST | `/change-password` | Changer mot de passe | ✅ |
    | GET | `/users` | Liste utilisateurs | 👑 Admin |

    ### 📦 Produits (`/api/produits`)
    | Méthode | Endpoint | Description | Auth |
    |---------|----------|-------------|------|
    | GET | `/` | Liste produits | - |
    | GET | `/{id}` | Produit spécifique | - |  
    | GET | `/search?q=term` | Recherche produits | - |
    | POST | `/` | Créer produit | 👑 Admin |
    | PUT | `/{id}` | Modifier produit | 👑 Admin |
    | DELETE | `/{id}` | Supprimer produit | 👑 Admin |
    | PATCH | `/{id}/stock` | Mettre à jour stock | 👑 Admin |

    ### 🏷️ Catégories (`/api/categories`)
    | Méthode | Endpoint | Description | Auth |
    |---------|----------|-------------|------|
    | GET | `/` | Liste catégories | - |
    | GET | `/{id}` | Catégorie spécifique | - |
    | POST | `/` | Créer catégorie | 👑 Admin |
    | PUT | `/{id}` | Modifier catégorie | 👑 Admin |
    | DELETE | `/{id}` | Supprimer catégorie | 👑 Admin |

    ### 🛒 Commandes (`/api/commandes`)
    | Méthode | Endpoint | Description | Auth |
    |---------|----------|-------------|------|
    | GET | `/` | Liste commandes | ✅ |
    | GET | `/{id}` | Commande spécifique | ✅ |
    | GET | `/{id}/lignes` | Lignes de commande | ✅ |
    | POST | `/` | Créer commande | ✅ |
    | PATCH | `/{id}` | Modifier statut | 👑 Admin |
    | POST | `/{id}/cancel` | Annuler commande | ✅ |
    | GET | `/stats` | Statistiques | 👑 Admin |

    > 📘 **Documentation complète** disponible dans [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

    ## 🧪 Tests

    ```bash
    # Lancer tous les tests
    pytest

    # Tests avec coverage
    pytest --cov=app

    # Tests spécifiques
    pytest tests/test_auth.py
    pytest tests/test_products.py
    ```

    ## 📊 Données de test

    L'application inclut un script de génération de données de test avec :
    - **1 administrateur** + **3 clients**
    - **6 catégories** de produits informatiques
    - **16 produits** variés (laptops, PC, composants, périphériques...)
    - **3 commandes** d'exemple avec différents statuts

    ```bash
    # Regénérer les données de test
    flask --app run.py seed-db
    ```

    ## 🚨 Contraintes respectées

    ### Technologies imposées
    - ✅ **Langage**: Python
    - ✅ **Framework**: Flask
    - ✅ **Base de données**: SQLite avec SQLAlchemy ORM
    - ✅ **Authentification**: JWT avec stockage utilisateurs en SQL

    ### Architecture
    - ✅ **Architecture modulaire** avec Blueprints Flask
    - ✅ **Séparation MVC** (Modèles, Contrôleurs, Vues JSON)
    - ✅ **Bonnes pratiques REST** avec codes HTTP appropriés
    - ✅ **Gestion d'erreurs** centralisée
    - ✅ **Code documenté** et commenté

    ### Sécurité
    - ✅ **Authentification JWT** sécurisée
    - ✅ **Hachage des mots de passe**
    - ✅ **Vérification des autorisations** par rôle
    - ✅ **Protection contre injections SQL** (ORM)
    - ✅ **Validation des entrées** stricte

    ### Qualité du code
    - ✅ **Structure de projet** claire et organisée  
    - ✅ **Tests unitaires** et fonctionnels
    - ✅ **Documentation technique** complète
    - ✅ **Base de données initialisée** avec données de test
    - ✅ **Fichier requirements.txt** avec toutes les dépendances

    ## 🔍 Exemples d'utilisation

    ### Scénario complet : Du catalogue à la commande

    ```bash
# 1. Consulter les produits disponibles
curl http://localhost:5001/api/produits

# 2. S'inscrire comme nouveau client  
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nouveau@client.com",
                "password": "monmotdepasse",
                    "first_name": "Alice",
                        "last_name": "Durand",
                            "address": "123 Rue de la Technologie, Paris"
                              }'

                              # 3. Se connecter (récupérer le token)
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"nouveau@client.com","password":"monmotdepasse"}' \
  | jq -r '.access_token')

# 4. Passer une commande
curl -X POST http://localhost:5001/api/commandes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "shipping_address": "123 Rue de la Technologie, Paris",
    "order_lines": [
      {"product_id": 1, "quantity": 1},
      {"product_id": 9, "quantity": 1}
    ]
  }'

# 5. Consulter ses commandes
curl http://localhost:5001/api/commandes \
  -H "Authorization: Bearer $TOKEN"
                                                                      ```

                                                                      ## 📈 Évolutions possibles

                                                                      - **Paiement** : Intégration Stripe/PayPal
                                                                      - **Images** : Upload et gestion d'images produits
                                                                      - **Stock** : Alertes de stock bas
                                                                      - **Email** : Notifications par email
                                                                      - **Recherche avancée** : Filtres par prix, marque, etc.
                                                                      - **Reviews** : Système d'avis clients
                                                                      - **Cache** : Redis pour améliorer les performances
                                                                      - **Docker** : Conteneurisation de l'application

                                                                      ## 👥 Contribution

                                                                      1. Fork le repository
                                                                      2. Créer une branche feature (`git checkout -b feature/NouvelleFeature`)
                                                                      3. Commit les changements (`git commit -m 'Ajout NouvelleFeature'`)
                                                                      4. Push vers la branche (`git push origin feature/NouvelleFeature`)
                                                                      5. Créer une Pull Request

                                                                      ## 📄 Licence

                                                                      Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

                                                                      ---

                                                                      **🎯 Projet réalisé dans le cadre de la formation Blent LLM Engineering**