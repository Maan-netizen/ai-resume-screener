"""
app.py
Flask API for the AI Resume Screener.

Endpoints:
  POST /api/scan        -> upload resume + job description, get match score
  GET  /api/history      -> get past scan results for a user
  GET  /api/health        -> health check
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

from matcher import extract_text, compute_match_score

load_dotenv()

app = Flask(__name__)
CORS(app)  # allow the React frontend (different origin) to call this API

# --- MongoDB setup ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["resume_screener"]
scans_collection = db["scans"]


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/scan", methods=["POST"])
def scan_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    jd_text = request.form.get("job_description", "").strip()
    if not jd_text:
        return jsonify({"error": "Job description is required"}), 400

    resume_file = request.files["resume"]
    filename = resume_file.filename
    file_bytes = resume_file.read()

    try:
        resume_text = extract_text(filename, file_bytes)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not resume_text.strip():
        return jsonify({"error": "Could not extract text from resume"}), 422

    result = compute_match_score(resume_text, jd_text)

    # Save scan to MongoDB for history/dashboard
    record = {
        "filename": filename,
        "job_description_snippet": jd_text[:200],
        "score": result["score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "created_at": datetime.utcnow(),
    }
    inserted = scans_collection.insert_one(record)

    return jsonify({
        "id": str(inserted.inserted_id),
        "filename": filename,
        "score": result["score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
    }), 200


@app.route("/api/history", methods=["GET"])
def get_history():
    records = list(
        scans_collection.find().sort("created_at", -1).limit(20)
    )
    for r in records:
        r["_id"] = str(r["_id"])
        r["created_at"] = r["created_at"].isoformat()
    return jsonify(records), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
