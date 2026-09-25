import json
import random
from pathlib import Path


INPUT_FILE = Path("data/fever/train.jsonl")
OUTPUT_FILE = Path("data/fever/train_2000.jsonl")

SAMPLES_PER_CLASS = {
    "SUPPORTS": 667,
    "REFUTES": 667,
    "NOT ENOUGH INFO": 666,
}


def create_subset():

    data = {
        "SUPPORTS": [],
        "REFUTES": [],
        "NOT ENOUGH INFO": [],
    }

    # Read FEVER dataset
    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:
            item = json.loads(line)

            label = item.get("label")

            if label in data:
                data[label].append(item)

    # Make selection reproducible
    random.seed(42)

    selected = []

    for label, count in SAMPLES_PER_CLASS.items():

        if len(data[label]) < count:
            raise ValueError(
                f"Not enough samples for {label}. "
                f"Available: {len(data[label])}"
            )

        samples = random.sample(data[label], count)

        selected.extend(samples)

    # Shuffle the final dataset
    random.shuffle(selected)

    # Create output directory if necessary
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        for item in selected:
            file.write(json.dumps(item) + "\n")

    print("Subset created!")
    print(f"Total samples: {len(selected)}")
    print(f"Output: {OUTPUT_FILE}")

    print("\nClass distribution:")

    counts = {}

    for item in selected:
        label = item["label"]
        counts[label] = counts.get(label, 0) + 1

    for label, count in counts.items():
        print(f"{label}: {count}")


if __name__ == "__main__":
    create_subset()