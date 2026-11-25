# 🏥 Arogya Seva — AI Healthcare & Clinic Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![Emergency](https://img.shields.io/badge/Emergency-108%20%2F%20112-red)

An intelligent, culturally grounded **Healthcare & Clinic Information Chatbot** tailored for **Indian State Healthcare Systems**. Grounded in clinical literacy and local clinic protocols, featuring real-time **108 Emergency Ambulance Triage**, OPD booking guidance, Ayushman Bharat (PM-JAY) schemes, and lifestyle health guidance.

---

## 🌐 Live Web Demo

You can test the live chatbot directly in your browser (no installation required):

👉 **[Launch Arogya Seva Chatbot](https://share.streamlit.io)**  
*(Hosted 24/7 on Streamlit Community Cloud)*

---

## 🌟 Key Features

* 🚑 **108 Indian Emergency Triage:**
  Immediate high-priority alert and instructions to dial **108** (Ambulance) or **112** (National Emergency) upon detecting acute symptoms like severe chest pain, left-arm numbness, stroke signs, breathlessness, or trauma.
* 🧠 **No Robotic Templates:**
  Intelligently analyzes incoming messages for clinical intent, urgency, and user context to synthesize warm, natural, and personalized responses.
* 🏛️ **Indian Healthcare & Public Schemes:**
  Answers queries about clinic OPD timings, token registration, consultation fees (₹200), and free coverage under **Ayushman Bharat (PM-JAY)** and State Health Cards (e.g. Aarogyasri).
* 🥗 **Indian Lifestyle & Dietary Guidance:**
  Practical advice on managing Hypertension and Type 2 Diabetes suited for Indian diets (millets, ragi, jowar, whole wheat rotis, limiting pickles/achar, papads, and namkeens).
* 🔒 **Strict Medical Safety Guardrails:**
  Provides health literacy and doctor visit preparation while explicitly barring unauthorized prescription of allopathic drugs and antibiotic dosages.

---

## 📁 Repository Structure

```
medical-chatbot/
├── streamlit_app.py     # 24/7 Cloud deployment app (Streamlit Cloud + Cloud AI)
├── server.py            # High-performance FastAPI RAG backend
├── index.html           # Modern responsive HTML5/JS web chat interface
├── knowledge.txt        # Verified Indian clinic protocols and health literacy data
├── simple_bot.py        # Lightweight zero-dependency rule-based terminal bot
├── requirements.txt     # Python dependencies
├── start.bat            # Windows 1-click local launcher
└── README.md            # Project documentation
```

---

## 🚀 How to Run Locally

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

### 2. Run Options

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

---

## ⚙️ Cloud Deployment (24/7 Free)

This repository is configured for 1-click deployment on **Streamlit Community Cloud**:
1. Fork or push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Select this repository and set **Main file path** to `streamlit_app.py`.
4. In **App Settings → Secrets**, add your free Groq API key:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Deploy!**

---

## ⚠️ Medical Disclaimer
This application is an educational prototype and clinic FAQ tool. It is **not** a diagnostic device and cannot replace consultation with a qualified medical professional. In life-threatening emergencies, always dial **108** or visit the nearest hospital casualty ward.
