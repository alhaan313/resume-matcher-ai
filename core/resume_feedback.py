import os
import google.generativeai as genai
from core.job_role_matcher import get_predefined_roles

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # ✅ Load from environment variable
genai.configure(api_key=GEMINI_API_KEY)

def fetch_gemini_suggestions(job_role, resume_text, missing_skills):
    """Uses Gemini API to generate personalized resume improvement suggestions."""
    prompt = f"""
    You are an AI resume optimizer. The user is applying for a **{job_role}** role. 
    Their resume text is as follows:

    {resume_text}

    Missing key skills: {', '.join(missing_skills)}

    Provide **three concise, actionable suggestions** to improve their resume to align better with this job.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.split("\n")[:3]  # Return top 3 suggestions
    except Exception as e:
        print(f"Error using Gemini API: {str(e)}")
        return ["Error fetching AI-based suggestions. Try again later."]

def generate_resume_suggestions(detected_job_role, resume_skills, resume_text, ats_score):
    """Generates AI-enhanced ATS suggestions based on missing skills & resume format."""
    
    job_roles = get_predefined_roles()
    required_skills = job_roles.get(detected_job_role, [])

    # Identify missing skills
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    # Generate improvement suggestions
    suggestions = []
    
    if ats_score < 50:
        suggestions.append("Your ATS score is low. Consider optimizing your resume for better keyword matching.")

    if missing_skills:
        suggestions.append(f"Consider adding these important skills: {', '.join(missing_skills[:5])}")

    if len(resume_text.split()) < 200:
        suggestions.append("Your resume is too short. Add more details about your experience and skills.")

    if "-" not in resume_text and "•" not in resume_text:  # Check if bullet points exist
        suggestions.append("Use bullet points to highlight your experience more clearly.")

    # Fetch AI-powered suggestions from Gemini
    ai_suggestions = fetch_gemini_suggestions(detected_job_role, resume_text, missing_skills)
    suggestions.extend(ai_suggestions)  # Add AI-generated suggestions

    return suggestions
