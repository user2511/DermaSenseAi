from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama

from app.services.vision_service1 import analyze_skin_image
from app.services.query_service import build_grounded_query
from app.services.retrieval_service import retrieve_similar_chunks
from app.services.memory_service1 import get_memory, store_memory

# Session-based persistence
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
    model="mistral",
    temperature=0.2,
    num_predict=300  # limit token generation
)


# =====================================================
# 1️⃣ VISION NODE (SESSION-AWARE)
# =====================================================

def vision_node(state: DermaState):
    print("\n[VISION NODE]")

    session_id = state["session_id"]
    image = state.get("image")

    # CASE 1 — New image uploaded
    if image:
        summary = analyze_skin_image(image)
        state["vision_context"] = summary or ""

        # Store vision per session (so we reuse later)
        create_or_update_session(session_id, state["vision_context"])

        print("New image analyzed and stored.")
        print("Vision summary:", state["vision_context"])

    # CASE 2 — Follow-up question (reuse previous image)
    else:
        stored_vision = get_session_vision(session_id)

        if stored_vision:
            state["vision_context"] = stored_vision
            print("Reusing previous vision context.")
        else:
            state["vision_context"] = ""
            print("No image context found.")

    return state


# =====================================================
# 2️⃣ QUERY BUILDER NODE
# =====================================================

def query_node(state: DermaState):
    print("\n[QUERY NODE]")

    question = state["question"]
    image_summary = state.get("vision_context", "")

    grounded_query, dependency = build_grounded_query(
        question=question,
        image_summary=image_summary
    )

    state["grounded_query"] = grounded_query
    state["dependency"] = dependency

    print("Dependency:", dependency)
    print("Grounded Query:", grounded_query)

    return state


# =====================================================
# 3️⃣ MEMORY FETCH NODE (SEMANTIC SEARCH)
# =====================================================

def memory_fetch_node(state: DermaState):
    print("\n[MEMORY FETCH NODE]")

    query = state["grounded_query"]

    memories = get_memory(query)
    state["memory"] = " ".join(memories[::2]) if memories else ""

    print("Memory retrieved:", state["memory"])
    return state


# =====================================================
# 4️⃣ RAG NODE (KNOWLEDGE BASE)
# =====================================================

def rag_node(state: DermaState):
    print("\n[RAG NODE]")

    query = state["grounded_query"]

    docs = retrieve_similar_chunks(query)
    state["rag_context"] = " ".join(docs) if docs else ""

    print("RAG context:", state["rag_context"])
    return state


# =====================================================
# 5️⃣ MERGE NODE
# =====================================================

def merge_node(state: DermaState):
    print("\n[MERGE NODE]")

    combined_context = f"""
Vision Analysis:
{state.get("vision_context", "")}

User Query:
{state["grounded_query"]}

Personal Memory:
{state.get("memory", "")}

Knowledge Base Context:
{state.get("rag_context", "")}
"""

    state["final_context"] = combined_context

    print("Final context prepared.")
    return state


# =====================================================
# 6️⃣ FINAL LLM NODE
# =====================================================

def llm_node(state: DermaState):
    print("\n[LLM NODE]")

   

    prompt = f"""
You are DermaSense AI, a dermatology assistant.

You are given structured context that may include:
- Skin analysis from image
- Retrieved medical knowledge
- Previous conversation history

Use this context to answer the current question.

IMPORTANT RULES:
- If this is a follow-up question, answer ONLY what is asked.
- Do NOT repeat full skincare routines unless explicitly requested.
- Be concise and medically safe.
- Avoid repeating previous answers.
- If context is insufficient, say you don't know.

Context:
{state["final_context"]}

Current Question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    # handle langchain return types safely
    if hasattr(response, "content"):
        state["answer"] = response.content
    else:
        state["answer"] = str(response)

    print("LLM Answer:", state["answer"])
    return state


# =====================================================
# 7️⃣ MEMORY STORE NODE
# =====================================================

def memory_store_node(state: DermaState):
    print("\n[MEMORY STORE NODE]")

    session_id = state["session_id"]

    # Store semantic vector memory
    store_memory(
        grounded_query=state["grounded_query"],
        original_question=state["question"],
        vision_summary=state.get("vision_context", ""),
        answer=state["answer"],
        dependency=state.get("dependency", "independent"),
    )

    # Store chat history (SQLite session memory)
    save_message(session_id, "user", state["question"])
    save_message(session_id, "assistant", state["answer"])

    print("Memory stored.")
    return state


# =====================================================
# GRAPH CONSTRUCTION
# =====================================================

graph = StateGraph(DermaState)

graph.add_node("vision", vision_node)
graph.add_node("query", query_node)
graph.add_node("memory_fetch", memory_fetch_node)
graph.add_node("rag", rag_node)
graph.add_node("merge", merge_node)
graph.add_node("llm", llm_node)
graph.add_node("memory_store", memory_store_node)

graph.set_entry_point("vision")

graph.add_edge("vision", "query")
graph.add_edge("query", "memory_fetch")
graph.add_edge("memory_fetch", "rag")
graph.add_edge("rag", "merge")
graph.add_edge("merge", "llm")
graph.add_edge("llm", "memory_store")
graph.add_edge("memory_store", END)

derma_app = graph.compile()