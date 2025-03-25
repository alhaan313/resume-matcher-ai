import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
import uuid
from utils.resume_parser import extract_text_from_pdf  
from core.ats_scoring import compute_sbert_similarity  
from core.resume_feedback import generate_resume_suggestions 
from services.aws_handler import upload_to_s3, store_resume_metadata, get_resume_by_id, get_all_resumes
from core.job_role_matcher import match_resume_to_job_role  
from core.resume_skill_extractor import extract_resume_skills  
from core.job_description import JOB_DESCRIPTIONS  # Import predefined job descriptions


app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Uploads resume, extracts text, computes ATS score, and stores metadata."""
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

        # Add the job role and job description descripency
        
        # this is where we obtain our ats score from our function
        ats_score = compute_sbert_similarity(resume_text, job_description)
        suggestions = generate_resume_suggestions(detected_job_role, resume_skills, resume_text, ats_score)


        # Upload file to S3 database aws which ive integrated
        file_url = upload_to_s3(file, unique_filename)

        # Store metadata in DynamoDB
        store_resume_metadata(resume_id, original_filename, file_url, ats_score)

        return jsonify({
            "message": "Upload successful!",
            "resume_id": resume_id,
            "job_role": detected_job_role,
            "skills": resume_skills,
            "ats_score": ats_score,
            "suggestions": suggestions,
            "file_url": file_url
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Print full error in logs
        return jsonify({"error": str(e)}), 500

@app.route("/view/<resume_id>")
def view_pdf(resume_id):
    """Fetches a PDF from S3 using its unique resume_id and returns its URL."""
    try:
        resume_metadata = get_resume_by_id(resume_id)
        if not resume_metadata:
            return jsonify({"error": "Resume not found"}), 404

        return jsonify({"file_url": resume_metadata["file_url"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/metadata", methods=["GET"])
def get_resumes():
    """Fetches all stored resume metadata from DynamoDB."""
    try:
        resumes = get_all_resumes()
        return jsonify({"resumes": resumes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
