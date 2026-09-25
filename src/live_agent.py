import os
import sys
import subprocess
import traceback
import numpy as np
from stable_baselines3 import PPO

# Ensure Python can find the project modules
sys.path.append(os.getcwd())

from src.ci.github_actions import GitHubActionsProvider
from src.runner.test_discovery import TestDiscoverer
from src.runner.test_runner import SingleTestRunner
from src.features.change_analyzer import ChangeAnalyzer
from src.features.dependency_analyzer import DependencyAnalyzer
from src.features.state_builder import StateBuilder


def get_test_features(features: dict, test_name: str) -> dict:
    """Resolve features stored for either a test file or a pytest node ID."""
    test_features = features.get(test_name)
    if test_features is not None:
        return test_features

    test_file = test_name.split("::", 1)[0]
    return features.get(
        test_file,
        {
            "is_dependent": 0.0,
            "fail_rate": 0.0,
            "avg_duration": 0.1
        }
    )


def main():
    print("==================================================")
    print("🤖 CI/CD Test Selection Agent - Continuous Execution")
    print("==================================================")

    try:
        # ============================================================
        # 1. PATH CONFIGURATION
        # ============================================================

        # Main agent repository
        base_path = os.getcwd()

        # Synthetic repository containing the actual tests
        test_repo_env = os.getenv("TEST_REPO_PATH")
        if test_repo_env:
            test_repo = os.path.abspath(test_repo_env)
        else:
            test_repo = os.path.abspath(
                os.path.join(base_path, "data", "synthetic", "demo_repo")
            )

        history_path = os.path.join(
            base_path,
            "data",
            "processed",
            "test_history.csv"
        )

        model_path = os.path.join(
            base_path,
            "models",
            "ppo_ci_agent_v1.zip"
        )

        # Python must be able to import our agent modules AND pytest
        # must be able to work with the synthetic repository.
        python_paths = [base_path, test_repo]
        if "PYTHONPATH" in os.environ and os.environ["PYTHONPATH"]:
            python_paths.append(os.environ["PYTHONPATH"])
        os.environ["PYTHONPATH"] = os.pathsep.join(python_paths)

        print(f"[Config] Agent repo : {base_path}")
        print(f"[Config] Test repo  : {test_repo}")

        # ============================================================
        # 2. CI CONTEXT
        # ============================================================

        context = GitHubActionsProvider.get_context(test_repo)
        target_repo = context.test_repo_path or test_repo

        print(
            f"[Context] Provider: {context.provider} | "
            f"Git Repo: {context.repo_path} | "
            f"Test Repo: {target_repo}"
        )

        # ============================================================
        # 3. EXTRACT FEATURES
        # ============================================================

        print("[Agent] Analyzing changes & dependencies...")

        c_analyzer = ChangeAnalyzer(context.repo_path)

        changed_data = c_analyzer.get_diff_info(
            context.base_commit,
            context.current_commit
        )

        d_analyzer = DependencyAnalyzer(target_repo)
        dep_graph = d_analyzer.map_dependencies()
        print("\n[Agent] Dependency tree:")
        print(d_analyzer.format_dependency_tree(dep_graph, changed_data.keys()))

        # ============================================================
        # 4. DYNAMIC TEST DISCOVERY
        # ============================================================

        print("[Agent] Discovering live tests...")

        live_tests = TestDiscoverer.discover_tests(
            target_repo
        )

        num_tests = len(live_tests)

        if num_tests == 0:
            print("No tests found. Exiting.")
            sys.exit(0)

        print(f"[Agent] Discovered {num_tests} tests.")

        # ============================================================
        # 5. BUILD RL STATE
        # ============================================================

        state_builder = StateBuilder(
            target_repo,
            history_path
        )

        features = state_builder.build_features(
            changed_data,
            dep_graph
        )

        # ============================================================
        # 6. LOAD PPO MODEL
        # ============================================================

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}"
            )

        model = PPO.load(model_path)

        # ============================================================
        # 7. CONTINUOUS TEST SELECTION
        # ============================================================

        print("\n[Agent] Commencing Continuous Test Selection...")

        executed_indices = set()
        failures_found = 0
        model_rows, feature_width = model.observation_space.shape

        if feature_width != 4:
            raise ValueError(
                f"Unsupported PPO feature width: {feature_width}; expected 4"
            )

        for step in range(num_tests):

            # --------------------------------------------------------
            # Build observation for every test
            # --------------------------------------------------------

            valid_actions = [
                i for i in range(num_tests)
                if i not in executed_indices
            ]
            dependent_actions = [
                index for index in valid_actions
                if get_test_features(
                    features,
                    live_tests[index]
                )["is_dependent"] > 0
            ]
            independent_actions = [
                index for index in valid_actions
                if index not in dependent_actions
            ]
            priority_actions = dependent_actions or independent_actions
            candidate_indices = priority_actions[:model_rows]

            obs = np.zeros(
                (model_rows, feature_width),
                dtype=np.float32
            )

            for row, test_index in enumerate(candidate_indices):
                test = live_tests[test_index]

                feat = get_test_features(features, test)

                obs[row] = [
                    feat["is_dependent"],
                    feat["fail_rate"],
                    feat["avg_duration"],
                    0.0
                ]

            # Unused rows are masked as already executed for fixed-size models.
            for row in range(len(candidate_indices), model_rows):
                obs[row, 3] = 1.0

            # --------------------------------------------------------
            # PPO selects next test
            # --------------------------------------------------------

            action, _ = model.predict(
                obs,
                deterministic=True
            )

            action = int(action)

            # --------------------------------------------------------
            # Prevent duplicate execution
            # --------------------------------------------------------

            if action >= len(candidate_indices):
                action = 0

            action = candidate_indices[action]

            executed_indices.add(action)

            test_to_run = live_tests[action]

            # --------------------------------------------------------
            # Execute selected test
            # --------------------------------------------------------

            print(
                f"  [{step + 1}/{num_tests}] "
                f"PPO Selected: {test_to_run}"
            )

            result = SingleTestRunner.run_test(
                target_repo,
                test_to_run
            )

            if result["outcome"] == "FAIL":

                print(
                    f"      -> ❌ FAIL "
                    f"(Duration: {result['duration']}s)"
                )

                failures_found += 1

            else:

                print(
                    f"      -> ✅ PASS "
                    f"(Duration: {result['duration']}s)"
                )

        # ============================================================
        # 8. FINAL CI STATUS
        # ============================================================

        print("\n==================================================")
        print(
            f"Execution Complete. "
            f"Failures Found: {failures_found}"
        )

        if failures_found > 0:
            print("CI Status: FAILED")
        else:
            print("CI Status: PASSED")

        print("==================================================")

        # A real test failure should fail the CI job.
        sys.exit(
            1 if failures_found > 0 else 0
        )

    except Exception as e:

        # ============================================================
        # HARD FALLBACK
        # ============================================================

        print("\n⚠️ AGENT FAILURE OR TIMEOUT DETECTED")

        print(f"Error: {e}")

        traceback.print_exc()

        print(
            "\nInitiating Hard Fallback -> "
            "Standard Full Suite Execution\n"
        )

        fallback_repo = (
            context.test_repo_path
            if "context" in locals() and getattr(context, "test_repo_path", None)
            else (test_repo if "test_repo" in locals() else os.path.abspath(
                os.path.join(os.getcwd(), "data", "synthetic", "demo_repo")
            ))
        )

        fallback_paths = [os.getcwd(), fallback_repo]
        if "PYTHONPATH" in os.environ and os.environ["PYTHONPATH"]:
            fallback_paths.append(os.environ["PYTHONPATH"])
        os.environ["PYTHONPATH"] = os.pathsep.join(fallback_paths)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v"
            ],
            cwd=fallback_repo
        )

        sys.exit(result.returncode)


if __name__ == "__main__":
    main()