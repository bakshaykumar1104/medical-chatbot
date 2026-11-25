import os
import requests
import streamlit as st

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = "llama3.2:latest"

st.set_page_config(
    page_title="Arogya Seva Healthcare Assistant",
    page_icon="🏥",
    layout="centered",
)

st.title("🏥 Arogya Seva Clinic Assistant")
st.caption("Community Health Literacy & Clinic Guidance • Indian State Healthcare")

st.error(
    "🚨 **EMERGENCY HELPLINE (INDIA):** In case of life-threatening emergencies (chest pain, stroke symptoms, severe breathlessness, uncontrolled bleeding), "
    "immediately dial **108** for Free Ambulance Services or **112** for Emergency Services. Do not delay for a chatbot response."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your healthcare assistant at Arogya Seva Community Health Clinic. I can help you with OPD hours, token registration, consultation fees (₹200 / Free under Ayushman Bharat PM-JAY), or Indian dietary advice for managing blood pressure, diabetes, and cholesterol. How can I help you?",
        }
    ]

# Sidebar
with st.sidebar:
    st.header("Indian Health Helplines")
    st.write("🚑 **Ambulance / Medical:** `108`")
    st.write("🚨 **Unified Emergency:** `112`")
    st.write("👶 **Pregnant & Infant:** `102`")
    st.write("🩺 **Health Advice:** `104`")
    st.divider()

    # Ollama status
    active_model = DEFAULT_MODEL
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=1.5)
        if r.status_code == 200:
            models = [m.get("name") for m in r.json().get("models", [])]
            if DEFAULT_MODEL in models:
                active_model = DEFAULT_MODEL
            elif models:
                active_model = models[0]
            st.success(f"Ollama Online ✅ ({active_model})")
        else:
            st.warning("Ollama offline")
    except Exception:
        st.info("Using Local Knowledge Engine")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask a health or clinic question...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing message and preparing response..."):
            try:
                knowledge = ""
                if os.path.exists("knowledge.txt"):
                    with open("knowledge.txt", "r", encoding="utf-8") as f:
                        knowledge = f.read()

                system_prompt = (
                    "You are a compassionate healthcare assistant for Arogya Seva Health Clinic in India. "
                    "Analyze the user's message thoroughly. Never give robotic or generic template responses. "
                    "In severe emergencies, immediately advise calling 108 or 112. "
                    "Provide tailored Indian dietary and lifestyle advice. "
                    "Do NOT prescribe medicines or dosages.\n\n"
                    f"Clinic Knowledge:\n{knowledge[:2500]}"
                )

                payload = {
                    "model": active_model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages[-4:],
                    ],
                }

                resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=90)
                if resp.status_code == 200:
                    answer = resp.json().get("message", {}).get("content", "")
                else:
                    answer = "Unable to generate answer from Ollama. Please check connection."
            except Exception as e:
                # Fallback to direct analysis
                q_l = user_question.lower()
                if any(k in q_l for k in ["chest pain", "breath", "stroke", "bleeding"]):
                    answer = "🚨 **EMERGENCY:** Please dial **108** (Ambulance) or **112** immediately and go to the nearest casualty ward."
                else:
                    answer = "For consultation, please visit Arogya Seva Clinic during OPD hours (8:30 AM – 1:00 PM, 4:30 PM – 8:00 PM). General OPD is ₹200 or Free with Ayushman Bharat PM-JAY. In emergencies, call **108**."

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
