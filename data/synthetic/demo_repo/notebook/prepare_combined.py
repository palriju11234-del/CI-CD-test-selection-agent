import json
from pathlib import Path


FEVER_PATH = Path("data/fever/train.jsonl")
FEVEROUS_PATH = Path("data/feverous/train.jsonl")
OUTPUT_PATH = Path("data/combined/train.jsonl")


LABEL_MAP = {
    "SUPPORTS": "true",
    "REFUTES": "false",
    "NOT ENOUGH INFO": "uncertain",
}


def read_fever(path):
    records = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)

            label = item.get("label")
            claim = item.get("claim")

            if label in LABEL_MAP and claim:
                records.append({
                    "claim": claim.strip(),
                    "label": LABEL_MAP[label],
                    "source": "fever"
                })

    return records


def read_feverous(path):
    records = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)

            label = item.get("label")
            claim = item.get("claim")

            if label in LABEL_MAP and claim:
                records.append({
                    "claim": claim.strip(),
                    "label": LABEL_MAP[label],
                    "source": "feverous"
                })

    return records


def main():

    print("Loading FEVER...")
    fever = read_fever(FEVER_PATH)

    print("Loading FEVEROUS...")
    feverous = read_feverous(FEVEROUS_PATH)

    print(f"FEVER samples: {len(fever)}")
    print(f"FEVEROUS samples: {len(feverous)}")

    combined = fever + feverous

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        for item in combined:
            file.write(
                json.dumps(
                    item,
                    ensure_ascii=False
                ) + "\n"
            )

    print()
    print("Combined dataset created!")
    print(f"Total samples: {len(combined)}")

    print()
    print("Label distribution:")

    counts = {}

    for item in combined:
        label = item["label"]
        counts[label] = counts.get(label, 0) + 1

    for label, count in counts.items():
        print(f"{label}: {count}")


if __name__ == "__main__":
    main()