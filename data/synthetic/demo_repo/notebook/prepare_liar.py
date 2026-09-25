import pandas as pd
import json
from pathlib import Path


LIAR_DIR = Path("data/liar")
OUTPUT = LIAR_DIR / "normalized.jsonl"


LABEL_MAP = {
    "true": "true",
    "mostly-true": "true",

    "half-true": "uncertain",
    "barely-true": "uncertain",

    "false": "false",
    "pants-fire": "false",
}


COLUMNS = [
    "id",
    "label",
    "statement",
    "subject",
    "speaker",
    "speaker_job",
    "state",
    "party",
    "barely_true_count",
    "false_count",
    "half_true_count",
    "mostly_true_count",
    "pants_fire_count",
    "context",
]


def process_file(path, records):

    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=COLUMNS,
        dtype=str,
        keep_default_na=False,
    )

    print(f"{path.name}: {len(df)} samples")

    for _, row in df.iterrows():

        original_label = row["label"].strip()
        claim = row["statement"].strip()

        if original_label not in LABEL_MAP:
            continue

        if not claim:
            continue

        records.append({
            "claim": claim,
            "label": LABEL_MAP[original_label],
            "source": "liar",
            "original_label": original_label,
        })


def main():

    records = []

    for filename in ["train.tsv", "valid.tsv", "test.tsv"]:

        path = LIAR_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Missing: {path}"
            )

        process_file(path, records)

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        for record in records:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print("\nLIAR normalization complete!")
    print(f"Total samples: {len(records)}")

    print("\nLabel distribution:")

    counts = {}

    for record in records:
        label = record["label"]
        counts[label] = counts.get(label, 0) + 1

    for label, count in counts.items():
        print(f"{label}: {count}")


if __name__ == "__main__":
    main()