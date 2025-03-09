import os
import logging
from flask import Flask, request, jsonify
from transformers import pipeline
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from lime.lime_text import LimeTextExplainer
import requests
from PIL import Image
from io import BytesIO
from peft import PeftModel
import torch
from flask_cors import CORS

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load environment variables and models
API_KEY = os.getenv("FACT_CHECK_API_KEY")
model_name = "distilbert-base-uncased"
model = DistilBertForSequenceClassification.from_pretrained(model_name)
model.eval()
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
lora_model = PeftModel.from_pretrained(model, "./fine_tuned_model")
image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
explainer = LimeTextExplainer(class_names=["REAL", "FAKE"])

def predict_proba(text_list):
    # Tokenize
    inputs = tokenizer(text_list, padding=True, truncation=True, return_tensors='pt')
    
    # Move to GPU if available
    # inputs = inputs.to("cuda")
    with torch.no_grad():
        # outputs = model(**inputs.to("cuda"))
        outputs = model(**inputs)
    
    # Convert logits -> probabilities
    probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()
    return probs

@app.route('/classify', methods=['POST'])
def classify_sentence():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        if probs[0][0] > probs[0][1]:
            label = "REAL"
            score = probs[0][0].item()
            explanation = explainer.explain_instance(text, predict_proba, num_features=5)
            weights_for_fake = explanation.as_list(label=1)
            sorted_list = sorted(weights_for_fake, key=lambda x: x[1], reverse=True)
            top_3_suspicious = []
            for token, weight in weights_for_fake:
                if weight > 0:                  # Only include words that push the model toward FAKE
                    top_3_suspicious.append(token)
                if len(top_3_suspicious) == 3:
                    break
            # 4. Build a sentence from these tokens
            if len(top_3_suspicious) > 0:
                # e.g. "The words token1, token2, token3 are suspicious."
                suspicious_str = ", ".join(top_3_suspicious)
            else:
                suspicious_str = ""
        else:
            label = "FAKE"
            score = probs[0][1].item()
            suspicious_str = ""
        if suspicious_str:
            explanation = f"The words {suspicious_str} are suspicious."
        else:
            explanation = "No suspicious words found."
        
       

        return jsonify({"label": label, "score": score, "explanation": explanation})
    except Exception as e:
        logging.error(f"Classification error: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500



@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
