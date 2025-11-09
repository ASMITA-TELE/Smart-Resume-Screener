import streamlit as st
import pandas as pd
from utils import safe_extract_text, clean_text, rank_resumes_tfidf, rank_resumes_bert
import time  # For progress bar simulation

# Page setup
st.set_page_config(
    page_title="Smart Resume Screener",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced hackathon-style UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
            color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00c6ff, #0072ff, #ff0072);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #d0d0d0;
            margin-bottom: 30px;
            animation: fadeIn 2.5s ease-in-out;
        }
        .stButton>button {
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
        }
        .stButton>button:hover {
            transform: scale(1.08);
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            box-shadow: 0 6px 20px rgba(0, 198, 255, 0.5);
        }
        .stTextArea textarea, .stFileUploader {
            border-radius: 12px;
            border: 1px solid #0072ff;
            background-color: #161b22;
            color: #f5f5f5;
        }
        .css-1d391kg {
            background-color: #161b22 !important;
            border-radius: 15px;
        }
        .section-header {
            color: #00c6ff;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 50px;
            text-align: center;
            border-bottom: 2px solid #0072ff;
            padding-bottom: 10px;
        }
        .candidate-box {
            background: linear-gradient(135deg, #161b22 0%, #1f2937 100%);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 8px 25px rgba(0, 114, 255, 0.3);
            transition: transform 0.3s ease;
        }
        .candidate-box:hover {
            transform: translateY(-5px);
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            margin-top: 50px;
            padding: 20px;
            background-color: #0e1117;
            border-radius: 10px;
        }
        .progress-bar {
            width: 100%;
            height: 10px;
            background-color: #333;
            border-radius: 5px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            transition: width 0.5s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("<h1 class='main-title'>🚀 Smart Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Candidate Ranking for the Future of Hiring </p>", unsafe_allow_html=True)

# Sidebar with icons
st.sidebar.header("⚙️ Settings & Controls")
method = st.sidebar.selectbox("🔍 Similarity Method", ["BERT (semantic)", "TF-IDF (keyword)"], help="Choose how to match resumes to the job description.")
top_k = st.sidebar.slider("📊 Show Top K Candidates", 1, 20, 5, help="Select how many top matches to display.")

# Job Description section
st.markdown("<h3 class='section-header'>1️⃣ Job Description Input</h3>", unsafe_allow_html=True)
jd_input_type = st.radio("📝 Provide Job Description as:", ("Paste Text", "Upload File (.txt)"), horizontal=True)
job_desc = ""
if jd_input_type == "Paste Text":
    job_desc = st.text_area("Paste job description here", height=200, placeholder="Describe the role, skills, and qualifications (e.g., 'Python developer with 3+ years experience in ML...')")
else:
    jd_file = st.file_uploader("Upload job description (.txt)", type=['txt'])
    if jd_file:
        try:
            raw = jd_file.read()
            if isinstance(raw, bytes):
                raw = raw.decode(errors="ignore")
            job_desc = raw
            st.success("✅ Job description loaded!")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

# Resume upload section
st.markdown("<h3 class='section-header'>2️⃣ Upload Resumes</h3>", unsafe_allow_html=True)
uploaded = st.file_uploader("📤 Upload resumes (PDF, DOCX, TXT) — Multiple allowed", accept_multiple_files=True, type=['pdf', 'docx', 'txt'])
if uploaded:
    st.success(f"✅ {len(uploaded)} resumes uploaded successfully!")
    cols = st.columns(min(len(uploaded), 3))  # Responsive grid
    for i, f in enumerate(uploaded):
        with cols[i % 3]:
            st.markdown(f"📄 **{f.name}**")

# Evaluate button with progress
if st.button("🚀 Evaluate Resumes"):
    if not job_desc or not uploaded:
        st.error("⚠️ Please provide both a job description and at least one resume.")
    else:
        # Progress bar simulation
        progress_bar = st.empty()
        progress_text = st.empty()
        for percent in range(0, 101, 10):
            progress_bar.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percent}%"></div>
                </div>
            """, unsafe_allow_html=True)
            progress_text.text(f"🔍 Analyzing resumes... {percent}% complete")
            time.sleep(0.2)  # Simulate processing
        progress_bar.empty()
        progress_text.empty()

        with st.spinner("🧠 Finalizing rankings..."):
            resumes_raw, names = [], []
            for f in uploaded:
                try:
                    f.seek(0)
                except:
                    pass
                text = safe_extract_text(f) or ""
                resumes_raw.append(clean_text(text))
                names.append(f.name)
            job_desc_clean = clean_text(job_desc)

            # Rank resumes
            if method.startswith("BERT"):
                ranked = rank_resumes_bert(job_desc_clean, resumes_raw)
            else:
                ranked = rank_resumes_tfidf(job_desc_clean, resumes_raw)

            rows = [{"rank_index": idx, "name": names[idx], "score": float(score)} for idx, score in ranked]
            df = pd.DataFrame(rows)
            df['rank'] = df['score'].rank(method='dense', ascending=False).astype(int)
            df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
            df['score_pct'] = (df['score'] - df['score'].min()) / (df['score'].max() - df['score'].min() + 1e-8) * 100

        st.success("✅ Evaluation complete! 🎉")

        # Results section with visualization
        st.markdown("<h3 class='section-header'>🏆 Top Results & Visualization</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df[['rank', 'name', 'score', 'score_pct']].head(top_k), use_container_width=True)
        with col2:
            # Simple bar chart for scores
            chart_data = df.head(top_k)[['name', 'score_pct']].set_index('name')
            st.bar_chart(chart_data, use_container_width=True)

        # Candidate details
        st.markdown("<h3 class='section-header'>📋 Top Candidates Details</h3>", unsafe_allow_html=True)
        for i, row in df.head(top_k).iterrows():
            with st.container():
                st.markdown(f"""
                    <div class='candidate-box'>
                        <h4>🏅 Rank {i+1}: {row['name']}</h4>
                        <p>🔹 Score: {row['score']:.4f} ({row['score_pct']:.1f}% match)</p>
                    </div>
                """, unsafe_allow_html=True)
                candidate_file = uploaded[row['rank_index']]
                try:
                    candidate_file.seek(0)
                    preview_text = safe_extract_text(candidate_file)
                    if preview_text:
                        st.text_area(f"📖 Preview — {row['name']}", value=preview_text[:3000], height=200, disabled=True)
                except:
                    st.write("❌ Preview not available.")
                try:
                    st.download_button(label=f"⬇️ Download {row['name']}", data=candidate_file.getvalue(), file_name=row['name'], mime="application/octet-stream")
                except:
                    pass

# Footer
st.markdown("""
    <div class='footer'>
        <p>Built with ❤️ for QUANTBIT TECHNOLOGIES hackathon | Powered by Streamlit & AI | © 2025 Code n Coffee</p>
    </div>
""", unsafe_allow_html=True)
