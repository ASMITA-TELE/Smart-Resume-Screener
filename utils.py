# utils.py
import re
from typing import List, Tuple
import PyPDF2
from docx import Document
import nltk
from nltk.corpus import stopwords
import spacy
import os
from joblib import Memory

# Initialize NLP resources
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

try:
    nltk_stopwords = set(stopwords.words("english"))
except Exception:
    nltk_stopwords = set()

# ML imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Optional caching directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), "embeddings_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
memory = Memory(CACHE_DIR, verbose=0)

# -------------------- FILE EXTRACTION --------------------
def extract_text_from_pdf(file_stream) -> str:
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = []
        for page in reader.pages:
            p = page.extract_text()
            if p:
                text.append(p)
        return "\n".join(text)
    except Exception:
        return ""


def extract_text_from_docx(file_stream) -> str:
    try:
        doc = Document(file_stream)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""


def safe_extract_text(uploaded_file) -> str:
    name = getattr(uploaded_file, "name", "")
    try:
        uploaded_file.seek(0)
    except Exception:
        pass

    if name.lower().endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif name.lower().endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        try:
            raw = uploaded_file.read()
            if isinstance(raw, bytes):
                raw = raw.decode(errors="ignore")
            return raw
        except Exception:
            return ""


# -------------------- TEXT CLEANING --------------------
def clean_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"(http|https)://\S+", " ", text)
    text = re.sub(r"[^A-Za-z0-9\s.,]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower().strip()

    tokens = [t for t in text.split() if t not in nltk_stopwords and len(t) > 1]

    if nlp is not None:
        doc = nlp(" ".join(tokens))
        lemmas = [token.lemma_ for token in doc]
        return " ".join(lemmas)
    return " ".join(tokens)


# -------------------- TF-IDF RANKING --------------------
def rank_resumes_tfidf(job_desc: str, resumes: List[str]) -> List[Tuple[int, float]]:
    """Return list of (index, score) sorted descending by score"""
    docs = [job_desc] + resumes
    vect = TfidfVectorizer(ngram_range=(1, 2), max_features=20000, stop_words="english")
    vecs = vect.fit_transform(docs)  # ✅ FIXED (removed comma)
    jd_vec = vecs[0:1]
    resume_vecs = vecs[1:]
    sims = cosine_similarity(jd_vec, resume_vecs)[0]
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    return ranked


# -------------------- BERT RANKING --------------------
def rank_resumes_bert(job_desc: str, resumes: List[str], model_name="all-MiniLM-L6-v2") -> List[Tuple[int, float]]:
    model = SentenceTransformer(model_name)
    jd_emb = model.encode(job_desc, convert_to_tensor=True)
    res_emb = model.encode(resumes, convert_to_tensor=True)
    sims = util.cos_sim(jd_emb, res_emb)[0].cpu().tolist()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    return ranked
