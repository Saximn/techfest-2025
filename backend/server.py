from flask import Flask, request, jsonify
import numpy as np
from transformers import pipeline
from lime.lime_text import LimeTextExplainer
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Use the specified model and fix the deprecated parameter.
classifier = pipeline("text-classification", model="openai-community/roberta-base-openai-detector", top_k=None)

def predict_proba(texts):
    predictions = classifier(texts)
    probs = np.array([[pred["score"] for pred in preds] for preds in predictions])
    return probs

# Update class names if needed. Here we use "REAL" and "FAKE".
class_names = ["REAL", "FAKE"]
explainer = LimeTextExplainer(class_names=class_names)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    explanation = explainer.explain_instance(text, predict_proba, num_features=10, num_samples=500)
    html_explanation = explanation.as_html()
    return jsonify({"explanation_html": html_explanation})

image_classifier = pipeline("image-classification")

@app.route('/analyze_media', methods=['POST'])
def analyze_media():
    data = request.get_json()
    images = data.get("images", [])
    videos = data.get("videos", [])
    results_html = "<div>"
    if images:
        results_html += "<h4>Image Analysis:</h4>"
        for url in images:
            try:
                response = requests.get(url, timeout=5)
                image = Image.open(BytesIO(response.content)).convert("RGB")
                prediction = image_classifier(image)[0]
                results_html += f"<p><strong>{url}:</strong> {prediction['label']} (score: {prediction['score']:.2f})</p>"
            except Exception as e:
                results_html += f"<p><strong>{url}:</strong> Error processing image.</p>"
    if videos:
        results_html += "<h4>Video Analysis:</h4>"
        for url in videos:
            results_html += f"<p><strong>{url}:</strong> Video analysis not supported yet.</p>"
    results_html += "</div>"
    return jsonify({"media_analysis_html": results_html})

@app.route('/google_fact_check', methods=['POST'])
def google_fact_check():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    api_key = "AIzaSyCadrHYAqCBuPJ_iOGVU3FM2WYOQOy743c"  # Replace with your actual API key.
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}&query={query}"
    r = requests.get(url)
    if r.status_code == 200:
        return jsonify(r.json())
    else:
        return jsonify({"error": "Error calling Google Fact Checker API"}), r.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
