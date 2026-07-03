# EduGuide AI Mentorship Companion

EduGuide AI is an intelligent study assistant designed to transform the way you interact with educational materials. By processing uploaded academic documents (PDFs), the system provides summarized content, conceptual search, and custom quiz generation.

## 🚀 Features

- **Smart Document Parser:** Robust text extraction from multi-page PDFs using PyMuPDF.
- **RAG-based Mentorship:** Query your academic materials directly, receiving answers based on the retrieved context.
- **Quiz Generator:** Automatically generates interactive quizzes to test your understanding of the materials.
- **Offline History:** Keeps track of your query sessions, quiz scores, and learning progress.

---

## 📂 Project Structure

```text
eduguide_tutor/
├── app/
│   ├── __init__.py          # Marks app/ as a Python package
│   ├── app.py               # Main Streamlit user interface & state management
│   ├── document_handler.py  # PDF text extraction utilities
│   ├── quiz_engine.py       # LLM-based quiz questions generator
│   ├── rag_engine.py        # Search and RAG response orchestration
│   └── vector_handler.py    # Local document embedding index and lookup
├── config/
│   └── .env.example         # Template for environment keys (e.g. Gemini API Key)
├── database/
│   ├── __init__.py          # Marks database/ as a Python package
│   └── db_manager.py        # SQLite helper for persistent user logs and quiz history
├── docs/
│   └── sample.pdf           # Sample academic material (PDFs to tutor from)
├── .gitignore               # Configured git ignore files
├── requirements.txt         # Project dependencies
└── run.py                   # Automatic env initialization and Streamlit runner
```

---

## 🛠️ Setup & Installation

### 1. Clone the Project & Set Up Virtual Environment

Open your terminal in the project directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

Install requirements using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside the `config` folder by copying the example template:

```bash
cp config/.env.example config/.env
```

Open `config/.env` and update with your Google Gemini API Key:
```env
GEMINI_API_KEY=AIzaSy...your_gemini_api_key...
```

---

## 🎮 Running the Application

Start the application using the launcher script:

```bash
python run.py
```

This will check your environment and launch the Streamlit frontend. If your browser does not open automatically, copy the URL provided in the terminal (usually `http://localhost:8501`).
