import pandas as pd

df = pd.read_csv("data/skincare_data.csv")

print("Shape:", df.shape)

print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
df.isnull().sum()
print("\nMissing values per column:")
print(df.isnull().sum())
