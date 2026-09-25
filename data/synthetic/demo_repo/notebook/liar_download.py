from huggingface_hub import hf_hub_download
from pathlib import Path
import shutil
import sys

REPO = "ucsbnlp/liar"
REVISION = "110b00c693ef1844bf3c59637a1b46e0d61389c2"

OUTPUT_DIR = Path("data/liar")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = [
    "liar-train.parquet",
    "liar-validation.parquet",
    "liar-test.parquet",
]

def try_hf_download(repo_id, revision, filename):
    try:
        return hf_hub_download(
            repo_id=repo_id,
            repo_type="dataset",
            revision=revision,
            filename=filename,
        )
    except Exception as e:
        return e


for filename in files:
    print(f"Downloading {filename}...")

    downloaded = None
    errors = []

    # Try a few likely paths/repos
    attempts = [
        (REPO, f"liar/default/{filename}"),
        (REPO, filename),
        ("ucsbai/liar", f"liar/default/{filename}"),
        ("ucsbai/liar", filename),
    ]

    for repo_id, fn in attempts:
        result = try_hf_download(repo_id, REVISION, fn)
        if isinstance(result, Exception):
            errors.append((repo_id, fn, str(result)))
            continue
        downloaded = result
        print(f"Downloaded from {repo_id} -> {fn}")
        break

    # If huggingface_hub attempts failed, try using the datasets library as a fallback
    if downloaded is None:
        try:
            from datasets import load_dataset

            print("Attempting to load via `datasets` package as a fallback...")
            ds = load_dataset("liar")
            split_name = "train" if "train" in filename else ("validation" if "validation" in filename else "test")
            out_path = OUTPUT_DIR / filename
            ds[split_name].to_parquet(str(out_path))
            print(f"Saved via datasets: {out_path}")
            continue
        except Exception as e:
            errors.append(("datasets", filename, str(e)))

    if downloaded is None:
        print("Failed to download", filename)
        print("Attempted locations and errors:")
        for repo_id, fn, err in errors:
            print(f" - {repo_id}:{fn} -> {err}")
        print("\nYou can try:")
        print(" - checking the dataset page on Hugging Face for the correct filenames and revision")
        print(" - installing the `datasets` package: pip install datasets")
        sys.exit(1)

    destination = OUTPUT_DIR / filename
    shutil.copy2(downloaded, destination)

    print(f"Saved: {destination}")

print("\nLIAR download complete!")

OUTPUT_DIR = Path("data/liar")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading LIAR dataset...")

dataset = load_dataset("ucsbnlp/liar")

print("\nDataset loaded successfully!")
print(dataset)

for split in dataset:
    output_file = OUTPUT_DIR / f"{split}.parquet"

    print(f"Saving {split}...")

    dataset[split].to_parquet(output_file)

    print(f"Saved: {output_file}")

print("\nLIAR download complete!")