
import streamlit as st
from proglog import ProgressBarLogger

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