from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

app = Flask(__name__)
CORS(app)

# Load the disease prediction model and symptom list
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("symptom_list.pkl", "rb") as f:
    symptom_list = pickle.load(f)

GENERIC_SUGGESTIONS = [
    "🩺 Ask about recent travel or dietary changes.",
    "🧪 Recommend basic tests for further clarity.",
    "📋 Monitor symptoms over the next 24–48 hours.",
    "💧 Encourage hydration and good rest.",
    "🧍‍♂️ Discuss any ongoing medications or allergies."
]

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route("/assist", methods=["POST"])
def assist():
    data = request.get_json()
    input_symptoms = data.get("symptoms", [])

    if not input_symptoms:
        return jsonify({"error": "No symptoms provided."}), 400

    try:
        input_vector = [1 if s in input_symptoms else 0 for s in symptom_list]
        probabilities = model.predict_proba([input_vector])[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [(model.classes_[i], float(probabilities[i])) for i in top_indices]
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

    # Compose a prompt for Gemini
    prompt = (
        f"ML predicts:\n" +
        "\n".join([f"{disease} ({prob*100:.0f}%)" for disease, prob in top_predictions]) +
        "\n\nAs a medical assistant, help the doctor differentiate between these diseases. "
        "For each, mention distinguishing symptoms, suggest what to ask the patient, and recommend specific tests. "
        "Format your answer like this example:\n"
        '"Both diseases present with fever and fatigue. To differentiate:\n'
        'Dengue: pain behind eyes, rash.\n'
        'Malaria: chills, cyclical fever.\n'
        'Ask: Recent travel to malaria area?\n'
        'Tests: Dengue NS1, malaria smear."\n'
        "Each suggestion, symptom, question, or test must be only 1 line. The context should be clear and immediately understandable to a doctor. Be extremely brief."
    )
    gemini_suggestion = None
    if GEMINI_API_KEY:
        try:
            gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            gemini_response = gemini_model.generate_content([prompt])
            answer = gemini_response.text
            # Clean answer: remove unusual characters (##, &, etc), extra whitespace, and leading/trailing newlines
            answer = re.sub(r"[#&]+", "", answer)
            answer = re.sub(r"\n{3,}", "\n\n", answer)
            answer = answer.strip()
            gemini_suggestion = answer
        except Exception:
            gemini_suggestion = "Could not retrieve suggestions from Gemini."
    else:
        gemini_suggestion = "Gemini API key not configured."

    return jsonify({
        "top_predictions": top_predictions,
        "suggestion": gemini_suggestion
    })

@app.route("/gemini-answer", methods=["POST"])
def gemini_answer():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided."}), 400
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt])
        answer = response.text
    except Exception as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
