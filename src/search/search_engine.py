import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/faiss/index.faiss"
METADATA_PATH = "data/embeddings/metadata.pkl"


class SearchEngine:
    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("Loading metadata...")
        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        print("Loading model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec), top_k)

        results = []
        for idx, score in zip(I[0], D[0]):
            item = self.metadata[idx]
            results.append({
                "movie_id": item["movie_id"],
                "text": item["text"],
                "score": float(score)
            })

        return results