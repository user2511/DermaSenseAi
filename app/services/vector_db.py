# app/services/vector_db.py

import chromadb
from chromadb.utils import embedding_functions


# =====================================================
# Persistent Chroma Client
# =====================================================

client = chromadb.PersistentClient(path="./chroma_db")


# =====================================================
# Embedding Function (IMPORTANT)
# =====================================================

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
     model_name="all-MiniLM-L6-v2"
 )
#embedding_function = None

# =====================================================
# RAG Collection
# =====================================================

rag_collection = client.get_or_create_collection(
    name="derma_rag",
    embedding_function=embedding_function
)


# =====================================================
# Memory Collection
# =====================================================

memory_collection = client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_function
)

