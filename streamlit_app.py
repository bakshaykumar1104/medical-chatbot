import os
from pathlib import Path
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge.txt"

# Default configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]

st.set_page_config(
    page_title="Arogya Seva Healthcare Assistant",
    page_icon="🏥",
    layout="centered",
)

# Custom header styling
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
        <div style="font-size:36px; background:#e0f2fe; padding:8px 14px; border-radius:12px;">🏥</div>
        <div>
            <h2 style="margin:0; font-size:24px; color:#0f172a;">Arogya Seva Health Clinic</h2>
            <p style="margin:0; font-size:14px; color:#64748b;">Community Healthcare Assistant • Indian State Guidelines</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.error(
    "🚨 **EMERGENCY ADVISORY (INDIA):** In severe emergencies (chest pain, stroke, breathlessness, heavy bleeding), "
    "immediately dial **108** for Free Ambulance Services or **112** for Emergency Services. Do not delay for an AI response."
)

# Load Knowledge Base
knowledge_text = ""
if KNOWLEDGE_FILE.exists():
    knowledge_text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

# Sidebar for Cloud & API Configuration
with st.sidebar:
    st.header("⚙️ Cloud Configuration")
    st.info("☁️ **Hosted 24/7 on Streamlit Cloud**\n\nRuns independently of your PC!")

    # Check for Groq API key in secrets or input
    saved_key = ""
    try:
        saved_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass

    if saved_key:
        st.success("Cloud AI: Connected & Active ✅")
        user_api_key = saved_key
    else:
        user_api_key = st.text_input(
            "Groq API Key (Free):",
            value=GROQ_API_KEY,
            type="password",
            help="Get a 100% free key at console.groq.com (no credit card needed).",
        )

    st.divider()
    st.subheader("🚑 Indian Helplines")
    st.write("• **Ambulance (Emergency):** `108`")
    st.write("• **National All-in-One:** `112`")
    st.write("• **Pregnant & Infant Transport:** `102`")
    st.write("• **Telemedicine Advice:** `104`")
    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your **Arogya Seva Healthcare Assistant**.\n\n"
                       "🩺 **Ask Any Health Question:** Feel free to ask about any symptoms, medical terms, blood pressure, sugar/diabetes, or Indian dietary guidance without hesitation.\n\n"
                       "🏥 **Doctor Consultation & Hospital Finder:** If you wish to consult a doctor or see a specialist, simply tell me your **city or area** and I will recommend the best reputed hospitals near you along with their contact details.\n\n"
                       "How may I assist you today?",
        }
    ]

# Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
user_question = st.chat_input("Ask a health or clinic question...")

if user_question:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Process and Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing message and consulting clinic guidelines..."):
            q_lower = user_question.lower()

            # 1. Emergency Red-Flag Intercept (High Priority)
            if any(k in q_lower for k in ["chest pain", "arm numbness", "heart attack", "stroke", "paralysis", "breathing", "heavy bleeding"]):
                answer = (
                    "🚨 **CRITICAL EMERGENCY ALERT**\n\n"
                    "Your symptoms could indicate an acute medical emergency (such as a heart attack or stroke).\n\n"
                    "• **PLEASE CALL 108 (FREE AMBULANCE) OR 112 IMMEDIATELY.**\n"
                    "• Do not delay or wait for further chat replies.\n"
                    "• Keep the patient sitting down, resting, and calm while the ambulance is en route, or head directly to the nearest hospital casualty ward."
                )
            # 2. Free Cloud AI via Groq (LLaMA 3.3 70B / LLaMA 3.2)
            elif user_api_key.strip():
                try:
                    headers = {
                        "Authorization": f"Bearer {user_api_key.strip()}",
                        "Content-Type": "application/json",
                    }
                    system_prompt = (
                        "You are an empathetic, culturally aware clinical assistant for Arogya Seva Community Health Clinic in India.\n\n"
                        "CORE OPERATING PRINCIPLES:\n"
                        "1. HEALTH & MEDICAL QUESTIONS (FREE TO ASK):\n"
                        "   - Users are encouraged to ask ANY health-related question without hesitation (symptoms, diet, wellness, lab tests, blood pressure, diabetes, cholesterol, etc.).\n"
                        "   - Provide an in-depth, limitless, and comprehensive explanation with practical Indian lifestyle advice. Do NOT hold back or truncate.\n\n"
                        "2. DOCTOR CONSULTATION & LOCATION-BASED HOSPITAL FINDER (CRITICAL):\n"
                        "   - When a user indicates they want to consult a doctor, book an appointment, or visit a hospital:\n"
                        "     • IF the user HAS NOT specified their location: Warmly ask: 'I would be happy to help you find the best doctor and hospital for your consultation! Could you please share your city, town, or area/district?'\n"
                        "     • IF the user HAS specified their location (or gives their city/state):\n"
                        "       Recommend the TOP reputable government and private hospitals in that location. For each hospital, provide:\n"
                        "       a) Hospital Name & Area/Locality\n"
                        "       b) Key Specialties & Facilities\n"
                        "       c) OPD / Consultation Booking Contact Numbers\n"
                        "       d) Emergency / Casualty Contact Number\n"
                        "       e) Ayushman Bharat (PM-JAY) coverage info where applicable\n"
                        "       Also mention the National Ayushman Bharat Helpline: 14555 and State Health Helpline: 104 for district-level hospital searches.\n\n"
                        "3. EMERGENCY RED-FLAG PROTOCOL:\n"
                        "   - If severe symptoms appear (chest pain, stroke signs, severe breathlessness, profuse bleeding), immediately urge calling 108 (Ambulance) or 112.\n\n"
                        "4. Never prescribe allopathic drugs or antibiotic dosages.\n\n"
                        f"Clinic & Indian Hospital Directory Reference:\n{knowledge_text[:4000]}"
                    )
                    answer = ""
                    for model_name in GROQ_MODELS:
                        payload = {
                            "model": model_name,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                *st.session_state.messages[-4:],
                            ],
                            "temperature": 0.4,
                        }
                        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=120)
                        if resp.status_code == 200:
                            data = resp.json()
                            answer = data["choices"][0]["message"]["content"]
                            break
                    if not answer:
                        answer = ""
                except Exception:
                    answer = ""

            # 3. Fallback Knowledge Engine (Runs 100% Free without any API key)
            if not locals().get("answer"):
                if any(k in q_lower for k in ["time", "timing", "timings", "hours", "open", "sunday"]):
                    answer = (
                        "**Arogya Seva Clinic Timings (Plot 45, Main Hospital Road, Gandhi Nagar):**\n\n"
                        "• **Morning OPD:** 8:30 AM to 1:00 PM (Monday to Saturday)\n"
                        "• **Evening OPD:** 4:30 PM to 8:00 PM (Monday to Saturday)\n"
                        "• **Sunday:** Closed for routine OPD (emergency cases directed to Government District Hospital / Area Hospital casualty, or call **108**).\n"
                        "• **Lab Blood Tests:** 7:00 AM to 10:30 AM daily for fasting samples."
                    )
                elif any(k in q_lower for k in ["consult", "doctor", "specialist", "hospital", "clinic near me", "appointment"]):
                    city_data = {
                        "hyderabad": (
                            "**Top Recommended Hospitals in Hyderabad for Doctor Consultation:**\n\n"
                            "1. **Apollo Hospitals (Jubilee Hills)**\n"
                            "   • Specialties: Cardiology, Oncology, Neurology, Orthopedics\n"
                            "   • Consultation Booking: 040-23607777 | Emergency: 1066\n\n"
                            "2. **Gandhi Hospital / Osmania General Hospital (Government Tertiary)**\n"
                            "   • Free & Subsidized Super-Specialty Consultations\n"
                            "   • Gandhi Hospital Contact: 040-27702222 | Osmania: 040-24600121\n\n"
                            "3. **Yashoda Hospitals (Somajiguda / Secunderabad / Malakpet)**\n"
                            "   • Multi-Specialty & Organ Transplant Center\n"
                            "   • Contact: 040-45674567\n\n"
                            "4. **Care Hospitals (Banjara Hills / Hitec City)**\n"
                            "   • Contact: 040-61656565\n\n"
                            "💡 *For nearby Ayushman Bharat / Aarogyasri empanelled hospitals, call toll-free: 14555.*"
                        ),
                        "bangalore": (
                            "**Top Recommended Hospitals in Bengaluru (Bangalore):**\n\n"
                            "1. **Manipal Hospital (Old Airport Road / Whitefield)**\n"
                            "   • Contact: 080-25024444 | Toll-Free: 1800-102-5555\n\n"
                            "2. **Victoria Hospital & BMCRI (Government Super-Specialty)**\n"
                            "   • Contact: 080-26701150\n\n"
                            "3. **Narayana Health City (Bommasandra)**\n"
                            "   • Cardiac, Oncology & Multi-Specialty Care\n"
                            "   • Contact: 080-71222222\n\n"
                            "4. **Fortis Hospital (Bannerghatta Road / Cunningham Rd)**\n"
                            "   • Contact: 080-66214444\n\n"
                            "💡 *Ayushman Bharat Hospital Helpline: 14555.*"
                        ),
                        "delhi": (
                            "**Top Recommended Hospitals in Delhi / NCR:**\n\n"
                            "1. **AIIMS New Delhi (Ansari Nagar)**\n"
                            "   • Premier Super-Specialty Care | Contact: 011-26588500 | Portal: orsdashboard.gov.in\n\n"
                            "2. **Safdarjung Hospital & Dr. RML Hospital (Government)**\n"
                            "   • Safdarjung: 011-26707444 | RML: 011-23365525\n\n"
                            "3. **Max Super Speciality Hospital (Saket / Patparganj)**\n"
                            "   • Contact: 011-26515050\n\n"
                            "4. **Medanta The Medicity (Gurugram)**\n"
                            "   • Contact: 0124-4141414\n\n"
                            "💡 *National Health Helpline: 104 / 14555.*"
                        ),
                        "mumbai": (
                            "**Top Recommended Hospitals in Mumbai:**\n\n"
                            "1. **KEM Hospital & Sion Hospital (Government/Municipal)**\n"
                            "   • KEM Contact: 022-24107000 | Sion: 022-24076381\n\n"
                            "2. **Hinduja Hospital (Mahim / Khar)**\n"
                            "   • Contact: 022-24451515\n\n"
                            "3. **Lilavati Hospital (Bandra West)**\n"
                            "   • Contact: 022-26751000\n\n"
                            "4. **Kokilaben Dhirubhai Ambani Hospital (Andheri West)**\n"
                            "   • Contact: 022-42696969\n\n"
                            "💡 *PM-JAY Scheme Helpline: 14555.*"
                        ),
                        "chennai": (
                            "**Top Recommended Hospitals in Chennai:**\n\n"
                            "1. **Apollo Hospitals (Greams Road)**\n"
                            "   • Contact: 044-28290200 | Emergency: 1066\n\n"
                            "2. **Rajiv Gandhi Government General Hospital (RGGGH)**\n"
                            "   • Contact: 044-25305000\n\n"
                            "3. **MIOT International (Manapakkam)**\n"
                            "   • Contact: 044-42002288\n\n"
                            "💡 *State Health Helpline: 104 | PM-JAY: 14555.*"
                        ),
                    }
                    found_city_info = None
                    for c_key, c_val in city_data.items():
                        if c_key in q_lower:
                            found_city_info = c_val
                            break
                    if found_city_info:
                        answer = found_city_info
                    else:
                        answer = (
                            "I would be glad to help you find the best doctor and hospital for your consultation!\n\n"
                            "📍 **Could you please tell me your city, town, or area?**\n\n"
                            "Once you share your location, I will provide the top-recommended government and private hospitals near you with full appointment contact numbers, emergency helplines, and specialty details.\n\n"
                            "*(Tip: You can also locate nearby Ayushman Bharat PM-JAY empanelled hospitals anytime by calling toll-free **14555** or **104**.)*"
                        )
                elif any(k in q_lower for k in ["fee", "fees", "cost", "price", "ayushman", "pmjay", "card"]):
                    answer = (
                        "**Consultation Fees & Ayushman Bharat Scheme:**\n\n"
                        "• **General OPD Consultation:** ₹200\n"
                        "• **Ayushman Bharat (PM-JAY) & State Health Cards:** 100% Free consultation and essential generic medicines.\n"
                        "• Walk-in tokens are available at the front desk, or you can pre-book via the clinic portal."
                    )
                elif any(k in q_lower for k in ["blood pressure", "bp", "hypertension"]):
                    answer = (
                        "**Blood Pressure Guidance (Indian Health Guidelines):**\n\n"
                        "• **Normal BP:** Below 120/80 mmHg. Elevated/Hypertension is 130/80 mmHg or higher.\n"
                        "• **Dietary Advice:** Strictly limit table salt, pickles (achar), papads, and salted namkeens. Aim for less than 1 level teaspoon (5g) salt per day.\n"
                        "• Eat millets (ragi, jowar) and whole wheat rotis. Walk 30–45 mins daily.\n"
                        "• Take prescribed morning BP tablets without skipping."
                    )
                elif any(k in q_lower for k in ["diabetes", "sugar", "glucose", "hba1c"]):
                    answer = (
                        "**Diabetes (Blood Sugar) Care:**\n\n"
                        "• **Fasting Sugar:** 70–99 mg/dL is normal (126+ indicates diabetes).\n"
                        "• **HbA1c (3-Month Average):** Below 5.7% is normal; 6.5% or above indicates diabetes.\n"
                        "• **Diet:** Reduce white polished rice, maida, sweets, and sugary chai. Increase moong dal, chana, sprouts, paneer, and leafy greens (palak, methi)."
                    )
                else:
                    answer = (
                        f"Thank you for your question regarding '{user_question}'.\n\n"
                        "For comprehensive evaluation or persistent symptoms, please visit Arogya Seva Clinic during OPD hours (8:30 AM–1:00 PM, 4:30 PM–8:00 PM) to consult an MBBS doctor. "
                        "For any acute medical emergency, immediately dial **108**."
                    )

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
