# 🌐 DigiMarket API Web GUI

## Description

This is a Streamlit-based web GUI for testing the DigiMarket API REST functions. It provides an intuitive interface to authenticate as a user or admin and test all API endpoints.

## Features

### 🔐 Authentication
- Quick login as Admin or Client
- Manual login with any credentials
- Profile management
- Password change functionality
- User listing (Admin only)

### 📦 Products Management
- **Public Access:**
  - List all products with pagination
  - View product details
  - Search products by name/description
  
- **Admin Only:**
  - Create new products
  - Update existing products
  - Delete products
  - Update stock quantities

### 🏷️ Categories Management
- **Public Access:**
  - List all categories
  - View category details
  
- **Admin Only:**
  - Create new categories
  - Update categories
  - Delete categories

### 🛒 Orders Management
- **Authenticated Users:**
  - List their orders
  - View order details
  - View order lines
  - Create new orders
  - Cancel their orders
  
- **Admin Only:**
  - View all orders
  - Update order status
  - View order statistics

## Installation

1. Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

2. The API server must be running on `http://localhost:5001`:
```bash
python run.py
```

3. Initialize the database if not already done:
```bash
flask --app run.py init-db
flask --app run.py seed-db
```

## Running the GUI

Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

The GUI will open in your default web browser at `http://localhost:8501`

## Default Test Accounts

### Admin Account
- **Email:** admin@digimarket.com
- **Password:** admin123
- **Capabilities:** Full access to all endpoints

### Client Accounts
1. **Jean Dupont**
   - **Email:** jean.dupont@email.com
   - **Password:** client123

2. **Marie Martin**
   - **Email:** marie.martin@email.com
   - **Password:** client123

3. **Pierre Bernard**
   - **Email:** pierre.bernard@email.com
   - **Password:** client123

## Usage Guide

### 1. Login
- Use the quick login buttons for default accounts
- Or enter credentials manually

### 2. Navigate Sections
- Use the sidebar to switch between different API sections
- Each section provides relevant functionality based on your role

### 3. Test API Endpoints
- Fill in the required fields
- Click the action buttons
- View the API response (status code and JSON data)

### 4. Common Workflows

#### As a Client:
1. Login with a client account
2. Browse products and categories
3. Create an order with desired products
4. View your order history
5. Cancel an order if needed

#### As an Admin:
1. Login with the admin account
2. Manage products (create, update, delete, update stock)
3. Manage categories
4. View all orders and update their status
5. View order statistics
6. Manage all users

## API Connection

The GUI connects to the API at `http://localhost:5001/api`

If you need to change the API URL, modify the `API_BASE_URL` constant in `streamlit_app.py`:

```python
API_BASE_URL = "http://localhost:5001/api"
```

## Troubleshooting

### Connection Error
If you see a "Connection Error" message:
1. Make sure the API server is running
2. Check that it's accessible at `http://localhost:5001`
3. Verify the API is properly initialized

### Authentication Failed
If login fails:
1. Check the credentials are correct
2. Ensure the database is seeded with test data
3. Verify the API authentication endpoints are working

### 401 Unauthorized Errors
If you get 401 errors:
1. Your session may have expired - logout and login again
2. Make sure you're using the correct role for restricted endpoints

## Features by Role

| Feature | Public | Client | Admin |
|---------|--------|--------|-------|
| List Products | ✅ | ✅ | ✅ |
| View Product Details | ✅ | ✅ | ✅ |
| Search Products | ✅ | ✅ | ✅ |
| Create Products | ❌ | ❌ | ✅ |
| Update Products | ❌ | ❌ | ✅ |
| Delete Products | ❌ | ❌ | ✅ |
| List Categories | ✅ | ✅ | ✅ |
| View Category Details | ✅ | ✅ | ✅ |
| Manage Categories | ❌ | ❌ | ✅ |
| View Own Profile | ❌ | ✅ | ✅ |
| Update Own Profile | ❌ | ✅ | ✅ |
| Change Password | ❌ | ✅ | ✅ |
| List All Users | ❌ | ❌ | ✅ |
| Create Orders | ❌ | ✅ | ✅ |
| View Own Orders | ❌ | ✅ | ✅ |
| View All Orders | ❌ | ❌ | ✅ |
| Update Order Status | ❌ | ❌ | ✅ |
| Cancel Own Orders | ❌ | ✅ | ✅ |
| Order Statistics | ❌ | ❌ | ✅ |

## Technology Stack

- **Frontend Framework:** Streamlit 1.29.0
- **HTTP Client:** requests
- **Backend API:** Flask REST API
- **Authentication:** JWT tokens

## License

This is part of the DigiMarket API project - MIT License
