import pandas as pd
import re


DATA_PATH = "data/claims_balanced_negation.csv"


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    # Make sure the required columns exist
    if "claim" not in df.columns:
        raise ValueError(f"'claim' column not found. Columns: {list(df.columns)}")

    if "label" not in df.columns:
        raise ValueError(f"'label' column not found. Columns: {list(df.columns)}")

    df["claim"] = df["claim"].apply(clean_text)

    X = df["claim"]
    y = df["label"]

    return X, y