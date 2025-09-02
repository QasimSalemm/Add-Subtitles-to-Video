import streamlit as st
from datetime import datetime
import overlay_settings as settings_overlay
# ==============================
# seo configuration
# ==============================
settings_overlay.apply_styles()


def app():
    
    st.set_page_config(
        page_title="Sitemap",
        page_icon="images/theme.png"
    )
    # Sitemap XML content
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://videotexteditor.streamlit.app/</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
        <url>
            <loc>https://videotexteditor.streamlit.app/About_Us</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
        <url>
            <loc>https://videotexteditor.streamlit.app/Contact_Us</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
        <url>
            <loc>https://videotexteditor.streamlit.app/Privacy_Policy</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
        <url>
            <loc>https://videotexteditor.streamlit.app/Terms_Conditions</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
        <url>
            <loc>https://videotexteditor.streamlit.app/How_To_Use</loc>
            <lastmod>{datetime.today().date()}</lastmod>
        </url>
    </urlset>
    """

    # Show raw XML
    st.code(sitemap, language="xml")

    # Force content type (so Google/Bing read it correctly)
    st.markdown(
        f"""
        <pre style="white-space: pre-wrap;">{sitemap}</pre>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    app()
