import streamlit as st
import overlay_settings as settings_overlay
import pandas as pd
import os


# ✅ Apply global styles
settings_overlay.apply_styles()
st.set_page_config(
    page_title="Contact - Add Text to Video Tool",
    page_icon="images/theme.png"
)

st.markdown(
    """
    <div class="section-card">
        <h1>Contact Us - Add Text to Video Tool</h1>
        <p>If you have questions, feedback, or suggestions, we`d love to hear from you. Reach out using the details below.</p>
    </div>

    <div class="section-card">
        <h3>Email</h3>
        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=qasimsaleem317@gmail.com&su=Support%20Request%20-%20Video%20Overlay%20Tool&body=Hello,%0D%0A%0D%0AI would like to ask about..." target="_blank">
            qasimsaleem317@gmail.com
        </a>
    </div>

    <div class="section-card">
        <h3>Social / Community</h3>
        <ul>
            <li><b>GitHub:</b> <a href="https://github.com/QasimSalemm/">https://github.com/QasimSalemm/</a></li>
            <li><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/qasim-saleem-b74a73168/">https://www.linkedin.com/in/qasim-saleem-b74a73168/</a></li>
        </ul>
    </div>

    <div class="section-card">
        <h3>Feedback Form</h3>
    </div>
    """,
    unsafe_allow_html=True
)

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
st.markdown("We`d love to hear from you! 💬")

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
    for fb in reversed(st.session_state.feedback_messages):
        st.markdown(
            f"""
            <div class="section-card">
                <div style="margin-bottom: 8px;">
                    <span style="font-weight:600; font-size:16px; color:#2C3E50;">
                        {fb['name']}
                    </span>
                    <span style="font-size:13px; color:#777; margin-left:8px;">
                        {fb['email']}
                    </span>
                </div>
                <div style="font-size:15px; line-height:1.6; color:#333;">
                    {fb['message']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ✅ Footer
settings_overlay.footer()
