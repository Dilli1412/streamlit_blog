import streamlit as st
from database import get_db_connection
from datetime import datetime
from streamlit_quill import st_quill

def show():
    st.header("Post Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Posts", "Add Post", "Edit Post", "Delete Post"])

    with tab1:
        view_posts()
    
    with tab2:
        add_post()
    
    with tab3:
        edit_post()
    
    with tab4:
        delete_post()

def view_posts():
    st.subheader("View Posts")
    conn = get_db_connection()
    posts = conn.execute("SELECT id, title, author_id, publish_date FROM posts ORDER BY publish_date DESC").fetchall()
    conn.close()

    for post in posts:
        with st.expander(f"Post: {post['title']}"):
            st.text(f"Author ID: {post['author_id']}")
            st.text(f"Publish Date: {post['publish_date']}")

def add_post():
    st.subheader("Add New Post")
    title = st.text_input("Title", key="add_title")
    use_wysiwyg = st.toggle("Use WYSIWYG Editor", key="add_use_wysiwyg")
    
    if use_wysiwyg:
        content = st_quill(placeholder="Write your post content here...", key="add_content_wysiwyg")
    else:
        content = st.text_area("Content", key="add_content_normal")
    
    category = st.text_input("Category", key="add_category")
    tags = st.text_input("Tags (comma-separated)", key="add_tags")

    if st.button("Add Post", key="add_post_button"):
        if title and content and category:
            conn = get_db_connection()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("""
                INSERT INTO posts (title, content, author_id, publish_date, category, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, content, st.session_state.user['id'], current_time, category, tags))
            conn.commit()
            conn.close()
            st.toast("Post added successfully!", icon="✅")
        else:
            st.toast("Please fill out all required fields", icon="🚫")

def edit_post():
    st.subheader("Edit Post")
    conn = get_db_connection()
    posts = conn.execute("SELECT id, title FROM posts").fetchall()
    post_titles = [post['title'] for post in posts]
    selected_post = st.selectbox("Select Post to Edit", post_titles, key="edit_post_select")

    if selected_post:
        post = conn.execute("SELECT * FROM posts WHERE title = ?", (selected_post,)).fetchone()
        title = st.text_input("Title", value=post['title'], key="edit_title")
        
        use_wysiwyg = st.toggle("Use WYSIWYG Editor", key="edit_use_wysiwyg")
        
        if use_wysiwyg:
            content = st_quill(value=post['content'], key="edit_content_wysiwyg")
        else:
            content = st.text_area("Content", value=post['content'], key="edit_content_normal")
        
        category = st.text_input("Category", value=post['category'], key="edit_category")
        tags = st.text_input("Tags", value=post['tags'], key="edit_tags")

        if st.button("Update Post", key="update_post_button"):
            conn.execute("""
                UPDATE posts 
                SET title = ?, content = ?, category = ?, tags = ?
                WHERE id = ?
            """, (title, content, category, tags, post['id']))
            conn.commit()
            st.toast("Post updated successfully!", icon="✅")

    conn.close()

def delete_post():
    st.subheader("Delete Post")
    conn = get_db_connection()
    posts = conn.execute("SELECT id, title FROM posts").fetchall()
    post_titles = [post['title'] for post in posts]
    selected_post = st.selectbox("Select Post to Delete", post_titles, key="delete_post_select")

    if selected_post:
        with st.expander("Confirm Deletion"):
            st.write(f"Are you sure you want to delete the post: '{selected_post}'?")
            if st.button("Delete Post", key="delete_post_button"):
                post = conn.execute("SELECT id FROM posts WHERE title = ?", (selected_post,)).fetchone()
                conn.execute("DELETE FROM posts WHERE id = ?", (post['id'],))
                conn.commit()
                st.toast("Post deleted successfully!", icon="✅")

    conn.close()