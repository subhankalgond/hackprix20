from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from llama_cpp import Llama

app = Flask(__name__)
CORS(app)

# Load the disease prediction model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("symptom_list.pkl", "rb") as f:
    symptom_list = pickle.load(f)

# Load the LLM (Phi-3 Mini GGUF) — Faster config
llm = Llama(
    model_path="C:\\llm\\models\\Phi-3-mini-4k-instruct-Q5_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    n_batch=512,
    verbose=False
)

@app.route("/ai-suggest", methods=["POST"])
def ai_suggest():
    data = request.get_json()
    input_symptoms = data.get("symptoms", [])

    if not input_symptoms:
        return jsonify({"error": "No symptoms provided."}), 400

    input_vector = [1 if s in input_symptoms else 0 for s in symptom_list]

    try:
        probabilities = model.predict_proba([input_vector])[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [(model.classes_[i], float(probabilities[i])) for i in top_indices]
    except Exception as e:
        return jsonify({"error": f"ML prediction error: {str(e)}"}), 500

    prompt = f"""
A doctor reports that a patient is experiencing the following symptoms: {', '.join(input_symptoms)}.
As an AI assistant, suggest helpful next steps, questions to ask the patient, or possible medical directions to consider.
Do not provide a diagnosis.
"""

    try:
        print("Sending prompt to LLM...")
        result = llm(prompt, max_tokens=128, stop=["</s>"])
        print("LLM responded.")
        suggestion = result["choices"][0]["text"].strip()
    except Exception as e:
        suggestion = f"AI Assistant Error: {str(e)}"

    return jsonify({
        "top_predictions": top_predictions,
        "suggestion": suggestion
    })

if __name__ == "__main__":
    app.run(debug=True)
