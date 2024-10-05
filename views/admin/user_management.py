import streamlit as st
from database import get_db_connection
from werkzeug.security import generate_password_hash

def show():
    st.header("User Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Users", "Add User", "Edit User", "Delete User"])

    with tab1:
        view_users()
    
    with tab2:
        add_user()
    
    with tab3:
        edit_user()
    
    with tab4:
        delete_user()

def view_users():
    st.subheader("View Users")
    conn = get_db_connection()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    conn.close()

    for user in users:
        st.text(f"Username: {user['username']}")
        st.text(f"Email: {user['email']}")
        st.text(f"Role: {user['role']}")
        st.markdown("---")

def add_user():
    st.subheader("Add New User")
    username = st.text_input("Username", key="add_username")
    email = st.text_input("Email", key="add_email")
    password = st.text_input("Password", type="password", key="add_password")
    role = st.selectbox("Role", ["admin", "author", "subscriber"], key="add_role")

    if st.button("Add User", key="add_user_button"):
        if username and email and password:
            conn = get_db_connection()
            hashed_password = generate_password_hash(password)
            conn.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                         (username, email, hashed_password, role))
            conn.commit()
            conn.close()
            st.toast("User added successfully!", icon="✅")
        else:
            st.toast("Please fill out all fields", icon="🚫")

def edit_user():
    st.subheader("Edit User")
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    user_names = [user['username'] for user in users]
    selected_user = st.selectbox("Select User to Edit", user_names, key="edit_user_select")

    if selected_user:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (selected_user,)).fetchone()
        email = st.text_input("Email", value=user['email'], key="edit_email")
        role = st.selectbox("Role", ["admin", "author", "subscriber"], 
                            index=["admin", "author", "subscriber"].index(user['role']),
                            key="edit_role")
        new_password = st.text_input("New Password (leave blank to keep current)", type="password", key="edit_password")

        if st.button("Update User", key="update_user_button"):
            if new_password:
                hashed_password = generate_password_hash(new_password)
                conn.execute("UPDATE users SET email = ?, role = ?, password = ? WHERE id = ?", (email, role, hashed_password, user['id']))
            else:
                conn.execute("UPDATE users SET email = ?, role = ? WHERE id = ?", (email, role, user['id']))
            conn.commit()
            st.toast("User updated successfully!", icon="✅")

    conn.close()

def delete_user():
    st.subheader("Delete User")
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    user_names = [user['username'] for user in users]
    selected_user = st.selectbox("Select User to Delete", user_names, key="delete_user_select")

    if selected_user and st.button("Delete User", key="delete_user_button"):
        user = conn.execute("SELECT id FROM users WHERE username = ?", (selected_user,)).fetchone()
        conn.execute("DELETE FROM users WHERE id = ?", (user['id'],))
        conn.commit()
        st.toast("User deleted successfully!", icon="✅")

    conn.close()