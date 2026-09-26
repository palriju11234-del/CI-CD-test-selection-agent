import subprocess
import json
import csv
import os
import sys
import tempfile
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


def get_repository_root():
    result = subprocess.run(
        ["git", "-C", str(REPO_PATH), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True
    )

    return Path(result.stdout.strip())


def get_commit_timestamp(commit):
    result = subprocess.run(
        ["git", "-C", str(REPO_PATH), "show", "-s", "--format=%cI", commit],
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

    if tracked_bytecode:
        subprocess.run(
            [
                "git",
                "-C",
                str(REPO_PATH),
                "restore",
                "--worktree",
                "--",
                *tracked_bytecode
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
    REPORT_FILE.unlink(missing_ok=True)

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
    try:
        with REPORT_FILE.open("r") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        if not test_files:
            return []
        return [
            {
                "test": test_file,
                "result": "COLLECTION_ERROR",
                "duration": 0.0
            }
            for test_file in test_files
        ]

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


def store_test_history_in_tiger_data(records, commit_timestamps):
    connection_string = os.getenv("TIGER_DATA_URL")
    if not connection_string:
        return None

    rows = [
        (
            commit_timestamps[record["commit"]],
            record["commit"],
            record["test"],
            record["result"],
            float(record["duration"])
        )
        for record in records
    ]
    if not rows:
        return 0

    import psycopg

    create_table = """
        CREATE TABLE IF NOT EXISTS test_history (
            commit_time TIMESTAMPTZ NOT NULL,
            commit_sha TEXT NOT NULL,
            test_name TEXT NOT NULL,
            result TEXT NOT NULL,
            duration DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (commit_time, commit_sha, test_name)
        ) WITH (
            tsdb.hypertable,
            tsdb.segmentby = 'commit_sha',
            tsdb.orderby = 'commit_time DESC'
        )
    """
    insert_rows = """
        INSERT INTO test_history (
            commit_time, commit_sha, test_name, result, duration
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (commit_time, commit_sha, test_name) DO UPDATE SET
            result = EXCLUDED.result,
            duration = EXCLUDED.duration
    """

    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table)
            cursor.executemany(insert_rows, rows)

    return len(rows)


def main():
    global REPO_PATH

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    commits = get_commits()
    original_commit = get_current_commit()
    repository_root = get_repository_root()
    original_repo_path = REPO_PATH
    history_repo_path = REPO_PATH.relative_to(repository_root)
    commit_timestamps = {}

    print(f"Found {len(commits)} commits.")

    all_records = []

    with tempfile.TemporaryDirectory(prefix="ci-test-history-") as temp_dir:
        worktree_root = Path(temp_dir) / "repo"
        subprocess.run(
            [
                "git",
                "-C",
                str(repository_root),
                "worktree",
                "add",
                "--quiet",
                "--detach",
                str(worktree_root),
                original_commit
            ],
            check=True
        )
        REPO_PATH = worktree_root / history_repo_path

        try:
            for commit in commits:

                print(f"\nProcessing commit: {commit}")
                commit_timestamps[commit] = get_commit_timestamp(commit)

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
            REPO_PATH = original_repo_path
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository_root),
                    "worktree",
                    "remove",
                    "--force",
                    str(worktree_root)
                ],
                check=True
            )

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

    stored_count = store_test_history_in_tiger_data(
        all_records,
        commit_timestamps
    )
    if stored_count is None:
        print("Tiger Data skipped: set TIGER_DATA_URL to enable database storage.")
    else:
        print(f"Stored {stored_count} test-history rows in Tiger Data.")


if __name__ == "__main__":
    main()