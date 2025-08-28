
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