# AWS is included here
# Main backend for my project

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
import uuid
from utils.resume_parser import extract_text_from_pdf  
from core.ats_scoring import compute_sbert_similarity  
from core.resume_feedback import generate_resume_suggestions 
from services.aws_handler import upload_to_s3, store_resume_metadata, get_resume_by_id, get_all_resumes
from core.job_role_matcher import match_resume_to_job_role  
from core.resume_skill_extractor import extract_resume_skills  
from core.job_description import JOB_DESCRIPTIONS  

app = Flask(__name__, 
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
)

# Ensure template directory exists
os.makedirs(app.template_folder, exist_ok=True)
os.makedirs(app.static_folder, exist_ok=True)

# Web Routes
@app.route("/")
def home():
    """Landing page with resume upload form."""
    return render_template('index.html')

@app.route("/history")
def history():
    """Page to view uploaded resumes."""
    resumes = get_all_resumes()
    return render_template('history.html', resumes=resumes)

@app.route("/analyze", methods=["POST"])
def analyze():
    """Page to show analysis results."""
    try:
        file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()
        
        if not file:
            return redirect(url_for('home'))
        
        # Process resume
        resume_text = extract_text_from_pdf(file)
        resume_skills = extract_resume_skills(resume_text)
        detected_job_role = match_resume_to_job_role(resume_skills)
        
        if not job_description:
            job_description = JOB_DESCRIPTIONS.get(detected_job_role, "Looking for a skilled software engineer.")
        
        # Generate unique ID and save file
        resume_id = str(uuid.uuid4())
        unique_filename = f"{resume_id}.pdf"
        
        # Upload to S3 or local storage
        file_url = upload_to_s3(file, unique_filename)
        
        # Compute scores and get suggestions
        ats_score = compute_sbert_similarity(resume_text, job_description)
        suggestions = generate_resume_suggestions(detected_job_role, resume_skills, resume_text, ats_score)
        
        # Store metadata
        store_resume_metadata(resume_id, file.filename, file_url, ats_score)
        
        return render_template('results.html',
            resume_id=resume_id,
            filename=file.filename,
            job_role=detected_job_role,
            skills=resume_skills,
            ats_score=ats_score,
            suggestions=suggestions,
            file_url=file_url
        )
        
    except Exception as e:
        return render_template('error.html', error=str(e))

# API Routes (existing routes modified to return both JSON and HTML based on Accept header)
@app.route("/upload", methods=["POST"])
def upload_resume():
    """API endpoint for resume upload."""
    try:
        file = request.files["resume"]
        if not file:
            return jsonify({"error": "No file received"}), 400
        
        job_description = request.form.get("job_description", "").strip()
        if not job_description:
            detected_job_role = match_resume_to_job_role(extract_resume_skills(extract_text_from_pdf(file)))
            job_description = JOB_DESCRIPTIONS.get(detected_job_role, "Looking for a skilled software engineer.")
        
        original_filename = file.filename

        resume_id = str(uuid.uuid4())  
        unique_filename = f"{resume_id}.pdf"

        resume_text = extract_text_from_pdf(file)
        resume_skills = extract_resume_skills(resume_text)
        detected_job_role = match_resume_to_job_role(resume_skills)

        ats_score = compute_sbert_similarity(resume_text, job_description)
        suggestions = generate_resume_suggestions(detected_job_role, resume_skills, resume_text, ats_score)

        file_url = upload_to_s3(file, unique_filename)

        store_resume_metadata(resume_id, original_filename, file_url, ats_score)

        response_data = {
            "message": "Upload successful!",
            "resume_id": resume_id,
            "job_role": detected_job_role,
            "skills": resume_skills,
            "ats_score": ats_score,
            "suggestions": suggestions,
            "file_url": file_url
        }

        if request.headers.get('Accept') == 'application/json':
            return jsonify(response_data)
        return redirect(url_for('analyze'))

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Print full error in logs
        return jsonify({"error": str(e)}), 500

@app.route("/view/<resume_id>")
def view_pdf(resume_id):
    """View or download PDF."""
    try:
        resume_metadata = get_resume_by_id(resume_id)
        if not resume_metadata:
            return jsonify({"error": "Resume not found"}), 404

        file_url = resume_metadata["file_url"]
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"file_url": file_url})
        return send_file(file_url, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/metadata", methods=["GET"])
def get_resumes():
    """Get all resumes metadata."""
    try:
        resumes = get_all_resumes()
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"resumes": resumes})
        return render_template('history.html', resumes=resumes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
