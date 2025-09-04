import sys
import pandas as pd
import streamlit as st
import utility_functions as uf
from moviepy import VideoFileClip
import overlay_settings as settings_overlay
from PySide6.QtWidgets import QApplication
if not QApplication.instance():
    app = QApplication(sys.argv)

# ✅ Apply global styles
settings_overlay.apply_styles()
# ✅ Works on new Streamlit
import streamlit as st

params = st.query_params

# Robots.txt
if "robots" in params:
    st.html(
        "<pre>User-agent: *\nAllow: /\n"
        "Sitemap: https://videotexteditor.streamlit.app/?sitemap</pre>"
    )
    st.stop()

# Sitemap.xml
if "sitemap" in params:
    st.html(
        """<pre><?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://videotexteditor.streamlit.app/</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://videotexteditor.streamlit.app/About</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://videotexteditor.streamlit.app/Contact</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://videotexteditor.streamlit.app/Privacy_Policy</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://videotexteditor.streamlit.app/Terms_Conditions</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://videotexteditor.streamlit.app/How_To_Use</loc>
    <lastmod>2025-09-03T00:00:00Z</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset></pre>"""
    )
    st.stop()

# ==============================
# seo configuration
# ==============================
st.set_page_config(
    page_title="Add Text to Video Manually or Upload CSV/Subtitles File",
    page_icon="images/theme.png"
)
st.markdown(
    """
    <div class="section-card">
        <h1>Easily Add Custom Text to Your Videos</h1>
        <p>Upload a video and add custom text manually or via CSV/XLSX/subtitles file. Customize font, color, size, and position, then generate your final video with text overlays.</p>
    </div>""",unsafe_allow_html=True
)
# ==============================
# Apply Buttons Width
# ==============================
settings_overlay.local_css("styles/style.css")

# ==============================
# footer Session State Initialization
# ==============================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ==============================
# Video Session State Initialization
# ==============================
if "video_temp" not in st.session_state:
    st.session_state.video_temp = None
if "video_key" not in st.session_state:
    st.session_state.video_key = uf.generate_key("video")

    # ==============================
    # Upload Video
    # ==============================
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"], key=st.session_state.video_key)
if video_file:
    st.session_state.video_temp = uf.save_temp_file(video_file, ".mp4")
    clip = VideoFileClip(st.session_state.video_temp)

    # -----------------------------
    # Show Video Details
    # -----------------------------
    st.subheader("Video Details")
    col1, col2, col3, col4 = st.columns(4)
    col1.success(f"{clip.duration:.2f}s")
    col2.success(f"{clip.w}x{clip.h}")
    col3.success(f"{clip.fps} FPS")

    # -----------------------------
    # n_frames may not always be available; guard it
    # -----------------------------
    n_frames = getattr(getattr(clip, "reader", None), "n_frames", None)
    if n_frames is None:
        try:
            n_frames = int(clip.duration * clip.fps)
        except Exception:
            n_frames = "Unknown"
    col4.success(f"{n_frames} frames")

    manual_entry,upload_files = st.tabs(["Manual Entry", "Upload Overlays File"])

    with manual_entry:

        # ==============================
        # manual overlays Session State Initialization
        # ==============================
        if "manual_overlays" not in st.session_state:
            st.session_state.manual_overlays = []

        # -----------------------------
        # Add Overlay
        # -----------------------------
        st.header("Add Text to Video Manually")
        user_text = st.text_area("Enter text")

        # -----------------------------
        # --- Start Time ---
        # -----------------------------
        st.subheader("Set Overlay Timing")
        sh, sm, ss = st.columns(3)
        with sh:
            start_h = st.number_input("Start Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
        with sm:
            start_m = st.number_input("Start Minute 0 - 59", min_value=0, max_value=59, value=0)
        with ss:
            start_s = st.number_input("Start Second 0 -59", min_value=0, max_value=59, value=0)
        start_time = uf.hms_to_seconds(start_h, start_m, start_s)
        
        # -----------------------------
        # --- End Time ---
        # -----------------------------
        eh, em, es = st.columns(3)
        with eh:
            end_h = st.number_input("End Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
        with em:
            end_m = st.number_input("End Minute 0 - 59", min_value=0, max_value=59, value=0)
        with es:
            end_s = st.number_input("End Second 0 - 59", min_value=0, max_value=59, value=min(5, int(clip.duration)))
        end_time = uf.hms_to_seconds(end_h, end_m, end_s)

        # -----------------------------
        # Add Manual overlay Button
        # -----------------------------
        overlay_settings_data = settings_overlay.overlay_setting_fields("manual_text_overlay_key")
        if st.button("➕ Add Overlay", help='Add the overlay with the specified settings'):
            if user_text.strip() == "":
                st.warning("Please enter some text!")
            elif end_time <= start_time:
                st.warning("End time must be greater than start time.")
            else:
                settings_overlay.add_overlay_entry(user_text, start_time, end_time, overlay_settings_data,target="manual_overlays")
                st.success(f'✅ Overlay added: "{user_text}" ({start_time}-{end_time}s)')
                st.info("💡 Add overlays one by one, then click **'Generate Video'**.")

        if st.session_state.manual_overlays:
            st.subheader("Current Overlays")

            # -----------------------------
            # Show Current Overlays
            # -----------------------------
            settings_overlay.show_current_overlays("manual_text",target='manual_overlays')
            
            # -----------------------------
            # Generate Manual Text Final Video
            # -----------------------------
            settings_overlay.generate_finel_video(clip,"generate_from_manual_video_key",target='manual_overlays')
            
            # -----------------------------
            # Clear All Button
            # -----------------------------
            settings_overlay.clear_all(clip, "manual_text_data_cleared_key", target="manual_overlays")
    with upload_files:

        # ==============================
        # File Overlays Session State Initialization
        # ==============================
        if "file_overlays" not in st.session_state:
            st.session_state.file_overlays = []
        
        # ==============================
        # CSV or xlsx Session State Initialization 
        # ==============================
        if "overlays_temp" not in st.session_state:
            st.session_state.overlays_temp = None
        if "overlays_key" not in st.session_state:
            st.session_state.overlays_key = uf.generate_key("overlays_upload")
            
        # ==============================
        # Upload Overlay File
        # ==============================
        st.header("Upload (CSV or Excel) Subtitles File")
        overlay_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"], key=st.session_state.overlays_key)
        if overlay_file is not None:
            ext = ".csv" if overlay_file.name.endswith(".csv") else ".xlsx"
            st.session_state.overlays_temp = uf.save_temp_file(overlay_file, ext)
            if overlay_file.name.endswith(".csv"):
                df = pd.read_csv(st.session_state.overlays_temp)
            else:
                df = pd.read_excel(st.session_state.overlays_temp)
            
            # ==============================
            # required overlay columns (same fields as your manual app)
            # ==============================
            required_cols = ["text", "start", "end"]
            missing_cols = [c for c in required_cols if c not in df.columns]

            if missing_cols:
                st.error(f"❌ Missing columns: {missing_cols}")
            else:
                st.success("✅ File loaded successfully!")
                st.write("Preview & Edit:")
                edited_df = st.data_editor(df, num_rows="dynamic")

                # ==============================
                # # Add file overlay Button
                # ==============================
                overlay_settings_data = settings_overlay.overlay_setting_fields("file_text_overlay_key")
                if st.button("➕ Add Overlays",help='Add all overlays with specified settings'):
                    for _, overlay in edited_df.iterrows():
                        if str(overlay.get("text", "")).strip() == "":
                            st.warning("Please enter some text!")
                        elif int(overlay['start']) >= int(overlay['end']):
                            st.warning("End time must be greater than start time.")
                        else:
                            settings_overlay.add_overlay_entry(overlay['text'], overlay['start'], overlay['end'], overlay_settings_data,target="file_overlays")
                            st.success(f'✅ Overlay added: \"{overlay['text']}\" ({overlay['start']}-{overlay['end']}s)')
                    st.info("💡 All valid overlays from file have been added. Click **'Generate Video'**.")                        
        if st.session_state.file_overlays:
            st.subheader("Current Overlays")

            # -----------------------------
            # Show Current Overlays
            # -----------------------------
            settings_overlay.show_current_overlays("file_text",target="file_overlays")
            
            # -----------------------------
            # Generate Final Video
            # -----------------------------
            settings_overlay.generate_finel_video(clip=clip,key_suffix="generate_from_file_video_key",target="file_overlays")
  
            # -----------------------------
            # Clear All Button
            # -----------------------------
            settings_overlay.clear_all(clip, "file_text_data_cleared_key", target="file_overlays")
    st.divider()
    reset_header,clear_all = st.columns([5.5,1])
    with reset_header:
        st.subheader("Reset Application")
    with clear_all:
        settings_overlay.clear_all(clip, "all_data_cleared_key", target="video")

# -----------------------------
# footer
# -----------------------------
settings_overlay.footer()
