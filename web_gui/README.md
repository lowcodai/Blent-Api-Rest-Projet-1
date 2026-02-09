# DigiMarket API Web GUI

A lightweight Streamlit-based web interface for testing the DigiMarket API with role-based access control.

## Features

- **Authentication**: Login and registration with JWT token management
- **Role-Based Access**: Different interfaces for admin and client users
- **Product Management**: List, search, create, update, and delete products (admin)
- **Category Management**: Manage product categories (admin)
- **Order Management**: Create and view orders, update status (admin)
- **User Profile**: View and update profile information
- **Admin Panel**: User management and order statistics (admin only)

## Running the Application

### Prerequisites

1. Make sure the API server is running on port 5001:
   ```bash
   python run.py
   ```

2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

### Start the Web GUI

From the repository root:
```bash
streamlit run web_gui/app.py
```

The interface will be available at `http://localhost:8501`

### In Codespaces

The Streamlit app works seamlessly in GitHub Codespaces with automatic port forwarding.

1. Start the API server:
   ```bash
   python run.py
   ```

2. In a new terminal, start the web GUI:
   ```bash
   streamlit run web_gui/app.py
   ```

3. Codespaces will automatically forward port 8501 and provide a URL to access the interface.

## Test Accounts

Use these pre-configured accounts to test the interface:

- **Admin**: 
  - Email: `admin@digimarket.com`
  - Password: `admin123`

- **Client**: 
  - Email: `jean.dupont@email.com`
  - Password: `client123`

## Usage Guide

### For Clients

After logging in as a client, you can:

1. **Browse Products**: View all available products with pagination and filtering
2. **Search Products**: Search for products by name or description
3. **Create Orders**: Place orders by selecting products and quantities
4. **View Orders**: See your order history and status
5. **Manage Profile**: Update your personal information and change password

### For Administrators

Admin users have access to all client features plus:

1. **Product Management**: 
   - Create new products
   - Update existing products
   - Delete products
   - Update stock quantities

2. **Category Management**:
   - Create new categories
   - Update existing categories
   - Delete categories

3. **Order Management**:
   - View all orders from all users
   - Update order status (pending, validated, shipped, delivered, cancelled)
   - View order statistics

4. **User Management**:
   - View all registered users
   - See user details and roles

## API Configuration

By default, the interface connects to `http://localhost:5001/api`.

To change the API URL, set the `API_BASE_URL` environment variable:

```bash
export API_BASE_URL=http://your-api-url:port/api
streamlit run web_gui/app.py
```

## Response Display

All API responses are displayed with:
- HTTP status code (color-coded: green for success, red for errors)
- Full JSON response body
- Request parameters shown in the UI

## Error Handling

The interface handles common scenarios:
- Connection errors (API not running)
- Authentication errors (invalid credentials, expired tokens)
- Authorization errors (insufficient permissions)
- Validation errors (invalid input)
- Server errors

## Technology Stack

- **Streamlit**: Web framework for rapid UI development
- **Requests**: HTTP library for API communication
- **Python 3.10+**: Programming language

## File Structure

```
web_gui/
├── app.py          # Main Streamlit application
└── README.md       # This file
```
