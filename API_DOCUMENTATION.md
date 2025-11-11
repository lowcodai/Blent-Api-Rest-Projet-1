# Documentation de l'API DigiMarket E-commerce

## Aperçu

Cette API REST permet la gestion complète d'une boutique en ligne de matériel informatique. Elle offre des fonctionnalités pour la gestion des utilisateurs, produits, catégories et commandes, avec un système d'authentification JWT.

## Base URL
```
http://localhost:5000/api
```

## Authentification

L'API utilise des tokens JWT (JSON Web Tokens) pour l'authentification. Après connexion, incluez le token dans l'en-tête de vos requêtes :

```
Authorization: Bearer <votre_token>
```

## Codes de réponse HTTP

- `200 OK` - Succès
- `201 Created` - Ressource créée avec succès
- `400 Bad Request` - Données invalides
- `401 Unauthorized` - Authentification requise
- `403 Forbidden` - Accès refusé
- `404 Not Found` - Ressource introuvable
- `409 Conflict` - Conflit (ex: email déjà utilisé)
- `422 Unprocessable Entity` - Erreur de logique métier
- `500 Internal Server Error` - Erreur serveur

---

## 🔐 Authentification

### POST /auth/register
Inscription d'un nouvel utilisateur.

**Corps de la requête :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123",
  "first_name": "Jean",
  "last_name": "Dupont",
  "address": "123 Rue de la Paix, Paris",
  "phone": "+33123456789"
}
```

**Réponse (201) :**
```json
{
  "message": "Utilisateur créé avec succès",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "role": "client",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

### POST /auth/login
Connexion d'un utilisateur.

**Corps de la requête :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

### GET /auth/profile
🔒 Récupérer le profil de l'utilisateur connecté.

### PUT /auth/profile
🔒 Mettre à jour le profil de l'utilisateur.

### POST /auth/change-password
🔒 Changer le mot de passe.

### GET /auth/users
🔒 **Admin uniquement** - Lister tous les utilisateurs avec pagination.

---

## 📦 Produits

### GET /produits
Récupérer la liste des produits avec pagination et recherche.

**Paramètres de requête :**
- `page` (int, défaut: 1) - Numéro de page
- `per_page` (int, défaut: 10, max: 50) - Produits par page
- `search` (string) - Recherche par nom
- `category_id` (int) - Filtrer par catégorie

**Réponse (200) :**
```json
{
  "products": [
    {
      "id": 1,
      "name": "MacBook Pro M2 13\"",
      "description": "MacBook Pro avec puce M2...",
      "price": 1299.99,
      "stock_quantity": 15,
      "category_id": 1,
      "category_name": "Ordinateurs Portables",
      "sku": "MBP-M2-13-256",
      "is_active": true,
      "is_available": true,
      "created_at": "2024-01-01T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 5,
    "per_page": 10,
    "total": 42
  }
}
```

### GET /produits/{id}
Récupérer un produit spécifique.

### GET /produits/search
Recherche de produits par nom ou description.

**Paramètres :**
- `q` (string, requis) - Terme de recherche

### POST /produits
🔒 **Admin uniquement** - Créer un nouveau produit.

**Corps de la requête :**
```json
{
  "name": "Nom du produit",
  "description": "Description détaillée",
  "price": 199.99,
  "stock_quantity": 10,
  "category_id": 1,
  "sku": "PROD-001"
}
```

### PUT /produits/{id}
🔒 **Admin uniquement** - Mettre à jour un produit.

### DELETE /produits/{id}
🔒 **Admin uniquement** - Supprimer un produit.

### PATCH /produits/{id}/stock
🔒 **Admin uniquement** - Mettre à jour uniquement le stock.

---

## 🏷️ Catégories

### GET /categories
Récupérer la liste des catégories.

### GET /categories/{id}
Récupérer une catégorie spécifique.

### POST /categories
🔒 **Admin uniquement** - Créer une nouvelle catégorie.

**Corps de la requête :**
```json
{
  "name": "Nouvelle Catégorie",
  "description": "Description de la catégorie",
  "is_active": true
}
```

### PUT /categories/{id}
🔒 **Admin uniquement** - Mettre à jour une catégorie.

### DELETE /categories/{id}
🔒 **Admin uniquement** - Supprimer une catégorie.

---

## 🛒 Commandes

### GET /commandes
🔒 Récupérer les commandes (toutes pour admin, personnelles pour client).

**Paramètres :**
- `page` (int) - Pagination
- `per_page` (int) - Items par page
- `status` (string) - Filtrer par statut

### GET /commandes/{id}
🔒 Récupérer une commande spécifique.

### GET /commandes/{id}/lignes
🔒 Consulter les lignes d'une commande.

### POST /commandes
🔒 Créer une nouvelle commande.

**Corps de la requête :**
```json
{
  "shipping_address": "123 Rue de Livraison, Paris",
  "order_lines": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

**Réponse (201) :**
```json
{
  "message": "Commande créée avec succès",
  "order": {
    "id": 1,
    "user_id": 1,
    "status": "en_attente",
    "total_amount": 2599.98,
    "shipping_address": "123 Rue de Livraison, Paris",
    "created_at": "2024-01-01T10:00:00",
    "order_lines": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "MacBook Pro M2 13\"",
        "quantity": 2,
        "unit_price": 1299.99,
        "subtotal": 2599.98
      }
    ]
  }
}
```

### PATCH /commandes/{id}
🔒 **Admin uniquement** - Mettre à jour le statut d'une commande.

**Corps de la requête :**
```json
{
  "status": "validee"
}
```

**Statuts valides :**
- `en_attente` - En attente
- `validee` - Validée
- `expediee` - Expédiée  
- `livree` - Livrée
- `annulee` - Annulée

### POST /commandes/{id}/cancel
🔒 Annuler une commande (client pour ses commandes, admin pour toutes).

### GET /commandes/stats
🔒 **Admin uniquement** - Statistiques des commandes.

---

## 🎯 Exemples d'utilisation

### 1. Inscription et connexion
```bash
# Inscription
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "password123",
    "first_name": "Jean",
    "last_name": "Dupont"
  }'

# Connexion
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "password123"
  }'
```

### 2. Consulter les produits
```bash
# Tous les produits
curl http://localhost:5000/api/produits

# Recherche
curl "http://localhost:5000/api/produits/search?q=MacBook"

# Par catégorie
curl "http://localhost:5000/api/produits?category_id=1"
```

### 3. Passer une commande
```bash
curl -X POST http://localhost:5000/api/commandes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "shipping_address": "123 Rue de la Paix, Paris",
    "order_lines": [
      {
        "product_id": 1,
        "quantity": 1
      }
    ]
  }'
```

---

## 🛡️ Sécurité

### Authentification JWT
- Tokens d'accès valides 1 heure
- Tokens de rafraîchissement valides 30 jours
- Mots de passe hachés avec bcrypt

### Autorisations
- **Public** : Consultation des produits et catégories actifs
- **Client authentifié** : Gestion du profil, passage de commandes, consultation de ses commandes
- **Administrateur** : Toutes les opérations, gestion des stocks, suivi des commandes

### Validation
- Validation des emails avec regex
- Mots de passe minimum 6 caractères
- Validation des données d'entrée sur tous les endpoints
- Protection contre les injections SQL avec SQLAlchemy ORM

---

## 📊 Codes d'erreur spécifiques

### Erreurs de validation (400)
```json
{
  "error": "Erreur de validation",
  "message": "Cette adresse email est déjà utilisée",
  "field": "email"
}
```

### Erreurs métier (422)
```json
{
  "error": "Erreur métier",
  "message": "Stock insuffisant. Disponible: 2, Demandé: 5",
  "code": "INSUFFICIENT_STOCK"
}
```

### Erreurs d'authentification (401)
```json
{
  "error": "Token invalide",
  "message": "Le token d'authentification est invalide ou a expiré"
}
```

### Erreurs d'autorisation (403)
```json
{
  "error": "Accès refusé",
  "message": "Droits administrateur requis"
}
```