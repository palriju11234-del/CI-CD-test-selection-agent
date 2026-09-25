import random

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
    # Same exact mock features from our RL training
    mock_features = {
      "tests/test_calculator.py::test_add": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.2},
      "tests/test_calculator.py::test_divide": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.5},
      "tests/test_calculator.py::test_multiply": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_subtract": {"is_dependent": 1.0, "fail_rate": 0.5, "avg_duration": 0.3}
    }
    
    prioritizer = BaselinePrioritizer(mock_features)
    
    print("--- Baseline Test Ordering Strategies ---")
    print(f"\n1. Alphabetical (Default): \n   {prioritizer.alphabetical_order()}")
    print(f"\n2. Random: \n   {prioritizer.random_order()}")
    print(f"\n3. Cheapest First: \n   {prioritizer.cheapest_first()}")
    print(f"\n4. Historical Failure Rate: \n   {prioritizer.historical_failure_rate()}")
    print(f"\n5. Dependency-Based: \n   {prioritizer.dependency_based()}")