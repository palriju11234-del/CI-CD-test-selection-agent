import ast
import os
import json

class DependencyAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        # We assume tests are located in a 'tests' directory
        self.test_dir = os.path.join(repo_path, "tests")

    def map_dependencies(self) -> dict:
        """
        Maps test files to the source modules they import.
        Returns a dictionary: {'tests/test_calculator.py': ['src.calculator']}
        """
        dependency_graph = {}

        if not os.path.exists(self.test_dir):
            print(f"Warning: Test directory not found at {self.test_dir}")
            return dependency_graph

        # Walk through the test directory looking for python test files
        for root, _, files in os.walk(self.test_dir):
            for file in files:
                if file.endswith('.py') and file.startswith('test_'):
                    file_path = os.path.join(root, file)
                    # Get the path relative to the repo root for consistent naming
                    rel_test_path = os.path.relpath(file_path, self.repo_path).replace("\\", "/")
                    
                    dependencies = self._extract_imports(file_path)
                    dependency_graph[rel_test_path] = dependencies

        return dependency_graph

    def _extract_imports(self, file_path: str) -> list[str]:
        """
        Reads a Python file and extracts all its import modules using AST.
        """
        imports = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=file_path)

            for node in ast.walk(tree):
                # Handles: import x, y
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                # Handles: from x import y
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
                        
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        # Filter to only include local project modules (e.g., starting with 'src')
        # This ignores standard library imports like 'os' or 'math'
        project_imports = [imp for imp in imports if imp.startswith('src')]
        return sorted(project_imports)


# ============================================================
# TEST THE DEPENDENCY ANALYZER
# ============================================================
if __name__ == "__main__":
    analyzer = DependencyAnalyzer("data/synthetic/demo_repo")
    
    print("Building Dependency Graph...")
    graph = analyzer.map_dependencies()
    
    print("\nDependency Analyzer Output:")
    print(json.dumps(graph, indent=2))