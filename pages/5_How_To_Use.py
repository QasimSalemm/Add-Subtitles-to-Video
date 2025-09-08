import streamlit as st

def how_to_use():
    st.set_page_config(
        page_title="How to Use - Text Overlay Studio", 
                       page_icon="images/theme.png")

    # Title
    st.title("How to Use Text Overlay Studio")

    # Intro
    st.write(
        "Follow this step-by-step guide to add text, captions, or subtitles to your videos using "
        "Text Overlay Studio. Our tool is designed to be simple, fast, and effective."
    )

    # Step 1
    st.subheader("Step 1: Upload Your Video")
    st.write(
        "Click on the **Upload Video** option to import your video file. The application supports "
        "popular formats like MP4 and MOV."
    )

    # Step 2
    st.subheader("Step 2: Add Text Overlays")
    st.write(
        "Use the input fields to type the text you want to display. Customize the font, color, size, "
        "and position to match your style."
    )

    # Step 3
    st.subheader("Step 3: Import Subtitles (Optional)")
    st.write(
        "You can also upload CSV or XLSX files containing subtitles. Each entry should include "
        "the text, start time, and end time."
    )

    # Step 4
    st.subheader("Step 4: Preview Your Video")
    st.write(
        "After adding your overlays, preview the video inside the app to ensure everything looks perfect."
    )

    # Step 5
    st.subheader("Step 5: Export the Final Video")
    st.write(
        "Click on **Generate Video** to export your final video with overlays. The processed file "
        "will be available to download in MP4 format."
    )
        # Footer
    st.write("---")
    st.success("""**Tips:**\n
                    ✔ Use high-quality video for clear overlays.\n
                    ✔ Keep subtitles concise for readability.\n
                    ✔ Choose contrasting text colors for better visibility.\n
                    ✔ Align text consistently for a professional look.
                """)

if __name__ == "__main__":
    how_to_use()