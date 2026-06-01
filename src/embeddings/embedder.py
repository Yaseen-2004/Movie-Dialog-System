import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

INPUT_PATH = "data/processed/chunks.json"
EMBEDDING_PATH = "data/embeddings/embeddings.npy"
METADATA_PATH = "data/embeddings/metadata.pkl"


def generate_embeddings():
    print("Loading chunks...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]

    print("Loading model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print("Saving embeddings...")
    np.save(EMBEDDING_PATH, embeddings)

    print("Saving metadata...")
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(data, f)

    print(f"Saved {len(embeddings)} embeddings")


if __name__ == "__main__":
    generate_embeddings()