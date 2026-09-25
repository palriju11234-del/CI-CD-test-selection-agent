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
            # We use python -m pytest to ensure it runs in the current virtual environment
            # --collect-only tells pytest not to run the tests, just list them
            # -q (quiet) strips out the verbose headers and footers
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            tests = []
            for line in result.stdout.splitlines():
                # Pytest node IDs always contain '::' (e.g., tests/test_file.py::test_function)
                if "::" in line:
                    # Isolate the exact test ID, ignoring any trailing characters or status messages
                    test_id = line.strip().split(" ")[0]
                    tests.append(test_id)
                    
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