import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Add Subtitle",
        page_icon="images/theme.png",
        layout="wide"
    )
    st.title("Add Subtitle to Video",)
# Buttons style
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

