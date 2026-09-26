import subprocess
import os
import sys

class TestDiscoverer:
    @staticmethod
    def discover_tests(repo_path: str) -> list[str]:
        """
        Runs pytest in collect-only mode to discover all available tests
        in the target repository exactly as pytest sees them.
        """
        try:
            test_dir = next(
                (
                    directory
                    for directory in ("tests", "test")
                    if os.path.isdir(os.path.join(repo_path, directory))
                ),
                ".",
            )

            tests = []
            collection_errors = []
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_dir, "--collect-only", "-q"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )

            for line in result.stdout.splitlines():
                # Pytest node IDs contain '::', unlike its summary lines.
                if "::" in line:
                    test_id = line.strip()
                    if test_id not in tests:
                        tests.append(test_id)

            if result.returncode != 0:
                collection_errors.append(
                    result.stderr.strip() or result.stdout.strip()
                )

            if collection_errors:
                if tests:
                    print(
                        "Pytest collection reported errors; "
                        f"continuing with {len(tests)} collected tests."
                    )
                else:
                    print("Pytest collection reported errors; no runnable tests were discovered.")
                for error_output in collection_errors:
                    if error_output:
                        print(error_output)
                    
            return tests
        except Exception as e:
            print(f"Error discovering tests: {e}")
            return []

# ============================================================
# TEST THE DISCOVERER
# ============================================================
if __name__ == "__main__":
    # Simulate where our local demo repo is
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    local_repo = os.path.join(base_path, "data", "synthetic", "demo_repo")
    
    print(f"Scanning repository for tests: {local_repo}")
    tests = TestDiscoverer.discover_tests(local_repo)
    
    print("\n--- Discovered Tests ---")
    for t in tests:
        print(t)
    print(f"\nTotal tests found: {len(tests)}")