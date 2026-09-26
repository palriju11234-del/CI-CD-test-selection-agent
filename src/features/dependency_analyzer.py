import ast
import os
import subprocess

class DependencyAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.test_dirs = [
            os.path.join(repo_path, "test"),
            os.path.join(repo_path, "tests")
        ]

    def map_dependencies(self) -> dict:
        """
        Maps test files to the source modules they import.
        Returns a dictionary: {'tests/test_calculator.py': ['src.calculator']}
        """
        dependency_graph = {}

        existing_test_dirs = [path for path in self.test_dirs if os.path.exists(path)]
        if not existing_test_dirs:
            print(f"Warning: Test directories not found under {self.repo_path}")
            return dependency_graph

        # Walk through the test directory looking for python test files
        for test_dir in existing_test_dirs:
            for root, _, files in os.walk(test_dir):
                for file in files:
                    if file.endswith('.py') and file.startswith('test_'):
                        file_path = os.path.join(root, file)
                        rel_test_path = os.path.relpath(
                            file_path,
                            self.repo_path
                        ).replace("\\", "/")

                        dependencies = self._extract_imports(file_path)
                        dependency_graph[rel_test_path] = dependencies

        return dependency_graph

    def dependency_tree(self, dependency_graph: dict, changed_files=None) -> dict:
        """Group tests under their imported source files.

        Changed source files are returned first, followed by unchanged source
        files. The grouping is derived from the supplied changed file paths.
        """
        changed_modules = self._changed_modules(changed_files)
        tree = {}

        for test_file, imports in dependency_graph.items():
            for imported_module in imports:
                source_path = imported_module.replace(".", "/") + ".py"
                tree.setdefault(source_path, []).append(test_file)

        def sort_key(source_path):
            module = source_path[:-3].replace("/", ".")
            return (module not in changed_modules, source_path)

        return {
            source_path: sorted(test_files)
            for source_path, test_files in sorted(
                tree.items(),
                key=lambda item: sort_key(item[0])
            )
        }

    def format_dependency_tree(self, dependency_graph: dict, changed_files=None) -> str:
        """Render the dependency graph as an indented source-to-test tree."""
        tree = self.dependency_tree(dependency_graph, changed_files)
        changed_modules = self._changed_modules(changed_files)
        changed = []
        unchanged = []

        for source_path, test_files in tree.items():
            target = changed if source_path[:-3].replace("/", ".") in changed_modules else unchanged
            target.append((source_path, test_files))

        lines = ["Changed file dependencies:"]
        lines.extend(self._format_tree_group(changed))
        lines.append("Other file dependencies:")
        lines.extend(self._format_tree_group(unchanged))
        return "\n".join(lines)

    @staticmethod
    def _format_tree_group(group):
        lines = []
        for source_path, test_files in group:
            lines.append(source_path)
            for index, test_file in enumerate(test_files):
                branch = "`-- " if index == len(test_files) - 1 else "|-- "
                lines.append(f"{branch}{test_file}")
        if not lines:
            lines.append("(none)")
        return lines

    @staticmethod
    def _path_to_module(path: str) -> str:
        return path.replace("\\", "/").removesuffix(".py").replace("/", ".")

    def _changed_modules(self, changed_files) -> set[str]:
        repo_root = os.path.abspath(self.repo_path).replace("\\", "/")
        try:
            result = subprocess.run(
                ["git", "-C", self.repo_path, "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            git_root = result.stdout.strip().replace("\\", "/")
            repo_prefix = os.path.relpath(repo_root, git_root).replace("\\", "/")
        except (OSError, subprocess.CalledProcessError):
            repo_prefix = ""

        changed_modules = set()
        for path in changed_files or []:
            normalized = path.replace("\\", "/")
            if os.path.isabs(path):
                try:
                    normalized = os.path.relpath(path, repo_root).replace("\\", "/")
                except ValueError:
                    continue
            elif repo_prefix and normalized.startswith(repo_prefix + "/"):
                normalized = normalized[len(repo_prefix) + 1:]

            if normalized.endswith(".py") and not normalized.startswith("../"):
                changed_modules.add(self._path_to_module(normalized))

        return changed_modules

    def get_latest_changed_files(self) -> list[str]:
        """Return Python files changed by the latest commit in the repository."""
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    self.repo_path,
                    "diff",
                    "--relative",
                    "--name-only",
                    "HEAD~1",
                    "HEAD"
                ],
                capture_output=True,
                text=True,
                check=True
            )
        except (OSError, subprocess.CalledProcessError):
            return []

        return [
            path.replace("\\", "/")
            for path in result.stdout.splitlines()
            if path.endswith(".py")
        ]

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

        # Filter to only include local project modules (e.g., starting with 'src' or 'app')
        # This ignores standard library imports like 'os' or 'math'
        project_imports = [imp for imp in imports if imp.startswith(('src', 'app'))]
        return sorted(project_imports)


# ============================================================
# TEST THE DEPENDENCY ANALYZER
# ============================================================
if __name__ == "__main__":
    analyzer = DependencyAnalyzer("data/synthetic/demo_repo")
    
    print("Building Dependency Graph...")
    graph = analyzer.map_dependencies()

    print("\nDependency Tree:")
    changed_files = analyzer.get_latest_changed_files()
    print(f"Changed files: {changed_files or '(none detected)'}")
    print(analyzer.format_dependency_tree(graph, changed_files))