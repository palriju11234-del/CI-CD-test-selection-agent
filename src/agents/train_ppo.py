import os
import sys
import numpy as np
from stable_baselines3 import PPO

# Ensure Python can find the src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.environment.ci_env import CITestEnvironment

def train_and_evaluate():
    # 1. Use the exact feature profile we built earlier
    mock_features = {
      "tests/test_calculator.py::test_add": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_divide": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_multiply": {"is_dependent": 1.0, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_subtract": {"is_dependent": 1.0, "fail_rate": 0.5, "avg_duration": 0.1}
    }
    
    # We simulate a commit where subtract is broken
    mock_true_outcomes = {
        "tests/test_calculator.py::test_subtract": "FAIL"
    }
    
    # 2. Initialize Environment
    env = CITestEnvironment(features=mock_features, true_outcomes=mock_true_outcomes)
    
    # 3. Initialize the PPO Agent
    # MlpPolicy is a standard Neural Network. verbose=1 prints training progress.
    print("--- Training PPO Agent (This will take a few seconds) ---")
    model = PPO("MlpPolicy", env, verbose=0, learning_rate=0.001)
    
    # Train for 5,000 steps. The agent will interact with the environment, 
    # receive rewards, and update its neural network.
    model.learn(total_timesteps=5000)
    
    # Save the trained model
    os.makedirs("models", exist_ok=True)
    model.save("models/ppo_ci_agent_v1")
    print("Model saved to models/ppo_ci_agent_v1.zip")
    
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