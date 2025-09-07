import os
import pandas as pd
import streamlit as st

def contact_page():
    st.set_page_config(
        page_title="Contact Us - Text Overlay Studio", 
        layout="wide",
        page_icon="images/theme.png"
        )

    # Page Title (H1)
    st.title("Contact Us")

    st.write(
        "We`d love to hear from you! Whether you have questions, feedback, or need support, "
        "please use the form below to reach out."
    )

    # Contact Information
    st.header("Our Contact Details")
    st.write("🐙 Github: https://github.com/QasimSalemm/")
    st.write("💼 LinkedIn: https://www.linkedin.com/in/qasim-saleem-b74a73168/")


    # =======================
    # Feedback Storage Setup
    # =======================
    FEEDBACK_FILE = "feedback.csv"

    def load_feedback():
        if os.path.exists(FEEDBACK_FILE):
            return pd.read_csv(FEEDBACK_FILE).to_dict("records")
        return []

    def save_feedback(feedback_list):
        df = pd.DataFrame(feedback_list)
        df.to_csv(FEEDBACK_FILE, index=False)

    # =======================
    # Streamlit Feedback Form
    # =======================
    st.header("Feedback Form")
    st.write("We`d love to hear from you! 💬")

    # Initialize session state
    if "feedback_messages" not in st.session_state:
        st.session_state.feedback_messages = load_feedback()

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send Message")

        if submitted:
            if name.strip() and email.strip() and message.strip():
                # Remove old message from same email
                st.session_state.feedback_messages = [
                    fb for fb in st.session_state.feedback_messages if fb["email"] != email
                ]
                # Add new message
                st.session_state.feedback_messages.append({
                    "name": name,
                    "email": email,
                    "message": message
                })
                # Keep only latest 50
                if len(st.session_state.feedback_messages) > 50:
                    st.session_state.feedback_messages.pop(0)
                # Save
                save_feedback(st.session_state.feedback_messages)
                st.success("✅ Thank you! Your message has been received.")
            else:
                st.error("⚠️ Please fill in all fields before submitting.")

    # =======================
    # Display Latest Feedback
    # =======================
    if st.session_state.feedback_messages:
        st.subheader("Latest Feedback")
        # Display feedback messages
        for fb in reversed(st.session_state.feedback_messages):
            with st.container():
                # Name & email
                st.subheader(fb["name"])
                #st.caption(fb["email"])

                # Message
                st.write(fb["message"])

                # Optional divider for style
    # Footer
    st.write("---")
    st.info("💡 We aim to respond to all inquiries within 24-48 hours.")
if __name__ == "__main__":
    contact_page()
