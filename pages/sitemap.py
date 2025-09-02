import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sitemap", page_icon="🗺️")

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

st.markdown(f"<pre>{sitemap}</pre>", unsafe_allow_html=True)
