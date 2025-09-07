import streamlit as st

def terms_and_conditions():
    st.set_page_config(
        page_title="Terms and Conditions - Text Overlay Studio", 
        page_icon="images/theme.png")

    # Title
    st.title("Terms and Conditions")

    # Intro
    st.write(
        "Welcome to Text Overlay Studio. By using our application, you agree to the following terms "
        "and conditions. Please read them carefully before proceeding."
    )

    # Usage terms
    st.subheader("Use of the Application")
    st.write("💡 You may use Text Overlay Studio to add text, captions, or subtitles to your videos.")
    st.write("💡 You are responsible for ensuring that the content you upload does not violate any copyright or laws.")
    st.write("💡 Misuse of the platform for harmful or illegal activities is strictly prohibited.")

    # Intellectual property
    st.subheader("Intellectual Property")
    st.write(
        "All rights to the software, design, and branding of Text Overlay Studio are owned by us. "
        "You may not copy, distribute, or resell the platform without written permission."
    )

    # File handling
    st.subheader("Uploaded Files")
    st.write(
        "Files uploaded to our application are processed securely and stored temporarily. "
        "We do not keep your files after processing is completed."
    )

    # Limitation of liability
    st.subheader("Limitation of Liability")
    st.write(
        "We strive to provide a reliable service, but we are not liable for any damages, losses, "
        "or issues arising from the use of this application."
    )

    # Termination
    st.subheader("Termination of Use")
    st.write(
        "We reserve the right to suspend or terminate access to the platform if a user violates these terms."
    )

    # Updates
    st.subheader("Changes to Terms")
    st.write(
        "We may update these Terms and Conditions from time to time. Any changes will be posted here "
        "with the updated date."
    )

    # Footer
    st.write("---")
    st.info("📌 If you have questions about these Terms & Conditions, please contact us at qasimsaleem317@gmail.com")


if __name__ == "__main__":
    terms_and_conditions()
