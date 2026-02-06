from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval_service import retrieve_similar_chunks
from app.services.llm_service import generate_answer

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask(q: Question):
    docs = retrieve_similar_chunks(q.question)

    if not docs:
        return {"answer": "No data available."}

    context = "\n".join(docs)

    answer = generate_answer(context, q.question)

    return {"answer": answer}

