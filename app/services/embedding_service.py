
from app.services.vector_db import rag_collection
from app.services.vector_db import memory_collection
import uuid

def embed_and_store(text_chunks):
    ids = []
    
    for chunk in text_chunks:
        ids.append(str(uuid.uuid4()))

    rag_collection.add(
        documents=text_chunks,
        ids=ids
    )

    

    return len(text_chunks)

