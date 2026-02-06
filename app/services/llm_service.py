
import subprocess

def generate_answer(context, question):
    prompt = f"""
You are a skincare expert AI.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8"
    )

    return result.stdout.strip()
