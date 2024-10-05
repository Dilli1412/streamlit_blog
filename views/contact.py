import streamlit as st

def show():
    st.title("Contact Us")

    st.write("We'd love to hear from you! Please fill out the form below to get in touch.")

    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    if st.button("Send"):
        if name and email and message:
            # Here you would typically send an email or save to database
            # For this example, we'll just show a success message
            st.success("Thank you for your message! We'll get back to you soon.")
        else:
            st.error("Please fill out all fields.")

    st.header("Connect With Us")
    st.write("Follow us on social media:")
    st.write("- [Twitter](https://twitter.com)")
    st.write("- [Facebook](https://facebook.com)")
    st.write("- [Instagram](https://instagram.com)")