"""
main.py - CI/CD Test Selection Agent Pipeline
==============================================
Runs the full pipeline in order:
  1. Collect test history
  2. Analyze code changes  (old commit -> new commit, changed files)
  3. Analyze dependencies  (dependency graph)
  4. Train PPO agent
  5. Run baseline heuristics
  6. Evaluate all strategies  (comparison table)
  7. Run live agent           (real-time test selection output)

Usage:
    python main.py
"""

import os
import sys
import textwrap
from pathlib import Path

# ── make sure the project root is on sys.path ─────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("PYTHONIOENCODING", "utf-8")


# ── tiny display helpers ──────────────────────────────────────────────────────

def _banner(title):
    bar = "=" * 66
    print("\n" + bar)
    print("  " + title)
    print(bar)


def _section(title):
    bar = "-" * 60
    print("\n" + bar)
    print("  " + title)
    print(bar)


def _ok(msg):
    print("  [OK]  " + msg)


def _warn(msg):
    print("  [!!]  " + msg)


# =============================================================================
# STEP 1 - collect test history
# =============================================================================

def step_collect_history():
    _banner("STEP 1 - Collect Test History")
    from src.data.collect_history import main as _collect
    try:
        _collect()
        _ok("test_history.csv written")
    except Exception as exc:
        _warn("collect_history skipped: " + str(exc))


# =============================================================================
# STEP 2 - change analysis
# =============================================================================

def step_change_analysis():
    """Print old/new commit info + changed files. Returns changed_data dict."""
    _banner("STEP 2 - Change Analysis  (old commit -> new commit)")

    from src.features.change_analyzer import ChangeAnalyzer
    from git import Repo

    test_repo = Path(
        os.getenv("TEST_REPO_PATH",
                  str(PROJECT_ROOT / "data" / "synthetic" / "demo_repo"))
    ).resolve()

    try:
        repo = Repo(str(test_repo), search_parent_directories=True)
    except Exception as exc:
        _warn("Cannot open git repo at {}: {}".format(test_repo, exc))
        return {}

    commits = list(repo.iter_commits())
    if len(commits) < 2:
        _warn("Need at least 2 commits to compare - skipping.")
        return {}

    new_commit = commits[0]
    old_commit = commits[1]

    print("\n  Old commit : {}  {}".format(
        old_commit.hexsha[:12], old_commit.message.strip()[:60]))
    print("  New commit : {}  {}".format(
        new_commit.hexsha[:12], new_commit.message.strip()[:60]))

    analyzer = ChangeAnalyzer(str(test_repo))
    changed_data = analyzer.get_diff_info(old_commit.hexsha, new_commit.hexsha)

    if not changed_data:
        print("\n  No Python file changes detected between the two commits.")
        return {}

    _section("Changed Files & Affected Functions")
    for file_path, info in changed_data.items():
        print("\n  File    : " + file_path)
        print("  Lines   : " + str(info["lines"]))
        funcs = info.get("functions", [])
        print("  Funcs   : " + (str(funcs) if funcs else "(none detected)"))

    return changed_data


# =============================================================================
# STEP 3 - dependency analysis
# =============================================================================

def step_dependency_analysis():
    _banner("STEP 3 - Dependency Graph")

    from src.features.dependency_analyzer import DependencyAnalyzer

    test_repo = Path(
        os.getenv("TEST_REPO_PATH",
                  str(PROJECT_ROOT / "data" / "synthetic" / "demo_repo"))
    ).resolve()

    dep_graph = DependencyAnalyzer(str(test_repo)).map_dependencies()

    if not dep_graph:
        print("  No test -> source dependencies found.")
        return {}

    print()
    for test_file, deps in sorted(dep_graph.items()):
        deps_str = ", ".join(deps) if deps else "(no local imports)"
        wrapped = textwrap.fill(
            deps_str, width=55, subsequent_indent="               ")
        print("  " + test_file)
        print("      imports -> " + wrapped)

    return dep_graph


# =============================================================================
# STEP 4 - train PPO
# =============================================================================

def step_train_ppo():
    """Train (or retrain) the PPO agent. Returns (features, true_outcomes)."""
    _banner("STEP 4 - Train PPO Agent")

    from src.agents.train_ppo import build_training_data, train_and_evaluate

    test_repo = Path(
        os.getenv("TEST_REPO_PATH",
                  str(PROJECT_ROOT / "data" / "synthetic" / "demo_repo"))
    ).resolve()

    # Build features so we can display them before training
    features, true_outcomes = build_training_data(test_repo)

    _section("Live Test Features")
    col_w = 50
    print("  {:<{}} {:>4}  {:>8}  {:>8}  {}".format(
        "Test", col_w, "Dep", "FailRate", "AvgDur", "Status"))
    print("  " + "-" * col_w + " ----  --------  --------  ------")
    for name, f in features.items():
        short = name.split("/", 1)[-1] if "/" in name else name
        status = " FAIL" if true_outcomes.get(name) == "FAIL" else ""
        print("  {:<{}} {:>4.0f}  {:>8.4f}  {:>8.4f}{}".format(
            short, col_w, f["is_dependent"], f["fail_rate"],
            f["avg_duration"], status))

    if true_outcomes:
        print("\n  Failing tests: " +
              ", ".join(k.split("/")[-1] for k in true_outcomes))
    else:
        print("\n  No failing tests detected in the current suite.")

    print()
    train_and_evaluate()

    return features, true_outcomes


# =============================================================================
# STEP 5 - baseline heuristics
# =============================================================================

def step_baselines(features):
    _banner("STEP 5 - Baseline Heuristics")

    from src.baselines.heuristics import BaselinePrioritizer
    p = BaselinePrioritizer(features)

    strategies = {
        "Alphabetical (default)": p.alphabetical_order(),
        "Random":                  p.random_order(),
        "Cheapest first":          p.cheapest_first(),
        "Historical fail rate":    p.historical_failure_rate(),
        "Dependency based":        p.dependency_based(),
    }

    for name, order in strategies.items():
        short = [t.split("/")[-1] for t in order]
        wrapped = textwrap.fill(
            ", ".join(short), width=58,
            subsequent_indent="                      ")
        print("\n  {}:".format(name))
        print("    order -> " + wrapped)

    return p


# =============================================================================
# STEP 6 - evaluation table
# =============================================================================

def step_evaluate(features, true_outcomes, prioritizer):
    _banner("STEP 6 - Evaluation - Strategy Comparison Table")

    import pandas as pd
    from stable_baselines3 import PPO
    from src.evaluation.evaluator import Evaluator, get_model_order

    model_path = PROJECT_ROOT / "models" / "ppo_ci_agent_v1.zip"
    ppo_order = None

    if not model_path.exists():
        _warn("Model not found at {} - skipping RL strategy.".format(model_path))
    else:
        model = PPO.load(str(model_path))
        try:
            ppo_order = get_model_order(model, features)
        except Exception as exc:
            _warn("PPO ordering failed: " + str(exc))

    evaluator = Evaluator(features, true_outcomes)

    strategies = {
        "Alphabetical (default)": prioritizer.alphabetical_order(),
        "Random":                  prioritizer.random_order(),
        "Cheapest First":          prioritizer.cheapest_first(),
        "Historical Fail Rate":    prioritizer.historical_failure_rate(),
        "Dependency Based":        prioritizer.dependency_based(),
    }
    if ppo_order:
        strategies["Trained RL Agent (PPO)"] = ppo_order

    results = [
        evaluator.evaluate_sequence(name, seq)
        for name, seq in strategies.items()
    ]
    df = pd.DataFrame(results)

    print("\n  Total suite execution time : {:.4f}s".format(
        evaluator.total_suite_duration))
    print("  Total tests               : {}".format(evaluator.total_tests))
    print()
    print(df.to_string(index=False))


# =============================================================================
# STEP 7 - live agent
# =============================================================================

def step_live_agent():
    _banner("STEP 7 - Live Agent - Real-Time PPO Test Selection")

    import importlib
    from unittest import mock

    exit_code_holder = [0]

    def _capture_exit(code=0):
        exit_code_holder[0] = int(code) if code is not None else 0
        raise SystemExit(code)

    live_agent_mod = importlib.import_module("src.live_agent")

    with mock.patch("sys.exit", side_effect=_capture_exit):
        try:
            live_agent_mod.main()
        except SystemExit:
            pass

    print()
    if exit_code_holder[0] == 0:
        _ok("Live agent finished - CI Status: PASSED")
    else:
        _warn("Live agent finished - CI Status: FAILED  "
              "(failures detected in repo)")


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    _banner("CI/CD TEST SELECTION AGENT - Full Pipeline")
    print("  Project root : " + str(PROJECT_ROOT))

    step_collect_history()           # 1
    changed_data = step_change_analysis()  # 2
    step_dependency_analysis()       # 3
    features, true_outcomes = step_train_ppo()   # 4
    prioritizer = step_baselines(features)        # 5
    step_evaluate(features, true_outcomes, prioritizer)  # 6
    step_live_agent()                # 7

    _banner("Pipeline Complete")
    print()


if __name__ == "__main__":
    main()
