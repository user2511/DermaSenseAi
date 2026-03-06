import os
import json
import uuid
import asyncio
from PIL import Image
import imagehash

from app.graph.derma_graph1 import derma_stream_app, llm
from app.services import query_service


# 🔥 Enable precompute mode
query_service.PRECOMPUTE_MODE = True

IMAGE_FOLDER = "precompute/images"
OUTPUT_FILE = "data/precomputed_results.json"


QUERY_TEMPLATES = [
    "What skin condition is visible in this image?",
    "How severe does this condition appear?",
    "What treatment routine would you suggest?",
    "What ingredients would help improve this?",
    "What should be avoided?",
    "When should someone consult a dermatologist?"
]


def build_prompt(final_context, question):
    return f"""
You are DermaSense AI, a dermatology assistant.

Use the structured context below to answer clearly and safely.

Context:
{final_context}

Question:
{question}

Answer:
"""


async def generate():

    results = []

    image_files = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"Found {len(image_files)} images.")

    for image_name in image_files:

        print(f"\nProcessing: {image_name}")

        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # 🔥 Read image bytes (for graph)
        with open(image_path, "rb") as img:
            image_bytes = img.read()

        # 🔥 Generate perceptual hash (for lightweight runtime matching)
        image_pil = Image.open(image_path)
        img_hash = str(imagehash.phash(image_pil))

        session_id = str(uuid.uuid4())

        # 🔥 STEP 1 — Run full graph ONCE
        state = await derma_stream_app.ainvoke({
            "session_id": session_id,
            "question": "Provide structured dermatological analysis of this image.",
            "image": image_bytes,
            "vision_context": "",
            "grounded_query": "",
            "dependency": "",
            "memory": "",
            "rag_context": "",
            "final_context": "",
        })

        final_context = state.get("final_context", "")

        conversations = []

        # 🔥 STEP 2 — Generate multiple answers from same context
        for query in QUERY_TEMPLATES:

            prompt = build_prompt(final_context, query)
            response = llm.invoke(prompt)

            answer = response.content if hasattr(response, "content") else str(response)

            conversations.append({
                "question": query,
                "answer": answer
            })

        results.append({
            "image_name": image_name,
            "hash": img_hash,                     # ✅ lightweight matching key
            "vision_context": state.get("vision_context", ""),
            "final_context": final_context,
            "conversations": conversations
        })

        print(f"Saved {len(conversations)} responses for {image_name}")

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Precomputed results saved successfully!")


if __name__ == "__main__":
    asyncio.run(generate())