import streamlit as st

# Title and logo (optional)
st.title("My App")
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")  # Uncomment if you have a logo

# -------------------
# Define pages
# -------------------

home_page = st.Page("Home.py", title="Home", icon=":house:", default=True)
about_us = st.Page("pages/1_About_Us.py", title="About Us", icon=":information:")
contact_us = st.Page("pages/2_Contact_Us.py", title="Contact Us", icon=":email:")
privacy_policy = st.Page("pages/3_Privacy_policy.py", title="Privacy Policy", icon=":lock:")
terms_conditions = st.Page("pages/4_Terms_Conditions.py", title="Terms & Conditions", icon=":file_document:")
how_to_use = st.Page("pages/5_How_To_Use.py", title="How To Use", icon=":book:")

# -------------------
# Build navigation
# -------------------

pages = [home_page, about_us, contact_us, privacy_policy, terms_conditions, how_to_use]

pg = st.navigation(pages)
pg.run()
