# 🎬 Movie Dialog System — Dialogue-Based Movie Recommendation

**Semantic Movie Recommendations from What You Say, Not Just What You Search**

[![Python](https://img.shields.io/badge/Python-3.x-3776ab?style=flat-square&logo=python&logoColor=white)](#)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-Embeddings-ff6f00?style=flat-square)](#)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-0467DF?style=flat-square)](#)
[![Cornell Corpus](https://img.shields.io/badge/Data-Cornell_Movie--Dialogs-6a1b9a?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-Unspecified-lightgrey?style=flat-square)](#)

---

Movie-Dialog-System is an **NLP-powered movie recommender** that matches the *meaning* of a user's query — not just its keywords — against real lines of movie dialogue. It embeds queries and dialogue lines with **Sentence Transformers**, indexes those embeddings with **FAISS** for fast approximate nearest-neighbor search, and surfaces the movies whose dialogue is semantically closest to what the user typed, using the **Cornell Movie-Dialogs Corpus** as its source of dialogue.

> ℹ️ **A note on how this README was put together:** this repo's `README.md`, `config.py`, and `requirements.txt` are currently empty placeholder files, and GitHub's automated-access restrictions prevented a listing of what's actually inside `app/`, `src/`, and `notebooks/`. The workflow, architecture, and tech stack below are written from the repo's own description (Sentence Transformers + FAISS + Cornell Movie-Dialogs Corpus, split across `app/` / `src/` / `notebooks/`) rather than from reading the implementation directly. Treat the class/function names and exact file layout as a **recommended structure** to fill in or correct against what you actually built, not a verified transcription of your code.

## ✨ Key Features (as described)

| Feature | Description |
|---|---|
| **Semantic Query Matching** | User input is embedded and compared against dialogue embeddings by meaning, not by exact keyword overlap |
| **Sentence Transformers Embeddings** | Both dialogue lines and user queries are mapped into the same dense vector space for like-for-like comparison |
| **FAISS Similarity Search** | A FAISS index enables fast nearest-neighbor lookup over the embedded dialogue corpus, scaling well past a brute-force comparison |
| **Cornell Movie-Dialogs Corpus** | Uses a well-known, large-scale conversational dataset of movie dialogue as its grounding source |
| **Notebook-Driven Development** | `notebooks/` suggests the embedding/indexing pipeline was prototyped and validated interactively before being moved into `src/` |
| **Separated App Layer** | `app/` isolates the user-facing interface from `src/`'s core retrieval logic |

## 🏗️ Suggested Architecture

```mermaid
graph LR
    A["📚 Cornell Movie-Dialogs Corpus"] --> B["🧹 Preprocessing<br/><small>clean & pair dialogue lines</small>"]
    B --> C["🧠 Sentence Transformer<br/><small>embed dialogue lines</small>"]
    C --> D["📦 FAISS Index<br/><small>vector store</small>"]
    E["💬 User Query"] --> F["🧠 Sentence Transformer<br/><small>embed query</small>"]
    F --> G["🔍 FAISS Similarity Search"]
    D --> G
    G --> H["🎬 Matched Dialogue Lines"]
    H --> I["🍿 Recommended Movies"]

    style A fill:#6a1b9a22,stroke:#6a1b9a,color:#e2e8f0
    style B fill:#eab30822,stroke:#eab308,color:#e2e8f0
    style C fill:#ff6f0022,stroke:#ff6f00,color:#e2e8f0
    style D fill:#0467DF22,stroke:#0467DF,color:#e2e8f0
    style E fill:#06b6d422,stroke:#06b6d4,color:#e2e8f0
    style F fill:#ff6f0022,stroke:#ff6f00,color:#e2e8f0
    style G fill:#0467DF22,stroke:#0467DF,color:#e2e8f0
    style H fill:#22c55e22,stroke:#22c55e,color:#e2e8f0
    style I fill:#7c3aed22,stroke:#7c3aed,color:#e2e8f0
```

### Model Workflow

1. **Corpus ingestion** — The Cornell Movie-Dialogs Corpus is loaded and parsed into individual dialogue lines, each linked back to its source movie.
2. **Embedding** — Every dialogue line is encoded into a dense vector using a Sentence Transformers model (e.g. an `all-MiniLM`-style model), capturing semantic meaning rather than surface wording.
3. **Indexing** — The dialogue embeddings are loaded into a FAISS index, enabling sub-linear approximate nearest-neighbor search instead of comparing a query against every line in the corpus.
4. **Query embedding** — When a user types a query (e.g. *"a story about betrayal between old friends"*), it's embedded with the same Sentence Transformers model so it lives in the same vector space as the corpus.
5. **Similarity search** — FAISS returns the `k` dialogue lines whose embeddings are closest to the query embedding.
6. **Recommendation** — The movies those lines belong to are looked up and surfaced back to the user as recommendations, typically ranked by similarity score.

## 📂 Project Structure

```
Movie-Dialog-System/
├── app/                  # User-facing interface (likely a Streamlit/Flask/CLI entry point)
├── src/                  # Core pipeline: preprocessing, embedding generation, FAISS indexing/search
├── notebooks/            # Exploratory/prototyping notebooks for the corpus and embedding pipeline
├── config.py             # Intended for paths, model name, and FAISS parameters (currently empty)
├── requirements.txt      # Project dependencies (currently empty)
├── .gitignore
└── README.md
```

> 📝 Since `app/`, `src/`, and `notebooks/` couldn't be listed automatically, fill in the real file names under each (e.g. `src/embed.py`, `src/faiss_index.py`, `app/streamlit_app.py`) and I can tighten this structure to match exactly.

## 🚀 Quick Start (fill in against your actual entry point)

### Prerequisites

- **Python 3.x**
- A downloaded copy of the **Cornell Movie-Dialogs Corpus**
- Sufficient RAM/disk to hold sentence embeddings for the corpus you index

### Installation

```bash
git clone https://github.com/Yaseen-2004/Movie-Dialog-System.git
cd Movie-Dialog-System

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

> ℹ️ `requirements.txt` is currently empty. Based on the project description, it likely needs at least:
> `sentence-transformers`, `faiss-cpu` (or `faiss-gpu`), `numpy`, `pandas`, plus whatever web framework `app/` uses (e.g. `streamlit` or `flask`).

### Configure

`config.py` is currently empty — this is where paths to the corpus, the Sentence Transformers model name, and FAISS index parameters (e.g. index type, number of neighbors `k`) would typically live.

### Run

```bash
# Adjust to your actual entry point once src/ and app/ contents are confirmed, e.g.:
python -m src.build_index      # build/persist the FAISS index from the corpus
python -m app.app               # launch the recommendation interface
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Embeddings** | [Sentence Transformers](https://www.sbert.net/) | Turns dialogue lines and queries into comparable dense vectors |
| **Vector Search** | [FAISS](https://github.com/facebookresearch/faiss) | Fast approximate nearest-neighbor search over embedded dialogue |
| **Dataset** | [Cornell Movie-Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) | Source of real movie dialogue lines and movie metadata |
| **Prototyping** | Jupyter notebooks (`notebooks/`) | Exploratory data analysis and pipeline validation |
| **Interface** | App layer (`app/`) | User-facing query input and recommendation display |

## 🔮 Roadmap & Suggested Next Steps

- [ ] Populate `README.md`, `config.py`, and `requirements.txt` — all three are currently empty in the repo
- [ ] Pin exact dependency versions once the pipeline is finalized
- [ ] Persist the FAISS index to disk so it doesn't need to be rebuilt from the corpus on every run
- [ ] Add evaluation of retrieval quality (e.g. manual spot-checks or a held-out query set) to validate that semantic matches are actually relevant
- [ ] Consider batching/caching embeddings for large corpora to keep indexing time reasonable
- [ ] Add a deployed demo link or screenshot once `app/` is stable

## 📜 License

No license file is currently present in this repository — add one (e.g. MIT) if you intend for others to reuse this code.

---

Built with Sentence Transformers, FAISS, and the Cornell Movie-Dialogs Corpus.
