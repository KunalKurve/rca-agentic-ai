from sentence_transformers import SentenceTransformer
import pickle
import numpy as np

def search_sops(state):
    query = state["input"]

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    query_vec = embedder.encode([query])

    with open("embeddings/sop_faiss_index.pkl", "rb") as f:
        index_data = pickle.load(f)

    index = index_data["index"]
    texts = index_data["texts"]

    distances, indices = index.search(np.array(query_vec), k=2)

    retrieved_docs = [texts[i] for i in indices[0]]

    return {
        **state,
        "retrieved_docs": retrieved_docs
    }