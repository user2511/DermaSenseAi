from typing import TypedDict, Optional
import asyncio

from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama

from app.services.vision_service1 import analyze_skin_image
from app.services.query_service import build_grounded_query
from app.services.retrieval_service import retrieve_similar_chunks
from app.services.memory_service1 import get_memory, store_memory

from app.services.memory_service import (
    create_or_update_session,
    get_session_vision,
    save_message
)

# =====================================================
# STATE
# =====================================================

class DermaState(TypedDict, total=False):
    session_id: str

    question: str
    image: Optional[bytes]

    vision_context: str
    grounded_query: str
    dependency: str

    memory: str
    rag_context: str
    final_context: str

    answer: str


# =====================================================
# LLM
# =====================================================

llm = Ollama(
    model="tinyllama",
    temperature=0.2,
    num_predict=300
)

# =====================================================
# 1️⃣ VISION NODE
# =====================================================

def vision_node(state: DermaState):
    print("\n[VISION NODE]")

    session_id = state["session_id"]
    image = state.get("image")

    if image:
        summary = analyze_skin_image(image)
        state["vision_context"] = summary or ""
        create_or_update_session(session_id, state["vision_context"])
        print("New image analyzed.")
    else:
        stored = get_session_vision(session_id)
        state["vision_context"] = stored or ""
        print("Reusing stored vision.")

    return state


# =====================================================
# 2️⃣ QUERY NODE
# =====================================================

def query_node(state: DermaState):
    print("\n[QUERY NODE]")

    grounded_query, dependency = build_grounded_query(
        question=state["question"],
        image_summary=state.get("vision_context", "")
    )

    state["grounded_query"] = grounded_query
    state["dependency"] = dependency

    print("Dependency:", dependency)
    return state


# =====================================================
# 3️⃣ PARALLEL RETRIEVAL NODE
# =====================================================

async def parallel_retrieval_node(state: DermaState):
    print("\n[PARALLEL RETRIEVAL NODE]")

    query = state["grounded_query"]

    async def memory_task():
        memories = get_memory(query)
        return " ".join(memories[:2]) if memories else ""

    async def rag_task():
        # # Skip RAG for follow-up
        # if state.get("dependency") == "follow_up":
        #     print("Skipping RAG (follow-up).")
        #     return ""

        docs = retrieve_similar_chunks(query)
        return " ".join(docs[:2]) if docs else ""

    memory_result, rag_result = await asyncio.gather(
        memory_task(),
        rag_task()
    )

    state["memory"] = memory_result
    state["rag_context"] = rag_result

    print("Parallel retrieval complete.")
    return state


# =====================================================
# 4️⃣ MERGE NODE
# =====================================================

def merge_node(state: DermaState):
    print("\n[MERGE NODE]")

    parts = []

    if state.get("vision_context"):
        parts.append(f"Skin Analysis:\n{state['vision_context']}")

    if state.get("memory"):
        parts.append(f"Previous Context:\n{state['memory']}")

    if state.get("rag_context"):
        parts.append(f"Medical Knowledge:\n{state['rag_context']}")

    state["final_context"] = "\n\n".join(parts)

    print("Context merged.")
    return state


# =====================================================
# 5️⃣ LLM NODE (STREAM-READY)
# =====================================================

def llm_node(state: DermaState):
    print("\n[LLM NODE]")

    prompt = f"""
You are DermaSense AI, a dermatology assistant.

Use the provided structured context to answer safely and concisely.

Rules:
- If follow-up, answer only what is asked.
- Do not repeat full routines unless requested.
- Avoid hallucinations.
- If unsure, say you don't know.

Context:
{state["final_context"]}

Current Question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        state["answer"] = response.content
    else:
        state["answer"] = str(response)

    return state


# =====================================================
# 6️⃣ MEMORY STORE NODE
# =====================================================

def memory_store_node(state: DermaState):
    print("\n[MEMORY STORE NODE]")

    session_id = state["session_id"]

    store_memory(
        grounded_query=state["grounded_query"],
        original_question=state["question"],
        vision_summary=state.get("vision_context", ""),
        answer=state["answer"],
        dependency=state.get("dependency", "independent"),
    )

    save_message(session_id, "user", state["question"])
    save_message(session_id, "assistant", state["answer"])

    print("Memory stored.")
    return state


# =====================================================
# GRAPH CONSTRUCTION
# =====================================================

# graph = StateGraph(DermaState)

# graph.add_node("vision", vision_node)
# graph.add_node("query", query_node)
# graph.add_node("parallel_retrieval", parallel_retrieval_node)
# graph.add_node("merge", merge_node)
# graph.add_node("llm", llm_node)
# graph.add_node("memory_store", memory_store_node)

# graph.set_entry_point("vision")

# graph.add_edge("vision", "query")
# graph.add_edge("query", "parallel_retrieval")
# graph.add_edge("parallel_retrieval", "merge")
# graph.add_edge("merge", "llm")
# graph.add_edge("llm", "memory_store")
# graph.add_edge("memory_store", END)

# derma_app = graph.compile()

# =====================================================
# STREAM GRAPH (NO LLM)
# =====================================================

stream_graph = StateGraph(DermaState)

stream_graph.add_node("vision", vision_node)
stream_graph.add_node("query", query_node)
stream_graph.add_node("parallel_retrieval", parallel_retrieval_node)
stream_graph.add_node("merge", merge_node)

stream_graph.set_entry_point("vision")

stream_graph.add_edge("vision", "query")
stream_graph.add_edge("query", "parallel_retrieval")
stream_graph.add_edge("parallel_retrieval", "merge")
stream_graph.add_edge("merge", END)

derma_stream_app = stream_graph.compile()