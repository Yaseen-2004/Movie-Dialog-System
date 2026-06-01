import numpy as np
import faiss

EMBEDDING_PATH = "data/embeddings/embeddings.npy"
INDEX_PATH = "data/faiss/index.faiss"


def build_index():
    print("Loading embeddings...")
    embeddings = np.load(EMBEDDING_PATH)

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(dimension)

    print("Adding embeddings...")
    index.add(embeddings)

    print("Saving index...")
    faiss.write_index(index, INDEX_PATH)

    print(f"Index built with {index.ntotal} vectors")


if __name__ == "__main__":
    build_index()