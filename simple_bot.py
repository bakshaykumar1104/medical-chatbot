"""
Rule-Based Medical Prototype Bot — Indian State Healthcare Context
Zero-dependency terminal bot.
"""

import re

topics = [
    {
        "keywords": {"hello", "hi", "hey", "namaste", "start"},
        "answer": "Namaste! Welcome to Arogya Seva Clinic Assistant. Ask me about OPD timings, doctor consultations, Ayushman Bharat, or health topics like blood pressure and diabetes.",
    },
    {
        "keywords": {"hours", "timing", "timings", "opd", "time", "open", "sunday", "schedule", "address", "location"},
        "answer": (
            "Arogya Seva Clinic Timings (Plot 45, Main Hospital Road, Gandhi Nagar):\n"
            "• Monday to Saturday:\n"
            "  - Morning OPD: 8:30 AM to 1:00 PM\n"
            "  - Evening OPD: 4:30 PM to 8:00 PM\n"
            "• Sunday: Closed for routine OPD (emergency patients should visit the Government Area Hospital casualty or call 108).\n"
            "• Lab Blood Collection: 7:00 AM to 10:30 AM daily."
        ),
    },
    {
        "keywords": {"appointment", "book", "token", "fee", "fees", "cost", "price", "ayushman", "pmjay", "card"},
        "answer": (
            "Registration & Fees:\n"
            "• General OPD Consultation: ₹200\n"
            "• Ayushman Bharat (PM-JAY) & State Health Cards (Aarogyasri): 100% Free consultation & generic medicines.\n"
            "• Tokens are issued at the clinic front desk, or you can book via our website/WhatsApp."
        ),
    },
    {
        "keywords": {"emergency", "chest", "pain", "breath", "breathing", "bleeding", "stroke", "paralysis", "unconscious", "ambulance", "108", "112"},
        "answer": (
            "🚨 CRITICAL EMERGENCY NOTICE:\n"
            "If you or someone nearby is experiencing acute chest pain, breathlessness, loss of consciousness, or severe bleeding:\n"
            "• Immediately dial 108 for Free Emergency Ambulance Service.\n"
            "• Dial 112 for the National All-in-One Emergency Helpline.\n"
            "• For pregnant women and infant emergency transport, call 102.\n"
            "Do not wait or delay in seeking in-person hospital casualty care."
        ),
    },
    {
        "keywords": {"blood", "pressure", "bp", "hypertension", "systolic", "diastolic"},
        "answer": (
            "Blood Pressure Guidelines:\n"
            "• Normal: Below 120/80 mmHg. High BP (Hypertension): 130/80 mmHg or higher.\n"
            "• Indian Diet Tips: Strictly reduce salt (under 5g/day). Cut down papads, pickles (achar), and namkeens.\n"
            "• Include millets (ragi, jowar) and whole wheat rotis. Walk 30-45 mins daily.\n"
            "• Take prescribed morning BP tablets without skipping."
        ),
    },
    {
        "keywords": {"diabetes", "sugar", "glucose", "hba1c"},
        "answer": (
            "Diabetes (Blood Sugar) Care:\n"
            "• Normal Fasting: 70-99 mg/dL. Normal Post-Meal: Under 140 mg/dL. Normal HbA1c: Under 5.7%.\n"
            "• Diet: Reduce white rice, maida, sweets, and sugary chai. Eat more moong dal, chana, sprouts, paneer, and leafy greens (palak, methi)."
        ),
    },
    {
        "keywords": {"cholesterol", "lipid", "ldl", "hdl", "triglycerides"},
        "answer": (
            "Cholesterol Management:\n"
            "• Target Total Cholesterol: Under 200 mg/dL. Keep LDL (bad cholesterol) under 100 mg/dL.\n"
            "• Reduce samosas, pakodas, and re-used cooking oils. Limit oil intake to under 500ml per person/month."
        ),
    },
]


def get_reply(message: str) -> str:
    words = set(re.findall(r"\b\w+\b", message.lower()))
    for topic in topics:
        if words & topic["keywords"]:
            return topic["answer"]
    return (
        "Thank you for your question. For detailed medical evaluation or symptoms, please visit Arogya Seva Clinic "
        "during OPD hours (8:30 AM–1:00 PM, 4:30 PM–8:00 PM) to consult an MBBS doctor. "
        "For medical emergencies, immediately dial 108."
    )


def main():
    print("=" * 65)
    print("  🏥 AROGYA SEVA COMMUNITY CLINIC — ASSISTANT (INDIAN HEALTHCARE)")
    print("  Emergency Helpline: 108 (Ambulance) / 112 (National Helpline)")
    print("  Type 'exit' to quit.")
    print("=" * 65 + "\n")

    while True:
        try:
            user_msg = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_msg:
            continue
        if user_msg.lower() in ("exit", "quit", "q"):
            print("Bot: Namaste, stay healthy!")
            break

        reply = get_reply(user_msg)
        print(f"\nBot:\n{reply}\n")


if __name__ == "__main__":
    main()
