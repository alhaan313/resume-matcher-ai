import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from resume_sample_data import resume_data, jd_data  # Import the data from the external file

# Function to generate PDF filename based on current date and time
def generate_filename():
    # Get current date and time
    current_time = datetime.now()
    
    # Format the time and date
    formatted_time = current_time.strftime("%I_%M%p")  # Hour_MinuteAM/PM
    formatted_date = current_time.strftime("%d_%b")    # Day_Month (e.g., 4_Apr)
    
    # Return the file name in the format you specified
    return f"{formatted_time}_{formatted_date}.pdf"

# Generate PDF
def generate_pdf():
    # Create 'gen_resume' folder if it doesn't exist
    if not os.path.exists(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume'):
        os.makedirs(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume')

    # Define the filename using current date and time
    filename = os.path.join(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume', generate_filename())
    
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Get the style sheet for the document
    styles = getSampleStyleSheet()
    style = styles['Normal']

    # Creating sections for the resume
    content = []

    # Contact Information
    contact_info = f"Name: {resume_data['name']}\nAddress: {resume_data['address']}\nPhone: {resume_data['phone']}\nEmail: {resume_data['email']}\nLinkedIn: {resume_data['linkedin']}\nGitHub: {resume_data['github']}"
    content.append(Paragraph(contact_info, style))

    # Education
    education = f"Education: {resume_data['education']}"
    content.append(Paragraph(education, styles['Heading2']))

    # Work Experience
    work_experience = 'Work Experience:\n'
    for experience in resume_data['work_experience']:
        work_experience += f"{experience['job_title']}, {experience['company']}, {experience['employment_dates']}\n"
        work_experience += f"{experience['brief_job_description']}\n"
        work_experience += 'Key Achievements:\n'
        for achievement in experience['key_achievements']:
            work_experience += f"- {achievement}\n"
        work_experience += '\n'
    content.append(Paragraph(work_experience, styles['Heading2']))

    # Skills
    skills = 'Skills:\n'
    skills += f"Programming Languages: {', '.join(resume_data['skills']['programming_languages'])}\n"
    skills += f"Tools: {', '.join(resume_data['skills']['tools'])}\n"
    skills += f"Soft Skills: {', '.join(resume_data['skills']['soft_skills'])}"
    content.append(Paragraph(skills, styles['Heading2']))

    # Summary
    summary = f"Summary: {resume_data['summary']}"
    content.append(Paragraph(summary, styles['Heading2']))

    # Job Description
    jd = 'Job Description:\n'
    jd += f"{jd_data['job_title']}, {jd_data['company']}, {jd_data['employment_dates']}\n"
    jd += f"{jd_data['brief_job_description']}\n"
    jd += 'Key Achievements:\n'
    for achievement in jd_data['key_achievements']:
        jd += f"- {achievement}\n"
    content.append(Paragraph(jd, styles['Heading2']))

    # Building PDF document
    doc.build(content)

    print(f"Resume successfully generated and saved as: {filename}")

# Generate the PDF
generate_pdf()
