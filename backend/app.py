from flask import Flask, request, jsonify, send_from_directory
import pickle
import PyPDF2
import re
import os

# Serve React build
app = Flask(__name__, static_folder="static", static_url_path="")

# Load model
model = pickle.load(open("model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    return text

# Extract text from PDF safely
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        try:
            text += page.extract_text() or ""
        except:
            continue
    return text

# Get top 3 predictions
def predict_details(text):
    cleaned = clean_text(text)
    vec = tfidf.transform([cleaned])

    probs = model.predict_proba(vec)[0]
    classes = model.classes_

    top_indices = probs.argsort()[-3:][::-1]

    results = []
    for i in top_indices:
        results.append({
            "role": classes[i],
            "confidence": round(probs[i] * 100, 2)
        })

    return results


# API route
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    text = extract_text(file)

    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"}), 400

    return jsonify({
        "predictions": predict_details(text),
        
    })

# Serve React frontend
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

# Handle React routes (important for refresh)
@app.route("/<path:path>")
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# Run app
if __name__ == "__main__":
    app.run(debug=True)