import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from stable_baselines3 import PPO

# Ensure Python can find the src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.environment.ci_env import CITestEnvironment
from src.runner.test_discovery import TestDiscoverer
from src.runner.test_runner import SingleTestRunner


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_training_data(test_repo: Path):
    test_names = TestDiscoverer.discover_tests(str(test_repo))
    if not test_names:
        raise RuntimeError(f"No runnable tests found in {test_repo}")

    history_path = PROJECT_ROOT / "data" / "processed" / "test_history.csv"
    history = pd.read_csv(history_path) if history_path.exists() else pd.DataFrame()
    features = {}
    true_outcomes = {}

    for test_name in test_names:
        matching = pd.DataFrame()
        if not history.empty and "test" in history:
            matching = history[history["test"].astype(str).str.endswith(
                test_name.split("/", 1)[-1]
            )]

        fail_rate = 0.0
        avg_duration = 0.1
        if not matching.empty:
            results = matching["result"].astype(str).str.upper()
            fail_rate = float(results.str.startswith("FAIL").mean())
            avg_duration = float(matching["duration"].mean())
            if results.iloc[-1].startswith("FAIL"):
                true_outcomes[test_name] = "FAIL"

        features[test_name] = {
            "is_dependent": 1.0,
            "fail_rate": fail_rate,
            "avg_duration": max(avg_duration, 0.001)
        }

    for test_name in test_names:
        result = SingleTestRunner.run_test(str(test_repo), test_name)
        if result["outcome"] == "FAIL":
            true_outcomes[test_name] = "FAIL"
        features[test_name]["avg_duration"] = max(
            float(result["duration"]),
            0.001
        )

    return features, true_outcomes

def train_and_evaluate():
    test_repo = Path(os.getenv(
        "TEST_REPO_PATH",
        str(PROJECT_ROOT / "data" / "synthetic" / "demo_repo")
    )).resolve()
    features, true_outcomes = build_training_data(test_repo)
    print(f"Training on {len(features)} tests from {test_repo}")
    
    # 2. Initialize Environment
    env = CITestEnvironment(features=features, true_outcomes=true_outcomes)
    
    # 3. Initialize the PPO Agent
    # MlpPolicy is a standard Neural Network. verbose=1 prints training progress.
    print("--- Training PPO Agent (This will take a few seconds) ---")
    model = PPO("MlpPolicy", env, verbose=0, learning_rate=0.001)
    
    # Train for 5,000 steps. The agent will interact with the environment, 
    # receive rewards, and update its neural network.
    model.learn(total_timesteps=5000)
    
    # Save the trained model
    model_path = PROJECT_ROOT / "models" / "ppo_ci_agent_v1"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))
    print(f"Model saved to {model_path}.zip")
    
    # 4. Evaluate the trained agent
    print("\n--- Evaluating Trained Agent ---")
    obs, info = env.reset()
    terminated = False
    step_count = 1
    
    while not terminated:
        # Ask the trained neural network for the best action based on current obs
        action, _states = model.predict(obs, deterministic=True)
        action = int(action)
        
        # Fallback mask: Standard PPO might occasionally suggest an already executed test.
        # If it does, we override it with a valid action.
        if action in env.executed_tests:
            action = np.random.choice(info['valid_actions'])
            
        test_picked = env.test_names[action]
        obs, reward, terminated, truncated, info = env.step(action)
        
        print(f"Step {step_count}: Agent Selected '{test_picked}'")
        print(f"  -> Reward: {reward} | Failures Found: {info['failures_found']}")
        step_count += 1
        
    print("--- Episode Complete ---")

if __name__ == "__main__":
    train_and_evaluate()