Video Text Editor (Subtitle & Overlay Tool)

An easy-to-use online video text editor built with Streamlit

With this tool, you can add subtitles, overlays, and custom text to your videos in just a few clicks.
No need for complex software — everything runs directly in your browser. 🚀

Features

Add subtitles or text overlays to your videos

Customize text style, position, and colors

Upload MP4 videos and preview in real-time

SEO optimized with sitemap & robots.txt for indexability

Privacy-friendly (no data sharing)

Project Structure
Video_Subtitles/
│
├── Home.py                 # Main entrypoint
├── About_Us.py
├── Contact_Us.py
├── Privacy_Policy.py
├── Terms_Conditions.py
├── How_To_Use.py
│
├── static/                 # SEO-related files
│   ├── sitemap.xml
│   └── robots.txt
│
└── .streamlit/
    └── config.toml         # Streamlit config

Deployment

This app is deployed on Streamlit Community Cloud:
Video Text Editor

SEO Setup

We added SEO essentials for indexability:

sitemap.xml → /static/sitemap.xml

robots.txt → /static/robots.txt

Meta tags (OpenGraph + Twitter cards) inside each page

Example in robots.txt:

User-agent: *
Allow: /

Sitemap: https://videotexteditor.streamlit.app/static/sitemap.xml

Run Locally

Clone the repo:

git clone https://github.com/your-username/Video_Subtitles.git
cd Video_Subtitles


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run Home.py


Visit 👉 http://localhost:8501

License

This project is licensed under the MIT License.
