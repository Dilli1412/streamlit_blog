import sqlite3
import streamlit as st
from werkzeug.security import generate_password_hash

def init_db():
    with sqlite3.connect('blogsite.db') as conn:
        c = conn.cursor()

        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, 
                     username TEXT UNIQUE, 
                     password TEXT, 
                     email TEXT UNIQUE, 
                     role TEXT)''')

        # Create posts table
        c.execute('''CREATE TABLE IF NOT EXISTS posts
                     (id INTEGER PRIMARY KEY, 
                     title TEXT, 
                     content TEXT, 
                     author_id INTEGER,
                     publish_date TEXT, 
                     category TEXT, 
                     tags TEXT, 
                     featured_image TEXT,
                     FOREIGN KEY (author_id) REFERENCES users(id))''')

        # Create comments table
        c.execute('''CREATE TABLE IF NOT EXISTS comments
                     (id INTEGER PRIMARY KEY, 
                     post_id INTEGER, 
                     user_id INTEGER, 
                     content TEXT,
                     comment_date TEXT, 
                     FOREIGN KEY (post_id) REFERENCES posts(id),
                     FOREIGN KEY (user_id) REFERENCES users(id))''')

        conn.commit()

def get_db_connection():
    conn = sqlite3.connect('blogsite.db')
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_posts(_conn, limit=None, category=None):
    query = "SELECT id, title, content, author_id, publish_date, category, tags FROM posts"
    params = []
    if category:
        query += " WHERE category = ?"
        params.append(category)
    query += " ORDER BY publish_date DESC"
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    with _conn as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        posts = [dict(row) for row in cursor.fetchall()]
    return posts

@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_categories(_conn):
    with _conn as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM posts")
        categories = [dict(row) for row in cursor.fetchall()]
    return categories

def add_post(title, content, author_id, category, tags, featured_image=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO posts (title, content, author_id, publish_date, category, tags, featured_image)
            VALUES (?, ?, ?, datetime('now'), ?, ?, ?)
        """, (title, content, author_id, category, tags, featured_image))
        conn.commit()
    get_posts.clear()
    get_categories.clear()

def update_post(post_id, title, content, category, tags, featured_image=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE posts 
            SET title = ?, content = ?, category = ?, tags = ?, featured_image = ?
            WHERE id = ?
        """, (title, content, category, tags, featured_image, post_id))
        conn.commit()
    get_posts.clear()
    get_categories.clear()

def delete_post(post_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        conn.commit()
    get_posts.clear()
    get_categories.clear()

def get_post(post_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        if post:
            return dict(post)
        return None

def add_comment(post_id, user_id, content):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO comments (post_id, user_id, content, comment_date)
            VALUES (?, ?, ?, datetime('now'))
        """, (post_id, user_id, content))
        conn.commit()

def get_comments(post_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT comments.*, users.username 
            FROM comments 
            JOIN users ON comments.user_id = users.id 
            WHERE post_id = ? 
            ORDER BY comment_date DESC
        """, (post_id,))
        comments = [dict(row) for row in cursor.fetchall()]
    return comments

def add_user(username, email, password, role='subscriber'):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (username, email, hashed_password, role))
        conn.commit()

def get_user(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None

def update_user(user_id, email, role):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET email = ?, role = ?
            WHERE id = ?
        """, (email, role, user_id))
        conn.commit()

def delete_user(user_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.execute("DELETE FROM posts WHERE author_id = ?", (user_id,))
        conn.execute("DELETE FROM comments WHERE user_id = ?", (user_id,))
        conn.commit()
    get_posts.clear()
    get_categories.clear()

def search_posts(query):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM posts 
            WHERE title LIKE ? OR content LIKE ? OR category LIKE ? OR tags LIKE ?
            ORDER BY publish_date DESC
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        posts = [dict(row) for row in cursor.fetchall()]
    return posts

def add_admin():
    admin = get_user('admin')
    if admin:
        print("Admin user already exists")
        return
    
    add_user('admin', 'admin@example.com', 'admin', 'admin')
    print("Admin user created successfully")

if __name__ == "__main__":
    init_db()
    add_admin()