import pandas as pd
from app.services.embedding_service import embed_and_store
import os


def run_ingestion():

    if os.path.exists("chroma_db"):
        print("Chroma DB already exists. Skipping ingestion.")
        return   

    print("Loading skincare dataset...")

    df = pd.read_csv("data/skincare_data.csv")

    df["combined"] = (
        "Ingredient: " + df["Ingredient Name"] +
        ". Function: " + df["Function"] +
        ". Safety: " + df["Safety Rating"].astype(str) +
        ". Description: " + df["Brief Description"]
    )

    texts = df["combined"].tolist()

    print(f"Embedding {len(texts)} records...")
    embed_and_store(texts)

    print("✅ Data ingestion completed.")


if __name__ == "__main__":
    run_ingestion()