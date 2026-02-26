import json
from typing import Tuple
from langchain_community.llms import Ollama

# -----------------------------
# LLM
# -----------------------------
llm = Ollama(model="mistral")


# -----------------------------
# 1. HEURISTIC SCORE
# -----------------------------
def _heuristic_image_dependency_score(question: str) -> float:
    """
    Returns a score between 0.0 and 1.0
    based on keyword matches indicating image dependence.
    """

    image_keywords = [
        "this",
        "my skin",
        "look at",
        "see",
        "in the image",
        "how does it look",
        "is this acne",
        "what is this",
        "these spots",
        "this rash",
        "does it look",
        "from the image",
        "based on the image"
    ]

    q_lower = question.lower()
    match_count = sum(1 for kw in image_keywords if kw in q_lower)

    # Normalize
    score = min(match_count / 3, 1.0)
    return score


# -----------------------------
# 2. LLM CLASSIFICATION
# -----------------------------
def _classify_dependency_with_confidence(
    question: str,
    image_summary: str
) -> Tuple[str, float]:
    """
    Uses LLM to classify dependency level and confidence.
    Returns: (category, confidence)
    """

    prompt = f"""
    Determine how much the user's question depends on the image.

    Question: {question}
    Image Analysis: {image_summary}

    Respond ONLY in JSON format:
    {{
        "category": "independent | semi-dependent | fully-dependent",
        "confidence": number between 0.0 and 1.0
    }}
    """

    response = llm.invoke(prompt)

    try:
        parsed = json.loads(response)
        category = parsed.get("category", "independent").strip().lower()
        confidence = float(parsed.get("confidence", 0.5))

        if category not in ["independent", "semi-dependent", "fully-dependent"]:
            category = "independent"

        confidence = max(0.0, min(confidence, 1.0))

        return category, confidence

    except Exception:
        # fallback if LLM response malformed
        return "independent", 0.5


# -----------------------------
# 3. FUSION LOGIC
# -----------------------------
def _fuse_dependency_decision(
    heuristic_score: float,
    llm_category: str,
    llm_confidence: float
) -> str:
    """
    Combines heuristic + LLM reasoning using weighted fusion.
    """

    category_score_map = {
        "independent": 0.0,
        "semi-dependent": 0.5,
        "fully-dependent": 1.0
    }

    llm_score = category_score_map.get(llm_category, 0.0)

    # Weighted fusion (LLM dominant)
    final_score = (0.4 * heuristic_score) + (0.6 * llm_score * llm_confidence)

    if final_score >= 0.7:
        return "fully-dependent"
    elif final_score >= 0.3:
        return "semi-dependent"
    else:
        return "independent"


# -----------------------------
# 4. OPTIMIZED QUERY BUILDER
# -----------------------------
def _build_optimized_query(
    question: str,
    image_summary: str,
    dependency: str
) -> str:

    if dependency == "independent":
        # No unnecessary token pollution
        return question

    elif dependency == "semi-dependent":
        return f"""
User Question:
{question}

Image Findings (use only if relevant):
{image_summary}

Provide a dermatology-aware answer integrating image insights if needed.
"""

    else:  # fully-dependent
        return f"""
The user's question depends strongly on the image.

User Question:
{question}

Image Findings:
{image_summary}

Generate a medically grounded dermatology response combining both.
"""


# -----------------------------
# 5. MAIN EXPORTED FUNCTION
# -----------------------------
def build_grounded_query(
    question: str,
    image_summary: str
) -> Tuple[str, str]:
    """
    Main function used by derma_graph.

    Returns:
        grounded_query (str),
        final_dependency (str)
    """

    # If no image → automatically independent
    if not image_summary:
        return question, "independent"

    # Step 1: Heuristic
    heuristic_score = _heuristic_image_dependency_score(question)

    # Optional optimization:
    # If heuristic extremely strong, skip LLM
    if heuristic_score > 0.9:
        final_dependency = "fully-dependent"
    else:
        # Step 2: LLM classification
        llm_category, llm_confidence = _classify_dependency_with_confidence(
            question,
            image_summary
        )

        # Step 3: Fusion
        final_dependency = _fuse_dependency_decision(
            heuristic_score,
            llm_category,
            llm_confidence
        )

    # Step 4: Build optimized query
    grounded_query = _build_optimized_query(
        question,
        image_summary,
        final_dependency
    )

    return grounded_query, final_dependency

