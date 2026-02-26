# app/routes/ask.py

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from uuid import uuid4
from app.graph.derma_graph import derma_app

router = APIRouter()


@router.post("/ask")
async def ask(
    question: str = Form(...),
    session_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    print("\n=== NEW REQUEST ===", flush=True)

    # Generate session if not provided
    if not session_id:
        session_id = str(uuid4())
        print("NEW SESSION CREATED:", session_id, flush=True)
    else:
        print("EXISTING SESSION:", session_id, flush=True)

    image_bytes = None
    if image:
        image_bytes = await image.read()
        print("IMAGE RECEIVED:", len(image_bytes), flush=True)

    # Initial Graph State (must match DermaState)
    result = derma_app.invoke({
        "session_id": session_id,

        "question": question,
        "image": image_bytes,

        "vision_context": "",
        "grounded_query": "",
        "dependency": "",

        "memory_context": "",
        "rag_context": "",
        "final_context": "",

        "answer": ""
    })

    return {
        "session_id": session_id,
        "answer": result["answer"]
    }

from app.services.memory_service import get_chat_history


@router.get("/history/{session_id}")
def get_history(session_id: str):
    history = get_chat_history(session_id)
    return {
        "session_id": session_id,
        "history": history
    }