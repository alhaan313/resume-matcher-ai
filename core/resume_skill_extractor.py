import re 

def extract_resume_skills(resume_text):
    resume_text = resume_text.lower()  # Convert all text to lowercase
    skill_keywords = ["python", "java", "c++", "aws", "sql", "machine learning", 
                      "deep learning", "tensorflow", "flask", "django", "react", "docker"]

    detected_skills = []
    for skill in skill_keywords:
        safe_skill = re.escape(skill)
        if re.search(rf"\b{safe_skill}\b", resume_text):
            detected_skills.append(skill.capitalize())  # Keep original casing for output

    print(f"🔹 Extracted Skills: {detected_skills}")  # Debugging
    return list(set(detected_skills))
