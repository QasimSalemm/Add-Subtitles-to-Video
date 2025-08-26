from datetime import datetime
import time
import os
import tempfile
from random import randint

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from proglog import ProgressBarLogger

# ==============================
# Streamlit Page Config
# ==============================
st.set_page_config(
    page_title="Add Subtitle",
    page_icon="images/theme.png",   # relative path
    layout="wide"
)
st.title("🎬 Add Subtitle to Video")

# ==============================
# Custom logger for Streamlit
# ==============================
class StreamlitLogger(ProgressBarLogger):
    def __init__(self, total_frames=None):
        super().__init__()
        self.progress_bar = st.progress(0)
        self.progress_text = st.empty()
        self.total_frames = total_frames

    def bars_callback(self, bar, attr, value, old_value=None):
        try:
            total = self.bars[bar]["total"]
            pct = int((value / max(total, 1)) * 100)
        except Exception:
            pct = 0

        if self.total_frames:
            self.progress_text.text(f"{bar.capitalize()} progress: {pct}% ({value}/{self.total_frames} frames)")
        else:
            self.progress_text.text(f"{bar} progress: {pct}%")

        self.progress_bar.progress(min(max(pct, 0), 100))

# ==============================
# Utility Functions
# ==============================
def seconds_to_hms(seconds: int):
    """Convert seconds → (h, m, s)."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return h, m, s

def hms_to_seconds(h: int, m: int, s: int):
    """Convert (h, m, s) → seconds."""
    return int(h) * 3600 + int(m) * 60 + int(s)

def save_temp_file(uploaded_file, suffix=".mp4"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name

def close_and_remove(*clips):
    for clip in clips:
        try:
            clip.close()
        except Exception:
            pass

def remove_temp_files(*paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

def generate_key(prefix):
    return f"{prefix}_{randint(0, 100000)}"


# ==============================
# Session State Initialization
# ==============================
if "video_temp" not in st.session_state:
    st.session_state.video_temp = None
if "video_key" not in st.session_state:
    st.session_state.video_key = generate_key("video")
if "overlays" not in st.session_state:
    st.session_state.overlays = []
if "editing_overlay" not in st.session_state:
    st.session_state.editing_overlay = None

# ==============================
# Text Image Generator
# ==============================
def create_image(
    text,
    font_path=r"arial.ttf",
    font_size=40,
    text_color=(255, 255, 255),
    bg_color=None,
    bottom_padding=10
):
    # Handle Arabic shaping and bidi
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    lines = bidi_text.split("\n")
    
    try:
        font = ImageFont.truetype(font_path, font_size, encoding="unic")
        #print("✅ Font loaded successfully:", font_path)
    except OSError as e:
        print("❌ Font loading failed:", e)
        font = ImageFont.load_default()


    # Metrics
    bbox_hg = font.getbbox("hg")
    line_height = bbox_hg[3] - bbox_hg[1]  # approximate line height
    max_width = 1
    widths = []
    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        widths.append(w)
        if w > max_width:
            max_width = w
    text_height = line_height * len(lines)

    # Canvas size
    img_width = max_width + bottom_padding * 2
    img_height = text_height + bottom_padding * 2

    # Transparent canvas
    img = Image.new("RGBA", (max(1, img_width), max(1, img_height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw lines (and optional background boxes)
    y_text = bottom_padding
    for idx, line in enumerate(lines):
        text_width = widths[idx]
        x_text = bottom_padding

        if bg_color is not None:
            # Opaque background box under each line
            draw.rectangle(
                [x_text, y_text, x_text + text_width, y_text + line_height + 7.5],
                fill=(*bg_color, 255)
            )

        draw.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += line_height

    return img

# ==============================
# Position Helpers
# ==============================
PRESET_POSITIONS = {
    "Bottom center": ("center", "bottom"),
    "Top center": ("center", "top"),
    "Center": ("center", "center"),
    "Top-left": ("left", "top"),
    "Top-right": ("right", "top"),
    "Bottom-left": ("left", "bottom"),
    "Bottom-right": ("right", "bottom"),
}

def compute_custom_xy_percent(vid_w, vid_h, overlay_w, overlay_h, x_percent, y_percent):
    """Compute pixel coordinates from percentages of the *available* area."""
    x = int((vid_w - overlay_w) * (x_percent / 100.0))
    y = int((vid_h - overlay_h) * (y_percent / 100.0))
    return x, y

# ==============================
# Upload Video
# ==============================
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"], key=st.session_state.video_key)

if video_file:
    st.session_state.video_temp = save_temp_file(video_file, ".mp4")
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
    st.subheader("➕ Add Text Overlay")
    user_text = st.text_area("Enter text")

    st.markdown("### ⏱ Set Overlay Timing")

    # --- Start Time ---
    sh, sm, ss = st.columns(3)
    with sh:
        start_h = st.number_input("Start Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
    with sm:
        start_m = st.number_input("Start Minute", min_value=0, max_value=59, value=0)
    with ss:
        start_s = st.number_input("Start Second", min_value=0, max_value=59, value=0)

    start_time = hms_to_seconds(start_h, start_m, start_s)

    # --- End Time ---
    eh, em, es = st.columns(3)
    with eh:
        end_h = st.number_input("End Hour", min_value=0, max_value=int(clip.duration // 3600), value=0)
    with em:
        end_m = st.number_input("End Minute", min_value=0, max_value=59, value=0)
    with es:
        end_s = st.number_input("End Second", min_value=0, max_value=59, value=min(5, int(clip.duration)))

    end_time = hms_to_seconds(end_h, end_m, end_s)



    font_size = st.slider("Font Size", 5, 200, 22)
    text_color_hex = st.color_picker("Pick Text Color", "#FFFFFF")

    enable_bg = st.checkbox("Enable background box")
    bg_color = None
    if enable_bg:
        bg_color_hex = st.color_picker("Pick Background Color", "#000000")
        bg_color = tuple(int(bg_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    bottom_padding = st.slider("Set bottom padding for background", 0, 500, 15)

    st.markdown("**Position**")
    pos_choice = st.selectbox(
        "Overlay position",
        ["Bottom center", "Top center", "Center", "Top-left", "Top-right", "Bottom-left", "Bottom-right", "Custom (percent)"],
        index=0
    )
    x_percent = y_percent = None
    if pos_choice == "Custom (percent)":
        x_percent = st.slider("Horizontal position (0% = left, 100% = right)", 0, 100, 50)
        y_percent = st.slider("Vertical position (0% = top, 100% = bottom)", 0, 100, 90)

    if st.button("➕ Add Overlay"):
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
                "color": text_color_hex,  # store hex; convert later
                "bg_color": bg_color,     # None or (r,g,b)
                "bottom_padding": int(bottom_padding),
                "position": pos_choice,
                "x_percent": x_percent,
                "y_percent": y_percent
            })
            st.success(f'✅ Overlay added: "{user_text}" ({start_time}-{end_time}s)')
            st.info("💡 Add more overlays by changing the text and times, then click **'➕ Add Overlay'** again. When done, click **'🎥 Generate Final Video'**.")

    # -----------------------------
    # Show Current Overlays
    # -----------------------------
    if st.session_state.overlays:
        st.subheader("Current Overlays")

        for i, overlay in enumerate(st.session_state.overlays, 1):
            col1, col2, col3 = st.columns([6, 1, 1])

            # Summary
            with col1:
                pos_label = overlay["position"]
                if pos_label == "Custom (percent)":
                    pos_label += f" [{overlay['x_percent']}%, {overlay['y_percent']}%]"
                st.write(f"**Overlay {i}:** {overlay['text']} "
                         f"({overlay['start']}s - {overlay['end']}s), Pos: {pos_label}")

            # Edit button
            with col2:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.editing_overlay = i
                    st.rerun()

            # Delete button
            with col3:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.overlays.pop(i-1)
                    st.success(f"Overlay {i} deleted!")
                    st.rerun()

            # Edit form
            if st.session_state.editing_overlay == i:
                with st.expander(f"Editing Overlay {i}", expanded=True):
                    new_text = st.text_area("Edit text", overlay["text"], key=f"text_{i}")

                    st.markdown("### ⏱ Edit Overlay Timing")

                    # --- Start Time ---
                    s_h, s_m, s_s = seconds_to_hms(overlay["start"])
                    esh, esm, ess = st.columns(3)
                    with esh:
                        new_start_h = st.number_input("Start Hour", min_value=0, max_value=int(clip.duration // 3600),
                                                      value=s_h, key=f"start_h_{i}")
                    with esm:
                        new_start_m = st.number_input("Start Minute", min_value=0, max_value=59,
                                                      value=s_m, key=f"start_m_{i}")
                    with ess:
                        new_start_s = st.number_input("Start Second", min_value=0, max_value=59,
                                                      value=s_s, key=f"start_s_{i}")

                    new_start = hms_to_seconds(new_start_h, new_start_m, new_start_s)

                    # --- End Time ---
                    e_h, e_m, e_s = seconds_to_hms(overlay["end"])
                    eeh, eem, ees = st.columns(3)
                    with eeh:
                        new_end_h = st.number_input("End Hour", min_value=0, max_value=int(clip.duration // 3600),
                                                    value=e_h, key=f"end_h_{i}")
                    with eem:
                        new_end_m = st.number_input("End Minute", min_value=0, max_value=59,
                                                    value=e_m, key=f"end_m_{i}")
                    with ees:
                        new_end_s = st.number_input("End Second", min_value=0, max_value=59,
                                                    value=e_s, key=f"end_s_{i}")

                    new_end = hms_to_seconds(new_end_h, new_end_m, new_end_s)

                    new_font_size = st.slider("Font Size", 5, 200,
                                              overlay["font_size"], key=f"font_{i}")
                    new_color = st.color_picker("Text Color", overlay["color"], key=f"color_{i}")

                    new_enable_bg = st.checkbox("Enable background box", value=(overlay["bg_color"] is not None), key=f"bg_en_{i}")
                    new_bg_color = overlay["bg_color"]
                    if new_enable_bg:
                        default_bg_hex = "#000000" if not overlay["bg_color"] else '#%02x%02x%02x' % overlay["bg_color"]
                        new_bg_hex = st.color_picker("Background Color", default_bg_hex, key=f"bg_{i}")
                        new_bg_color = tuple(int(new_bg_hex.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
                    else:
                        new_bg_color = None

                    new_padding = st.slider("Padding", 0, 500,
                                            overlay["bottom_padding"], key=f"pad_{i}")

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
                        if st.button("Save Changes", key=f"save_{i}"):
                            overlay["text"] = new_text
                            overlay["start"] = int(new_start)
                            overlay["end"] = int(new_end)
                            overlay["font_size"] = int(new_font_size)
                            overlay["color"] = new_color
                            overlay["bg_color"] = new_bg_color
                            overlay["bottom_padding"] = int(new_padding)
                            overlay["position"] = new_position
                            overlay["x_percent"] = new_x_percent
                            overlay["y_percent"] = new_y_percent
                            st.session_state.editing_overlay = None
                            st.success(f"Overlay {i} updated!")
                            st.rerun()

                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{i}"):
                            st.session_state.editing_overlay = None
                            st.rerun()

        # -----------------------------
        # Generate Final Video
        # -----------------------------
        if st.button("Generate Final Video"):
            st.write("Processing video...")
            text_clips = []

            for overlay in st.session_state.overlays:
                # Create RGBA text image
                pil_img = create_image(
                    overlay["text"],
                    font_size=overlay["font_size"],
                    text_color=tuple(int(overlay["color"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)),
                    bg_color=overlay["bg_color"],     # None or (r,g,b)
                    bottom_padding=overlay["bottom_padding"]
                )
                np_img = np.array(pil_img)  # RGBA

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
                    ov_w, ov_h = pil_img.size
                    x_percent = overlay.get("x_percent", 50) or 0
                    y_percent = overlay.get("y_percent", 90) or 0
                    x_px, y_px = compute_custom_xy_percent(clip.w, clip.h, ov_w, ov_h, x_percent, y_percent)
                    img_clip = img_clip.with_position((x_px, y_px))
                else:
                    img_clip = img_clip.with_position(PRESET_POSITIONS[position])

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
            logger = StreamlitLogger(total_frames)

            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                logger=logger
            )

            st.success("✅ Video generated successfully!")
            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button("📥 Download Final Video", f, file_name=output_filename)

            # Cleanup memory
            try:
                close_and_remove(final, *text_clips)
            except Exception:
                pass

        # -----------------------------
        # Clear All Button
        # -----------------------------
        if st.button("Clear All"):
            # Close and remove video clip
            close_and_remove(clip)

            # Remove temporary video file
            remove_temp_files(st.session_state.video_temp)

            # Reset session state
            st.session_state.overlays = []
            st.session_state.video_temp = None
            st.session_state.video_key = generate_key("video")

            # Refresh the app
            st.balloons()
            time.sleep(2)
            st.rerun()