import os
import sys
import subprocess
import traceback
import numpy as np
from stable_baselines3 import PPO

# Ensure Python can find the src modules from the project root
sys.path.append(os.getcwd())
from src.ci.github_actions import GitHubActionsProvider
from src.runner.test_discovery import TestDiscoverer
from src.runner.test_runner import SingleTestRunner
from src.features.change_analyzer import ChangeAnalyzer
from src.features.dependency_analyzer import DependencyAnalyzer
from src.features.state_builder import StateBuilder

def main():
    print("==================================================")
    print("🤖 CI/CD Test Selection Agent - Continuous Execution")
    print("==================================================")

    try:
        # 1. CI Context Initialization (Using strict absolute paths for Windows GitPython)
        base_path = os.getcwd()
        default_repo = os.path.join(base_path, "data", "synthetic", "demo_repo")
        history_path = os.path.join(base_path, "data", "processed", "test_history.csv")
        model_path = os.path.join(base_path, "models", "ppo_ci_agent_v1.zip")
        
        # FIX: Export PYTHONPATH globally so subprocesses (pytest) can find 'src' modules
        os.environ["PYTHONPATH"] = default_repo
        
        context = GitHubActionsProvider.get_context(default_repo)
        print(f"[Context] Provider: {context.provider} | Repo: {context.repo_path}")
        test_repo = context.test_repo_path or context.repo_path

        # 2. Extract Features
        print("[Agent] Analyzing changes & dependencies...")
        c_analyzer = ChangeAnalyzer(context.repo_path)
        changed_data = c_analyzer.get_diff_info(context.base_commit, context.current_commit)
        
        d_analyzer = DependencyAnalyzer(test_repo)
        dep_graph = d_analyzer.map_dependencies()

        # 3. Dynamic Test Discovery
        print("[Agent] Discovering live tests...")
        live_tests = TestDiscoverer.discover_tests(test_repo)
        num_tests = len(live_tests)
        if num_tests == 0:
            print("No tests found. Exiting.")
            sys.exit(0)

        # 4. Build RL State
        state_builder = StateBuilder(test_repo, history_path)
        features = state_builder.build_features(changed_data, dep_graph)
        
        # 5. Load RL Model
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        model = PPO.load(model_path)

        # 6. The Continuous Execution Loop
        print("\n[Agent] Commencing Continuous Test Selection...")
        executed_indices = set()
        failures_found = 0
        
        for step in range(num_tests):
            obs = np.zeros((num_tests, 4), dtype=np.float32)
            for i, test in enumerate(live_tests):
                feat = features.get(test, {'is_dependent': 0.0, 'fail_rate': 0.0, 'avg_duration': 0.1})
                is_executed = 1.0 if i in executed_indices else 0.0
                obs[i] = [feat['is_dependent'], feat['fail_rate'], feat['avg_duration'], is_executed]
            
            # Agent predicts the best next test
            action, _ = model.predict(obs, deterministic=True)
            action = int(action)
            
            # Mask invalid actions (prevent re-running tests)
            if action in executed_indices:
                valid_actions = [i for i in range(num_tests) if i not in executed_indices]
                action = np.random.choice(valid_actions)
                
            executed_indices.add(action)
            test_to_run = live_tests[action]
            
            # Execute the selected test immediately
            print(f"  [{step+1}/{num_tests}] PPO Selected: {test_to_run}")
            result = SingleTestRunner.run_test(test_repo, test_to_run)
            
            if result['outcome'] == 'FAIL':
                print(f"      -> ❌ FAIL (Duration: {result['duration']}s)")
                failures_found += 1
            else:
                print(f"      -> ✅ PASS (Duration: {result['duration']}s)")

        print("\n==================================================")
        print(f"Execution Complete. Failures Found: {failures_found}")
        print("CI Status: " + ("FAILED" if failures_found > 0 else "PASSED"))
        print("==================================================")
        
        sys.exit(1 if failures_found > 0 else 0)

    except Exception as e:
        # HARD FALLBACK CONTROLLER
        print("\n⚠️ AGENT FAILURE OR TIMEOUT DETECTED")
        print(f"Error: {e}")
        traceback.print_exc()
        print("Initiating Hard Fallback -> Standard Full Suite Execution\n")
        
        fallback_repo = os.path.join(os.getcwd(), "data", "synthetic", "demo_repo")
        os.environ["PYTHONPATH"] = fallback_repo
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], cwd=fallback_repo)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()