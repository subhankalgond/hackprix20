import streamlit as st
import requests

st.set_page_config(page_title="AI Doctor Assistant", layout="wide")

# ----- 🌌 Fullscreen Spline Background -----
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
    }
    iframe.spline-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        border: none;
    }
    .app-content {
        position: relative;
        z-index: 1;
        padding: 1rem 2rem;
        background-color: rgba(0, 0, 0, 0);
        color: white;
        border-radius: 1rem;
        margin-top: 2rem;
        margin-left: auto;
        margin-right: auto;
        max-width: 90%;
    }
    .block-container {
        padding-top: 1rem !important;  /* ⬆ Pulls UI closer to top */
    }
    </style>

    <iframe class="spline-bg" src="https://my.spline.design/biometricscan-0Wnn7NDMFW28vqU3JwW33kf7/" allowfullscreen></iframe>
""", unsafe_allow_html=True)

# ----- 🧠 App UI -----
st.markdown('<div class="app-content">', unsafe_allow_html=True)
st.title("🧠 AI-Assisted Doctor Tool")

st.markdown("""
Welcome to the AI Doctor Assistant.  
This tool helps healthcare professionals by suggesting next steps based on reported symptoms.  

⚠️ **Note**: This tool does *not* provide a diagnosis.
""")

# --- Layout columns: Input left, result right ---
col1, col2 = st.columns([1, 2])

# --- LEFT SIDE: Symptoms Selection ---
with col1:
    all_symptoms = [
        'itching','skin_rash','nodal_skin_eruptions','dischromic__patches','continuous_sneezing','shivering',
        'chills','watering_from_eyes','stomach_pain','acidity','ulcers_on_tongue','vomiting','cough',
        'chest_pain','yellowish_skin','nausea','loss_of_appetite','abdominal_pain','yellowing_of_eyes',
        # Add more symptoms as needed
    ]
    selected_symptoms = st.multiselect("Select Patient Symptoms", all_symptoms)
    submitted = st.button("Get Assistance")

# --- RIGHT SIDE: AI Suggestions & Predictions ---
with col2:
    if submitted:
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            with st.spinner("Consulting AI Doctor..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/assist",
                        json={"symptoms": selected_symptoms},
                        timeout=60
                    )
                    if response.status_code == 200:
                        result = response.json()

                        st.subheader("🧬 Top Disease Predictions")
                        for disease, prob in result.get("top_predictions", []):
                            st.markdown(f"- **{disease}** ({prob*100:.2f}% confidence)")

                        st.subheader("💡 AI Clinical Suggestions")
                        suggestion = result.get("suggestion")
                        if suggestion:
                            st.success(suggestion)
                        else:
                            st.success("General advice: Stay hydrated, monitor your condition, and consult a medical professional.")
                    else:
                        st.error(f"Server Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)
