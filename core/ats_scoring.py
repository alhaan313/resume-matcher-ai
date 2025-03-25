from sentence_transformers import SentenceTransformer, util

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_sbert_similarity(resume_text, job_description):
    """Computes ATS match percentage using SBERT."""
    resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)
    job_embedding = sbert_model.encode(job_description, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding)
    # 0.0 to 1.0 --> 64
    return round(similarity.item() * 100, 2)  # Convert to percentage

