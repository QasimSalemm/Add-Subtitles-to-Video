import streamlit as st
import overlay_settings as settings_overlay

# ✅ Apply global styles
settings_overlay.apply_styles()

# ==============================
# seo configuration
# ==============================

st.set_page_config(
    page_title="About - Add Text to Video Tool & Team",
    page_icon="images/theme.png"
)

st.markdown(
    """
    <div class="section-card">
        <h1>About Us - Our Mission and Team Behind Add Text to Video</h1>
        <p>Our mission is simple: To provide an easy, fast, and powerful way to add custom overlays, text, and subtitles to your videos.</p>
    </div>
    <div class="section-card">
        <h3>What We Do</h3>
        <ul>
            <li>Help creators, educators, and professionals enhance their videos with overlays.</li>
            <li>Provide a user-friendly tool that works directly in your browser.</li>
            <li>Ensure your data stays private by processing files locally and temporarily.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>Why Choose Us?</h3>
        <ul>
            <li>No permanent storage of your files.</li>
            <li>Simple interface built for productivity.</li>
            <li>Customizable overlays with fonts, colors, and positions.</li>
            <li>Continuous improvements based on user feedback.</li>
        </ul>
    </div>

    <div class="section-card">
        <h3>Our Vision</h3>
        <p>We believe that creating professional-looking videos should be accessible to everyone—whether you're a student, a content creator, or a business professional.</p>
    </div>

    <div class="section-card">
        <h3>Contact Us</h3>
        <p>If you`d like to share feedback, report an issue, or suggest a new feature:</p>
        <ul> 
            <li><b>Email:</b> 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=qasimsaleem317@gmail.com&su=Support%20Request%20-%20Video%20Overlay%20Tool&body=Hello,%0D%0A%0D%0AI would like to ask about..." target="_blank">open in Gmail</a>
            </li>
            <li><b>GitHub:</b> <a href="https://github.com/QasimSalemm/" target="_blank">Qasim Saleem</a></li>
            <li><b>Repository:</b> <a href="https://github.com/QasimSalemm/Add-Subtitles-to-Video" target="_blank">Add Text to Video Tool Repo</a></li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Footer
settings_overlay.footer()
