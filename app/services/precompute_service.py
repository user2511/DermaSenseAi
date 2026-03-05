import json
import os
import asyncio

PRECOMPUTED_FILE = "data/precomputed_results.json"

def load_precomputed():
    if not os.path.exists(PRECOMPUTED_FILE):
        return []
    with open(PRECOMPUTED_FILE, "r") as f:
        return json.load(f)

def find_precomputed_answer(image_name: str):
    data = load_precomputed()

    for item in data:
        if item["image_name"] == image_name:
            return item["answer"]

    return None


# Fake streaming generator
async def stream_text(text: str):
    words = text.split(" ")

    for word in words:
        yield word + " "
        await asyncio.sleep(0.02)  # demo delay