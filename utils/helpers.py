import streamlit as st
from datetime import datetime
from database import get_db_connection

def format_date(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%B %d, %Y at %I:%M %p")

def truncate_text(text, max_length=200):
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def display_post_preview(post):
    st.subheader(post['title'])
    st.write(f"Published on: {format_date(post['publish_date'])}")
    st.write(truncate_text(post['content']))
    if st.button("Read More", key=f"post_{post['id']}"):
        st.session_state.current_post = post['id']
        st.rerun()

def paginate(items, items_per_page=10):
    n_pages = len(items) // items_per_page + (1 if len(items) % items_per_page > 0 else 0)
    page_number = st.number_input('Page', min_value=1, max_value=n_pages, value=1)
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return items[start_index:end_index], page_number, n_pages

def display_pagination_info(page_number, n_pages):
    st.write(f"Page {page_number} of {n_pages}")

def search_posts(query):
    conn = get_db_connection()
    posts = conn.execute("""
        SELECT id, title, content, publish_date 
        FROM posts 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY publish_date DESC
    """, (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return posts

def get_popular_tags(limit=10):
    conn = get_db_connection()
    tags = conn.execute("""
        SELECT tag, COUNT(*) as count
        FROM (
            SELECT trim(value) as tag
            FROM posts, json_each('["' || replace(replace(posts.tags, ' ', ''), ',', '","') || '"]')
        )
        GROUP BY tag
        ORDER BY count DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return tags