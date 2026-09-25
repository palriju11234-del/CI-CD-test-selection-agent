import os
import sys
import subprocess
import traceback
import numpy as np
from stable_baselines3 import PPO

# Ensure Python can find the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.features.change_analyzer import ChangeAnalyzer
from src.features.dependency_analyzer import DependencyAnalyzer
from src.features.state_builder import StateBuilder

def run_tests_with_fallback():
    base_path = os.getcwd()
    repo_path = os.path.join(base_path, "data", "synthetic", "demo_repo")
    history_path = os.path.join(base_path, "data", "processed", "test_history.csv")
    model_path = os.path.join(base_path, "models", "ppo_ci_agent_v1.zip")
    
    # FIX: Set PYTHONPATH so pytest can find the 'src' module inside demo_repo
    env_vars = os.environ.copy()
    env_vars["PYTHONPATH"] = repo_path
    
    print("==================================================")
    print("🤖 CI/CD Test Selection Agent - Live Execution")
    print("==================================================")
    
    try:
        # 1. Feature Extraction Pipeline
        print("[Agent] Analyzing Git changes...")
        c_analyzer = ChangeAnalyzer(repo_path)
        commits = list(c_analyzer.repo.iter_commits(max_count=2))
        changed_data = c_analyzer.get_diff_info(commits[1].hexsha, commits[0].hexsha)
        
        print("[Agent] Mapping test dependencies...")
        d_analyzer = DependencyAnalyzer(repo_path)
        dep_graph = d_analyzer.map_dependencies()
        
        print("[Agent] Building RL state features...")
        state_builder = StateBuilder(repo_path, history_path)
        features = state_builder.build_features(changed_data, dep_graph)
        test_names = list(features.keys())
        num_tests = len(test_names)
        
        # 2. Load the trained RL Model
        print("[Agent] Loading PPO Neural Network...")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        model = PPO.load(model_path)
        
        # 3. Predict the optimal execution order
        print("[Agent] Generating priority sequence...")
        ordered_tests = []
        executed_indices = set()
        
        # Build the sequence until all tests are ordered (Exhaustive Completion)
        for _ in range(num_tests):
            obs = np.zeros((num_tests, 4), dtype=np.float32)
            for i, test in enumerate(test_names):
                feat = features[test]
                is_executed = 1.0 if i in executed_indices else 0.0
                obs[i] = [feat['is_dependent'], feat['fail_rate'], feat['avg_duration'], is_executed]
            
            action, _ = model.predict(obs, deterministic=True)
            action = int(action)
            
            if action in executed_indices:
                valid_actions = [i for i in range(num_tests) if i not in executed_indices]
                action = np.random.choice(valid_actions)
                
            executed_indices.add(action)
            ordered_tests.append(test_names[action])
            
        print(f"[Agent] Optimal Order:\n  " + "\n  ".join(ordered_tests) + "\n")
        
        # 4. Execute pytest in the prioritized order
        pytest_args = ["pytest", "-v"] + [test.split("::")[0] + "::" + test.split("::")[1] for test in ordered_tests]
        print(f"[Runner] Executing: {' '.join(pytest_args)}\n")
        
        # FIX: Added env=env_vars to subprocess
        result = subprocess.run(pytest_args, cwd=repo_path, env=env_vars)
        sys.exit(result.returncode)

    except Exception as e:
        # HARD FALLBACK CONTROLLER
        print("\n==================================================")
        print("⚠️ AGENT FAILURE OR TIMEOUT DETECTED")
        print(f"Error: {e}")
        print("Initiating Hard Fallback -> Standard Full Suite Execution")
        print("==================================================\n")
        
        # FIX: Added env=env_vars to subprocess
        result = subprocess.run(["pytest", "-v", "tests/"], cwd=repo_path, env=env_vars)
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_tests_with_fallback()