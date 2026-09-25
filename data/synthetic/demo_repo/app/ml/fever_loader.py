import json
import pandas as pd


LABEL_MAP = {
    "SUPPORTS": "true",
    "REFUTES": "false",
    "NOT ENOUGH INFO": "uncertain"
}


def load_fever_dataset(path: str):

    data = []

    with open(path, "r", encoding="utf-8") as file:

        for line in file:

            item = json.loads(line)

            if item["label"] not in LABEL_MAP:
                continue

            data.append(
                {
                    "claim": item["claim"],
                    "label": LABEL_MAP[item["label"]]
                }
            )

    return pd.DataFrame(data)