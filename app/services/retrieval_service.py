# import numpy as np
# from sentence_transformers import SentenceTransformer
# from app.services.vector_store import VECTOR_STORE

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def retrieve_similar_chunks(query, top_k=3):
#     if len(VECTOR_STORE) == 0:
#         return []

#     query_embedding = model.encode(query)

#     scores = []

#     for item in VECTOR_STORE:
#         sim = np.dot(query_embedding, item["embedding"]) / (
#             np.linalg.norm(query_embedding) *
#             np.linalg.norm(item["embedding"])
#         )
#         scores.append((sim, item["text"]))

#     scores.sort(reverse=True, key=lambda x: x[0])

#     return [text for _, text in scores[:top_k]]

from app.services.vector_db import collection

def retrieve_similar_chunks(query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return results["documents"][0] if results["documents"] else []

