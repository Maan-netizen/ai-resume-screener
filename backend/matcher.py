"""
matcher.py
Core NLP logic: extract text from resumes (PDF/DOCX), clean it,
compare against a job description using TF-IDF + cosine similarity,
and return a match score + missing keywords.
"""

import re
import io
from PyPDF2 import PdfReader
import docx

# A small curated skill vocabulary. In a real product you'd pull this
# from a bigger taxonomy (O*NET, ESCO, etc). Kept lightweight on purpose.
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "angular", "vue",
    "node", "express", "django", "flask", "fastapi", "mongodb", "mysql",
    "postgresql", "sql", "nosql", "docker", "kubernetes", "aws", "azure",
    "gcp", "git", "rest api", "graphql", "html", "css", "tailwind",
    "redux", "next.js", "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "agile",
    "scrum", "ci/cd", "jenkins", "linux", "bash", "microservices",
    "unit testing", "pytest", "junit", "figma", "excel", "power bi",
    "tableau", "data structures", "algorithms", "oop"
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text.append(content)
    return "\n".join(text)


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(filename: str, file_bytes: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text)  # keep c++, c#, .net etc.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_skills(text: str) -> set:
    cleaned = clean_text(text)
    found = set()
    for skill in SKILL_KEYWORDS:
        if skill in cleaned:
            found.add(skill)
    return found


def compute_match_score(resume_text: str, jd_text: str) -> dict:
    """
    Returns similarity score (0-100) using TF-IDF + cosine similarity,
    plus skill overlap analysis.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    if not resume_clean or not jd_clean:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score = round(float(similarity) * 100, 2)

    resume_skills = find_skills(resume_text)
    jd_skills = find_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }
