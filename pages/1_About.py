import streamlit as st

def about_us():
    st.set_page_config(
        page_title="About Us - Text Overlay Studio", 
        page_icon="images/theme.png")

    # Page Title (SEO-friendly H1 equivalent in Streamlit)
    st.title("About Text Overlay Studio")

    # Subtitle with keywords
    st.subheader("Your Easy Tool for Adding Custom Text, Captions, and Subtitles to Videos")

    # Main description
    st.write(
        "Text Overlay Studio is a simple and powerful web application that allows you "
        "to add text, captions, and subtitles to your videos with ease. Whether you want "
        "to highlight important points, create engaging social media content, or add "
        "professional-looking subtitles, our tool makes the process effortless."
    )

    # Value points (bullet-like but using st.write for SEO clarity)
    st.write("Why choose us?")
    st.write("💡 User-friendly interface with no technical skills required")
    st.write("💡 Upload CSV/XLSX subtitle files or add text manually")
    st.write("💡 Choose custom fonts, colors, sizes, and positions")
    st.write("💡 Export high-quality MP4 videos with crisp overlays")

    # Mission section
    st.subheader("Our Mission")
    st.write(
        "Our mission is to make video editing accessible to everyone. We believe that "
        "adding professional subtitles and text to videos should be simple, fast, and "
        "affordable—without the need for expensive software."
    )

    # Closing statement
    st.subheader("Who We Serve")
    st.write(
        "Creators, educators, businesses, and social media enthusiasts around the world "
        "use Text Overlay Studio to create engaging videos that reach wider audiences."
    )
        # Footer
    st.write("---")
    st.info("💡 This project is open-source and community-driven. Contributions & feedback are always welcome!")


if __name__ == "__main__":
    about_us()
