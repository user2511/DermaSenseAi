import json
from PIL import Image
import imagehash

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from langchain_community.llms import Ollama


# lightweight LLM
llm = Ollama(model="tinyllama")

DATA_FILE = "data/precomputed_results.json"

with open(DATA_FILE) as f:
    PRECOMPUTED = json.load(f)


# ---------------------------------------
# STEP 1: IMAGE MATCHING
# ---------------------------------------

def find_matching_image(uploaded_image_path):

    uploaded_hash = imagehash.phash(Image.open(uploaded_image_path))

    best_match = None
    best_distance = 999

    for item in PRECOMPUTED:

        stored_hash = imagehash.hex_to_hash(item["hash"])

        distance = uploaded_hash - stored_hash

        if distance < best_distance:
            best_distance = distance
            best_match = item

    # threshold for similarity
    if best_distance <= 8:
        return best_match

    return None


# ---------------------------------------
# STEP 2: QUESTION MATCHING
# ---------------------------------------

def match_question(user_question, conversations):

    questions = [c["question"] for c in conversations]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(questions + [user_question])

    similarity_scores = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_index]

    if best_score > 0.75:
        return conversations[best_index]["answer"]

    return None


# ---------------------------------------
# STEP 3: GENERATE RESPONSE
# ---------------------------------------

def generate_response(image_path, user_question):

    # 1️⃣ find closest image
    matched = find_matching_image(image_path)

    if matched is None:
        return "Sorry, I cannot identify this skin condition."

    # 2️⃣ check stored questions
    stored_answer = match_question(
        user_question,
        matched["conversations"]
    )

    if stored_answer:
        return stored_answer

    # 3️⃣ fallback to LLM
    context = matched["final_context"]

    prompt = f"""
You are DermaSense AI.

Use the dermatology context to answer the question.

Context:
{context}

Question:
{user_question}

Answer:
"""

    response = llm.invoke(prompt)

    return response


# ---------------------------------------
# TEST
# ---------------------------------------

if __name__ == "__main__":

    image_path = "test.jpg"

    question = "How can this condition be treated?"

    answer = generate_response(image_path, question)

    print("\nAI Response:\n")
    print(answer)