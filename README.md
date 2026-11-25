# Medical RAG Chatbot — Complete Project Guide

A full-stack, local-first **Healthcare & Clinic Information Chatbot** featuring **Retrieval-Augmented Generation (RAG)**, local AI models (via **Ollama**), and an interactive modern web interface.

---

## 🌟 Key Features

1. **Local-First & Offline Capable**: Runs completely on your computer with Ollama (`gemma3:4b` + `embeddinggemma`), ensuring zero per-query API bills and full privacy.
2. **Retrieval-Augmented Generation (RAG)**: Answers questions based on clinic policies, hours, services, and reviewed medical literacy documents in `knowledge.txt`.
3. **Clinical Safeguards & Guardrails**:
   - Explicit warnings and immediate emergency triage advice for life-threatening symptoms (e.g. chest pain, breathing difficulty).
   - Strict instructions barring diagnostic claims, prescriptions, and dosage advice.
4. **Interactive Modern Web UI**: Fast, responsive HTML5/JS interface with quick question chips, expandable source citations, and real-time backend status detection.
5. **Multiple Interfaces**:
   - **Modern Web App (Recommended)**: `server.py` + `index.html` (FastAPI + RAG + Ollama)
   - **Streamlit Interface**: `streamlit_app.py`
   - **Zero-Dependency Terminal Bot**: `simple_bot.py`

---

## 📁 Project Structure

```
Chatbot/
├── knowledge.txt        # Verified clinic FAQ and medical literacy knowledge base
├── server.py            # FastAPI RAG backend (chunking, vector search, Ollama chat)
├── index.html           # Modern responsive web chat interface with source citations
├── streamlit_app.py     # Streamlit web UI alternative
├── simple_bot.py        # Lightweight zero-dependency rule-based terminal bot
├── requirements.txt     # Python package dependencies
├── start.bat            # Windows 1-click startup script
└── README.md            # Comprehensive project documentation
```

---

## 🚀 Quick Start Guide

### Step 1: Set Up Python Virtual Environment

Open PowerShell in `c:\Users\aksha\Chatbot`:

```powershell
# Create virtual environment
python -m venv .venv

# Activate and install dependencies
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

### Step 2: Configure Ollama (Local AI)

Ollama is already installed on your system. To use the local AI models:

1. **Start Ollama service**:
   ```powershell
   ollama serve
   ```
2. **Download the recommended models** (in another terminal):
   ```powershell
   # Chat model (~3.4 GB)
   ollama pull gemma3:4b

   # Embedding model for RAG search
   ollama pull embeddinggemma
   ```

*(Note: If you run the server before Ollama models are pulled, the server will automatically activate **Local Fallback Mode** with TF-IDF indexing so you can still search and test without errors!)*

---

### Step 3: Run the Chatbot

#### Option A: Modern Web App (Recommended)
Run:
```powershell
.\.venv\Scripts\python.exe server.py
```
Or simply double-click **`start.bat`**.

Then open your browser to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

#### Option B: Streamlit Dashboard
```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```
Open: **[http://localhost:8501](http://localhost:8501)**.

#### Option C: Terminal Rule-Based Bot (Zero Dependencies)
```powershell
python simple_bot.py
```

---

## ⚙️ Customizing the Knowledge Base

To add your own clinic schedules, doctor names, or patient guides:
1. Open `knowledge.txt`.
2. Add your text blocks separated by double line breaks (`\n\n`).
3. Save the file.
4. Send a `POST` request to `http://127.0.0.1:8000/api/reload-knowledge` or restart `server.py` to re-index automatically.
