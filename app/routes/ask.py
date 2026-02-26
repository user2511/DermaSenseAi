
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional

from app.graph.derma_graph1 import derma_stream_app, llm

# ✅ memory services
from app.services.memory_service1 import store_memory
from app.services.memory_service import save_message

router = APIRouter()


@router.post("/ask-stream")
async def ask_stream(
    question: str = Form(...),
    session_id: str = Form(...),
    image: Optional[UploadFile] = File(None),
):

    print("\n=== STREAM REQUEST ===")

    image_bytes = None
    if image:
        image_bytes = await image.read()

    async def event_generator():

        # =================================================
        # 1️⃣ RUN GRAPH (VISION + QUERY + MEMORY + RAG)
        # =================================================
        state = await derma_stream_app.ainvoke({
            "session_id": session_id,
            "question": question,
            "image": image_bytes,
            "vision_context": "",
        "grounded_query": "",
        "dependency": "",

        "memory": "",
        "rag_context": "",
        "final_context": "",
        })

        # =================================================
        # 2️⃣ BUILD FINAL PROMPT
        # =================================================
        prompt = f"""
You are DermaSense AI, a dermatology assistant.

Use the provided structured context to answer safely.

Context:
{state.get("final_context", "")}

Current Question:
{question}

Answer:
"""

        # =================================================
        # 3️⃣ STREAM LLM OUTPUT
        # =================================================
        full_answer = ""

        async for chunk in llm.astream(prompt):

            token = (
                chunk.content
                if hasattr(chunk, "content")
                else str(chunk)
            )

            full_answer += token
            yield token   # ✅ send to frontend live

        # =================================================
        # 4️⃣ STORE MEMORY AFTER STREAM COMPLETES
        # =================================================
        print("\n[POST STREAM MEMORY STORE]")

        # semantic vector memory
        store_memory(
            grounded_query=state.get("grounded_query", ""),
            original_question=question,
            vision_summary=state.get("vision_context", ""),
            answer=full_answer,
            dependency=state.get("dependency", "independent"),
        )

        # chat history memory
        save_message(session_id, "user", question)
        save_message(session_id, "assistant", full_answer)

        print("Memory stored successfully.")

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )