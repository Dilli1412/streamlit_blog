import streamlit as st
from database import get_db_connection, get_posts, get_categories

def show():
    st.title("Welcome to Our Blog")

    # Display featured posts
    st.header("Featured Posts")
    conn = get_db_connection()
    featured_posts = get_posts(conn, limit=3)

    if not featured_posts:
        st.info("No posts have been created yet. Be the first to add a post!")
    else:
        for post in featured_posts:
            with st.expander(f"{post.get('title')} - {post.get('publish_date')}"):
                st.write(post.get('content'))
                st.write(f"Category: {post.get('category')}")
                st.write(f"Tags: {post.get('tags')}")

    # Display categories
    st.sidebar.header("Categories")
    categories = get_categories(conn)

    if not categories:
        st.sidebar.info("No categories available yet.")
    else:
        for category in categories:
            if st.sidebar.button(category.get('category'), key=f"cat_{category.get('category')}"):
                st.session_state.current_category = category.get('category')
                st.rerun()

    # Search bar
    st.sidebar.header("Search")
    search_query = st.sidebar.text_input("Search posts", key="search_input")
    if st.sidebar.button("Search", key="search_button"):
        st.session_state.search_query = search_query
        st.rerun()