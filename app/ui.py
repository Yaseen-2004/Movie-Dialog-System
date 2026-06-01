import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import streamlit as st
from src.recommendation.recommender import Recommender

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ------------------- GLOBAL CSS -------------------
st.markdown("""
<style>

/* Main Cards */
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.title {
    font-size: 24px;
    font-weight: bold;
    color: #00ffd5;
}

.score {
    color: #aaa;
    font-size: 14px;
}

/* Dialogue Styling */
.dialogue {
    margin-top: 8px;
    padding-left: 10px;
    border-left: 3px solid #00ffd5;
    color: #ddd;
    font-style: italic;
}

.highlight {
    color: #00ffd5;
    font-weight: bold;
}

/* Sidebar Cards */
.sidebar-card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}

.sidebar-title {
    font-size: 18px;
    font-weight: bold;
    color: #00ffd5;
    margin-bottom: 10px;
}

.sidebar-text {
    font-size: 14px;
    color: #ccc;
}

</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.markdown("""
<div class="sidebar-card">
    <div class="sidebar-title">🎬 About This Project</div>
    <div class="sidebar-text">
    This is a <b>Dialogue-Based Movie Recommendation System</b> that suggests movies based on the meaning of conversations instead of simple keywords.<br><br>

    <b>How it works:</b><br>
    • Dialogues → embeddings<br>
    • Query → embedding<br>
    • FAISS finds similar vectors<br>
    • Movies ranked by semantic similarity<br><br>

    <b>Tech Stack:</b><br>
    • Sentence Transformers<br>
    • FAISS<br>
    • Streamlit<br><br>

    Search using <i>feelings, themes, or ideas</i>.
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-card">
    <div class="sidebar-title">💡 Example Queries</div>
    <div class="sidebar-text">
    • existential dread space<br>
    • deep romantic confession<br>
    • war and sacrifice<br>
    • fear of death philosophy
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.title("🎬 Movie Recommender")
st.write("Find movies based on **dialogue meaning**, not just keywords")

query = st.text_input("🔍 Enter your query")

# ------------------- LOAD MODEL -------------------
if "recommender" not in st.session_state:
    with st.spinner("Loading system..."):
        st.session_state.recommender = Recommender()

# ------------------- HIGHLIGHT FUNCTION -------------------
def highlight_text(text, query):
    words = set(query.lower().split())

    def replace(match):
        word = match.group(0)
        if word.lower() in words:
            return f'<span class="highlight">{word}</span>'
        return word

    return re.sub(r'\w+', replace, text)

# ------------------- SEARCH -------------------
if query:
    st.markdown("### 🔎 Results")

    with st.spinner("Searching..."):
        results = st.session_state.recommender.recommend(query)

    for r in results:
        st.markdown(f"""
        <div class="card">
            <div class="title">{r['title']}</div>
            <div class="score">Score: {round(r['score'], 3)}</div>
        </div>
        """, unsafe_allow_html=True)

        # 📊 Score Bar
        score = min(r["score"], 2.0) / 2.0
        st.progress(score)

        st.markdown("**Sample Dialogues:**")

        for d in r["samples"]:
            highlighted = highlight_text(d[:150], query)
            st.markdown(f"""
            <div class="dialogue">"{highlighted}..."</div>
            """, unsafe_allow_html=True)

        st.markdown("---")