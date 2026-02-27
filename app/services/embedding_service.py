from app.services.vector_db import rag_collection
import uuid


def embed_and_store(text_chunks):

    ids = [str(uuid.uuid4()) for _ in text_chunks]

    metadata = [{"source": "skincare_dataset"} for _ in text_chunks]

    rag_collection.add(
        documents=text_chunks,
        ids=ids,
        metadatas=metadata
    )

    return len(text_chunks)