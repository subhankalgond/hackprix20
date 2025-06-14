from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("symptom_list.pkl", "rb") as f:
    Sympton = pickle.load(f)

@app.route("/assist", methods=["POST"])
def assist():
    data = request.json
    input_symptoms = data.get("symptoms", [])

    input_vector = [1 if symptom in input_symptoms else 0 for symptom in Sympton]

    try:
        probabilities = model.predict_proba([input_vector])[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [(model.classes_[i], float(probabilities[i])) for i in top_indices]

        return jsonify({"suggestions": top_predictions})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
