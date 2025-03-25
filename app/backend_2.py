import os
import sys
import uuid
import sqlite3
from flask import Flask, request, jsonify, send_file

# Ensure modules from other directories are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import core functionalities
from utils.resume_parser import extract_text_from_pdf  
from core.ats_scoring import compute_sbert_similarity  
from core.resume_feedback import generate_resume_suggestions 
from core.job_role_matcher import match_resume_to_job_role  
from core.resume_skill_extractor import extract_resume_skills  
from core.job_description import JOB_DESCRIPTIONS  

# Initialize Flask app
app = Flask(__name__)

# Directory to store resumes locally
UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SQLite Database Setup
DB_FILE = "resume_metadata.db"

def init_db():
    """Initializes the SQLite database for storing resume metadata."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                            resume_id TEXT PRIMARY KEY,
                            original_filename TEXT,
                            file_path TEXT,
                            ats_score REAL,
                            job_role TEXT,
                            skills TEXT
                        )''')
        conn.commit()

# Initialize the database
init_db()

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Uploads resume, extracts text, computes ATS score, and stores metadata locally."""
    try:
        file = request.files["resume"]
        if not file:
            return jsonify({"error": "No file received"}), 400
        
        job_description = request.form.get("job_description", "").strip()

        # Extract text & skills from resume
        resume_text = extract_text_from_pdf(file)
        resume_skills = extract_resume_skills(resume_text)
        
        # Determine job role
        detected_job_role = match_resume_to_job_role(resume_skills)

        # If no job description provided, use a default one based on detected job role
        if not job_description:
            job_description = JOB_DESCRIPTIONS.get(detected_job_role, "Looking for a skilled software engineer.")
        print("✅ Final Job Description:", job_description)  # Debug print

        # Generate unique resume ID & save locally
        resume_id = str(uuid.uuid4())  
        unique_filename = f"{resume_id}.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        # Compute ATS Score
        ats_score = compute_sbert_similarity(resume_text, job_description)
        suggestions = generate_resume_suggestions(detected_job_role, resume_skills, resume_text, ats_score)

        # Store metadata in SQLite
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO resumes (resume_id, original_filename, file_path, ats_score, job_role, skills) VALUES (?, ?, ?, ?, ?, ?)",
                           (resume_id, file.filename, file_path, ats_score, detected_job_role, ",".join(resume_skills)))
            conn.commit()

        return jsonify({
            "message": "Upload successful!",
            "resume_id": resume_id,
            "job_role": detected_job_role,
            "skills": resume_skills,
            "ats_score": ats_score,
            "suggestions": suggestions,
            "file_path": file_path
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Log error
        return jsonify({"error": str(e)}), 500

@app.route("/view/<resume_id>")
def view_pdf(resume_id):
    """Fetches a PDF file stored locally using its unique resume_id."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM resumes WHERE resume_id = ?", (resume_id,))
            result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Resume not found"}), 404

        return send_file(result[0], as_attachment=True)  # Serve the file for download

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/metadata", methods=["GET"])
def get_resumes():
    """Fetches all stored resume metadata from SQLite."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT resume_id, original_filename, ats_score, job_role, skills FROM resumes")
            resumes = [{"resume_id": row[0], "original_filename": row[1], "ats_score": row[2], "job_role": row[3], "skills": row[4].split(",")} for row in cursor.fetchall()]

        return jsonify({"resumes": resumes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
