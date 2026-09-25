import random
import os
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.runner.test_discovery import TestDiscoverer

class BaselinePrioritizer:
    def __init__(self, features: dict):
        self.features = features
        self.test_names = list(features.keys())

    def alphabetical_order(self) -> list[str]:
        """Baseline 1: Standard test runner execution (e.g., pytest default)."""
        return sorted(self.test_names)

    def random_order(self, seed: int = 42) -> list[str]:
        """Baseline 2: Random selection."""
        random.seed(seed)
        shuffled = self.test_names.copy()
        random.shuffle(shuffled)
        return shuffled

    def cheapest_first(self) -> list[str]:
        """Baseline 3: Maximize throughput by running the fastest tests first."""
        # Sort by avg_duration ascending
        return sorted(self.test_names, key=lambda t: self.features[t]['avg_duration'])

    def historical_failure_rate(self) -> list[str]:
        """Baseline 4: Always run the most historically flaky/broken tests first."""
        # Sort by fail_rate descending
        return sorted(self.test_names, key=lambda t: self.features[t]['fail_rate'], reverse=True)

    def dependency_based(self) -> list[str]:
        """Baseline 5: Run tests that directly import the changed code."""
        # Sort by is_dependent descending (1 first, then 0)
        return sorted(self.test_names, key=lambda t: self.features[t]['is_dependent'], reverse=True)

# ============================================================
# TEST THE BASELINES
# ============================================================
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    test_repo = Path(os.getenv(
        "TEST_REPO_PATH",
        str(project_root / "data" / "synthetic" / "demo_repo")
    )).resolve()
    test_names = TestDiscoverer.discover_tests(str(test_repo))
    if not test_names:
        raise RuntimeError(f"No runnable tests found in {test_repo}")

    history_path = project_root / "data" / "processed" / "test_history.csv"
    history = pd.read_csv(history_path) if history_path.exists() else pd.DataFrame()
    mock_features = {}

    for test_name in test_names:
        matching = pd.DataFrame()
        if not history.empty and "test" in history:
            matching = history[history["test"].astype(str).str.endswith(
                test_name.split("/", 1)[-1]
            )]

        if matching.empty:
            fail_rate = 0.0
            avg_duration = 0.1
        else:
            results = matching["result"].astype(str).str.upper()
            fail_rate = float(results.str.startswith("FAIL").mean())
            avg_duration = max(float(matching["duration"].mean()), 0.001)

        mock_features[test_name] = {
            "is_dependent": 1.0,
            "fail_rate": fail_rate,
            "avg_duration": avg_duration
        }
    
    prioritizer = BaselinePrioritizer(mock_features)
    
    print(f"--- Baseline Test Ordering Strategies ({len(test_names)} tests) ---")
    print(f"\n1. Alphabetical (Default): \n   {prioritizer.alphabetical_order()}")
    print(f"\n2. Random: \n   {prioritizer.random_order()}")
    print(f"\n3. Cheapest First: \n   {prioritizer.cheapest_first()}")
    print(f"\n4. Historical Failure Rate: \n   {prioritizer.historical_failure_rate()}")
    print(f"\n5. Dependency-Based: \n   {prioritizer.dependency_based()}")