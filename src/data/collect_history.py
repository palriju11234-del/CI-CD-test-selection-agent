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


def clean_generated_bytecode():
    """Remove Python bytecode that would block historical checkouts."""
    tracked_bytecode = subprocess.check_output(
        ["git", "-C", str(REPO_PATH), "ls-files", "*.pyc"],
        text=True
    ).splitlines()

    subprocess.run(
        [
            "git",
            "-C",
            str(REPO_PATH),
            "restore",
            "--worktree",
            "--",
            "*.pyc"
        ],
        check=True
    )

    for cache_dir in REPO_PATH.rglob("__pycache__"):
        if not cache_dir.is_dir():
            continue

        for bytecode_file in cache_dir.glob("*.pyc"):
            relative_path = bytecode_file.relative_to(REPO_PATH).as_posix()
            if relative_path not in tracked_bytecode:
                bytecode_file.unlink()


def checkout_commit(commit):
    clean_generated_bytecode()
    subprocess.run(
        ["git", "-C", str(REPO_PATH), "checkout", "--quiet", commit],
        check=True
    )


def get_test_files():
    result = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_PATH),
            "ls-files",
            "test",
            "tests"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return [
        path for path in result.stdout.splitlines()
        if Path(path).name.startswith("test_")
        and Path(path).suffix == ".py"
    ]


def run_tests(test_files):
    env = os.environ.copy()

    # Allow tests to import modules from the repository root
    env["PYTHONPATH"] = str(REPO_PATH)

    # Prevent Python from creating __pycache__ files
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    command = [
        sys.executable,
        "-m",
        "pytest",
        "--json-report",
        f"--json-report-file={REPORT_FILE}",
        *test_files
    ]

    result = subprocess.run(
        command,
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


def read_test_results(test_files, test_run):
    with REPORT_FILE.open("r") as file:
        data = json.load(file)

    records = []

    for test in data.get("tests", []):
        records.append({
            "test": test["nodeid"],
            "result": test["outcome"].upper(),
            "duration": test.get("duration", 0)
        })

    if records or not test_files:
        return records

    # Some historical commits contain executable test scripts rather than
    # pytest functions. Preserve their collection result in the dataset.
    duration = data.get("duration", 0)
    outcome = "PASSED" if test_run.returncode == 0 else "COLLECTION_ERROR"
    return [
        {
            "test": test_file,
            "result": outcome,
            "duration": duration / len(test_files)
        }
        for test_file in test_files
    ]


def main():

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    commits = get_commits()
    original_commit = get_current_commit()

    print(f"Found {len(commits)} commits.")

    all_records = []

    try:
        for commit in commits:

            print(f"\nProcessing commit: {commit}")

            checkout_commit(commit)

            test_files = get_test_files()
            test_run = run_tests(test_files)

            test_records = read_test_results(test_files, test_run)

            for record in test_records:

                record["commit"] = commit

                all_records.append(record)

                print(
                    record["test"],
                    "->",
                    record["result"],
                    f"({record['duration']:.4f}s)"
                )
    finally:
        clean_generated_bytecode()
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