import os
import re
from datetime import datetime
from resume_sample_data import resume_data, jd_data  # Import the data from the external file

def generate_latex_filename():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I_%M%p")
    formatted_date = current_time.strftime("%d_%b")
    return f"JakeResume_{formatted_time}_{formatted_date}.tex"

def escape_latex_special_chars(text):
    if not isinstance(text, str):
        return text
    
    # First, escape backslashes (must be done first)
    text = text.replace('\\', '\\textbackslash{}')
    
    # Escape other special LaTeX characters
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    
    for char, escape in special_chars.items():
        text = text.replace(char, escape)
    
    # Additional safety check: remove any LaTeX command patterns
    text = re.sub(r'\\([a-zA-Z]+)', r'\\textbackslash{}\1', text)    
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
    
    # Create deep copies to avoid modifying the original data
    import copy
    resume_data_copy = copy.deepcopy(resume_data)
    jd_data_copy = copy.deepcopy(jd_data)
    
    # Process the data
    resume_data_processed = process_data(resume_data_copy)
    jd_data_processed = process_data(jd_data_copy)

    # Start building the LaTeX content - using the Jake template style
    latex_content = r"""
%-------------------------
% Resume in Latex
% Based on Jake Gutierrez's template
% License: MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontspec}

% Fix for XeLaTeX compatibility
\defaultfontfeatures{Ligatures=TeX}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

%----------HEADING----------
\begin{center}
    \textbf{\Huge \scshape """ + resume_data_processed['name'] + r"""} \\ \vspace{1pt}
    \small """ + resume_data_processed['phone'] + r""" $|$ \href{mailto:""" + resume_data_processed['email'] + r"""}{\underline{""" + resume_data_processed['email'] + r"""}} $|$ 
    \href{""" + resume_data_processed['linkedin'] + r"""}{\underline{""" + resume_data_processed['linkedin'].replace('https://', '') + r"""}} $|$
    \href{""" + resume_data_processed['github'] + r"""}{\underline{""" + resume_data_processed['github'].replace('https://', '') + r"""}}
\end{center}

%----------SUMMARY SECTION----------
\section{Summary}
""" + resume_data_processed['summary'] + r"""

%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {""" + resume_data_processed['education']['degree'] + r"""}{""" + resume_data_processed['education']['dates'] + r"""}
      {""" + resume_data_processed['education']['institution'] + r"""}{GPA: """ + resume_data_processed['education']['gpa'] + r"""}
    % Additional education entries can be added here
  \resumeSubHeadingListEnd

%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart
"""

    # Add work experience dynamically using the custom commands
    for experience in resume_data_processed['work_experience']:
        latex_content += f"""
    \\resumeSubheading
      {{{experience['job_title']}}}{{{experience['employment_dates']}}}
      {{{experience['company']}}}{{{experience.get('location', '')}}}
      \\resumeItemListStart"""
        
        # Add each achievement as a separate item
        for achievement in experience['key_achievements']:
            latex_content += f"""
        \\resumeItem{{{achievement}}}"""
            
        latex_content += """
      \\resumeItemListEnd
"""

    latex_content += r"""
  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
  \resumeSubHeadingListStart
"""

    # Add projects dynamically
    if 'projects' in resume_data_processed:
        for project in resume_data_processed['projects']:
            technologies = ', '.join(project['technologies'])
            latex_content += f"""
    \\resumeProjectHeading
        {{\\textbf{{{project['name']}}} $|$ \\emph{{{technologies}}}}}{{{project['date']}}}
        \\resumeItemListStart"""
            
            for achievement in project['achievements']:
                latex_content += f"""
          \\resumeItem{{{achievement}}}"""
                
            latex_content += """
        \\resumeItemListEnd
"""

    latex_content += r"""
  \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: """ + ', '.join(resume_data_processed['skills']['programming_languages']) + r"""} \\
     \textbf{Tools}{: """ + ', '.join(resume_data_processed['skills']['tools']) + r"""} \\
     \textbf{Soft Skills}{: """ + ', '.join(resume_data_processed['skills']['soft_skills']) + r"""} 
    }}
 \end{itemize}

% Optional Job Description Section for comparison
\section{Job Description}
  \resumeSubHeadingListStart
    \resumeSubheading
      {""" + jd_data_processed['job_title'] + r"""}{""" + jd_data_processed['employment_dates'] + r"""}
      {""" + jd_data_processed['company'] + r"""}{""" + jd_data_processed.get('location', '') + r"""}
      \resumeItemListStart"""

    for achievement in jd_data_processed['key_achievements']:
        latex_content += f"""
        \\resumeItem{{{achievement}}}"""
    
    latex_content += """
      \\resumeItemListEnd
  \\resumeSubHeadingListEnd

%-------------------------------------------
\\end{document}"""

    # Write the LaTeX content to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"LaTeX resume successfully generated and saved as: {filename}")
    print("Compile this file with XeLaTeX to generate the PDF.")
    print("If you encounter any issues, check your resume_sample_data.py file for special characters or LaTeX commands.")

# Generate the LaTeX resume
generate_latex_resume()