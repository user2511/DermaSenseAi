from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama

from utils.image_matcher import find_matching_image


llm = Ollama(model="tinyllama")


def match_question(user_question, conversations):

    questions = [c["question"] for c in conversations]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(questions + [user_question])

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_index = similarity.argmax()
    best_score = similarity[0][best_index]

    if best_score > 0.75:
        return conversations[best_index]["answer"]

    return None


async def generate_response(image_file, question):

    matched = find_matching_image(image_file)

    if matched is None:
        yield "Sorry, I cannot recognize this skin condition."
        return

    stored_answer = match_question(
        question,
        matched["conversations"]
    )

    if stored_answer:
        yield stored_answer
        return

    context = matched["final_context"]

    prompt = f"""
You are DermaSense AI dermatology assistant.

Use the following dermatology context to answer.

Context:
{context}

Question:
{question}

Answer:
"""

    # STREAM TOKENS FROM OLLAMA
    for chunk in llm.stream(prompt):

        if hasattr(chunk, "content"):
            yield chunk.content
        else:
            yield str(chunk)