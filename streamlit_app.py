import streamlit as st
from streamlit_option_menu import option_menu
from database import init_db
from views import home, blog_post, category, about, contact, search
from views.admin import dashboard, post_management, comment_management, user_management
from utils.auth import login_user, register_user, logout_user, is_authenticated, require_auth, get_current_user, user_profile

def main():
    st.set_page_config(page_title="Streamlit Blog", layout="wide")
    init_db()

    st.title("Streamlit Blog")

    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Sidebar for authentication
    with st.sidebar:
        if not st.session_state.authenticated:
            login_tab, register_tab = st.tabs(["Login", "Register"])
            
            with login_tab:
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                if st.button("Login", key="login_button"):
                    if login_user(username, password):
                        st.rerun()
            
            with register_tab:
                new_username = st.text_input("Username", key="register_username")
                new_email = st.text_input("Email", key="register_email")
                new_password = st.text_input("Password", type="password", key="register_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
                if st.button("Register", key="register_button"):
                    if register_user(new_username, new_email, new_password, confirm_password):
                        st.rerun()
        else:
            st.write(f"Welcome, {st.session_state.user['username']}!")
            if st.button("Logout", key="logout_button"):
                logout_user()
                st.rerun()

    # Main content
    if st.session_state.authenticated:
        # Navigation bar
        if st.session_state.user['role'] == 'admin':
            page = option_menu(
                menu_title=None,
                options=["Home", "Blog Posts", "Categories", "About", "Contact", "Search", "User Profile", "Admin Dashboard"],
                icons=["house", "file-text", "tags", "info-circle", "envelope", "search", "person", "gear"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )
        else:
            page = option_menu(
                menu_title=None,
                options=["Home", "Blog Posts", "Categories", "About", "Contact", "Search", "User Profile"],
                icons=["house", "file-text", "tags", "info-circle", "envelope", "search", "person"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )

        if page == "Home":
            home.show()
        elif page == "Blog Posts":
            blog_post.show_list()
        elif page == "Categories":
            category.show()
        elif page == "About":
            about.show()
        elif page == "Contact":
            contact.show()
        elif page == "Search":
            search.show()
        elif page == "User Profile":
            user_profile()
        elif page == "Admin Dashboard":
            if require_auth(role="admin"):
                admin_dashboard()

        # Footer
        st.sidebar.markdown("---")
        st.sidebar.text("© 2024 Blog. All rights reserved.")
    else:
        st.write("Please login or register to access the blog.")

def admin_dashboard():
    st.title("Admin Dashboard")
    
    admin_page = option_menu(
        menu_title=None,
        options=["Overview", "Post Management", "Comment Management", "User Management"],
        icons=["speedometer2", "file-earmark-text", "chat-dots", "people"],
        menu_icon="list",
        default_index=0,
        orientation="horizontal",
    )

    if admin_page == "Overview":
        dashboard.show()
    elif admin_page == "Post Management":
        post_management.show()
    elif admin_page == "Comment Management":
        comment_management.show()
    elif admin_page == "User Management":
        user_management.show()

if __name__ == "__main__":
    main()