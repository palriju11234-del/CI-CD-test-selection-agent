import json
from pathlib import Path
import pandas as pd


FEVER_FILE = Path("data/fever/train.jsonl")
FEVEROUS_FILE = Path("data/feverous/train.jsonl")
LIAR_FILE = Path("data/liar/normalized.jsonl")

OUTPUT_FILE = Path("data/claims_all.csv")


def load_jsonl(path):
    records = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            records.append(json.loads(line))

    return records


def normalize_fever(records):
    output = []

    for r in records:
        claim = r.get("claim")
        label = r.get("label")

        if not claim or not label:
            continue

        # FEVER labels
        if label == "SUPPORTS":
            label = "true"
        elif label == "REFUTES":
            label = "false"
        elif label == "NOT ENOUGH INFO":
            label = "uncertain"
        else:
            continue

        output.append({
            "claim": claim.strip(),
            "label": label,
            "source": "fever"
        })

    return output


def normalize_feverous(records):
    output = []

    for r in records:

        claim = r.get("claim")
        label = r.get("label")

        if not claim or not label:
            continue

        label_upper = str(label).upper()

        if label_upper in ["SUPPORTS", "SUPPORTED", "TRUE"]:
            label = "true"

        elif label_upper in ["REFUTES", "REFUTED", "FALSE"]:
            label = "false"

        elif label_upper in [
            "NOT ENOUGH INFO",
            "NOT_ENOUGH_INFO",
            "NEI",
            "UNCERTAIN"
        ]:
            label = "uncertain"

        else:
            continue

        output.append({
            "claim": str(claim).strip(),
            "label": label,
            "source": "feverous"
        })

    return output


def load_liar():

    output = []

    with open(LIAR_FILE, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            r = json.loads(line)

            claim = r.get("claim")
            label = r.get("label")

            if not claim or label not in {
                "true",
                "false",
                "uncertain"
            }:
                continue

            output.append({
                "claim": claim.strip(),
                "label": label,
                "source": "liar"
            })

    return output


def main():

    print("Loading FEVER...")
    fever_raw = load_jsonl(FEVER_FILE)
    fever = normalize_fever(fever_raw)

    print(f"FEVER samples: {len(fever)}")

    print("\nLoading FEVEROUS...")
    feverous_raw = load_jsonl(FEVEROUS_FILE)
    feverous = normalize_feverous(feverous_raw)

    print(f"FEVEROUS samples: {len(feverous)}")

    print("\nLoading LIAR...")
    liar = load_liar()

    print(f"LIAR samples: {len(liar)}")

    combined = fever + feverous + liar

    df = pd.DataFrame(combined)

    # Remove empty claims
    df["claim"] = df["claim"].fillna("").astype(str)
    df = df[df["claim"].str.strip() != ""]

    # Remove exact duplicate claims
    before = len(df)

    df = df.drop_duplicates(
        subset=["claim"],
        keep="first"
    )

    duplicates = before - len(df)

    # Shuffle
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\n==============================")
    print("COMBINED DATASET CREATED")
    print("==============================")

    print(f"Total samples: {len(df)}")
    print(f"Duplicates removed: {duplicates}")

    print("\nSource distribution:")
    print(df["source"].value_counts())

    print("\nLabel distribution:")
    print(df["label"].value_counts())

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()