import streamlit as st
import requests

st.set_page_config(page_title="AI Doctor Assistant", layout="wide")

# ----- 🌌 Fullscreen Spline Background -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [data-testid="stApp"] {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: #10131a;
        font-family: 'Inter', sans-serif;
    }
    .spline-bg-embed {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        border: none;
        opacity: 0.18;
        pointer-events: none;
    }
    .medical-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .medical-logo {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: #e6f6fd;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #2D9CDB;
        box-shadow: 0 2px 8px rgba(45,156,219,0.10);
    }
    .medical-title {
        font-size: 2.1rem;
        font-weight: 600;
        color: #1a365d;
        letter-spacing: -1px;
    }
    .app-content {
        position: relative;
        z-index: 1;
        background-color: #fff;
        color: #3a4a5d;
        border-radius: 1.2rem;
        margin-top: 2.5rem;
        margin-left: auto;
        margin-right: auto;
        max-width: 900px;
        box-shadow: 0 4px 32px rgba(45,156,219,0.08);
    }
    .card-section {
        background: #fafdff;
        border-radius: 1rem;
        box-shadow: 0 2px 12px rgba(45,156,219,0.07);
        margin-bottom: 1.5rem;
        border-left: 4px solid #2D9CDB;
    }
    .ai-answer-container {
        background: #e6f6fd;
        color: #1a365d;
        border-radius: 0.8rem;
        box-shadow: 0 1px 8px rgba(45,156,219,0.08);
        margin-top: 1.2rem;
        max-height: 180px;
        overflow-y: auto;
        font-size: 1.08rem;
        line-height: 1.6;
        border: 1px solid #b3e0fa;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2D9CDB 0%, #56CCF2 100%);
        color: #fff;
        border-radius: 0.5rem;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.2rem;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        transition: background 0.2s;
        box-shadow: 0 2px 8px rgba(45,156,219,0.08);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2196F3 0%, #2D9CDB 100%);
    }
    .stMultiSelect>div>div {
        background: #fafdff !important;
        color: #1a365d !important;
    }
    </style>

    <iframe class="spline-bg-embed" src="https://my.spline.design/biometricscan-0Wnn7NDMFW28vqU3JwW33kf7/" allowfullscreen></iframe>
""", unsafe_allow_html=True)

# Embed Spline as a subtle background
st.markdown('<iframe class="spline-bg-embed" src="https://my.spline.design/biometricscan-0Wnn7NDMFW28vqU3JwW33kf7/" allowfullscreen></iframe>', unsafe_allow_html=True)

# Professional Medical Header
st.markdown('<div class="medical-header"><div class="medical-logo">🩺</div><div class="medical-title">AI Clinical Assistant</div></div>', unsafe_allow_html=True)

st.markdown('<div class="app-content">', unsafe_allow_html=True)

st.markdown("""
This tool is designed for medical professionals to assist in clinical decision-making. Enter patient symptoms to receive ML-based predictions and concise, actionable AI suggestions for differential diagnosis and next steps.

⚠️ <b>Note</b>: This tool does <i>not</i> provide a final diagnosis. Use clinical judgment and confirm with appropriate tests.
""", unsafe_allow_html=True)

# --- Layout columns: Input left, result right ---
col1, col2 = st.columns([1, 2])

# --- LEFT SIDE: Symptoms Selection ---
with col1:
    st.markdown('<div class="card-section">', unsafe_allow_html=True)
    st.markdown("<b>Patient Symptoms</b>", unsafe_allow_html=True)
    all_symptoms = [
         'itching','skin_rash','nodal_skin_eruptions','dischromic__patches','continuous_sneezing','shivering',
    'chills','watering_from_eyes','stomach_pain','acidity','ulcers_on_tongue','vomiting','cough',
    'chest_pain','yellowish_skin','nausea','loss_of_appetite','abdominal_pain','yellowing_of_eyes',
    'burning_micturition','spotting__urination','passage_of_gases','internal_itching','indigestion',
    'muscle_wasting','patches_in_throat','high_fever','extra_marital_contacts','fatigue','weight_loss',
    'restlessness','lethargy','irregular_sugar_level','blurred_and_distorted_vision','obesity','excessive_hunger',
    'increased_appetite','polyuria','sunken_eyes','dehydration','diarrhoea','breathlessness','family_history','mucoid_sputum',
    'headache','dizziness','loss_of_balance','lack_of_concentration','stiff_neck','depression','irritability','visual_disturbances',
    'back_pain','weakness_in_limbs','neck_pain','weakness_of_one_body_side','altered_sensorium','dark_urine','sweating',
    'muscle_pain','mild_fever','swelled_lymph_nodes','malaise','red_spots_over_body','joint_pain','pain_behind_the_eyes',
    'constipation','toxic_look_(typhos)','belly_pain','yellow_urine','receiving_blood_transfusion','receiving_unsterile_injections',
    'coma','stomach_bleeding','acute_liver_failure','swelling_of_stomach','distention_of_abdomen','history_of_alcohol_consumption',
    'fluid_overload','phlegm','blood_in_sputum','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion',
    'loss_of_smell','fast_heart_rate','rusty_sputum','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus',
    'cramps','bruising','swollen_legs','swollen_blood_vessels','prominent_veins_on_calf','weight_gain','cold_hands_and_feets',
    'mood_swings','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','abnormal_menstruation','muscle_weakness',
    'anxiety','slurred_speech','palpitations','drying_and_tingling_lips','knee_pain','hip_joint_pain','swelling_joints','painful_walking','movement_stiffness',
    'spinning_movements','unsteadiness','pus_filled_pimples','blackheads','scurring','bladder_discomfort','foul_smell_of_urine','continuous_feel_of_urine',
    'skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze'
    ]
    selected_symptoms = st.multiselect("Select Symptoms", all_symptoms)
    submitted = st.button("Get AI Suggestions")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT SIDE: AI Suggestions & Predictions ---
with col2:
    if submitted:
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            with st.spinner("Consulting AI Clinical Assistant..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/assist",
                        json={"symptoms": selected_symptoms},
                        timeout=60
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown('<div class="card-section">', unsafe_allow_html=True)
                        st.markdown("<b>🧬 Top Disease Predictions</b>", unsafe_allow_html=True)
                        for disease, prob in result.get("top_predictions", []):
                            st.markdown(f"- <b>{disease}</b> ({prob*100:.2f}% confidence)", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('<div class="card-section">', unsafe_allow_html=True)
                        st.markdown("<b>💡 AI Differential Suggestions</b>", unsafe_allow_html=True)
                        suggestion = result.get("suggestion")
                        if suggestion:
                            st.markdown('<div class="ai-answer-container">', unsafe_allow_html=True)
                            for line in suggestion.split("\n"):
                                if line.strip():
                                    l = line.strip().lower()
                                    if any(k in l for k in ["test", "investigat", "lab"]):
                                        icon = "🧪"
                                    elif any(k in l for k in ["ask", "question", "history"]):
                                        icon = "❓"
                                    elif any(k in l for k in ["symptom", "sign", "present"]):
                                        icon = "🔎"
                                    elif any(k in l for k in ["differenti", "consider", "rule out"]):
                                        icon = "🩺"
                                    else:
                                        icon = "💡"
                                    st.markdown(f"<span style='font-size:18px;'>{icon}</span> {line}", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.success("General advice: Stay hydrated, monitor your condition, and consult a medical professional.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"Server Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)
