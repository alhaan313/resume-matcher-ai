import streamlit as st
import requests
import pdfplumber
import os
from datetime import datetime

st.set_page_config(page_title="Resume ATS Checker", layout="wide")

st.markdown(
    """
    <style>
        /* Button Styling */
        .stButton>button {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            transition: 0.3s;
        }

        /* Success Message */
        .success-box {
            background-color: #1E392A;
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }

        /* Grid layout for results */
        .result-container {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-top: 10px;
        }

        .result-box {
            flex: 1;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }

        .job-role { background-color: #4CAF50; color: white; }
        .extracted-skills { background-color: #2196F3; color: white; }
        .ats-score { background-color: #FF9800; color: white; }

        /* Improvement Suggestions */
        .improvement {
            padding: 15px;
            border-radius: 8px;
            background-color: #222;
            color: white;
            margin-top: 10px;
        }

        /* Resume Metadata */
        .resume-metadata {
            background-color: #333;
            color: white;
            padding: 10px;
            border-radius: 8px;
        }

        /* Resume Preview */
        .resume-preview {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 8px;
        }

        /* Download Button */
        .download-link {
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 8px;
            display: inline-block;
            text-decoration: none;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def display_result_box(title, value, color):
    st.markdown(
        f'<div class="result-box" style="background-color: {color}; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;">'
        f"{title}: {value}"
        f"</div>",
        unsafe_allow_html=True,
    )

BACKEND_URL = "http://127.0.0.1:5000"  # Change this when deployed with the appropriate url address

DEFAULT_JOB_DESCRIPTION = "Looking for a Software Engineer with Python, AWS, and Machine Learning experience."



# Sidebar UI
st.sidebar.markdown(
    """
    <style>
        /* Sidebar section with border */
        .sidebar-section {
            padding: 15px;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #1E1E1E;
            text-align: center;
            margin-bottom: 15px;
        }

        /* Full-width buttons */
        .stButton>button {
            width: 100%;
            display: block;
            padding: 12px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }

        /* Button hover effect */
        .stButton>button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown('<div class="sidebar-section"><h2 style="color:white;">📂 Navigation</h2></div>', unsafe_allow_html=True)

if st.sidebar.button("🏠 Upload Resume", key="upload_page"):
    st.session_state["page"] = "upload"

if st.sidebar.button("📜 View Past Resumes", key="history_page"):
    st.session_state["page"] = "history"

page = st.session_state.get("page", "upload")
st.sidebar.markdown("---")

if st.sidebar.button("🔍 Search Resumes", key="search_page"):
    st.warning("Feature Coming Soon!")

if st.sidebar.button("⚙️ Settings", key="settings_page"):
    st.warning("Settings Page Under Development!")



def extract_pdf_preview(file):
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        return first_page.extract_text()



if page == "upload":
    st.title("📄 Resume ATS Checker")

    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    job_description = st.text_area(
        "Enter Job Description (Leave empty for default):", 
        placeholder="Paste job description here..."
    )


    analyze_clicked = st.button("🔍 Analyze Resume")

    if uploaded_file and analyze_clicked:
        if not job_description.strip():
            job_description = DEFAULT_JOB_DESCRIPTION  # Use default if empty

        with st.spinner("Uploading & Analyzing..."):
            files = {"resume": uploaded_file}
            data = {"job_description": job_description.strip()}  # Ensures a valid string is sent
            response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)

            if response.status_code == 200:
                data = response.json()
                st.markdown('<div class="success-box">✅ Resume Analysis Complete!</div>', unsafe_allow_html=True)


                col1, col2, col3 = st.columns(3)

                with col1:
                    display_result_box("Job Role", data["job_role"], "#4CAF50")  # Green

                with col2:
                    display_result_box("Extracted Skills", ", ".join(data["skills"]), "#2196F3")  # Blue

                with col3:
                    display_result_box("ATS Score", f"{data['ats_score']}%", "#FF9800")  # Orange

                st.markdown('<div class="improvement"><b>📌 Improvement Suggestions</b>', unsafe_allow_html=True)
                for suggestion in data["suggestions"]:
                    st.markdown(f'<li style="color:white;">{suggestion}</li>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="resume-metadata"><b>📄 Resume Metadata</b>', unsafe_allow_html=True)
                st.markdown(f"📂 **File Name:** {uploaded_file.name}", unsafe_allow_html=True)
                st.markdown(f"📏 **File Size:** {round(uploaded_file.size / 1024, 2)} KB", unsafe_allow_html=True)
                st.markdown(f"🕒 **Upload Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Resume Preview
                st.markdown('<div class="resume-metadata"><b>📜 Resume Preview</b>', unsafe_allow_html=True)
                pdf_text = extract_pdf_preview(uploaded_file)
                st.text_area("First Page Preview:", pdf_text, height=200)
                st.markdown("</div>", unsafe_allow_html=True)

                # Downloadable Resume Link
                # First line is when we had AWS
                # st.markdown(f'<a class="download-link" href="{data["file_url"]}" download>📥 Download Resume</a>', unsafe_allow_html=True)
                st.markdown(f'<a class="download-link" href="http://127.0.0.1:5000/view/{data["resume_id"]}" download>📥 Download Resume</a>', unsafe_allow_html=True)

                if st.button("📄 Generate ATS Report"):
                    st.warning("This feature is under development!")

            else:
                st.error("❌ Error processing the resume. Please try again.")


if page == "history":
    st.title("📜 View Uploaded Resumes")

    response = requests.get(f"{BACKEND_URL}/metadata")

    if response.status_code == 200:
        resumes = response.json().get("resumes", [])
        if resumes:
            for resume in resumes:
                ats_score = resume.get("ats_score", "N/A")  # Use "N/A" if missing
                with st.expander(f"📄 {resume['original_filename']} (ATS Score: {ats_score}%)"):
                    st.write(f"📂 **Resume ID:** {resume['resume_id']}")
                    # st.write(f"🔗 **Resume Link:** [View Resume]({resume['file_url']})")
                    # The line above was used when we had aws established
                    st.write(f"🔗 **Resume Link:** [View Resume](http://127.0.0.1:5000/view/{resume['resume_id']})")

        else:
            st.info("No resumes found.")
    else:
        st.error("❌ Failed to load resumes.")
