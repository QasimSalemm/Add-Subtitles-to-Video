from datetime import datetime
import os
import tempfile
import time
import streamlit as st
import image_generator as ig
import numpy as np
from PIL import Image
from moviepy import ImageClip, CompositeVideoClip
import position_helpers as ph
import streamlit_logger as sl
import utility_functions as uf

# -----------------------------
# Add Overlays setting data
# -----------------------------

def overlay_setting_fields(key_suffix):
    FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
    fonts = {}
    if os.path.exists(FONTS_DIR):
        font_files = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith((".ttf",))]
        fonts = {os.path.splitext(f)[0]: os.path.join(FONTS_DIR, f) for f in font_files}

    # Option selection
    font_option = st.radio(
        "Select font option:", 
        ["Use preloaded font", "Upload custom font"], 
        horizontal=True,
        key=f"{key_suffix}_font_option_radio"
    )

    font_path = None
    font_name = None

    if font_option == "Use preloaded font":
        if fonts:
            selected_font = st.selectbox(
                "Select a font", 
                list(fonts.keys()), 
                key=f"{key_suffix}_font_selectbox"
            )
            font_path = fonts[selected_font].replace("\\", "/")
            font_name = selected_font
        else:
            st.warning("No fonts found in the fonts folder.")
            font_path = None
    elif font_option == "Upload custom font":
        uploaded_font_file = st.file_uploader(
            "Upload a .ttf font file",
            type=["ttf"],
            key=f"{key_suffix}_font_upload"
        )
        if uploaded_font_file is not None:
            tmp_font = tempfile.NamedTemporaryFile(delete=False, suffix=".ttf")
            tmp_font.write(uploaded_font_file.read())
            tmp_font.close()
            font_path = tmp_font.name
            font_name = os.path.splitext(uploaded_font_file.name)[0]

    # fallback
    if font_path is None:
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Arial.ttf")
        font_name = "Arial"

    st.write(f"Using font: {font_name}")

    font_size = st.number_input(
        "Font Size 5 - 200", 
        min_value=5, max_value=200, value=22,
        key=f"{key_suffix}_font_size"
    )

    st.subheader("Set Text & Background Color")
    text_color_hex = st.color_picker("Pick Text Color", "#FFFFFF", key=f"{key_suffix}_text_color")

    enable_bg = st.checkbox("Enable background box", key=f"{key_suffix}_enable_bg")
    bg_opacity = 0.0
    bg_color = None
    if enable_bg:
        bg_color_hex = st.color_picker("Pick Background Color", "#000000", key=f"{key_suffix}_bg_color")
        bg_color = tuple(int(bg_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        bg_opacity = st.slider(
            "Background Opacity", 0.0, 1.0, 0.7, 0.01,
            key=f"{key_suffix}_bg_opacity"
        )

    st.subheader("Set Position")
    bottom_padding = st.number_input(
        "Set frame bottom padding 0 - 500", 
        min_value=0, max_value=500, value=15,
        key=f"{key_suffix}_bottom_padding"
    )

    pos_choice = st.selectbox(
        "Overlay position",
        ["Bottom center", "Top center", "Center", "Top-left", "Top-right", "Bottom-left", "Bottom-right", "Custom (percent)"],
        index=0,
        key=f"{key_suffix}_pos_choice"
    )

    x_percent = y_percent = None
    if pos_choice == "Custom (percent)":
        x_percent = st.slider("Horizontal position", 0, 100, 50, key=f"{key_suffix}_x_percent")
        y_percent = st.slider("Vertical position", 0, 100, 90, key=f"{key_suffix}_y_percent")

    return {
        "font_option": font_option,
        "font_name": font_name,
        "font_path": font_path,
        "font_size": font_size,
        "text_color": text_color_hex,
        "enable_bg": enable_bg,
        "bg_color": bg_color,
        "bg_opacity": bg_opacity,
        "bottom_padding": bottom_padding,
        "pos_choice": pos_choice,
        "x_percent": x_percent,
        "y_percent": y_percent,
    }

# -----------------------------
# Generate Final Video
# -----------------------------
def generate_finel_video(clip, key_suffix, target="overlays"):
    overlays = st.session_state.get(target, [])
    
    if st.button(
        "Generate Video",
        help="Generate the final video with all overlays applied",
        key=f"gen_video_{key_suffix}"
    ):
        st.write("Processing video...")
        text_clips = []

        for overlay in overlays:
            # Create RGBA text image
            pil_img = ig.create_image_qt_text_bg(  
                overlay["text"],
                font_path=overlay["font_path"],
                font_size=overlay["font_size"],
                text_color=tuple(int(overlay["color"].lstrip("#")[i:i+2], 16) for i in (0,2,4)),
                bg_color=overlay["bg_color"],
                bg_opacity=overlay.get("bg_opacity", 0.5),
                padding=overlay["bottom_padding"]
            )

            np_img = np.array(Image.open(pil_img))

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
                x_px, y_px = ph.compute_custom_xy_percent(
                    clip.w, clip.h, ov_w, ov_h, x_percent, y_percent
                )
                img_clip = img_clip.with_position((x_px, y_px))
            else:
                img_clip = img_clip.with_position(ph.PRESET_POSITIONS[position])

            # Timing
            img_clip = (
                img_clip.with_start(overlay["start"])
                        .with_duration(max(0.01, overlay["end"] - overlay["start"]))
            )
            text_clips.append(img_clip)

        # Compose and export
        final = CompositeVideoClip([clip, *text_clips])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"video_with_text_{timestamp}.mp4"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        try:
            total_frames = int(final.fps * final.duration)
        except Exception:
            total_frames = None

        logger = sl.StreamlitLogger(total_frames)
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            logger=logger
        )

        st.success("✅ Video generated successfully!")
        st.video(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                "📥 Download", f, file_name=output_filename,
                help="Download Final Video", key=f"dl_{key_suffix}"
            )

        # Cleanup
        try:
            uf.close_and_remove(final, *text_clips)
        except Exception:
            pass

# -----------------------------
# Delete overlays button 
# -----------------------------

def delete_text_file_overlays(i, key_suffix, target="overlays"):
    """Delete a single overlay from a chosen target list in session_state."""
    if st.button("Delete", key=f"del_{key_suffix}_{i}", help='Delete this overlay'):
        if target in st.session_state and 0 < i <= len(st.session_state[target]):
            st.session_state[target].pop(i - 1)
            st.success(f"Overlay {i} deleted!")
            st.rerun()


# -----------------------------
# Add Overlay Button
# -----------------------------
def add_overlay_entry(text, start, end, overlay_settings_data, target="overlays"):
    """Helper to add one overlay entry into a chosen session_state list."""
    if target not in st.session_state:
        st.session_state[target] = []

    st.session_state[target].append({
        "text": str(text),
        "start": int(start),
        "end": int(end),
        "font_path": overlay_settings_data["font_path"],
        "font_size": int(overlay_settings_data["font_size"]),
        "color": overlay_settings_data["text_color"],
        "bg_color": overlay_settings_data["bg_color"],
        "bg_opacity": overlay_settings_data["bg_opacity"], 
        "bottom_padding": int(overlay_settings_data["bottom_padding"]),
        "position": overlay_settings_data["pos_choice"],
        "x_percent": overlay_settings_data["x_percent"],
        "y_percent": overlay_settings_data["y_percent"]
    })

# -----------------------------
# Clear All Data Button
# -----------------------------
def clear_all(clip, key_suffix, target="overlays"):
    """
    Creates a 'Clear All' button that resets data depending on target:
      - manual_overlays → clears only manual overlays
      - file_overlays → clears only file overlays
      - video → clears EVERYTHING (video + overlays + temp files)
    """
    if st.button("Clear All", help="Clear All Data or Fields", key=f"{key_suffix}"):
        # Always close clip if provided
        uf.close_and_remove(clip)

        if target == "manual_overlays":
            st.session_state.manual_overlays = []

        elif target == "file_overlays":
            st.session_state.file_overlays = []
            st.session_state.overlays_temp = None
            st.session_state.overlays_key = uf.generate_key("overlays_upload")

        elif target == "video":
            # Clear everything
            st.session_state.manual_overlays = []
            st.session_state.file_overlays = []
            st.session_state.overlays_temp = None
            st.session_state.video_temp = None

            # Reset uploader keys
            st.session_state.video_key = uf.generate_key("video_upload")
            st.session_state.overlays_key = uf.generate_key("overlays_upload")

            # Remove temp files
            uf.remove_temp_files(
                st.session_state.get("video_temp"),
                st.session_state.get("overlays_temp")
            )

        elif target == "overlays":  # legacy fallback
            st.session_state.overlays = []

        # 🎉 Feedback
        st.balloons()
        time.sleep(2)
        st.rerun()

# -----------------------------
# Show Current Overlays
# -----------------------------

def show_current_overlays(key_suffix, target="overlays"):
    overlays = st.session_state.get(target, [])
    for i, overlay in enumerate(overlays, 1):
        # Create main layout: summary on left, buttons on right
        col_summary, btn_delete = st.columns([5.5,1])  
        
        # Overlay summary
        with col_summary:
            pos_label = overlay["position"]
            if pos_label == "Custom (percent)":
                pos_label += f" [{overlay['x_percent']}%, {overlay['y_percent']}%]"
            st.write(
                f"**Overlay {i}:** {overlay['text']} "
                f"({overlay['start']}s - {overlay['end']}s), Position: {pos_label}"
            )

        # Delete button
        with btn_delete:
            delete_text_file_overlays(i, key_suffix, target=target)

# -----------------------------
# Custom CSS
# -----------------------------
def apply_styles():
    st.markdown(
        """
        <style>
        /* Main page title */
        .page-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* Section card */
        .section-card {
            background-color: #F0F2F6;            
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
        .section-card h3 {
            margin-top: 0px;
        }
        .section-card p, .section-card li {
            font-size: 16px;
            line-height: 1.6;
        }

        /* Divider line */
        hr {
            border: none;
            height: 1px;
            background: #ddd;
            margin: 25px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# footer
# -----------------------------
def footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;           
            padding: 5px 0;
            background-color: rgba(255, 255, 255, 50);
        }
        </style>
        <div class="footer">
            <hr style="margin:2px 0;">
            © 2025 Video Overlay Tool
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Local Css All Buttons
# -----------------------------
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
