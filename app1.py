import streamlit as st
import os
import io
import zipfile
from dotenv import load_dotenv

import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="AI Portfolio Website Generator",
    page_icon="💻",
    layout="wide"
)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-flash-latest")

# --------------------------------------------------
# RESUME EXTRACTION
# --------------------------------------------------
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(p.extract_text() or "" for p in reader.pages)

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_resume(uploaded_file):
    data = uploaded_file.read()
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(data)
    if uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(data)
    return ""

# --------------------------------------------------
# GEMINI
# --------------------------------------------------
def call_gemini(prompt):
    response = model.generate_content(prompt)
    if not response or not response.text:
        raise ValueError("Empty response from Gemini")
    return response.text

# --------------------------------------------------
# PROMPT
# --------------------------------------------------
def build_prompt(resume_text):
    return f"""
You are a senior front-end developer.

Create a PROFESSIONAL portfolio website.

RULES:
- Clean layout
- Content wrapped inside containers
- No dark text on dark backgrounds
- Use semantic HTML

MUST INCLUDE:
<link rel="stylesheet" href="style.css">
<script defer src="script.js"></script>

OUTPUT FORMAT:
===HTML===
(html)

===CSS===
(css)

===JS===
(js)

RESUME:
{resume_text}
"""

# --------------------------------------------------
# PARSER
# --------------------------------------------------
def parse_blocks(text):
    def get(tag):
        return text.split(tag)[1].split("===")[0].strip() if tag in text else ""
    return get("===HTML==="), get("===CSS==="), get("===JS===")

# --------------------------------------------------
# FORCE CSS + JS
# --------------------------------------------------
def inject_assets(html):
    if "style.css" not in html:
        html = html.replace("<head>", "<head>\n<link rel='stylesheet' href='style.css'>")
    if "script.js" not in html:
        html = html.replace("</body>", "<script src='script.js'></script>\n</body>")
    return html

# --------------------------------------------------
# LIGHT SKYBLUE + GREEN THEME (FIXED VISIBILITY)
# --------------------------------------------------
def enhance_css(ai_css):
    base_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #e0f2fe, #d1fae5);
    color: #334155;
}

/* CONTAINER */
.container {
    max-width: 1200px;
    margin: auto;
    padding: 0 20px;
}

/* NAVBAR */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
}

.navbar a {
    color: #0f172a;
    font-weight: 600;
    text-decoration: none;
}

/* HERO */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.hero-content {
    background: #ffffff;
    padding: 60px;
    border-radius: 20px;
    max-width: 720px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.12);
}

.hero h1 {
    font-size: 3rem;
    color: #0f172a;
    margin-bottom: 10px;
}

.hero h3 {
    color: #475569;
    margin-bottom: 20px;
}

.hero p {
    color: #334155;
    margin-bottom: 32px;
    line-height: 1.7;
}

/* BUTTONS */
.hero-buttons {
    display: flex;
    gap: 16px;
}

.btn {
    padding: 12px 26px;
    border-radius: 10px;
    border: 2px solid #22c55e;
    background: transparent;
    color: #166534;
    font-weight: 600;
    cursor: pointer;
}

.btn.primary {
    background: #22c55e;
    color: #ffffff;
}

/* SECTIONS */
section {
    padding: 110px 0;
}

section h2 {
    font-size: 2.2rem;
    color: #0f172a;
    margin-bottom: 20px;
}

/* CARDS */
.card {
    background: #ffffff;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
}
"""
    return base_css + "\n\n" + (ai_css or "")

# --------------------------------------------------
# ZIP
# --------------------------------------------------
def create_zip(html, css, js):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("index.html", html)
        z.writestr("style.css", css)
        z.writestr("script.js", js)
    buf.seek(0)
    return buf

# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------
st.title("🚀 AI Portfolio Website Generator")

uploaded = st.file_uploader("Upload Resume (PDF / DOCX)", ["pdf", "docx"])

if uploaded:
    resume_text = extract_resume(uploaded)

    if not resume_text.strip():
        st.error("Resume extraction failed")
        st.stop()

    st.success("Resume loaded")

    if st.button("Generate Portfolio Website"):
        with st.spinner("Generating light-themed portfolio..."):
            html, css, js = parse_blocks(call_gemini(build_prompt(resume_text)))

            html = inject_assets(html)
            css = enhance_css(css)

            zip_file = create_zip(html, css, js)

            st.success("Portfolio generated successfully!")

            st.download_button(
                "⬇️ Download Website",
                zip_file,
                "portfolio_website.zip",
                "application/zip"
            )

            with st.expander("HTML Preview"):
                st.code(html, language="html")
