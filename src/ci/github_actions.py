import os
import subprocess
from src.ci.context import CIContext

class GitHubActionsProvider:
    @staticmethod
    def _get_previous_commit(repo_path: str, current_commit: str) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", f"{current_commit}~1"],
                cwd=repo_path,
                text=True
            ).strip()
        except subprocess.CalledProcessError:
            return current_commit

    @staticmethod
    def get_context(default_local_repo: str) -> CIContext:
        """
        Detects the CI environment. 
        Returns a CIContext object with the correct repo path and commits.
        """
        # GitHub Actions automatically sets this environment variable to "true"
        is_ci = os.getenv("GITHUB_ACTIONS") == "true"
        test_repo_path = os.getenv("TEST_REPO_PATH") or os.path.abspath(default_local_repo)
        
        if is_ci:
            # 1. We are running in the cloud. Get the workspace path.
            repo_path = os.getenv("GITHUB_WORKSPACE", os.getcwd())
            
            # 2. Get the current commit triggering the workflow
            current_commit = os.getenv("GITHUB_SHA", "HEAD")
            
            # 3. Determine the base commit (what we are comparing against)
            base_ref = os.getenv("GITHUB_BASE_REF")
            if base_ref:
                # It's a Pull Request. Compare against the target branch (e.g., origin/main)
                try:
                    base_commit = subprocess.check_output(
                        ["git", "rev-parse", f"origin/{base_ref}"], 
                        cwd=repo_path, text=True
                    ).strip()
                except Exception:
                    base_commit = "HEAD~1"
            else:
                # It's a direct push. Compare against the previous commit.
                base_commit = "HEAD~1"
                
            return CIContext(
                repo_path=repo_path,
                current_commit=current_commit,
                base_commit=base_commit,
                is_ci=True,
                provider="github_actions",
                test_repo_path=test_repo_path
            )
        else:
            # We are running locally on your machine.
            test_repo_path = os.path.abspath(default_local_repo)
            try:
                repo_path = subprocess.check_output(
                    ["git", "rev-parse", "--show-toplevel"],
                    cwd=test_repo_path,
                    text=True
                ).strip()
            except (OSError, subprocess.CalledProcessError):
                repo_path = os.getcwd()

            current_commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_path,
                text=True
            ).strip()

            return CIContext(
                repo_path=repo_path,
                current_commit=current_commit,
                base_commit=GitHubActionsProvider._get_previous_commit(
                    repo_path,
                    current_commit
                ),
                is_ci=False,
                provider="local_dev",
                test_repo_path=test_repo_path
            )

# ============================================================
# TEST THE CI ADAPTER
# ============================================================
if __name__ == "__main__":
    import json
    import sys
    
    # Simulate where our local demo repo is
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    local_repo = os.path.join(base_path, "data", "synthetic", "demo_repo")
    
    context = GitHubActionsProvider.get_context(default_local_repo=local_repo)
    
    print(f"--- CI Context Detected ---")
    print(f"Provider:       {context.provider}")
    print(f"Is CI Environment? {context.is_ci}")
    print(f"Repository Path: {context.repo_path}")
    print(f"Compare:        {context.base_commit} -> {context.current_commit}")