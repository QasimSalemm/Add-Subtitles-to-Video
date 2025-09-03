import streamlit as st
import overlay_settings as settings_overlay


# ✅ Apply global styles
settings_overlay.apply_styles()

st.set_page_config(
    page_title="Privacy Policy - Add Text to Video Tool",
    page_icon="images/theme.png"
)


st.markdown(
    """
    <div class="section-card">
        <h1>Privacy Policy - Add Text to Video Tool</h1>
        <p>Your privacy is important to us. This page explains how we collect, use, and protect your information while using the Add Text to Video Tool.</p>
    </div>

    <div class="section-card">
        <h3>1. Information We Collect</h3>
        <ul>
            <li><b>Uploaded Files</b>: Videos, overlay CSV/Excel files, and text you provide.</li>
            <li><b>Generated Outputs</b>: Processed videos with overlays.</li>
            <li><b>Session Data</b>: Temporary settings stored only during your session.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>2. How We Use Your Information</h3>
        <ul>
            <li>Files are processed only to generate your final video.</li>
            <li>Temporary files are not shared with third parties.</li>
            <li>Files are deleted when you clear data or end your session.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>3. Data Retention & Deletion</h3>
        <ul>
            <li><b>Temporary Files</b>: Deleted when you click “Clear All” or end your session.</li>
            <li><b>No Permanent Storage</b>: We do not log or archive your files.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>4. Sharing of Information</h3>
        <p>We do not share, sell, or trade your files or information with anyone. All processing is done locally.</p>
    </div>

    <div class="section-card">
        <h3>5. User Responsibility</h3>
        <p>You are responsible for ensuring uploaded content complies with copyright laws and does not contain sensitive data.</p>
    </div>

    <div class="section-card">
        <h3>6. Security</h3>
        <p>Temporary files are stored securely and deleted when no longer needed. Avoid uploading highly confidential material.</p>
    </div>

    <div class="section-card">
        <h3>7. Changes to This Policy</h3>
        <p>We may update this Privacy Policy from time to time. Updates will be posted within the tool with the effective date.</p>
    </div>

    <div class="section-card">
        <h3>8. Contact</h3>
        <p>If you have any questions about this Privacy Policy, please contact us.</p>
    </div>
    """,
    unsafe_allow_html=True
)

settings_overlay.footer()
