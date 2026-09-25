import subprocess
import json
import csv
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_PATH = PROJECT_ROOT / "data" / "synthetic" / "demo_repo"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "test_history.csv"
REPORT_FILE = PROJECT_ROOT / "data" / "processed" / "test_results.json"


def get_commits():
    result = subprocess.run(
        ["git", "-C", str(REPO_PATH), "log", "--format=%H", "--reverse"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip().splitlines()


def get_current_commit():
    result = subprocess.run(
        ["git", "-C", str(REPO_PATH), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


def checkout_commit(commit):
    subprocess.run(
        ["git", "-C", str(REPO_PATH), "checkout", "--quiet", commit],
        check=True
    )

def run_tests():
    env = os.environ.copy()

    # Allow tests to import modules from the repository root
    env["PYTHONPATH"] = str(REPO_PATH)

    # Prevent Python from creating __pycache__ files
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--json-report",
            f"--json-report-file={REPORT_FILE}"
        ],
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        env=env
    )

    print("Pytest exit code:", result.returncode)

    if result.stdout:
        print("Pytest output:")
        print(result.stdout)

    if result.stderr:
        print("Pytest errors:")
        print(result.stderr)

    return result

    

def read_test_results():
    with REPORT_FILE.open("r") as file:
        data = json.load(file)

    records = []

    for test in data["tests"]:
        test_name = test["nodeid"]

        outcome = test["outcome"].upper()

        duration = test.get("duration", 0)

        records.append({
            "test": test_name,
            "result": outcome,
            "duration": duration
        })

    return records


def main():

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    commits = get_commits()
    original_commit = get_current_commit()

    print(f"Found {len(commits)} commits.")

    all_records = []

    for commit in commits:

        print(f"\nProcessing commit: {commit}")

        checkout_commit(commit)

        run_tests()

        test_records = read_test_results()

        for record in test_records:

            record["commit"] = commit

            all_records.append(record)

            print(
                record["test"],
                "→",
                record["result"],
                f"({record['duration']:.4f}s)"
            )

    checkout_commit(original_commit)

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "commit",
                "test",
                "result",
                "duration"
            ]
        )

        writer.writeheader()
        writer.writerows(all_records)

    print("\nDataset created successfully!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()