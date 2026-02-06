import chromadb
from chromadb.utils import embedding_functions

# Persistent DB (saved to disk)
client = chromadb.PersistentClient(path="./chroma_db")

# Use sentence-transformer embeddings
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


collection = client.get_or_create_collection(
    name="documents",
    embedding_function=sentence_transformer_ef
)
