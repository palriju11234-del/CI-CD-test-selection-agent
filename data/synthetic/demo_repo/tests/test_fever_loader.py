from app.ml.fever_loader import load_fever_dataset

df = load_fever_dataset("data/fever/train.jsonl")

print(df.head())

print()

print(df["label"].value_counts())

print()

print("Total samples:", len(df))