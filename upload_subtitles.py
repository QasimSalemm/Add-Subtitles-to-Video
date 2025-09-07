import os
import sys
import tempfile
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image
import streamlit as st
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from PySide6.QtWidgets import QApplication
if not QApplication.instance():
    app = QApplication(sys.argv)
# import helpers from your existing project
import utility_functions as uf
import image_generator as ig
import position_helpers as ph
import streamlit_logger as sl
# ==============================
# Page Configuration
# ==============================
st.title("🎬 Video Overlay Generator (from Excel/CSV)")
# ==============================
# Session State Initialization
# ==============================
if "video_temp" not in st.session_state:
    st.session_state.video_temp = None
if "video_key" not in st.session_state:
    st.session_state.video_key = uf.generate_key("video_upload")

if "overlays_temp" not in st.session_state:
    st.session_state.overlays_temp = None
if "overlays_key" not in st.session_state:
    st.session_state.overlays_key = uf.generate_key("overlays_upload")

if "overlays" not in st.session_state:
    st.session_state.overlays = []

# ==============================
# Upload Video
# ==============================
video_file = st.file_uploader("📂 Upload a video", type=["mp4", "mov", "avi"], key=st.session_state.video_key)

if video_file:

    st.session_state.video_temp = uf.save_temp_file(video_file, ".mp4")
    clip = VideoFileClip(st.session_state.video_temp)

    st.subheader("Video Details")
    col1, col2, col3, col4 = st.columns(4)
    col1.success(f"{clip.duration:.2f}s")
    col2.success(f"{clip.w}x{clip.h}")
    col3.success(f"{clip.fps} FPS")
    n_frames = getattr(getattr(clip, "reader", None), "n_frames", None)
    if n_frames is None:
        try:
            n_frames = int(clip.duration * clip.fps)
        except Exception:
            n_frames = "Unknown"
    col4.success(f"{n_frames} frames")
    #font add 

    FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
    fonts = {}
    if os.path.exists(FONTS_DIR):
        font_files = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith((".ttf",))]
        fonts = {os.path.splitext(f)[0]: os.path.join(FONTS_DIR, f) for f in font_files}

    # Option selection
    font_option = st.radio(
        "Select font option:", 
        ["Use preloaded font", "Upload custom font"], 
        horizontal=True
    )

    font_path = None
    font_name = None  # store just the font name

    if font_option == "Use preloaded font":
        if fonts:
            selected_font = st.selectbox("Select a font", list(fonts.keys()), key="font_selectbox")
            font_path = fonts[selected_font].replace("\\", "/")
            font_name = selected_font  # just the name, not the path
        else:
            st.warning("No fonts found in the fonts folder.")
            font_path = None

    elif font_option == "Upload custom font":
        uploaded_font_file = st.file_uploader(
            "Upload a .ttf font file",
            type=["ttf"],
            key="font_upload"
        )
        if uploaded_font_file is not None:
            tmp_font = tempfile.NamedTemporaryFile(delete=False, suffix=".ttf")
            tmp_font.write(uploaded_font_file.read())
            tmp_font.close()
            font_path = tmp_font.name
            # extract name from uploaded file
            font_name = os.path.splitext(uploaded_font_file.name)[0]

    # Fallback to default font if none selected/uploaded
    if font_path is None:
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Arial.ttf")
        font_name = "Arial"

    st.write(f"Using font: {font_name}")

    # font size and text color
    font_size =st.number_input("Font Size 5 - 200", min_value=5, max_value=200, value=22)
    #font_size = st.slider("Font Size", 5, 200, 22)

    st.subheader("Set Text & Background Color")
    text_color_hex = st.color_picker("Pick Text Color", "#FFFFFF")
    # Add background color 
    enable_bg = st.checkbox("Enable background box")
    bg_opacity = 0.0
    bg_color = None
    if enable_bg:
        bg_color_hex = st.color_picker("Pick Background Color", "#000000")
        bg_color = tuple(int(bg_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        # Add opacity slider
        bg_opacity = st.slider("Background Opacity", 0.0, 1.0, 0.7, 0.01)  # 0 = fully transparent, 1 = opaque

    # Set Positioning
    st.header("Set Position")
    bottom_padding = st.number_input("Set frame bottom padding 0 - 500", min_value=0, max_value=500, value=15)
    pos_choice = st.selectbox(
        "Overlay position",
        ["Bottom center", "Top center", "Center", "Top-left", "Top-right", "Bottom-left", "Bottom-right", "Custom (percent)"],
        index=0
    )
    x_percent = y_percent = None
    if pos_choice == "Custom (percent)":
        x_percent = st.slider("Horizontal position (0% = left, 100% = right)", 0, 100, 50)
        y_percent = st.slider("Vertical position (0% = top, 100% = bottom)", 0, 100, 90)
 
    # ==============================
    # Upload Overlay File
    # ==============================
    st.subheader("Upload Overlays File (CSV or Excel)")
    overlay_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"], key=st.session_state.overlays_key)
    if overlay_file is not None:
        ext = ".csv" if overlay_file.name.endswith(".csv") else ".xlsx"
        st.session_state.overlays_temp = uf.save_temp_file(overlay_file, ext)

        if overlay_file.name.endswith(".csv"):
            df = pd.read_csv(st.session_state.overlays_temp)
        else:
            df = pd.read_excel(st.session_state.overlays_temp)

        # required overlay columns (same fields as your manual app)
        required_cols = [
            "text", "start_time", "end_time"
        ]
        missing_cols = [c for c in required_cols if c not in df.columns]

        if missing_cols:
            st.error(f"❌ Missing columns: {missing_cols}")
        else:
            st.success("✅ File loaded successfully!")
            st.write("Preview & Edit:")
            edited_df = st.data_editor(df, num_rows="dynamic")

            # ==============================
            # Generate Video
            # ==============================
            if st.button("🎥 add over lays"):
                text_clips = []
                
                for _, overlay in edited_df.iterrows():

                    if overlay.get("text").strip() == "":
                        st.warning("Please enter some text!")

                    elif int(overlay.get('start_time')) >= int(overlay.get('end_time')):
                        st.warning("End time must be greater than start time.")

                    else:
                        st.session_state.overlays.append({
                            "text":str(overlay.get("text")),
                            "start_time": int(overlay.get('start_time')),
                            "end_time": int(overlay.get('end_time')),
                            "font_size": int(font_size),
                            "color": text_color_hex,
                            "bg_color": bg_color ,
                            "bg_opacity": bg_opacity, 
                            "bottom_padding": int(bottom_padding),
                            "position":pos_choice,
                            "x_percent":x_percent,
                            "y_percent":y_percent
                        })
                        st.success(f'✅ Overlay added: "{overlay.get("text")}" ({int(overlay.get('start_time'))}-{int(overlay.get('end_time'))}s)')
                st.info("💡 Add more overlays by changing the text and times, then click **'➕ Add Overlay'** again. When done, click **' Generate Video'**.")


    # -----------------------------
    # Show Current Overlays
    # -----------------------------
    if st.session_state.overlays:
        st.subheader("Current Overlays")

        for i, overlay in enumerate(st.session_state.overlays, 1):
            # Create main layout: summary on left, buttons on right
            col_summary, btn_delete = st.columns([8, 4])  # summary takes 6 units, buttons 2 units

            # Overlay summary
            with col_summary:
                pos_label = overlay["position"]
                if pos_label == "Custom (percent)":
                    pos_label += f" [{overlay['x_percent']}%, {overlay['y_percent']}%]"
                st.write(f"**Overlay {i}:** {overlay['text']} "
                         f"({overlay['start_time']}s - {overlay['end_time']}s), Position: {pos_label}")

            # Delete button
            with btn_delete:
                    if st.button("Delete", key=f"del_{i}",help='Delete this overlay'):
                        st.session_state.overlays.pop(i-1)
                        st.success(f"Overlay {i} deleted!")
                        st.rerun()

        # -----------------------------
        # Generate Final Video
        # -----------------------------
        if st.button("Generate Video",help="Generate the final video with all overlays applied"):
            st.write("Processing video...")
            text_clips = []

            for overlay in st.session_state.overlays:
                # Create RGBA text image
                pil_img = ig.create_image_qt_text_bg(  
                    overlay["text"],
                    font_path=font_path,
                    font_size=overlay["font_size"],
                    text_color=tuple(int(overlay["color"].lstrip("#")[i:i+2], 16) for i in (0,2,4)),
                    bg_color=overlay["bg_color"],
                    bg_opacity=overlay.get("bg_opacity", 0.5),  # use opacity from overlay
                    padding=overlay["bottom_padding"]
                )
                np_img = np.array(Image.open(pil_img))
                #os.remove(pil_img)

                # Split RGB and Alpha → build mask for transparency
                if np_img.shape[-1] == 4:
                    rgb = np_img[:, :, :3]
                    alpha = np_img[:, :, 3] / 255.0
                    rgb_clip = ImageClip(rgb)
                    mask_clip = ImageClip(alpha, is_mask=True)
                    img_clip = rgb_clip.with_mask(mask_clip)
                else:
                    img_clip = ImageClip(np_img)

                # Determine position
                position = overlay["position"]
                if position == "Custom (percent)":
                    pil_img_obj = Image.open(pil_img)
                    ov_w, ov_h = pil_img_obj.size
                    x_percent = overlay.get("x_percent", 50) or 0
                    y_percent = overlay.get("y_percent", 90) or 0
                    x_px, y_px = ph.compute_custom_xy_percent(clip.w, clip.h, ov_w, ov_h, x_percent, y_percent)
                    img_clip = img_clip.with_position((x_px, y_px))
                else:
                    img_clip = img_clip.with_position(ph.PRESET_POSITIONS[position])

                # Timing
                img_clip = (img_clip
                            .with_start(overlay["start_time"])
                            .with_duration(max(0.01, overlay["end_time"] - overlay["start_time"])))

                text_clips.append(img_clip)

            # Compose and export
            final = CompositeVideoClip([clip, *text_clips])
            # Create unique output file path with datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_with_text_{timestamp}.mp4"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)


            # Logging
            try:
                total_frames = int(final.fps * final.duration)
            except Exception:
                total_frames = None
            logger =sl.StreamlitLogger(total_frames)

            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                logger=logger
            )

            st.success("✅ Video generated successfully!")
            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button("📥 Download", f, file_name=output_filename,help="Download Finel Video")

            # Cleanup memory
            try:
                uf.close_and_remove(final, *text_clips)
            except Exception:
                pass

        # -----------------------------
        # Clear All Button
        # -----------------------------
        # clear all button
        if st.button("Clear All",help="Clear All Data or Fields"):
            uf.close_and_remove(clip)
            uf.remove_temp_files(st.session_state.video_temp)
            uf.remove_temp_files(st.session_state.overlays_temp)
            st.session_state.overlays = []
            st.session_state.video_temp = None
            st.session_state.overlays_temp = None
            st.session_state.video_key = uf.generate_key("video_upload")
            st.session_state.overlays_key = uf.generate_key("overlays_upload")

            st.rerun()
