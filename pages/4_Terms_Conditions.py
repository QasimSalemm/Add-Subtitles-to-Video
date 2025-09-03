import streamlit as st
import overlay_settings as settings_overlay

# ✅ Apply global styles
settings_overlay.apply_styles()
st.set_page_config(
    page_title="Terms & Conditions - Add Text to Video Tool",
    page_icon="images/theme.png"
)
st.markdown(
    """
    <div class="section-card">
        <h1>Terms & Conditions - Add Text to Video Tool</h1>
        <p>Welcome to the Add Text to Video Tool. By using our service, you agree to comply with and be bound by these Terms & Conditions.</p>
    </div>

    <div class="section-card">
        <h3>1. Acceptance of Terms</h3>
        <p>By using this tool, you agree to comply with these Terms. If you do not agree, do not use the service.</p>
    </div>

    <div class="section-card">
        <h3>2. Usage</h3>
        <ul>
            <li>This tool is provided for personal and professional use.</li>
            <li>You agree not to misuse the service for illegal purposes.</li>
            <li>Uploaded content must not violate copyright or privacy laws.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>3. Data & Privacy</h3>
        <p>We respect your privacy. See our <a href='/Privacy_Policy'>Privacy Policy</a> for details.</p>
    </div>

    <div class="section-card">
        <h3>4. Intellectual Property</h3>
        <p>The tool`s design and code are owned by the developer. You retain rights to your uploaded media.</p>
    </div>

    <div class="section-card">
        <h3>5. Limitation of Liability</h3>
        <ul>
            <li>The tool is provided “as is” without warranties.</li>
            <li>We are not liable for data loss or damages arising from use.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>6. Modifications</h3>
        <p>We reserve the right to modify these Terms at any time. Continued use means you accept the revisions.</p>
    </div>

    <div class="section-card">
        <h3>7. Contact</h3>
        <p>For questions about these Terms, please reach out via our <a href='/Contact'>Contact Us</a> page.</p>
    </div>

    <div class="section-card">
        ✅ By continuing to use <b>Add Text to Video Tool</b>, you acknowledge that you have read and agree to these Terms.
    </div>
    """,
    unsafe_allow_html=True
)

settings_overlay.footer()
