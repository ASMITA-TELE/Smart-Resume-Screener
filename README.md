# Smart Resume Screener

Simple AI tool to rank resumes by job description fit using NLP.

## Project structure

```
smart-resume-screener/
├─ app.py
├─ utils.py
├─ requirements.txt
├─ Dockerfile
├─ README.md
├─ sample_data/
│  ├─ resumes/
│  │  ├─ resume_john.txt
│  │  └─ resume_mary.txt
│  └─ job_descriptions/
│     └─ data_scientist.txt
└─ embeddings_cache/ (auto-generated)
```

## Run locally

1. Create virtual environment (optional)
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   # venv\Scripts\activate  # windows
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python -c "import nltk; import nltk; nltk.download('stopwords')"
   ```
3. Run Streamlit app
   ```bash
   streamlit run app.py
   ```

## Notes
- The BERT model downloads on first run (internet required).
- Sample resumes are plain text for convenience; replace with PDFs/DOCX as needed.
