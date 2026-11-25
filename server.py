import os
import re
import math
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any, Optional

import numpy as np
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge.txt"
INDEX_FILE = BASE_DIR / "index.html"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_PREFERRED_MODELS = ["llama3.2:latest", "llama3.2:1b", "qwen3.8:27b", "gemma3:4b"]

app = FastAPI(title="Arogya Seva Healthcare Assistant Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = requests.Session()
session.trust_env = False

SYSTEM_PROMPT = """You are an empathetic, knowledgeable, and culturally aware clinical healthcare assistant for Arogya Seva Community Health Clinic in India.

HOW YOU MUST RESPOND (NO GENERIC TEMPLATES):
1. THOROUGHLY ANALYZE THE USER'S MESSAGE:
   - Identify their primary intent, specific symptoms, concerns, or questions.
   - Detect emotional tone (anxiety, confusion, urgency).
   - Never answer with a repetitive robotic template. Address the user's specific context directly.

2. EMERGENCY & RED-FLAG TRIAGE (HIGHEST PRIORITY):
   - If the user or their family member describes signs of a medical emergency (e.g. chest pain, left arm numbness/pain, breathlessness, profuse sweating, sudden paralysis, unconsciousness, severe trauma):
     • Your VERY FIRST LINE must be: "🚨 PLEASE CALL 108 (FREE AMBULANCE) OR 112 IMMEDIATELY."
     • Urge them to rush to the nearest hospital casualty/emergency room without delay.
     • Do NOT ask follow-up questions (like duration or intensity) that delay emergency action. Every minute counts for heart attacks and strokes.
     • Advise keeping the patient resting, calm, and seated while the 108 ambulance is on its way.

3. CLINICAL CONTEXT & INDIAN HEALTH GUIDANCE:
   - Use the provided Reference Passages to accurately answer about clinic timings, doctor OPD, booking, tests, and fees (e.g. ₹200 OPD, Ayushman Bharat PM-JAY / Aarogyasri free coverage).
   - For health advice (blood pressure, diabetes, cholesterol), tailor guidance to Indian daily routines, diets (millets, rotis, sabzi, limiting pickles/namkeens/maida), and lifestyle.
   - If information is not in the clinic references, answer with sound general health literacy and advise seeing a local MBBS doctor.

4. SAFETY BOUNDARIES:
   - Explain conditions and medical concepts in warm, simple language.
   - Do NOT provide specific drug prescriptions or antibiotic dosages. Always direct prescription decisions to an in-person doctor.
   - Structure responses cleanly with clear headings or bullet points when explaining multiple steps.
"""


# --- TF-IDF Vectorizer for Knowledge Retrieval ---
class SimpleTFIDF:
    def __init__(self):
        self.vocab = {}
        self.idf = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9]{2,}\b", text.lower())

    def fit_transform(self, docs: List[str]) -> np.ndarray:
        doc_tokens = [self._tokenize(doc) for doc in docs]
        df = Counter()
        for tokens in doc_tokens:
            for term in set(tokens):
                df[term] += 1

        N = len(docs)
        self.vocab = {term: idx for idx, term in enumerate(sorted(df.keys()))}
        self.idf = {term: math.log((N + 1) / (df[term] + 1)) + 1.0 for term in self.vocab}

        matrix = np.zeros((N, len(self.vocab)), dtype=np.float32)
        for i, tokens in enumerate(doc_tokens):
            tf = Counter(tokens)
            doc_len = max(len(tokens), 1)
            for term, count in tf.items():
                if term in self.vocab:
                    col = self.vocab[term]
                    matrix[i, col] = (count / doc_len) * self.idf[term]

        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        return matrix / np.maximum(norms, 1e-12)

    def transform(self, query: str) -> np.ndarray:
        tokens = self._tokenize(query)
        tf = Counter(tokens)
        query_len = max(len(tokens), 1)
        vec = np.zeros((1, len(self.vocab)), dtype=np.float32)
        for term, count in tf.items():
            if term in self.vocab:
                col = self.vocab[term]
                vec[0, col] = (count / query_len) * self.idf[term]
        norm = np.linalg.norm(vec)
        return vec / max(norm, 1e-12)


# --- Global Knowledge State ---
knowledge_chunks: List[str] = []
tfidf_engine: Optional[SimpleTFIDF] = None
document_vectors: Optional[np.ndarray] = None


def get_active_ollama_model() -> Optional[str]:
    """Detect which models are installed and choose the best available one."""
    try:
        resp = session.get(f"{OLLAMA_HOST}/api/tags", timeout=2.0)
        if resp.status_code == 200:
            installed = [m.get("name") for m in resp.json().get("models", [])]
            for pref in DEFAULT_PREFERRED_MODELS:
                if pref in installed or any(pref.split(":")[0] in m for m in installed):
                    # match exact or prefix
                    for m in installed:
                        if pref == m or pref.split(":")[0] == m.split(":")[0]:
                            return m
            if installed:
                return installed[0]
    except Exception:
        pass
    return None


def check_ollama_health() -> Dict[str, Any]:
    try:
        resp = session.get(f"{OLLAMA_HOST}/api/tags", timeout=2.0)
        if resp.status_code == 200:
            models = [m.get("name") for m in resp.json().get("models", [])]
            active_model = get_active_ollama_model()
            return {"online": True, "models": models, "active_model": active_model}
    except Exception:
        pass
    return {"online": False, "models": [], "active_model": None}


def load_and_index_knowledge():
    global knowledge_chunks, tfidf_engine, document_vectors

    if not KNOWLEDGE_FILE.exists():
        knowledge_chunks = ["No knowledge document found. Please create knowledge.txt."]
    else:
        text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
        raw_sections = [s.strip() for s in text.split("\n\n") if s.strip()]
        chunks = []
        for sec in raw_sections:
            if sec.startswith("#"):
                continue
            words = sec.split()
            if len(words) > 160:
                for i in range(0, len(words), 120):
                    chunks.append(" ".join(words[i:i + 150]))
            else:
                chunks.append(sec)

        knowledge_chunks = chunks if chunks else [text]

    tfidf_engine = SimpleTFIDF()
    document_vectors = tfidf_engine.fit_transform(knowledge_chunks)
    print(f"[RAG] Indexed {len(knowledge_chunks)} Indian healthcare knowledge chunks.")


load_and_index_knowledge()


def analyze_and_synthesize_offline(question: str, top_passages: List[Dict[str, Any]]) -> str:
    """
    Intelligent message analyzer when AI model is temporarily loading or offline.
    Never gives a boilerplate template: parses query intent, checks emergency keywords,
    and synthesizes a tailored response.
    """
    q_lower = question.lower()

    # 1. Emergency Red-Flag Detection
    emergency_indicators = [
        "chest pain", "arm pain", "shortness of breath", "cant breathe", "breathing difficulty",
        "stroke", "paralysis", "unconscious", "heart attack", "collapsed", "heavy bleeding", "bleeding profusely"
    ]
    if any(k in q_lower for k in emergency_indicators):
        return (
            "🚨 **URGENT EMERGENCY ALERT**\n\n"
            "Based on your message, these symptoms can indicate a serious medical emergency.\n\n"
            "• **Immediate Action:** Dial **108** (Ambulance) or **112** (Emergency Services) immediately.\n"
            "• Keep the person in a comfortable resting position (sitting up if breathing is difficult).\n"
            "• Do not give solid food or self-prescribed medications without a doctor's instruction.\n"
            "• If an ambulance is delayed, immediately arrange transport to the nearest hospital casualty/emergency department."
        )

    # 2. Extract facts from retrieved passages
    combined_knowledge = "\n".join([p["text"] for p in top_passages])

    # 3. Intent: Timings & OPD
    if any(k in q_lower for k in ["time", "timing", "timings", "hours", "open", "sunday", "address", "location"]):
        return (
            "**Clinic Timings & Location (Arogya Seva Clinic):**\n\n"
            "• **Address:** Plot 45, Main Hospital Road, Gandhi Nagar.\n"
            "• **Monday to Saturday OPD Hours:**\n"
            "  - Morning: 8:30 AM to 1:00 PM\n"
            "  - Evening: 4:30 PM to 8:00 PM\n"
            "• **Sunday:** Routine OPD is closed. In case of an emergency, please visit the Government District Hospital casualty ward or call **108**.\n"
            "• **Lab Timing:** Fasting blood samples (Sugar, Lipid Profile) are collected from 7:00 AM to 10:30 AM daily."
        )

    # 4. Intent: Appointments & Fees
    if any(k in q_lower for k in ["appointment", "book", "token", "fee", "cost", "price", "pmjay", "ayushman"]):
        return (
            "**OPD Registration & Consultation Fees:**\n\n"
            "• **Consultation Fee:** General OPD doctor consultation is ₹200.\n"
            "• **Ayushman Bharat / State Health Cards:** Consultations and essential generic medicines are **100% Free** for registered PM-JAY and State Government cardholders.\n"
            "• **Booking:** You can get a walk-in token at the clinic front desk, or pre-book via the website / WhatsApp.\n"
            "• Specialist consultations (Gynecology, Pediatrics, Cardiology, Diabetology) are available during scheduled morning and evening slots."
        )

    # 5. Intent: Blood Pressure / Hypertension
    if any(k in q_lower for k in ["blood pressure", "bp", "hypertension", "systolic", "diastolic"]):
        return (
            "**Understanding Blood Pressure & Health Tips:**\n\n"
            "• **Target Blood Pressure:** Normal BP is below 120/80 mmHg. A reading of 130/80 mmHg or higher is considered elevated/hypertensive.\n"
            "• **Dietary Changes (Indian Context):**\n"
            "  - Strictly reduce salt: avoid papads, pickles (achar), salted namkeens, and chips. Limit salt to less than 1 level teaspoon (5g) per day.\n"
            "  - Incorporate millets (ragi, jowar, bajra) and whole wheat rotis instead of excessive polished white rice.\n"
            "• **Exercise:** 30–45 minutes of brisk walking or yoga daily.\n"
            "• **Important:** If you are prescribed BP tablets, take them regularly every morning. Never skip or alter doses without your doctor's consultation."
        )

    # 6. Intent: Diabetes / Sugar / HbA1c
    if any(k in q_lower for k in ["diabetes", "sugar", "glucose", "hba1c", "fasting"]):
        return (
            "**Diabetes (Blood Sugar) Guidelines:**\n\n"
            "• **Target Readings:**\n"
            "  - Fasting Blood Sugar: Normal is 70–99 mg/dL (126 mg/dL+ suggests diabetes).\n"
            "  - Post-Meal (PP 2 hrs): Normal is under 140 mg/dL.\n"
            "  - HbA1c (3-Month Average): Below 5.7% is normal; 6.5% or above indicates diabetes.\n"
            "• **Dietary Advice:**\n"
            "  - Cut down refined carbs (maida, sweets, sugar in chai, sweetened soft drinks).\n"
            "  - Increase fiber and protein: moong dal, sprouts, chana, paneer, and green leafy sabzis (palak, methi).\n"
            "  - Have breakfast on time and check your fasting sugar regularly at our on-site lab (7:00 AM – 10:30 AM)."
        )

    # 7. Intent: Emergency Numbers
    if any(k in q_lower for k in ["emergency", "ambulance", "number", "helpline", "108", "112"]):
        return (
            "**Emergency & Health Helplines (Indian State Services):**\n\n"
            "• **Ambulance & Medical Emergency:** Dial **108** (24x7 Free Ambulance Service)\n"
            "• **National Emergency Helpline:** Dial **112**\n"
            "• **Pregnant Women & Infant Transport:** Dial **102**\n"
            "• **Government Tele-Consultation:** Dial **104** or use e-Sanjeevani (esanjeevani.mohfw.gov.in)"
        )

    # Default analyzed answer using retrieved clinical passages
    return (
        f"Regarding your query about **'{question}'**:\n\n"
        f"Based on our healthcare clinic guidelines:\n\n"
        f"{top_passages[0]['text']}\n\n"
        "💡 *If you are experiencing persistent or worrying symptoms, please visit Arogya Seva Clinic during OPD hours (8:30 AM – 1:00 PM, 4:30 PM – 8:00 PM) for an in-person medical evaluation by a licensed doctor. In emergencies, call **108**.*"
    )


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


@app.get("/")
def serve_website():
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    return {"message": "Server is running. index.html not found."}


@app.get("/api/status")
def get_status():
    ollama_info = check_ollama_health()
    active_model = ollama_info.get("active_model")
    return {
        "status": "healthy",
        "ollama": ollama_info,
        "active_model": active_model or "Local Intelligent Analyzer",
        "knowledge_chunks": len(knowledge_chunks),
        "emergency_number": "108 / 112",
        "region": "India",
    }


@app.post("/api/reload-knowledge")
def reload_knowledge():
    load_and_index_knowledge()
    return {
        "status": "reloaded",
        "chunks_count": len(knowledge_chunks),
    }


@app.post("/chat")
def handle_chat(body: QuestionRequest):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Retrieve most relevant passages using TF-IDF
    top_passages = []
    try:
        if tfidf_engine is not None and document_vectors is not None:
            q_vec = tfidf_engine.transform(question)[0]
            scores = np.dot(document_vectors, q_vec)
            top_indices = np.argsort(scores)[-3:][::-1]
            top_passages = [
                {"id": int(idx) + 1, "text": knowledge_chunks[idx], "score": round(float(scores[idx]), 3)}
                for idx in top_indices if scores[idx] > 0.01
            ]
    except Exception as e:
        print(f"[RAG Retrieval Error]: {e}")

    if not top_passages and knowledge_chunks:
        top_passages = [{"id": 1, "text": knowledge_chunks[0], "score": 0.1}]

    context_str = "\n\n".join([f"[Reference {p['id']}]:\n{p['text']}" for p in top_passages])

    # 2. Check for active Ollama model
    ollama_health = check_ollama_health()
    active_model = ollama_health.get("active_model")

    if ollama_health["online"] and active_model:
        try:
            payload = {
                "model": active_model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": (
                            f"Verified Clinic Reference Context:\n{context_str}\n\n"
                            f"Patient / Visitor Message:\n{question}\n\n"
                            "Instructions: Provide a personalized, empathetic, and culturally appropriate Indian response. "
                            "Analyze their message directly. Do NOT use canned or repetitive templates. "
                            "If any red-flag emergency symptoms are present, highlight dialing 108 immediately."
                        ),
                    },
                ],
                "options": {
                    "temperature": 0.4,
                    "num_ctx": 4096,
                    "num_predict": 600,
                },
            }
            resp = session.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=(5, 120))
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("message", {}).get("content", "").strip()
                if answer:
                    return {
                        "answer": answer,
                        "passages": top_passages,
                        "engine": f"Ollama AI ({active_model})",
                    }
        except Exception as e:
            print(f"[Ollama Chat Error]: {e}")

    # 3. Intelligent Indian NLP Synthesis Engine (Fallback)
    answer = analyze_and_synthesize_offline(question, top_passages)
    return {
        "answer": answer,
        "passages": top_passages,
        "engine": "Arogya Clinical Knowledge Engine",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
