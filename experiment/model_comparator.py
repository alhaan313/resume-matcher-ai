import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import fitz  
import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer, util
from utils.resume_parser import extract_text_from_pdf

# Load Models
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_bert_similarity(resume_text, job_description):
    """Computes similarity between a resume and job description using BERT embeddings."""
    
    # Limit resume text to first 500 words to fit within BERT’s 512-token limit
    resume_text = " ".join(resume_text.split()[:500])
    
    inputs = tokenizer(resume_text, job_description, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state
    

    resume_embedding = outputs[:, 0, :]
    job_embedding = outputs[:, 1, :]
    
    similarity = torch.cosine_similarity(resume_embedding, job_embedding)
    score = similarity.item() * 100  # Convert to percentage
    
    return round(score, 2)

def compute_sbert_similarity(resume_text, job_description):
    """Computes similarity using Sentence-BERT (SBERT)."""
    resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)
    job_embedding = sbert_model.encode(job_description, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding)
    return round(similarity.item() * 100, 2)  # Convert to percentage

if __name__ == "__main__":
    resume_path = r"./sample_resumes/Alhaan_resume.pdf"  # Use raw string
    job_description = "Looking for a software engineer with Python, AWS, and Machine Learning experience."

    # Extract text from PDF
    resume_text = extract_text_from_pdf(resume_path)

    # Compute ATS Scores
    ats_score_bert = compute_bert_similarity(resume_text, job_description)
    ats_score_sbert = compute_sbert_similarity(resume_text, job_description)
    
    # Calculate improvement percentage
    improvement = ((ats_score_sbert - ats_score_bert) / ats_score_bert) * 100 if ats_score_bert != 0 else 0

    # Print Comparison Results
    print("\n Match Score BERT:", ats_score_bert, "%")
    print("\n Match Score SBERT:", ats_score_sbert, "%")
    print(f"\n SBERT Improved ATS Score by {improvement:.2f}%\n")
