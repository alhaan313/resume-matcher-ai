# job_role_classifier.py

def get_predefined_roles():
    """Returns a dictionary of predefined job roles and their required skills."""
    return {
        "Software Engineer": ["Python", "Java", "C++", "System Design", "AWS", "SQL"],
        "Data Scientist": ["Python", "Pandas", "Machine Learning", "Deep Learning", "TensorFlow", "SQL"],
        "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "AWS"],
        "Backend Developer": ["Python", "Django", "Flask", "PostgreSQL", "Redis", "Microservices"],
        "Frontend Developer": ["JavaScript", "React", "Vue.js", "CSS", "HTML", "TypeScript"],
        "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux"],
        "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "Cryptography", "Ethical Hacking"],
        "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform"],
        "Database Administrator": ["SQL", "PostgreSQL", "MongoDB", "Oracle", "Database Optimization"],
        "AI Researcher": ["Machine Learning", "Neural Networks", "Deep Learning", "AI Ethics"],
        "Full-Stack Developer": ["JavaScript", "React", "Node.js", "Django", "Flask", "SQL", "MongoDB"],
        "Embedded Systems Engineer": ["C", "C++", "Microcontrollers", "IoT", "RTOS"],
        "Game Developer": ["Unity", "Unreal Engine", "C#", "Game Physics", "Graphics Programming"],
        "Blockchain Developer": ["Solidity", "Ethereum", "Smart Contracts", "Cryptography"],
        "Business Intelligence Analyst": ["SQL", "Power BI", "Tableau", "Data Warehousing"],
    }

def match_resume_to_job_role(resume_skills):
    """Finds the closest matching job role based on skill overlap."""
    roles = get_predefined_roles()
    
    print(f"🔹 Resume Skills for Matching: {resume_skills}")  # Debugging

    best_match = None
    highest_overlap = 0

    for role, required_skills in roles.items():
        overlap = len(set(resume_skills) & set(required_skills))
        if overlap > highest_overlap:
            highest_overlap = overlap
            best_match = role

    print(f"🔹 Matched Job Role: {best_match}")  # Debugging
    return best_match
