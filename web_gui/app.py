"""
DigiMarket API Testing Interface
A lightweight Streamlit GUI for testing the DigiMarket API with role-based access control.
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict, Any, Tuple
import os

# Configuration
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5001/api")

# Session state initialization
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None


def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    require_auth: bool = False
) -> Tuple[int, Any]:
    """Make HTTP request to the API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if require_auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return 400, {"error": "Invalid method"}
        
        try:
            return response.status_code, response.json()
        except requests.exceptions.JSONDecodeError:
            return response.status_code, {"message": response.text}
    except requests.exceptions.ConnectionError:
        return 503, {"error": "Cannot connect to API. Make sure the API server is running."}
    except Exception as e:
        return 500, {"error": str(e)}


def display_response(status_code: int, response: Any):
    """Display API response with appropriate formatting"""
    if status_code >= 200 and status_code < 300:
        st.success(f"Status: {status_code}")
    elif status_code >= 400 and status_code < 500:
        st.error(f"Status: {status_code}")
    elif status_code >= 500:
        st.error(f"Status: {status_code} - Server Error")
    else:
        st.info(f"Status: {status_code}")
    
    st.json(response)


def login_page():
    """Login interface"""
    st.title("🔐 DigiMarket API - Login")
    
    st.markdown("""
    ### Welcome to DigiMarket API Testing Interface
    
    Login with your credentials to test the API endpoints.
    
    **Test Accounts:**
    - Admin: `admin@digimarket.com` / `admin123`
    - Client: `jean.dupont@email.com` / `client123`
    """)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", value="admin@digimarket.com")
            password = st.text_input("Password", type="password", value="admin123")
            submit = st.form_submit_button("Login")
            
            if submit:
                status, response = make_request("POST", "/auth/login", {
                    "email": email,
                    "password": password
                })
                
                if status == 200:
                    st.session_state.token = response.get("access_token")
                    st.session_state.refresh_token = response.get("refresh_token")
                    st.session_state.user = response.get("user")
                    st.success(f"Welcome {response['user']['first_name']}!")
                    st.rerun()
                else:
                    display_response(status, response)
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Create New Account")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_first_name = st.text_input("First Name")
            reg_last_name = st.text_input("Last Name")
            reg_address = st.text_area("Address")
            reg_phone = st.text_input("Phone")
            register = st.form_submit_button("Register")
            
            if register:
                status, response = make_request("POST", "/auth/register", {
                    "email": reg_email,
                    "password": reg_password,
                    "first_name": reg_first_name,
                    "last_name": reg_last_name,
                    "address": reg_address,
                    "phone": reg_phone
                })
                
                if status == 201:
                    st.session_state.token = response.get("access_token")
                    st.session_state.refresh_token = response.get("refresh_token")
                    st.session_state.user = response.get("user")
                    st.success("Account created successfully!")
                    st.rerun()
                else:
                    display_response(status, response)


def products_page():
    """Products management interface"""
    st.header("📦 Products")
    
    tab1, tab2, tab3 = st.tabs(["List Products", "Search Products", "Manage Products"])
    
    with tab1:
        st.subheader("All Products")
        col1, col2, col3 = st.columns(3)
        with col1:
            page = st.number_input("Page", min_value=1, value=1, key="prod_page")
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=50, value=10, key="prod_per_page")
        with col3:
            category_id = st.number_input("Category ID (0=all)", min_value=0, value=0, key="prod_cat")
        
        if st.button("Load Products", key="load_products"):
            params = {"page": page, "per_page": per_page}
            if category_id > 0:
                params["category_id"] = category_id
            
            status, response = make_request("GET", "/produits", params=params)
            display_response(status, response)
    
    with tab2:
        st.subheader("Search Products")
        search_term = st.text_input("Search Term", key="search_term")
        if st.button("Search", key="search_btn"):
            if search_term:
                status, response = make_request("GET", "/produits/search", params={"q": search_term})
                display_response(status, response)
            else:
                st.warning("Please enter a search term")
    
    with tab3:
        if st.session_state.user and st.session_state.user.get("role") == "admin":
            st.subheader("Create/Update Product")
            
            action = st.radio("Action", ["Create", "Update", "Delete", "Update Stock"], horizontal=True)
            
            if action == "Create":
                with st.form("create_product"):
                    name = st.text_input("Name")
                    description = st.text_area("Description")
                    price = st.number_input("Price", min_value=0.0, format="%.2f")
                    stock = st.number_input("Stock Quantity", min_value=0, value=0)
                    cat_id = st.number_input("Category ID", min_value=1, value=1)
                    sku = st.text_input("SKU")
                    
                    if st.form_submit_button("Create Product"):
                        status, response = make_request("POST", "/produits", {
                            "name": name,
                            "description": description,
                            "price": price,
                            "stock_quantity": stock,
                            "category_id": cat_id,
                            "sku": sku
                        }, require_auth=True)
                        display_response(status, response)
            
            elif action == "Update":
                with st.form("update_product"):
                    prod_id = st.number_input("Product ID", min_value=1, value=1)
                    name = st.text_input("Name")
                    description = st.text_area("Description")
                    price = st.number_input("Price", min_value=0.0, format="%.2f")
                    stock = st.number_input("Stock Quantity", min_value=0, value=0)
                    cat_id = st.number_input("Category ID", min_value=1, value=1)
                    
                    if st.form_submit_button("Update Product"):
                        status, response = make_request("PUT", f"/produits/{prod_id}", {
                            "name": name,
                            "description": description,
                            "price": price,
                            "stock_quantity": stock,
                            "category_id": cat_id
                        }, require_auth=True)
                        display_response(status, response)
            
            elif action == "Delete":
                prod_id = st.number_input("Product ID to Delete", min_value=1, value=1, key="del_prod_id")
                if st.button("Delete Product", type="primary"):
                    status, response = make_request("DELETE", f"/produits/{prod_id}", require_auth=True)
                    display_response(status, response)
            
            else:  # Update Stock
                with st.form("update_stock"):
                    prod_id = st.number_input("Product ID", min_value=1, value=1)
                    new_stock = st.number_input("New Stock Quantity", min_value=0, value=0)
                    
                    if st.form_submit_button("Update Stock"):
                        status, response = make_request("PATCH", f"/produits/{prod_id}/stock", {
                            "stock_quantity": new_stock
                        }, require_auth=True)
                        display_response(status, response)
        else:
            st.info("⚠️ Admin access required for product management")


def categories_page():
    """Categories management interface"""
    st.header("🏷️ Categories")
    
    tab1, tab2 = st.tabs(["List Categories", "Manage Categories"])
    
    with tab1:
        st.subheader("All Categories")
        if st.button("Load Categories", key="load_categories"):
            status, response = make_request("GET", "/categories")
            display_response(status, response)
    
    with tab2:
        if st.session_state.user and st.session_state.user.get("role") == "admin":
            action = st.radio("Action", ["Create", "Update", "Delete"], horizontal=True, key="cat_action")
            
            if action == "Create":
                with st.form("create_category"):
                    name = st.text_input("Name")
                    description = st.text_area("Description")
                    is_active = st.checkbox("Active", value=True)
                    
                    if st.form_submit_button("Create Category"):
                        status, response = make_request("POST", "/categories", {
                            "name": name,
                            "description": description,
                            "is_active": is_active
                        }, require_auth=True)
                        display_response(status, response)
            
            elif action == "Update":
                with st.form("update_category"):
                    cat_id = st.number_input("Category ID", min_value=1, value=1)
                    name = st.text_input("Name")
                    description = st.text_area("Description")
                    is_active = st.checkbox("Active", value=True)
                    
                    if st.form_submit_button("Update Category"):
                        status, response = make_request("PUT", f"/categories/{cat_id}", {
                            "name": name,
                            "description": description,
                            "is_active": is_active
                        }, require_auth=True)
                        display_response(status, response)
            
            else:  # Delete
                cat_id = st.number_input("Category ID to Delete", min_value=1, value=1, key="del_cat_id")
                if st.button("Delete Category", type="primary"):
                    status, response = make_request("DELETE", f"/categories/{cat_id}", require_auth=True)
                    display_response(status, response)
        else:
            st.info("⚠️ Admin access required for category management")


def orders_page():
    """Orders management interface"""
    st.header("🛒 Orders")
    
    is_admin = st.session_state.user and st.session_state.user.get("role") == "admin"
    
    tab1, tab2, tab3 = st.tabs(["List Orders", "Create Order", "Manage Orders"])
    
    with tab1:
        st.subheader("Orders List")
        col1, col2, col3 = st.columns(3)
        with col1:
            page = st.number_input("Page", min_value=1, value=1, key="order_page")
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=50, value=10, key="order_per_page")
        with col3:
            status_filter = st.selectbox("Status", ["all", "en_attente", "validee", "expediee", "livree", "annulee"], key="order_status")
        
        if st.button("Load Orders", key="load_orders"):
            params = {"page": page, "per_page": per_page}
            if status_filter != "all":
                params["status"] = status_filter
            
            status, response = make_request("GET", "/commandes", params=params, require_auth=True)
            display_response(status, response)
    
    with tab2:
        st.subheader("Create New Order")
        with st.form("create_order"):
            shipping_address = st.text_area("Shipping Address")
            st.markdown("**Order Lines** (one per line: product_id,quantity)")
            order_lines_text = st.text_area("Product ID, Quantity", "1,2\n3,1")
            
            if st.form_submit_button("Create Order"):
                try:
                    order_lines = []
                    for line in order_lines_text.strip().split("\n"):
                        if line.strip():
                            prod_id, qty = line.split(",")
                            order_lines.append({
                                "product_id": int(prod_id.strip()),
                                "quantity": int(qty.strip())
                            })
                    
                    status, response = make_request("POST", "/commandes", {
                        "shipping_address": shipping_address,
                        "order_lines": order_lines
                    }, require_auth=True)
                    display_response(status, response)
                except Exception as e:
                    st.error(f"Invalid order lines format: {e}")
    
    with tab3:
        st.subheader("Order Management")
        
        order_id = st.number_input("Order ID", min_value=1, value=1, key="manage_order_id")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Order Details", key="view_order"):
                status, response = make_request("GET", f"/commandes/{order_id}", require_auth=True)
                display_response(status, response)
        
        with col2:
            if st.button("View Order Lines", key="view_order_lines"):
                status, response = make_request("GET", f"/commandes/{order_id}/lignes", require_auth=True)
                display_response(status, response)
        
        st.divider()
        
        if is_admin:
            st.subheader("Update Order Status (Admin)")
            new_status = st.selectbox("New Status", ["en_attente", "validee", "expediee", "livree", "annulee"], key="new_status")
            if st.button("Update Status", type="primary"):
                status, response = make_request("PATCH", f"/commandes/{order_id}", {
                    "status": new_status
                }, require_auth=True)
                display_response(status, response)
        
        st.divider()
        
        if st.button("Cancel Order", type="primary"):
            status, response = make_request("POST", f"/commandes/{order_id}/cancel", require_auth=True)
            display_response(status, response)


def profile_page():
    """User profile interface"""
    st.header("👤 Profile")
    
    tab1, tab2 = st.tabs(["View Profile", "Update Profile"])
    
    with tab1:
        if st.button("Load Profile"):
            status, response = make_request("GET", "/auth/profile", require_auth=True)
            display_response(status, response)
    
    with tab2:
        with st.form("update_profile"):
            st.subheader("Update Profile Information")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            address = st.text_area("Address")
            phone = st.text_input("Phone")
            
            if st.form_submit_button("Update Profile"):
                data = {}
                if first_name:
                    data["first_name"] = first_name
                if last_name:
                    data["last_name"] = last_name
                if address:
                    data["address"] = address
                if phone:
                    data["phone"] = phone
                
                status, response = make_request("PUT", "/auth/profile", data, require_auth=True)
                display_response(status, response)
        
        st.divider()
        
        with st.form("change_password"):
            st.subheader("Change Password")
            old_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                status, response = make_request("POST", "/auth/change-password", {
                    "old_password": old_password,
                    "new_password": new_password
                }, require_auth=True)
                display_response(status, response)


def admin_page():
    """Admin-specific features"""
    st.header("⚙️ Admin Panel")
    
    tab1, tab2 = st.tabs(["User Management", "Order Statistics"])
    
    with tab1:
        st.subheader("All Users")
        col1, col2 = st.columns(2)
        with col1:
            page = st.number_input("Page", min_value=1, value=1, key="user_page")
        with col2:
            per_page = st.number_input("Per Page", min_value=1, max_value=50, value=10, key="user_per_page")
        
        if st.button("Load Users"):
            status, response = make_request("GET", "/auth/users", 
                                          params={"page": page, "per_page": per_page}, 
                                          require_auth=True)
            display_response(status, response)
    
    with tab2:
        st.subheader("Order Statistics")
        if st.button("Load Statistics"):
            status, response = make_request("GET", "/commandes/stats", require_auth=True)
            display_response(status, response)


def main():
    """Main application"""
    st.set_page_config(
        page_title="DigiMarket API Testing",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check if user is logged in
    if not st.session_state.token:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.title("🛒 DigiMarket API")
        st.divider()
        
        if st.session_state.user:
            st.write(f"👤 **{st.session_state.user['first_name']} {st.session_state.user['last_name']}**")
            st.write(f"📧 {st.session_state.user['email']}")
            st.write(f"🔑 Role: **{st.session_state.user['role'].upper()}**")
            st.divider()
        
        # Navigation
        st.subheader("Navigation")
        
        page = st.radio(
            "Select Page",
            ["Products", "Categories", "Orders", "Profile"],
            label_visibility="collapsed"
        )
        
        # Admin-only navigation
        if st.session_state.user and st.session_state.user.get("role") == "admin":
            admin_nav = st.checkbox("Admin Panel", value=False)
            if admin_nav:
                page = "Admin"
        
        st.divider()
        
        # API Configuration
        with st.expander("⚙️ API Configuration"):
            st.text_input("API Base URL", value=API_BASE_URL, disabled=True)
            st.caption("Set API_BASE_URL environment variable to change")
        
        st.divider()
        
        # Logout
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.refresh_token = None
            st.rerun()
    
    # Main content
    if page == "Products":
        products_page()
    elif page == "Categories":
        categories_page()
    elif page == "Orders":
        orders_page()
    elif page == "Profile":
        profile_page()
    elif page == "Admin":
        admin_page()


if __name__ == "__main__":
    main()
