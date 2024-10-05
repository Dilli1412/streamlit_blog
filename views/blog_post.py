import streamlit as st
from database import get_db_connection, get_posts, delete_post, add_comment, get_comments

def show_list():
    st.title("Blog Posts")

    conn = get_db_connection()
    posts = get_posts(conn)

    if not posts:
        st.info("No posts have been created yet. Be the first to add a post!")
    else:
        for post in posts:
            with st.expander(f"{post.get('title')} - {post.get('publish_date')}"):
                st.write(post.get('content'))
                st.write(f"Category: {post.get('category')}")
                st.write(f"Tags: {post.get('tags')}")
                
                # Display comments
                comments = get_comments(post.get('id'))
                st.subheader("Comments")
                if not comments:
                    st.info("No comments yet. Be the first to comment!")
                else:
                    for comment in comments:
                        st.text(f"{comment.get('username')} says:")
                        st.write(comment.get('content'))

                # Add new comment
                new_comment = st.text_area("Your comment", key=f"comment_{post.get('id')}")
                if st.button("Submit Comment", key=f"submit_{post.get('id')}"):
                    if 'user_id' in st.session_state:  # Check if user is logged in
                        add_comment(post.get('id'), st.session_state.user['id'], new_comment)
                        st.toast("Comment added successfully!", icon="✅")
                        st.rerun()
                    else:
                        st.toast("Please log in to add a comment.", icon="🔒")

                # Delete post (for admin users)
                if st.session_state.user.get('role') == 'admin':
                    if st.button("Delete Post", key=f"delete_{post.get('id')}"):
                        delete_post(post.get('id'))
                        st.success("Post deleted successfully!")
                        st.rerun()