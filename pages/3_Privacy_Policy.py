import streamlit as st

def privacy_policy():
    st.set_page_config(
        page_title="Privacy Policy - Text Overlay Studio", 
        page_icon="images/theme.png"
        )

    # Title
    st.title("Privacy Policy")

    # Intro
    st.write(
        "At Text Overlay Studio, we value your privacy and are committed to protecting your "
        "personal information. This Privacy Policy explains how we collect, use, and safeguard "
        "your data when you use our application."
    )

    # Information collection
    st.subheader("Information We Collect")
    st.write("💡 Files you upload, such as videos, CSV, or XLSX subtitle files, are processed securely and temporarily.")
    st.write("💡 Basic information like your name or email may be collected if you contact us through the form.")
    st.write("💡 We do not sell, rent, or trade your personal data.")

    # Usage of information
    st.subheader("How We Use Your Information")
    st.write("💡 To provide video editing and text overlay services.")
    st.write("💡 To respond to your questions, feedback, or support requests.")
    st.write("💡 To improve our platform performance and user experience.")

    # Data security
    st.subheader("Data Security")
    st.write(
        "We use secure methods to handle your uploaded files and personal information. "
        "All temporary files are automatically removed after processing."
    )

    # User control
    st.subheader("Your Rights")
    st.write("💡 You may request deletion of your data at any time by contacting our support team.")
    st.write("💡 You can choose not to provide optional personal information.")

    # Updates
    st.subheader("Changes to This Policy")
    st.write(
        "We may update this Privacy Policy from time to time. Any changes will be posted here "
        "with the updated date."
    )

    st.write("---")
    st.info("📌 If you have any questions about this Privacy Policy, please contact us at qasimsaleem317@gmail.com")


if __name__ == "__main__":
    privacy_policy()
