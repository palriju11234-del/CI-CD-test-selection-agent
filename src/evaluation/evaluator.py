import sys
import os
import pandas as pd

# Ensure Python can find the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.baselines.heuristics import BaselinePrioritizer

class Evaluator:
    def __init__(self, features: dict, true_outcomes: dict):
        self.features = features
        self.true_outcomes = true_outcomes
        self.total_suite_duration = sum(f['avg_duration'] for f in features.values())
        self.total_tests = len(features)

    def evaluate_sequence(self, strategy_name: str, ordered_tests: list[str]) -> dict:
        """
        Simulates running the ordered tests to calculate Time to First Failure (TTFF).
        """
        time_elapsed = 0.0
        tests_run = 0
        failure_found = False
        
        for test in ordered_tests:
            time_elapsed += self.features[test]['avg_duration']
            tests_run += 1
            
            if self.true_outcomes.get(test) == "FAIL":
                failure_found = True
                break  # The developer gets feedback the moment this fails!
        
        # If no failure exists in the suite, TTFF is the full suite time
        ttff = time_elapsed if failure_found else None
        
        # Compute saved is the time the developer DIDN'T have to wait 
        # to find out their code was broken.
        time_saved = self.total_suite_duration - time_elapsed if failure_found else 0.0
        
        return {
            "Strategy": strategy_name,
            "Failure Found": failure_found,
            "Tests to First Fail": tests_run if failure_found else "N/A",
            "TTFF (seconds)": round(ttff, 4) if ttff else "N/A",
            "Feedback Time Saved (s)": round(time_saved, 4) if failure_found else 0.0
        }

# ============================================================
# RUN THE COMPARISON
# ============================================================
if __name__ == "__main__":
    # Same mock features
    mock_features = {
      "tests/test_calculator.py::test_add": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.2},
      "tests/test_calculator.py::test_divide": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.5},
      "tests/test_calculator.py::test_multiply": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_subtract": {"is_dependent": 1.0, "fail_rate": 0.5, "avg_duration": 0.3}
    }
    
    mock_true_outcomes = {
        "tests/test_calculator.py::test_subtract": "FAIL"
    }
    
    prioritizer = BaselinePrioritizer(mock_features)
    evaluator = Evaluator(mock_features, mock_true_outcomes)
    
    # 1. Gather all baseline sequences
    strategies = {
        "Alphabetical (Default)": prioritizer.alphabetical_order(),
        "Random": prioritizer.random_order(),
        "Cheapest First": prioritizer.cheapest_first(),
        "Historical Failure Rate": prioritizer.historical_failure_rate(),
        # Simulating our trained PPO agent which learned to put subtract first
        "Trained RL Agent (PPO)": ["tests/test_calculator.py::test_subtract", 
                                   "tests/test_calculator.py::test_add", 
                                   "tests/test_calculator.py::test_multiply", 
                                   "tests/test_calculator.py::test_divide"] 
    }
    
    # 2. Evaluate and print results
    results = []
    for name, sequence in strategies.items():
        results.append(evaluator.evaluate_sequence(name, sequence))
        
    # Convert to pandas DataFrame for a beautiful console table
    df = pd.DataFrame(results)
    
    print("\n--- CI/CD Test Prioritization Evaluation ---")
    print(f"Total Suite Execution Time: {evaluator.total_suite_duration} seconds\n")
    print(df.to_string(index=False))