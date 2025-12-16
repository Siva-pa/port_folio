# 🚀 AI Portfolio Website Generator

An **AI-powered portfolio website generator** that converts a resume (PDF or DOCX) into a **fully styled, responsive personal portfolio website** using **Google Gemini AI** and **Streamlit**.

This project automatically generates:
- `index.html`
- `style.css`
- `script.js`

all bundled into a downloadable ZIP file, ready to deploy or host.

---

## ✨ Features

- 📄 Upload resume in **PDF or DOCX**
- 🤖 Uses **Google Gemini AI** to generate website content
- 🎨 Professional **light sky-blue & green UI theme**
- 📱 Fully responsive layout
- 🧩 Structured sections:
  - Hero
  - About
  - Skills
  - Experience
  - Projects
  - Contact
- 🔗 Auto-linked CSS & JS (no broken styling)
- 📦 One-click ZIP download
- 🌐 Works offline after download

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit** – UI framework
- **Google Gemini AI** (`gemini-flash-latest`)
- **PyPDF2** – PDF text extraction
- **python-docx** – DOCX text extraction
- **HTML, CSS, JavaScript**
- **dotenv** – environment variable management

---

## 📂 Project Structure
├── app1.py # Main Streamlit application
├── .env # API key configuration
├── README.md # Project documentation
├── portfolio_website.zip # Generated output (after run)


---

## 🔑 Prerequisites

- Python **3.11**
- Google Gemini API Key (from Google AI Studio)

👉 Create API Key from:  
https://aistudio.google.com/app/apikey

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ai-portfolio-generator.git
cd ai-portfolio-generator
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install streamlit python-dotenv google-generativeai PyPDF2 python-docx
4️⃣ Configure API Key
Create a .env file:
GOOGLE_API_KEY=your_api_key_here
▶️ Run the Application
streamlit run app1.py

The app will open in your browser.

🧠 How It Works (End-to-End Flow)

1. User uploads a resume (PDF/DOCX)

2. Text is extracted using Python libraries

3. Resume content is sent to Gemini AI

4. AI generates:

  HTML structure
  
  CSS styling
  
  JavaScript (if required)

5. App enforces:

  Proper layout
  
  High-contrast colors
  
  Correct CSS & JS linking

6. Website files are zipped and downloaded

7. User opens index.html locally or deploys online

🎨 UI Theme

Background: Light sky-blue → green gradient

Text: High-contrast dark navy

Cards: White with shadow

Accent Color: Emerald green

Ensures maximum readability and professional appearance.
