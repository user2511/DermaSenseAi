import pandas as pd
from app.services.embedding_service import embed_and_store

df = pd.read_csv("data/skincare_data.csv")

df["combined"] = (
    "Ingredient: " + df["Ingredient Name"] +
    ". Function: " + df["Function"] +
    ". Safety: " + df["Safety Rating"].astype(str) +
    ". Description: " + df["Brief Description"]
)

texts = df["combined"].tolist()

embed_and_store(texts)

print("✅ Data ingested")

