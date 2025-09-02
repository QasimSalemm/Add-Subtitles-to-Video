import streamlit as st
import overlay_settings as settings_overlay

# Apply global styles
settings_overlay.apply_styles()

# Page config
st.set_page_config(
    page_title="How to Use - Add Text to Video Tool",
    page_icon="images/theme.png"
)

# -----------------------------
# H1 Section
# -----------------------------
st.markdown("""
<div class="section-card">
    <h1>How to Use the Add Text to Video Tool</h1>
    <p>Follow these simple steps to add custom text or subtitles to your videos manually or automatically.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Step-by-step Instructions
# -----------------------------
st.markdown("""
<div class="section-card">
    <h2>Step 1: Upload Your Video</h2>
    <p>Click on the upload button to select your video file (MP4, MOV, AVI, MPEG4). Maximum size: 1GB.</p>
</div>

<div class="section-card">
    <h2>Step 2: Add Text Manually</h2>
    <h3>Manual Tab</h3>
    <ul>
        <li>Enter the text you want to overlay.</li>
        <li>Set start and end times for the overlay.</li>
        <li>Choose font, size, color, background, and position.</li>
        <li>Click 'Add Overlay' to save it to the list.</li>
        <li>Repeat for additional overlays.</li>
        <li>Click 'Generate Video' to create the final video with all overlays.</li>
    </ul>
</div>

<div class="section-card">
    <h2>Step 3: Add Text Automatically via CSV/Subtitles</h2>
    <h3>Upload Tab</h3>
    <ul>
        <li>Upload a CSV, XLSX, or subtitle file containing start time, end time, and text.</li>
        <li>Click 'Add Overlays' to automatically import all entries.</li>
        <li>Click 'Generate Video' to create the final video with all text overlays.</li>
    </ul>
</div>

<div class="section-card">
    <h2>Step 4: Customize Text Overlays</h2>
    <p>Adjust font, size, color, background, and position for each overlay to match your style and preferences.</p>
</div>

<div class="section-card">
    <h2>Step 5: Download and Share</h2>
    <p>Once your video is generated, download it and share it wherever you like!</p>
</div>
""", unsafe_allow_html=True)

# Footer
settings_overlay.footer()
