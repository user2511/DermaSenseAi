
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
import uuid

from app.graph.derma_graph1 import derma_stream_app, llm
from app.services.precompute_service import find_precomputed_answer, stream_text

from app.services.memory_service1 import store_memory
from app.services.memory_service import save_message

router = APIRouter()

# 🔥 DEMO SWITCH
DEMO_MODE = True


@router.post("/ask-stream")
async def ask_stream(
    question: str = Form(...),
    session_id: str = Form(...),
    image: Optional[UploadFile] = File(None),
):

    print("\n=== STREAM REQUEST ===")

    image_bytes = None
    image_name = None

    if image:
        image_bytes = await image.read()
        image_name = image.filename

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
        # 2️⃣ DEMO MODE: USE PRECOMPUTED IF EXISTS
        # =================================================
        full_answer = ""

        if DEMO_MODE and image_name:
            precomputed = find_precomputed_answer(image_name)

            if precomputed:
                print("Using precomputed answer.")

                async for token in stream_text(precomputed):
                    full_answer += token
                    yield token

            else:
                print("No precomputed match. Falling back to LLM.")
                async for chunk in llm.astream(
                    build_prompt(state, question)
                ):
                    token = chunk.content if hasattr(chunk, "content") else str(chunk)
                    full_answer += token
                    yield token
        else:
            # LIVE MODE
            async for chunk in llm.astream(
                build_prompt(state, question)
            ):
                token = chunk.content if hasattr(chunk, "content") else str(chunk)
                full_answer += token
                yield token

        # =================================================
        # 3️⃣ STORE MEMORY
        # =================================================
        print("\n[POST STREAM MEMORY STORE]")

        store_memory(
            grounded_query=state.get("grounded_query", ""),
            original_question=question,
            vision_summary=state.get("vision_context", ""),
            answer=full_answer,
            dependency=state.get("dependency", "independent"),
        )

        save_message(session_id, "user", question)
        save_message(session_id, "assistant", full_answer)

        print("Memory stored successfully.")

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )


# =============================
# Prompt Builder
# =============================

def build_prompt(state, question):
    return f"""
You are DermaSense AI, a dermatology assistant.

Use the provided structured context to answer safely.

Context:
{state.get("final_context", "")}

Current Question:
{question}

Answer:
"""