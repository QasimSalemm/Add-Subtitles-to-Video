import os
from random import randint
import tempfile

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