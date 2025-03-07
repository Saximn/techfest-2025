# BERT-LIME Fact Checker & Google Fact Checker 🔍

## About :information_source:
BERT-LIME Fact Checker is a Chrome extension combined with a backend Flask service that analyzes news articles for bias and misinformation. It leverages a BERT-based text classification model with LIME for explainability, performs media analysis (image classification and video URL extraction), and integrates with the Google Fact Checker API to provide additional fact-checking data.

**Features:**
- **Text Analysis with Explainability:** Uses a BERT-based classifier combined with LIME to provide interpretable model predictions.
- **Media Analysis:** Extracts and classifies images (and video URLs as placeholders) from news pages.
- **Google Fact Checker API Integration:** Retrieves fact-checking data based on the article content.

## Installation

### Prerequisites
- **Python 3.9+**
- **Google Chrome**
- A valid API key for the [Google Fact Checker API](https://developers.google.com/fact-check/tools/api)

### Clone the Repository
```
git clone https://github.com/YourUsername/BERT-LIME-FactChecker.git
cd BERT-LIME-FactChecker
```

### Backend Setup
Install Python Dependencies
Navigate to the /backend directory and install the required packages:

```
cd backend
pip install -r requirements.txt
```

### Configure Environment Variables
Open server.py and replace "YOUR_GOOGLE_API_KEY" with your actual Google Fact Checker API key.

Run the Backend Server
```
python server.py
The server will run on http://localhost:5000.
```

### Chrome Extension Setup
Load the Extension in Chrome
1. Open Google Chrome and navigate to:
```
chrome://extensions/
```

2. Enable Developer Mode.
3. Click Load unpacked and select the chrome-extension/ folder.
   
### Usage
Ensure the Flask backend is running on port 5000.
Visit a news article page in Chrome.
Click the extension icon to open the popup.
Use the Analyze Article button to perform text (BERT+LIME) and media analysis, or use the Google Fact Check button to query the Google Fact Checker API.
Results (HTML explanations, image classification results, and fact-checker data) will be displayed in the popup.
Directory Structure

```
BERT-LIME-FactChecker/
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   └── icon.png
└── backend/
    ├── server.py
    └── requirements.txt
```

### Tech Stack
- Backend
- Python 3.9+
- Flask
- Hugging Face Transformers
- LIME
- Requests, Pillow, NumPy
- Chrome Extension
- HTML, CSS, JavaScript
- APIs
- Google Fact Checker API


