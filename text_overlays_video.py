import os
import sys 
import time
import tempfile
import numpy as np
from PIL import Image
import streamlit as st
from datetime import datetime
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

import utility_functions as uf
import image_generator as ig
import position_helpers as ph
import streamlit_logger as sl
import app_configuration as ac

from PySide6.QtWidgets import QApplication
if not QApplication.instance():
    app = QApplication(sys.argv)

#//page configuration
ac.setup_page()

# Buttons style
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load your CSS file
local_css("styles/style.css")

# ==============================
# Session State Initialization
# ==============================
if "video_temp" not in st.session_state:
    st.session_state.video_temp = None
if "video_key" not in st.session_state:
    st.session_state.video_key = uf.generate_key("video")
if "overlays" not in st.session_state:
    st.session_state.overlays = []
if "editing_overlay" not in st.session_state:
    st.session_state.editing_overlay = None

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
    # n_frames may not always be available; guard it
    n_frames = getattr(getattr(clip, "reader", None), "n_frames", None)
    if n_frames is None:
        try:
            n_frames = int(clip.duration * clip.fps)
        except Exception:
            n_frames = "Unknown"
    col4.success(f"{n_frames} frames")

    # -----------------------------
    # Add Overlay
    # -----------------------------
    st.subheader("Add Text Overlay")
    user_text = st.text_area("Enter text")
    
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

    # --- Start Time ---
    st.subheader("Set Overlay Timing")
    sh, sm, ss = st.columns(3)
    with sh:
        start_h = st.number_input("Start Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
    with sm:
        start_m = st.number_input("Start Minute 0 - 59", min_value=0, max_value=59, value=0)
    with ss:
        start_s = st.number_input("Start Second 0 -59", min_value=0, max_value=59, value=0)

    start_time = uf.hms_to_seconds(start_h, start_m, start_s)

    # --- End Time ---
    eh, em, es = st.columns(3)
    with eh:
        end_h = st.number_input("End Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
    with em:
        end_m = st.number_input("End Minute 0 - 59", min_value=0, max_value=59, value=0)
    with es:
        end_s = st.number_input("End Second 0 - 59", min_value=0, max_value=59, value=min(5, int(clip.duration)))

    end_time = uf.hms_to_seconds(end_h, end_m, end_s)
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
    # Add Overlay Button
    if st.button("➕ Add Overlay",help='Add the overlay with the specified settings'):
        if user_text.strip() == "":
            st.warning("Please enter some text!")
        elif end_time <= start_time:
            st.warning("End time must be greater than start time.")
        else:
            st.session_state.overlays.append({
                "text": user_text,
                "start": int(start_time),
                "end": int(end_time),
                "font_size": int(font_size),
                "color": text_color_hex,
                "bg_color": bg_color,
                "bg_opacity": bg_opacity, 
                "bottom_padding": int(bottom_padding),
                "position": pos_choice,
                "x_percent": x_percent,
                "y_percent": y_percent
            })
            st.success(f'✅ Overlay added: "{user_text}" ({start_time}-{end_time}s)')
            st.info("💡 Add more overlays by changing the text and times, then click **'➕ Add Overlay'** again. When done, click **' Generate Video'**.")

    # -----------------------------
    # Show Current Overlays
    # -----------------------------
    if st.session_state.overlays:
        st.subheader("Current Overlays")

        for i, overlay in enumerate(st.session_state.overlays, 1):
            # Create main layout: summary on left, buttons on right
            col_summary, col_buttons = st.columns([8, 4])  # summary takes 6 units, buttons 2 units

            # Overlay summary
            with col_summary:
                pos_label = overlay["position"]
                if pos_label == "Custom (percent)":
                    pos_label += f" [{overlay['x_percent']}%, {overlay['y_percent']}%]"
                st.write(f"**Overlay {i}:** {overlay['text']} "
                         f"({overlay['start']}s - {overlay['end']}s), Position: {pos_label}")

            # Buttons horizontally
            with col_buttons:
                btn_edit, btn_delete = st.columns([2, 2],gap='small')  # two small columns for buttons
                with btn_edit:
                    
                    if st.button("Edit", key=f"edit_{i}",help='Edit this overlay'):
                        st.session_state.editing_overlay = i
                        st.rerun()
                with btn_delete:
                    if st.button("Delete", key=f"del_{i}",help='Delete this overlay'):
                        st.session_state.overlays.pop(i-1)
                        st.success(f"Overlay {i} deleted!")
                        st.rerun()

            # Edit form
            if st.session_state.editing_overlay == i:
                with st.expander(f"Editing Overlay {i}", expanded=True):
                    new_text = st.text_area("Edit text", overlay["text"], key=f"text_{i}")

                    st.subheader("Edit Overlay Timing")

                    # --- Start Time ---
                    s_h, s_m, s_s = uf.seconds_to_hms(overlay["start"])
                    esh, esm, ess = st.columns(3)
                    with esh:
                        new_start_h = st.number_input("Start Hour", min_value=0, max_value=int(clip.duration // 3600),
                                                      value=s_h, key=f"start_h_{i}")
                    with esm:
                        new_start_m = st.number_input("Start Minute 0 - 59", min_value=0, max_value=59,
                                                      value=s_m, key=f"start_m_{i}")
                    with ess:
                        new_start_s = st.number_input("Start Second 0 - 59", min_value=0, max_value=59,
                                                      value=s_s, key=f"start_s_{i}")

                    new_start = uf.hms_to_seconds(new_start_h, new_start_m, new_start_s)

                    # --- End Time ---
                    e_h, e_m, e_s = uf.seconds_to_hms(overlay["end"])
                    eeh, eem, ees = st.columns(3)
                    with eeh:
                        new_end_h = st.number_input("End Hour", min_value=0, max_value=int(clip.duration // 3600),
                                                    value=e_h, key=f"end_h_{i}")
                    with eem:
                        new_end_m = st.number_input("End Minute 0 - 59", min_value=0, max_value=59,
                                                    value=e_m, key=f"end_m_{i}")
                    with ees:
                        new_end_s = st.number_input("End Second 0 - 59", min_value=0, max_value=59,
                                                    value=e_s, key=f"end_s_{i}")

                    new_end = uf.hms_to_seconds(new_end_h, new_end_m, new_end_s)

                    new_font_size = st.number_input("Font Size 5 - 200", 5, 200,
                                              overlay["font_size"], key=f"font_{i}")
                    new_color = st.color_picker("Text Color", overlay["color"], key=f"color_{i}")

                    new_enable_bg = st.checkbox(
                        "Enable background box",
                        value=(overlay["bg_color"] is not None),
                        key=f"bg_en_{i}"
                    )
                    new_bg_color = overlay["bg_color"]
                    new_bg_opacity = overlay.get("bg_opacity", 0.5)  # default 50%

                    if new_enable_bg:
                        default_bg_hex = "#000000" if not overlay["bg_color"] else '#%02x%02x%02x' % overlay["bg_color"]
                        new_bg_hex = st.color_picker("Background Color", default_bg_hex, key=f"bg_{i}")
                        new_bg_color = tuple(int(new_bg_hex.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))

                        # <-- Add opacity slider here -->
                        new_bg_opacity = st.slider(
                            "Background Opacity",
                            0.0, 1.0,
                            overlay.get("bg_opacity", 0.7),
                            0.05,
                            key=f"opacity_{i}"
                        )
                    else:
                        new_bg_color = None
                        new_bg_opacity = 0.0

                    new_padding = st.number_input("Padding 0 - 500", 0, 500, overlay["bottom_padding"], key=f"pad_{i}")

                    new_position = st.selectbox(
                        "Overlay position",
                        ["Bottom center", "Top center", "Center", "Top-left", "Top-right", "Bottom-left", "Bottom-right", "Custom (percent)"],
                        index=["Bottom center", "Top center", "Center", "Top-left", "Top-right", "Bottom-left", "Bottom-right", "Custom (percent)"].index(overlay["position"]),
                        key=f"pos_{i}"
                    )
                    new_x_percent = overlay.get("x_percent", 50)
                    new_y_percent = overlay.get("y_percent", 90)
                    if new_position == "Custom (percent)":
                        new_x_percent = st.slider("Horizontal position (0% = left, 100% = right)", 0, 100, int(new_x_percent), key=f"x_{i}")
                        new_y_percent = st.slider("Vertical position (0% = top, 100% = bottom)", 0, 100, int(new_y_percent), key=f"y_{i}")
                    else:
                        new_x_percent = None
                        new_y_percent = None

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("Save Changes", key=f"save_{i}",help='Save changes to this overlay'):
                            overlay["text"] = new_text
                            overlay["start"] = int(new_start)
                            overlay["end"] = int(new_end)
                            overlay["font_size"] = int(new_font_size)
                            overlay["color"] = new_color
                            overlay["bg_color"] = new_bg_color
                            overlay["bg_opacity"] = new_bg_opacity              
                            overlay["bottom_padding"] = int(new_padding)
                            overlay["position"] = new_position
                            overlay["x_percent"] = new_x_percent
                            overlay["y_percent"] = new_y_percent
                            st.session_state.editing_overlay = None
                            st.success(f"Overlay {i} updated!")
                            st.rerun()

                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{i}",help='Cancel editing'):
                            st.session_state.editing_overlay = None
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
                            .with_start(overlay["start"])
                            .with_duration(max(0.01, overlay["end"] - overlay["start"])))

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
        if st.button("Clear All",help="Clear All Data or Fields"):
            # Close and remove video clip
            uf.close_and_remove(clip)

            # Remove temporary video file
            uf.remove_temp_files(st.session_state.video_temp)

            # Reset session state
            st.session_state.overlays = []
            st.session_state.video_temp = None
            st.session_state.video_key = uf.generate_key("video")

            # Refresh the app
            st.balloons()
            time.sleep(2)
            st.rerun()