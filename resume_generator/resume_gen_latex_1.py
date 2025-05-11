import os
from datetime import datetime
from resume_sample_data import resume_data, jd_data  # Import the data from the external file

def generate_latex_filename():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I_%M%p")
    formatted_date = current_time.strftime("%d_%b")
    return f"JakeResume_{formatted_time}_{formatted_date}.tex"

def escape_latex_special_chars(text):
    # Escape special LaTeX characters
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    if isinstance(text, str):
        for char, escape in special_chars.items():
            text = text.replace(char, escape)
    return text

def generate_latex_resume():
    # Create 'gen_resume' folder if it doesn't exist
    if not os.path.exists(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume'):
        os.makedirs(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume')

    # Define the filename using current date and time
    filename = os.path.join(r'D:\Programming\resume-matcher-ai\resume_generator_test\gen_resume', generate_latex_filename())
    
    # Escape special characters in all text fields
    def process_data(data):
        if isinstance(data, str):
            return escape_latex_special_chars(data)
        elif isinstance(data, dict):
            return {k: process_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [process_data(item) for item in data]
        return data
    
    resume_data_processed = process_data(resume_data)
    jd_data_processed = process_data(jd_data)

    # Start building the LaTeX content for article class
    latex_content = r"""
\documentclass[letterpaper, 11pt]{article}
\usepackage[left=1in, top=1in, right=1in, bottom=1in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{fontspec}
\usepackage{microtype}
\usepackage{lmodern}
\usepackage{textcomp}

\setmainfont{Latin Modern Roman}[
    BoldFeatures={SmallCapsFont={Latin Modern Roman Caps}}
]

% For section formatting
\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}

\pagestyle{empty}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape """ + resume_data_processed['name'] + r"""} \\[2mm]
    """ + resume_data_processed['phone'] + r" | " + resume_data_processed['email'] + r" | " + resume_data_processed['linkedin'] + r" | " + resume_data_processed['github'] + r"""
\end{center}

%------------- Summary Section -------------
\section*{Summary}
""" + resume_data_processed['summary'] + r"""

%------------- Education Section -------------
\section*{Education}
\textbf{""" + resume_data_processed['education']['degree'] + r"""} \hfill \textbf{""" + resume_data_processed['education']['dates'] + r"""} \\
""" + resume_data_processed['education']['institution'] + r""" \hfill GPA: """ + resume_data_processed['education']['gpa'] + r""" \\[2mm]
\textit{""" + resume_data_processed['education']['details'] + r"""}

%------------- Technical Skills Section -------------
\section*{Technical Skills}
\begin{tabbing}
\hspace{4cm} \= \hspace{6cm} \= \hspace{4cm} \= \kill
\textbf{Languages:} \> """ + ', '.join(resume_data_processed['skills']['programming_languages']) + r""" \\
\textbf{Tools:} \> """ + ', '.join(resume_data_processed['skills']['tools']) + r""" \\
\textbf{Soft Skills:} \> """ + ', '.join(resume_data_processed['skills']['soft_skills']) + r"""
\end{tabbing}

%------------- Work Experience Section -------------
\section*{Work Experience}
"""

    # Add work experience dynamically
    for experience in resume_data_processed['work_experience']:
        latex_content += f"""
\\textbf{{{experience['job_title']}}} \\hfill \\textbf{{{experience['employment_dates']}}} \\\\
\\textit{{{experience['company']}}} \\hfill \\textit{{{experience.get('location', '')}}} \\\\
{experience['brief_job_description']} \\\\
\\begin{{itemize}}[left=0pt,itemsep=0pt,parsep=0pt]"""
        for achievement in experience['key_achievements']:
            latex_content += f"\\item {achievement}\n"
        latex_content += "\\end{itemize}\n"

    latex_content += r"""

%------------- Projects Section -------------
\section*{Projects}
"""

    # Add projects dynamically
    if 'projects' in resume_data_processed:
        for project in resume_data_processed['projects']:
            latex_content += r"""
\textbf{""" + project['name'] + r"""} \hfill \textbf{""" + project['date'] + r"""} \\
\textit{Technologies:} """ + ', '.join(project['technologies']) + r""" \\
""" + project['description'] + r""" \\[2mm]
\begin{itemize}[left=0in]
"""
            for achievement in project['achievements']:
                latex_content += r"\item " + achievement + r" \n"
            latex_content += r"\end{itemize}"

    latex_content += f"""

\\section*{{Job Description}}
\\textbf{{{jd_data_processed['job_title']}}} \\hfill \\textbf{{{jd_data_processed['employment_dates']}}} \\\\
\\textit{{{jd_data_processed['company']}}} \\hfill \\textit{{{jd_data_processed.get('location', '')}}} \\\\
{jd_data_processed['brief_job_description']} \\\\
\\begin{{itemize}}[left=0pt,itemsep=0pt,parsep=0pt]"""

    for achievement in jd_data_processed['key_achievements']:
        latex_content += f"\\item {achievement}\n"

    latex_content += """\\end{itemize}
\\end{document}"""

    # Write the LaTeX content to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"LaTeX resume successfully generated and saved as: {filename}")
    print("Compile this file with XeLaTeX or PDFLaTeX to generate the PDF.")

# Generate the LaTeX resume
generate_latex_resume()
