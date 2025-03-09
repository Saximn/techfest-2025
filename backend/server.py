import os
import logging
from flask import Flask, request, jsonify
from transformers import pipeline
from lime.lime_text import LimeTextExplainer
import requests
from PIL import Image
from io import BytesIO
from flask_cors import CORS

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load environment variables and models
API_KEY = os.getenv("FACT_CHECK_API_KEY")
classifier = pipeline("text-classification", model="openai-community/roberta-base-openai-detector", top_k=2)
image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
explainer = LimeTextExplainer(class_names=["REAL", "FAKE"])

@app.route('/classify', methods=['POST'])
def classify_sentence():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Run the classifier pipeline
        classification_results = classifier([text])  # Ensure input is passed as a list

        # `classifier` returns a list of dictionaries
        if not classification_results or not isinstance(classification_results, list):
            raise ValueError("Invalid output from classifier")

        # Initialize scores
        real_score, fake_score = 0.0, 0.0

        # Iterate through the list of results
        for result in classification_results[0]:  # Access the first (and only) item in the list
            if result["label"] == "REAL":
                real_score = result["score"]
            elif result["label"] == "FAKE":
                fake_score = result["score"]

        # Determine the final label and highest score
        label = "REAL" if real_score >= fake_score else "FAKE"
        score = max(real_score, fake_score)

        return jsonify({"label": label, "score": score})
    except Exception as e:
        logging.error(f"Classification error: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500



@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
