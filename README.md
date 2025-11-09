# 🚀 Smart Resume Screener

An **AI-powered Resume Screening System** built with **Streamlit** that automatically ranks resumes based on how well they match a given **job description** using **Natural Language Processing (NLP)** and **Machine Learning**.

---

## 🎯 Objective

To reduce manual resume screening time by using AI that:
- Extracts text from resumes (PDF/DOCX)
- Cleans and processes text using NLP
- Compares resumes with the job description
- Ranks candidates based on similarity scores (TF-IDF or BERT)

---

## 🧠 Features

✅ Upload multiple resumes (PDF, DOCX, TXT)  
✅ Paste or upload a job description  
✅ Choose between **TF-IDF** or **BERT** similarity methods  
✅ Displays top-matching candidates with scores and previews  
✅ Attractive animated **Streamlit UI**  
✅ Real-time progress bar and download options  
✅ Dockerized for easy deployment

---

## ⚙️ Tech Stack

| Category | Tools/Technologies |
|-----------|--------------------|
| **Frontend** | Streamlit (Python-based UI) |
| **Backend (AI)** | Python, NLP (spaCy, NLTK), Scikit-learn |
| **ML Models** | TF-IDF, BERT (Sentence Transformers) |
| **Deployment** | Docker, Streamlit |
| **File Handling** | PyPDF2, python-docx |

---

## 🧩 Project Structure

SmartResumeScreener/
│
├── app.py # Main Streamlit app (UI + logic)
├── utils.py # NLP and ranking functions
├── requirements.txt # All dependencies
├── Dockerfile # For containerization
└── embeddings_cache/ # (Optional) Cached BERT embeddings

yaml
Copy code

---

## 🧰 Installation & Usage

### 🔹 Step 1: Clone the repository
```bash
git clone https://github.com/AsmitaTele/Smart-Resume-Screener.git
cd Smart-Resume-Screener
🔹 Step 2: Install dependencies
bash
Copy code
pip install -r requirements.txt
python -m spacy download en_core_web_sm
🔹 Step 3: Run the app
bash
Copy code
streamlit run app.py
Then open the link shown in the terminal (usually http://localhost:8501).

🐳 Docker (Optional)
To run using Docker:

bash
Copy code
docker build -t smart-resume-screener .
docker run -p 8501:8501 smart-resume-screener
🌱 Future Scope
🚀 Integrate with LinkedIn / job portals for real-time candidate data
🧠 Use advanced LLMs (GPT-based models) for deeper resume understanding
📊 Add HR analytics dashboard for hiring insights
🤝 Enable AI-based candidate feedback and resume improvement tips
☁️ Deploy on AWS / Streamlit Cloud for real-world access

📸 Demo Preview
“Upload Job Description → Upload Resumes → Get Ranked Candidates”
