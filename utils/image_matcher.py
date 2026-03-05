import json
from PIL import Image
import imagehash
import numpy as np

DATA_FILE = "data/precomputed_results.json"

with open(DATA_FILE) as f:
    PRECOMPUTED = json.load(f)


def preprocess(img):

    img = img.convert("RGB")
    img = img.resize((256,256))

    return img


def find_matching_image(uploaded_image):

    uploaded_image = preprocess(uploaded_image)

    uploaded_hash = imagehash.phash(uploaded_image)

    distances = []
    best_match = None
    best_distance = 999

    for item in PRECOMPUTED:

        stored_hash = imagehash.hex_to_hash(item["hash"])

        distance = uploaded_hash - stored_hash

        distances.append(distance)

        if distance < best_distance:
            best_distance = distance
            best_match = item

    mean_distance = np.mean(distances)

    print("Distances:", distances)
    print("Mean distance:", mean_distance)
    print("Best distance:", best_distance)

    # Hybrid threshold
    if best_distance < (mean_distance - 2) and best_distance < 31:
        return best_match

    return None