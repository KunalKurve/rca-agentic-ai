import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

def build_faiss_index(data_path="data/sop_docs"):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    docs = []

    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        with open(file_path, "r") as f:
            docs.append(f.read())

    vectors = embedder.encode(docs)
    vectors = np.array(vectors)

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    os.makedirs("embeddings", exist_ok=True)

    with open("embeddings/sop_faiss_index.pkl", "wb") as f:
        pickle.dump({"index": index, "texts": docs}, f)

    print("FAISS index built successfully.")

if __name__ == "__main__":
    build_faiss_index()