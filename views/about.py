import streamlit as st

def show():
    st.title("About Our Blog")

    st.write("""
    Welcome to our blog! We are passionate about sharing knowledge and insights on various topics.
    Our team of writers and contributors come from diverse backgrounds, bringing unique perspectives to our content.
    """)

    st.header("Our Mission")
    st.write("""
    Our mission is to provide high-quality, informative, and engaging content to our readers.
    We strive to create a platform where ideas can be shared, discussed, and explored in depth.
    """)

    st.header("Meet the Team")
    st.subheader("John Doe - Founder")
    st.write("John has been writing and blogging for over a decade, with a focus on technology and innovation.")

    st.subheader("Jane Smith - Lead Editor")
    st.write("Jane brings her expertise in content curation and editing to ensure our blog maintains high standards.")

    st.subheader("Mike Johnson - Tech Writer")
    st.write("Mike is our go-to person for all things tech, from the latest gadgets to cutting-edge software.")