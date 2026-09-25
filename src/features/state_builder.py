import os
import json
import pandas as pd

class StateBuilder:
    def __init__(self, repo_path: str, history_csv_path: str):
        self.repo_path = repo_path
        self.history_csv_path = history_csv_path
        
        # 1. Load historical test data
        if os.path.exists(history_csv_path):
            self.history_df = pd.read_csv(history_csv_path)
        else:
            print(f"Warning: History CSV not found at {history_csv_path}")
            self.history_df = pd.DataFrame(columns=["commit", "test", "result", "duration"])
            
        self.test_stats = self._compute_historical_stats()

    def _compute_historical_stats(self) -> dict:
        """Calculates failure rate and average execution time for each test."""
        stats = {}
        if self.history_df.empty:
            return stats
            
        for test_name, group in self.history_df.groupby('test'):
            runs = len(group)
            
            # Robust check: matches 'FAIL', 'failed', 'Failed', etc.
            fails = len(group[group['result'].astype(str).str.upper().str.startswith('FAIL')])
            avg_duration = group['duration'].mean()
            
            stats[test_name] = {
                'fail_rate': float(fails / runs) if runs > 0 else 0.0,
                'avg_duration': float(avg_duration),
                'total_runs': runs
            }
        return stats

    def build_features(self, changed_data: dict, dependency_graph: dict) -> dict:
        """
        Creates a numerical feature dictionary for every available test, 
        suitable for the Reinforcement Learning agent.
        """
        # Convert file paths like 'src/calculator.py' to Python module names 'src.calculator'
        changed_modules = set()
        for file_path in changed_data.keys():
            if file_path.endswith('.py'):
                mod_name = file_path.replace('.py', '').replace('/', '.').replace('\\', '.')
                changed_modules.add(mod_name)
                # Also include submodule suffixes (e.g. data.synthetic.demo_repo.src.calculator -> src.calculator)
                parts = mod_name.split('.')
                for i in range(len(parts)):
                    changed_modules.add('.'.join(parts[i:]))

        features = {}
        
        for test_name, stats in self.test_stats.items():
            # Extract test_file directly from pytest node ID (e.g., 'tests/test_calc.py::test_add')
            test_file = test_name.split("::")[0].replace("\\", "/") if "::" in test_name else None
            
            # Feature 1: Dependency Match
            is_dependent = 0
            if test_file and test_file in dependency_graph:
                file_deps = dependency_graph[test_file]
                # Check if this test file imports any of the changed source modules
                if any(mod in file_deps for mod in changed_modules):
                    is_dependent = 1
            
            features[test_name] = {
                'is_dependent': is_dependent,                     # 1 if relevant to code change, 0 if not
                'fail_rate': round(stats['fail_rate'], 4),        # e.g., 0.5000
                'avg_duration': round(stats['avg_duration'], 4)   # e.g., 0.0020 seconds
            }
            
        return features


# ============================================================
# END-TO-END PIPELINE TEST
# ============================================================
if __name__ == "__main__":
    from change_analyzer import ChangeAnalyzer
    from dependency_analyzer import DependencyAnalyzer
    
    repo_path = "data/synthetic/demo_repo"
    history_path = "data/processed/test_history.csv"
    
    print("--- 1. Analyzing Changes ---")
    c_analyzer = ChangeAnalyzer(repo_path)
    commits = list(c_analyzer.repo.iter_commits())
    changed_data = c_analyzer.get_diff_info(commits[1].hexsha, commits[0].hexsha)
    print(f"Changed Data: {list(changed_data.keys())}")
    
    print("\n--- 2. Mapping Dependencies ---")
    d_analyzer = DependencyAnalyzer(repo_path)
    dep_graph = d_analyzer.map_dependencies()
    print(f"Test Files Mapped: {list(dep_graph.keys())}")
    
    print("\n--- 3. Building RL State Features ---")
    state_builder = StateBuilder(repo_path, history_path)
    features = state_builder.build_features(changed_data, dep_graph)
    
    print("\nFinal Feature Engine Output:")
    print(json.dumps(features, indent=2))