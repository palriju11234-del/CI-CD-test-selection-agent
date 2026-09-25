from datasets import load_dataset
import pandas as pd
import os

print("Downloading FEVER dataset...")

dataset = load_dataset("fever", "v1.0")

os.makedirs("data/fever", exist_ok=True)

label_map = {
    "SUPPORTS": "true",
    "REFUTES": "false",
    "NOT ENOUGH INFO": "uncertain"
}

for split in ["train", "labelled_dev", "labelled_test"]:

    records = []

    for item in dataset[split]:
        records.append({
            "claim": item["claim"],
            "label": label_map[item["label"]]
        })

    df = pd.DataFrame(records)

    output_path = f"data/fever/{split}.csv"

    df.to_csv(output_path, index=False)

    print(f"Saved {output_path} ({len(df)} rows)")

print("\nDone!")