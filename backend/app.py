from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

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

    return jsonify({
        "top_predictions": top_predictions,
        "suggestion": "\n".join(GENERIC_SUGGESTIONS)
    })



if __name__ == "__main__":
    app.run(debug=True)
