import streamlit as st
from database import get_db_connection

def show():
    st.title("Search Posts")

    search_query = st.text_input("Enter your search query")

    if st.button("Search"):
        if search_query:
            show_search_results(search_query)
        else:
            st.warning("Please enter a search query.")

def show_search_results(query):
    conn = get_db_connection()
    posts = conn.execute("""
        SELECT id, title, content, publish_date 
        FROM posts 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY publish_date DESC
    """, (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()

    if posts:
        st.subheader(f"Search Results for '{query}'")
        for post in posts:
            st.write(f"**{post['title']}**")
            st.write(f"Published on: {post['publish_date']}")
            st.write(post['content'][:200] + "...")  # Display a preview of the content
            if st.button("Read More", key=f"search_post_{post['id']}"):
                st.session_state.current_post = post['id']
                st.rerun()
    else:
        st.info("No results found. Try a different search query.")