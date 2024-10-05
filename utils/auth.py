import streamlit as st
from database import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash

def login_user(username, password):
    user = authenticate(username, password)
    if user:
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
        st.toast(f"Welcome back, {username}!", icon="👋")
        return True
    else:
        st.toast("Invalid username or password", icon="🚫")
        return False

def authenticate(username, password):
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user and check_password_hash(user['password'], password):
        return user
    return None

def is_authenticated():
    return st.session_state.get('authenticated', False)

def logout_user():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.toast("You have been logged out", icon="👋")

def register_user(username, email, password, confirm_password):
    if password != confirm_password:
        st.toast("Passwords do not match", icon="🚫")
        return False
    elif not username or not email or not password:
        st.toast("Please fill out all fields", icon="🚫")
        return False
    else:
        with get_db_connection() as conn:
            existing_user = conn.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email)).fetchone()
            if existing_user:
                st.toast("Username or email already exists", icon="🚫")
                return False
            else:
                hashed_password = generate_password_hash(password)
                conn.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                             (username, email, hashed_password, "subscriber"))
                conn.commit()
                st.toast("Registration successful. Please log in.", icon="✅")
                return True

def require_auth(role=None):
    if not is_authenticated():
        st.toast("Please log in to access this page", icon="🔒")
        return False
    elif role and st.session_state.user['role'] != role:
        st.toast(f"You need to be a {role} to access this page", icon="🚫")
        return False
    return True

def get_current_user():
    return st.session_state.user if is_authenticated() else None

def user_profile():
    if not is_authenticated():
        st.toast("Please log in to view your profile", icon="🔒")
        return

    user = get_current_user()
    st.subheader(f"User Profile: {user['username']}")
    st.write(f"Role: {user['role']}")

    with get_db_connection() as conn:
        email = conn.execute("SELECT email FROM users WHERE id = ?", (user['id'],)).fetchone()['email']
    st.write(f"Email: {email}")

    if user['role'] == 'author':
        with get_db_connection() as conn:
            posts = conn.execute("SELECT id, title FROM posts WHERE author_id = ?", (user['id'],)).fetchall()
        st.subheader("Your Posts")
        for post in posts:
            st.write(f"- {post['title']}")

    change_password_form()

def change_password_form():
    st.subheader("Change Password")
    current_password = st.text_input("Current Password", type="password", key="change_current_password")
    new_password = st.text_input("New Password", type="password", key="change_new_password")
    confirm_new_password = st.text_input("Confirm New Password", type="password", key="change_confirm_new_password")

    if st.button("Change Password", key="change_password_button"):
        if not is_authenticated():
            st.toast("You must be logged in to change your password", icon="🔒")
        elif new_password != confirm_new_password:
            st.toast("New passwords do not match", icon="🚫")
        else:
            with get_db_connection() as conn:
                user = conn.execute("SELECT * FROM users WHERE id = ?", (st.session_state.user['id'],)).fetchone()
                if check_password_hash(user['password'], current_password):
                    hashed_new_password = generate_password_hash(new_password)
                    conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_new_password, st.session_state.user['id']))
                    conn.commit()
                    st.toast("Password changed successfully", icon="✅")
                else:
                    st.toast("Current password is incorrect", icon="🚫")