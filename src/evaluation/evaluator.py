import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
from stable_baselines3 import PPO

# Ensure Python can find the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.baselines.heuristics import BaselinePrioritizer
from src.agents.train_ppo import build_training_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_model_order(model, features: dict) -> list[str]:
    """Generate a test order using the saved model's fixed observation shape."""
    test_names = list(features)
    model_rows, feature_width = model.observation_space.shape
    if feature_width != 4:
        raise ValueError(f"Unsupported PPO feature width: {feature_width}")

    remaining = list(range(len(test_names)))
    ordered = []
    while remaining:
        candidates = remaining[:model_rows]
        observation = np.zeros((model_rows, feature_width), dtype=np.float32)

        for row, index in enumerate(candidates):
            feature = features[test_names[index]]
            observation[row] = [
                feature["is_dependent"],
                feature["fail_rate"],
                feature["avg_duration"],
                0.0
            ]

        for row in range(len(candidates), model_rows):
            observation[row, 3] = 1.0

        action, _ = model.predict(observation, deterministic=True)
        row = min(int(action), len(candidates) - 1)
        selected = candidates[row]
        ordered.append(test_names[selected])
        remaining.remove(selected)

    return ordered

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
    test_repo = Path(os.getenv(
        "TEST_REPO_PATH",
        str(PROJECT_ROOT / "data" / "synthetic" / "demo_repo")
    )).resolve()
    features, true_outcomes = build_training_data(test_repo)
    model_path = PROJECT_ROOT / "models" / "ppo_ci_agent_v1.zip"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    model = PPO.load(str(model_path))
    
    prioritizer = BaselinePrioritizer(features)
    evaluator = Evaluator(features, true_outcomes)
    
    # 1. Gather all baseline sequences
    strategies = {
        "Alphabetical (Default)": prioritizer.alphabetical_order(),
        "Random": prioritizer.random_order(),
        "Cheapest First": prioritizer.cheapest_first(),
        "Historical Failure Rate": prioritizer.historical_failure_rate(),
        "Trained RL Agent (PPO)": get_model_order(model, features)
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