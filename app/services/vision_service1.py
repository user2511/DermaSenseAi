# app/services/vision_service.py

import torch
import clip
from PIL import Image
import io

# Load CLIP once (global)
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Predefined dermatology labels
DERMA_LABELS = [
    "acne",
    "dry skin",
    "oily skin",
    "hyperpigmentation",
    "dark spots",
    "redness",
    "wrinkles",
    "clear skin",
    "sensitive skin",
    "eczema"
]

def analyze_skin_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)

    text_inputs = torch.cat([
        clip.tokenize(f"a photo of {label}") for label in DERMA_LABELS
    ]).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        text_features = clip_model.encode_text(text_inputs)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    probs = similarity[0]
    top_indices = probs.topk(3).indices.tolist()

    detected = [DERMA_LABELS[i] for i in top_indices]

    summary = f"Detected skin conditions: {', '.join(detected)}."
    return summary
