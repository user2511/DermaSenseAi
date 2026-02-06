
from datasets import load_dataset
import pandas as pd
import os

# Change this to your dataset
DATASET_NAME = "Scanalyze/Skincare-ingredients"

dataset = load_dataset(DATASET_NAME)

# Convert train split to pandas
df = pd.DataFrame(dataset["train"])

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Save
df.to_csv("data/skincare_data.csv", index=False)

print("Dataset saved to data/skincare_data.csv")
