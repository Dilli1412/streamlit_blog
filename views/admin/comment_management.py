import streamlit as st
from database import get_db_connection

def show():
    st.header("Comment Management")

    tab1, tab2, tab3 = st.tabs(["View Comments", "Edit Comment", "Delete Comment"])

    with tab1:
        view_comments()
    
    with tab2:
        edit_comment()
    
    with tab3:
        delete_comment()

def view_comments():
    st.subheader("View Comments")
    conn = get_db_connection()
    comments = conn.execute("""
        SELECT comments.id, comments.content, comments.comment_date, users.username, posts.title
        FROM comments
        JOIN users ON comments.user_id = users.id
        JOIN posts ON comments.post_id = posts.id
        ORDER BY comments.comment_date DESC
    """).fetchall()
    conn.close()

    for comment in comments:
        with st.expander(f"Comment by {comment['username']} on '{comment['title']}'"):
            st.text(f"Date: {comment['comment_date']}")
            st.text(f"Content: {comment['content']}")

def edit_comment():
    st.subheader("Edit Comment")
    conn = get_db_connection()
    comments = conn.execute("SELECT id, content FROM comments").fetchall()
    comment_ids = [f"Comment {comment['id']}" for comment in comments]
    selected_comment = st.selectbox("Select Comment to Edit", comment_ids, key="edit_comment_select")

    if selected_comment:
        comment_id = int(selected_comment.split()[1])
        comment = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
        
        with st.expander("Edit Comment"):
            content = st.text_area("Content", value=comment['content'], key="edit_comment_content")

            if st.button("Update Comment", key="update_comment_button"):
                conn.execute("UPDATE comments SET content = ? WHERE id = ?", (content, comment_id))
                conn.commit()
                st.toast("Comment updated successfully!", icon="✅")

    conn.close()

def delete_comment():
    st.subheader("Delete Comment")
    conn = get_db_connection()
    comments = conn.execute("SELECT id, content FROM comments").fetchall()
    comment_ids = [f"Comment {comment['id']}: {comment['content'][:50]}..." for comment in comments]
    selected_comment = st.selectbox("Select Comment to Delete", comment_ids, key="delete_comment_select")

    if selected_comment:
        with st.expander("Confirm Deletion"):
            st.write(f"Are you sure you want to delete this comment?")
            st.text(selected_comment)
            if st.button("Delete Comment", key="delete_comment_button"):
                comment_id = int(selected_comment.split(':')[0].split()[1])
                conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
                conn.commit()
                st.toast("Comment deleted successfully!", icon="✅")

    conn.close()