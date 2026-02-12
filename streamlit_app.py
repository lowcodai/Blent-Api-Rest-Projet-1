"""
Streamlit Web GUI for DigiMarket API Testing
This application allows users to test API functions as either a user or an admin.
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configuration


def get_api_base_url():
    """Resolve API base URL from environment (Codespaces-aware)."""
    # Allow explicit override via environment variable
    configured_url = os.getenv("API_BASE_URL")
    if configured_url:
        return configured_url.rstrip('/')

    # In Codespaces, use localhost since Streamlit and API run in same container
    # (Public Codespace URLs require authentication that Streamlit can't provide)
    # Users can set API_BASE_URL env var if they need the public URL
    return "http://localhost:5001/api"


API_BASE_URL = get_api_base_url()

# Default test accounts
DEFAULT_USERS = {
    "admin": {"email": "admin@digimarket.com", "password": "admin123"},
    "user1": {"email": "jean.dupont@email.com", "password": "client123"},
    "user2": {"email": "marie.martin@email.com", "password": "client123"},
    "user3": {"email": "pierre.bernard@email.com", "password": "client123"}
}


def init_session_state():
    """Initialize session state variables"""
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False


def make_request(method, endpoint, data=None, requires_auth=True):
    """Make HTTP request to the API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if requires_auth and st.session_state.token:
        headers['Authorization'] = f"Bearer {st.session_state.token}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return None, "Invalid HTTP method"
        
        return response, None
    except requests.exceptions.ConnectionError:
        return None, f"Connection Error: Make sure the API server is running on {API_BASE_URL}"
    except Exception as e:
        return None, f"Error: {str(e)}"


def login_page():
    """Display login page"""
    st.title("🔐 DigiMarket API Tester - Login")
    
    # Show API target URL for debugging
    st.caption(f"🔗 API Target: `{API_BASE_URL}`")
    st.markdown("---")
    
    # Quick login buttons
    st.subheader("Quick Login")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👑 Login as Admin", use_container_width=True):
            login_user(DEFAULT_USERS["admin"]["email"], DEFAULT_USERS["admin"]["password"])
    
    with col2:
        if st.button("👤 Login as Client", use_container_width=True):
            login_user(DEFAULT_USERS["user1"]["email"], DEFAULT_USERS["user1"]["password"])
    
    st.markdown("---")
    
    # Manual login form
    st.subheader("Manual Login")
    with st.form("login_form"):
        email = st.text_input("Email", value="")
        password = st.text_input("Password", type="password", value="")
        submit = st.form_submit_button("Login")
        
        if submit:
            login_user(email, password)
    
    # Show default accounts info
    with st.expander("📋 Default Test Accounts"):
        st.json(DEFAULT_USERS)


def login_user(email, password):
    """Perform login"""
    response, error = make_request('POST', '/auth/login', 
                                   {'email': email, 'password': password},
                                   requires_auth=False)
    
    if error:
        st.error(error)
        return
    
    # Debug: show response details
    with st.expander("🔍 Debug Info"):
        st.write(f"Status Code: {response.status_code}")
        st.write(f"Headers: {dict(response.headers)}")
        st.write(f"Raw Content: {response.text[:500]}")
    
    try:
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get('access_token')
            st.session_state.user_info = data.get('user')
            st.session_state.logged_in = True
            st.success(f"✅ Logged in as {data['user']['first_name']} {data['user']['last_name']} ({data['user']['role']})")
            st.rerun()
        else:
            try:
                error_msg = response.json().get('message', 'Unknown error')
            except (ValueError, requests.exceptions.JSONDecodeError):
                error_msg = f"Non-JSON response: {response.text[:200]}"
            st.error(f"Login failed (Status {response.status_code}): {error_msg}")
    except (ValueError, requests.exceptions.JSONDecodeError) as e:
        st.error(f"❌ Invalid JSON response from API")
        st.error(f"Response content: {response.text[:500]}")
        st.error(f"Error: {str(e)}")


def logout():
    """Perform logout"""
    st.session_state.token = None
    st.session_state.user_info = None
    st.session_state.logged_in = False
    st.rerun()


def display_response(response):
    """Display API response"""
    if response:
        st.write(f"**Status Code:** {response.status_code}")
        
        if response.status_code in [200, 201]:
            st.success("Success!")
        elif response.status_code >= 400:
            st.error("Error!")
        
        try:
            json_data = response.json()
            st.json(json_data)
        except (ValueError, requests.exceptions.JSONDecodeError):
            st.text(response.text)


def auth_section():
    """Authentication endpoints section"""
    st.header("🔐 Authentication")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Update Profile", "Change Password", "List Users (Admin)"])
    
    with tab1:
        st.subheader("Get Profile")
        if st.button("Get My Profile", key="get_profile"):
            response, error = make_request('GET', '/auth/profile')
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tab2:
        st.subheader("Update Profile")
        with st.form("update_profile_form"):
            first_name = st.text_input("First Name", value=st.session_state.user_info.get('first_name', ''))
            last_name = st.text_input("Last Name", value=st.session_state.user_info.get('last_name', ''))
            address = st.text_input("Address")
            phone = st.text_input("Phone")
            submit = st.form_submit_button("Update Profile")
            
            if submit:
                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'address': address,
                    'phone': phone
                }
                response, error = make_request('PUT', '/auth/profile', data)
                if error:
                    st.error(error)
                else:
                    display_response(response)
    
    with tab3:
        st.subheader("Change Password")
        with st.form("change_password_form"):
            old_password = st.text_input("Old Password", type="password")
            new_password = st.text_input("New Password", type="password")
            submit = st.form_submit_button("Change Password")
            
            if submit:
                data = {
                    'old_password': old_password,
                    'new_password': new_password
                }
                response, error = make_request('POST', '/auth/change-password', data)
                if error:
                    st.error(error)
                else:
                    display_response(response)
    
    with tab4:
        st.subheader("List All Users (Admin Only)")
        col1, col2 = st.columns(2)
        with col1:
            page = st.number_input("Page", min_value=1, value=1)
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=100, value=10)
        
        if st.button("List Users", key="list_users"):
            response, error = make_request('GET', '/auth/users', {'page': page, 'per_page': per_page})
            if error:
                st.error(error)
            else:
                display_response(response)


def products_section():
    """Products endpoints section"""
    st.header("📦 Products")
    
    is_admin = st.session_state.user_info.get('role') == 'admin'
    
    if is_admin:
        tabs = st.tabs(["List Products", "Get Product", "Search", "Create (Admin)", "Update (Admin)", "Delete (Admin)", "Update Stock (Admin)"])
    else:
        tabs = st.tabs(["List Products", "Get Product", "Search"])
    
    with tabs[0]:
        st.subheader("List Products")
        col1, col2, col3 = st.columns(3)
        with col1:
            page = st.number_input("Page", min_value=1, value=1, key="prod_page")
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=50, value=10, key="prod_per_page")
        with col3:
            category_id = st.number_input("Category ID (optional)", min_value=0, value=0, key="prod_cat")
        
        if st.button("List Products", key="list_products"):
            params = {'page': page, 'per_page': per_page}
            if category_id > 0:
                params['category_id'] = category_id
            response, error = make_request('GET', '/produits', params, requires_auth=False)
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[1]:
        st.subheader("Get Single Product")
        product_id = st.number_input("Product ID", min_value=1, value=1, key="get_prod_id")
        if st.button("Get Product", key="get_product"):
            response, error = make_request('GET', f'/produits/{product_id}', requires_auth=False)
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[2]:
        st.subheader("Search Products")
        search_query = st.text_input("Search Query", value="", key="search_query")
        if st.button("Search", key="search_products"):
            response, error = make_request('GET', '/produits/search', {'q': search_query}, requires_auth=False)
            if error:
                st.error(error)
            else:
                display_response(response)
    
    if is_admin:
        with tabs[3]:
            st.subheader("Create Product (Admin Only)")
            with st.form("create_product_form"):
                name = st.text_input("Product Name")
                description = st.text_area("Description")
                price = st.number_input("Price", min_value=0.0, value=0.0, step=0.01)
                stock = st.number_input("Stock Quantity", min_value=0, value=0)
                cat_id = st.number_input("Category ID", min_value=1, value=1)
                sku = st.text_input("SKU")
                submit = st.form_submit_button("Create Product")
                
                if submit:
                    data = {
                        'name': name,
                        'description': description,
                        'price': price,
                        'stock_quantity': stock,
                        'category_id': cat_id,
                        'sku': sku
                    }
                    response, error = make_request('POST', '/produits', data)
                    if error:
                        st.error(error)
                    else:
                        display_response(response)
        
        with tabs[4]:
            st.subheader("Update Product (Admin Only)")
            update_id = st.number_input("Product ID to Update", min_value=1, value=1, key="update_prod_id")
            with st.form("update_product_form"):
                name = st.text_input("Product Name", key="upd_name")
                description = st.text_area("Description", key="upd_desc")
                price = st.number_input("Price", min_value=0.0, value=0.0, step=0.01, key="upd_price")
                stock = st.number_input("Stock Quantity", min_value=0, value=0, key="upd_stock")
                submit = st.form_submit_button("Update Product")
                
                if submit:
                    data = {}
                    if name:
                        data['name'] = name
                    if description:
                        data['description'] = description
                    if price > 0:
                        data['price'] = price
                    if stock >= 0:
                        data['stock_quantity'] = stock
                    
                    response, error = make_request('PUT', f'/produits/{update_id}', data)
                    if error:
                        st.error(error)
                    else:
                        display_response(response)
        
        with tabs[5]:
            st.subheader("Delete Product (Admin Only)")
            delete_id = st.number_input("Product ID to Delete", min_value=1, value=1, key="delete_prod_id")
            if st.button("⚠️ Delete Product", key="delete_product"):
                response, error = make_request('DELETE', f'/produits/{delete_id}')
                if error:
                    st.error(error)
                else:
                    display_response(response)
        
        with tabs[6]:
            st.subheader("Update Stock (Admin Only)")
            stock_id = st.number_input("Product ID", min_value=1, value=1, key="stock_prod_id")
            new_stock = st.number_input("New Stock Quantity", min_value=0, value=0, key="new_stock")
            if st.button("Update Stock", key="update_stock"):
                response, error = make_request('PATCH', f'/produits/{stock_id}/stock', {'stock_quantity': new_stock})
                if error:
                    st.error(error)
                else:
                    display_response(response)


def categories_section():
    """Categories endpoints section"""
    st.header("🏷️ Categories")
    
    is_admin = st.session_state.user_info.get('role') == 'admin'
    
    if is_admin:
        tabs = st.tabs(["List Categories", "Get Category", "Create (Admin)", "Update (Admin)", "Delete (Admin)"])
    else:
        tabs = st.tabs(["List Categories", "Get Category"])
    
    with tabs[0]:
        st.subheader("List Categories")
        if st.button("List All Categories", key="list_categories"):
            response, error = make_request('GET', '/categories', requires_auth=False)
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[1]:
        st.subheader("Get Single Category")
        category_id = st.number_input("Category ID", min_value=1, value=1, key="get_cat_id")
        if st.button("Get Category", key="get_category"):
            response, error = make_request('GET', f'/categories/{category_id}', requires_auth=False)
            if error:
                st.error(error)
            else:
                display_response(response)
    
    if is_admin:
        with tabs[2]:
            st.subheader("Create Category (Admin Only)")
            with st.form("create_category_form"):
                name = st.text_input("Category Name")
                description = st.text_area("Description")
                is_active = st.checkbox("Active", value=True)
                submit = st.form_submit_button("Create Category")
                
                if submit:
                    data = {
                        'name': name,
                        'description': description,
                        'is_active': is_active
                    }
                    response, error = make_request('POST', '/categories', data)
                    if error:
                        st.error(error)
                    else:
                        display_response(response)
        
        with tabs[3]:
            st.subheader("Update Category (Admin Only)")
            update_id = st.number_input("Category ID to Update", min_value=1, value=1, key="update_cat_id")
            with st.form("update_category_form"):
                name = st.text_input("Category Name", key="upd_cat_name")
                description = st.text_area("Description", key="upd_cat_desc")
                is_active = st.checkbox("Active", value=True, key="upd_cat_active")
                submit = st.form_submit_button("Update Category")
                
                if submit:
                    data = {}
                    if name:
                        data['name'] = name
                    if description:
                        data['description'] = description
                    data['is_active'] = is_active
                    
                    response, error = make_request('PUT', f'/categories/{update_id}', data)
                    if error:
                        st.error(error)
                    else:
                        display_response(response)
        
        with tabs[4]:
            st.subheader("Delete Category (Admin Only)")
            delete_id = st.number_input("Category ID to Delete", min_value=1, value=1, key="delete_cat_id")
            if st.button("⚠️ Delete Category", key="delete_category"):
                response, error = make_request('DELETE', f'/categories/{delete_id}')
                if error:
                    st.error(error)
                else:
                    display_response(response)


def orders_section():
    """Orders endpoints section"""
    st.header("🛒 Orders")
    
    is_admin = st.session_state.user_info.get('role') == 'admin'
    
    if is_admin:
        tabs = st.tabs(["List Orders", "Get Order", "Order Lines", "Create Order", "Update Status (Admin)", "Cancel Order", "Stats (Admin)"])
    else:
        tabs = st.tabs(["My Orders", "Get Order", "Order Lines", "Create Order", "Cancel Order"])
    
    with tabs[0]:
        st.subheader("List Orders")
        col1, col2 = st.columns(2)
        with col1:
            page = st.number_input("Page", min_value=1, value=1, key="order_page")
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=100, value=10, key="order_per_page")
        
        if st.button("List Orders", key="list_orders"):
            response, error = make_request('GET', '/commandes', {'page': page, 'per_page': per_page})
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[1]:
        st.subheader("Get Single Order")
        order_id = st.number_input("Order ID", min_value=1, value=1, key="get_order_id")
        if st.button("Get Order", key="get_order"):
            response, error = make_request('GET', f'/commandes/{order_id}')
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[2]:
        st.subheader("Get Order Lines")
        lines_order_id = st.number_input("Order ID", min_value=1, value=1, key="lines_order_id")
        if st.button("Get Order Lines", key="get_order_lines"):
            response, error = make_request('GET', f'/commandes/{lines_order_id}/lignes')
            if error:
                st.error(error)
            else:
                display_response(response)
    
    with tabs[3]:
        st.subheader("Create Order")
        with st.form("create_order_form"):
            shipping_address = st.text_area("Shipping Address")
            st.write("Order Lines (one per line, format: product_id,quantity)")
            order_lines_text = st.text_area("Order Lines", value="1,1\n2,2", height=150)
            submit = st.form_submit_button("Create Order")
            
            if submit:
                order_lines = []
                for line in order_lines_text.strip().split('\n'):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            try:
                                product_id = int(parts[0].strip())
                                quantity = int(parts[1].strip())
                                order_lines.append({'product_id': product_id, 'quantity': quantity})
                            except ValueError:
                                st.error(f"Invalid line: {line}")
                
                if order_lines:
                    data = {
                        'shipping_address': shipping_address,
                        'order_lines': order_lines
                    }
                    response, error = make_request('POST', '/commandes', data)
                    if error:
                        st.error(error)
                    else:
                        display_response(response)
                else:
                    st.error("No valid order lines provided")
    
    if is_admin:
        with tabs[4]:
            st.subheader("Update Order Status (Admin Only)")
            status_order_id = st.number_input("Order ID", min_value=1, value=1, key="status_order_id")
            status = st.selectbox("New Status", 
                                ["en_attente", "validee", "expediee", "livree", "annulee"])
            if st.button("Update Status", key="update_order_status"):
                response, error = make_request('PATCH', f'/commandes/{status_order_id}', {'status': status})
                if error:
                    st.error(error)
                else:
                    display_response(response)
        
        with tabs[5]:
            st.subheader("Cancel Order")
            cancel_order_id = st.number_input("Order ID to Cancel", min_value=1, value=1, key="cancel_order_id")
            if st.button("⚠️ Cancel Order", key="cancel_order"):
                response, error = make_request('POST', f'/commandes/{cancel_order_id}/cancel')
                if error:
                    st.error(error)
                else:
                    display_response(response)
        
        with tabs[6]:
            st.subheader("Order Statistics (Admin Only)")
            if st.button("Get Stats", key="get_order_stats"):
                response, error = make_request('GET', '/commandes/stats')
                if error:
                    st.error(error)
                else:
                    display_response(response)
    else:
        with tabs[4]:
            st.subheader("Cancel My Order")
            cancel_order_id = st.number_input("Order ID to Cancel", min_value=1, value=1, key="cancel_order_id_client")
            if st.button("⚠️ Cancel Order", key="cancel_order_client"):
                response, error = make_request('POST', f'/commandes/{cancel_order_id}/cancel')
                if error:
                    st.error(error)
                else:
                    display_response(response)


def main():
    """Main application"""
    st.set_page_config(
        page_title="DigiMarket API Tester",
        page_icon="🛒",
        layout="wide"
    )
    
    init_session_state()
    
    # Check if logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.title("🛒 DigiMarket API Tester")
            st.markdown("---")
            st.write(f"**User:** {st.session_state.user_info.get('first_name')} {st.session_state.user_info.get('last_name')}")
            st.write(f"**Email:** {st.session_state.user_info.get('email')}")
            st.write(f"**Role:** {st.session_state.user_info.get('role').upper()}")
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()
            
            st.markdown("---")
            st.markdown("### Navigation")
            section = st.radio(
                "Select Section:",
                ["🔐 Authentication", "📦 Products", "🏷️ Categories", "🛒 Orders"],
                label_visibility="collapsed"
            )
        
        # Main content
        if "Authentication" in section:
            auth_section()
        elif "Products" in section:
            products_section()
        elif "Categories" in section:
            categories_section()
        elif "Orders" in section:
            orders_section()


if __name__ == "__main__":
    main()
