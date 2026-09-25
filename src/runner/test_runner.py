import subprocess
import sys
import time
import os

class SingleTestRunner:
    @staticmethod
    def run_test(repo_path: str, test_id: str) -> dict:
        """
        Executes a single test, measures its duration, and determines 
        if it passed or failed based on pytest's exit code.
        """
        start_time = time.time()
        
        try:
            # Execute just the specific test node
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_id, "-q"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Pytest exit code 0 means PASS. Code 1 means FAIL.
            outcome = "PASS" if result.returncode == 0 else "FAIL"
            
            return {
                "test_id": test_id,
                "outcome": outcome,
                "duration": round(duration, 4)
            }
            
        except Exception as e:
            # If the subprocess crashes entirely, we treat it as a failure
            return {
                "test_id": test_id,
                "outcome": "FAIL",
                "duration": round(time.time() - start_time, 4),
                "error": str(e)
            }

# ============================================================
# TEST THE SINGLE RUNNER
# ============================================================
if __name__ == "__main__":
    import json
    
    # Locate the demo repo
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    local_repo = os.path.join(base_path, "data", "synthetic", "demo_repo")
    
    print(f"Executing tests in: {local_repo}\n")
    
    # 1. Run a test we know will PASS
    print("Running passing test (test_add)...")
    pass_result = SingleTestRunner.run_test(local_repo, "tests/test_calculator.py::test_add")
    print(json.dumps(pass_result, indent=2))
    
    print("\n--------------------------------------------------\n")
    
    # 2. Run the test we know will FAIL (because of the bug in commit 73117d5)
    print("Running failing test (test_subtract)...")
    fail_result = SingleTestRunner.run_test(local_repo, "tests/test_calculator.py::test_subtract")
    print(json.dumps(fail_result, indent=2))