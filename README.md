# 🏥 Arogya Seva — AI Healthcare & Clinic Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Model](https://img.shields.io/badge/Model-GPT--OSS%20120B%20%7C%20Qwen%2027B-purple)
![Inference](https://img.shields.io/badge/Inference-Limitless%20Token%20Generation-blue)
![Emergency](https://img.shields.io/badge/Emergency-108%20%2F%20112-red)

An intelligent, culturally grounded **Healthcare & Clinic Information Chatbot** tailored for **Indian State Healthcare Systems**. Powered by high-speed cloud LLMs (**OpenAI GPT-OSS 120B & Qwen 3.8 27B**) and local RAG capabilities, featuring real-time **108 Emergency Ambulance Triage**, OPD booking guidance, Ayushman Bharat (PM-JAY) schemes, and **unrestricted, limitless response generation**.

---

## 🌐 Live Web Demo

You can test the live chatbot directly in your browser (no installation or local PC required):

👉 **[Launch Arogya Seva Chatbot](https://share.streamlit.io)**  
*(Hosted 24/7 on Streamlit Community Cloud • Free to access on mobile and desktop)*

---

## 🌟 Key Features

* ♾️ **Limitless & Exhaustive Responses:**
  Configured without artificial token ceilings. When asked for full meal charts, multi-stage lifestyle guides, or detailed clinical literacy, the AI outputs the **complete, unabridged explanation** with zero mid-sentence cut-offs.
* 🚑 **108 Indian Emergency Protocol:**
  Immediate high-priority alert and instructions to dial **108** (Free Ambulance) or **112** (National Emergency) upon detecting red-flag acute symptoms such as crushing chest pain, left-arm numbness, stroke signs, breathing distress, or trauma.
* 🧠 **Dynamic Clinical Analysis (Zero Robotic Templates):**
  Actively assesses message intent, severity, and emotional context to provide warm, personalized, and empathetic responses tailored directly to the patient's inquiry.
* 🏛️ **Indian Public Healthcare & Schemes:**
  Answers queries about clinic OPD timings, token registration, consultation fees (₹200), and free healthcare benefits under **Ayushman Bharat (PM-JAY)** and State Health Cards (e.g. Aarogyasri).
* 🥗 **Culturally Tailored Dietary & Lifestyle Advice:**
  Practical advice on managing Hypertension and Type 2 Diabetes suited for Indian diets (millets, ragi, jowar, whole wheat rotis, portion control, limiting pickles/achar, papads, and namkeens).
* 🔒 **Strict Medical Safety Guardrails:**
  Provides health literacy and doctor visit preparation while strictly adhering to safety limits—barring unauthorized allopathic drug prescription or antibiotic dosage recommendations.

---

## 🏗️ Architecture & Tech Stack

| Layer | Technologies | Role |
|---|---|---|
| **Cloud AI (24/7)** | **OpenAI GPT-OSS 120B** & **Qwen 3.8 27B** (via Groq) | Ultra-fast, limitless cloud inference (300+ tok/s) with zero PC dependency |
| **Local AI (Offline)** | **LLaMA 3.2 3B / 1B** (via Ollama) | 100% offline local processing on your machine |
| **Grounding Engine** | In-Memory TF-IDF & Vector Similarity (`knowledge.txt`) | Retrieves verified clinic guidelines and Indian health facts |
| **Frontend Options** | **Streamlit Cloud** & **HTML5/Tailwind-style UI** | Responsive web chat interfaces with status pills and reference citations |
| **Backend API** | **FastAPI** + **Uvicorn** (Asynchronous Python 3.12) | High-performance REST endpoints (`/chat`, `/api/status`) |

---

## 📁 Repository Structure

```
medical-chatbot/
├── streamlit_app.py     # 24/7 Cloud deployment app (Streamlit Cloud + Limitless Groq AI)
├── server.py            # High-performance FastAPI RAG backend with infinite generation
├── index.html           # Modern responsive HTML5/JS web chat interface
├── knowledge.txt        # Verified Indian clinic protocols and health literacy data
├── simple_bot.py        # Lightweight zero-dependency rule-based terminal bot
├── requirements.txt     # Python dependencies
├── start.bat            # Windows 1-click local launcher
└── README.md            # Comprehensive project documentation
```

---

## 🚀 Running Locally

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/bakshaykumar1104/medical-chatbot.git
cd medical-chatbot

python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Launch Options

#### Option A: Streamlit Web Dashboard
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501).

#### Option B: FastAPI Backend + Custom HTML UI
```bash
python server.py
```
Open [http://localhost:8000](http://localhost:8000).

#### Option C: Zero-Dependency Terminal Bot
```bash
python simple_bot.py
```

---

## ⚙️ 24/7 Cloud Deployment Guide

This repository is pre-configured for instant deployment on **Streamlit Community Cloud**:
1. Fork or push this repository to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub.
3. Select your repository: `bakshaykumar1104/medical-chatbot`, branch: `main`, and main file: `streamlit_app.py`.
4. In **App Settings → Secrets**, add your free Groq API key:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Deploy!** Your app will be live 24/7 with limitless response generation and zero PC requirements.

---

## ⚠️ Medical Disclaimer
This application is an educational prototype and clinic FAQ tool. It is **not** a diagnostic medical device and cannot substitute for an in-person clinical consultation with a qualified doctor. In acute or life-threatening medical emergencies, immediately dial **108** or visit the nearest hospital casualty ward.
