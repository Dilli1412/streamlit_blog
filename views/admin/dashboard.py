import streamlit as st
from database import get_db_connection

def show():
    st.header("Admin Dashboard Overview")

    conn = get_db_connection()
    total_posts = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    total_comments = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Posts", total_posts)
    col2.metric("Total Comments", total_comments)
    col3.metric("Total Users", total_users)

    st.subheader("Recent Activity")
    conn = get_db_connection()
    recent_posts = conn.execute("SELECT title, publish_date FROM posts ORDER BY publish_date DESC LIMIT 5").fetchall()
    recent_comments = conn.execute("SELECT content, comment_date FROM comments ORDER BY comment_date DESC LIMIT 5").fetchall()
    conn.close()

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Recent Posts:")
        for post in recent_posts:
            st.write(f"- {post['title']} ({post['publish_date']})")

    with col2:
        st.write("Recent Comments:")
        for comment in recent_comments:
            st.write(f"- {comment['content'][:50]}... ({comment['comment_date']})")