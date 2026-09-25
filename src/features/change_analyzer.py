import ast
import os
import json

from git import Repo


class ChangeAnalyzer:

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def get_diff_info(self, old_commit_hash: str, new_commit_hash: str) -> dict:
        """
        Compare two commits and return:
        - changed Python files
        - changed line numbers
        - affected functions/classes
        """

        old_commit = self.repo.commit(old_commit_hash)
        new_commit = self.repo.commit(new_commit_hash)

        # Get the differences between the two commits
        diffs = old_commit.diff(
            new_commit,
            create_patch=True
        )

        changed_data = {}

        for diff in diffs:

            # Get the file path
            file_path = diff.b_path if diff.b_path else diff.a_path

            # Ignore files that we don't need
            if not file_path:
                continue

            if not file_path.endswith(".py"):
                continue

            if "__pycache__" in file_path:
                continue

            # Only process files that actually have a diff
            if not diff.diff:
                continue

            # Convert diff from bytes to string
            try:
                patch = diff.diff.decode(
                    "utf-8",
                    errors="replace"
                )
            except Exception as e:
                print(
                    f"Warning: Could not decode diff for {file_path}: {e}"
                )
                continue

            # Find changed lines
            changed_lines = self._parse_patch_lines(patch)

            changed_data[file_path] = {
                "lines": changed_lines,
                "functions": []
            }

            # Find affected functions/classes
            if changed_lines:

                try:
                    # Read the file from the NEW commit
                    file_blob = new_commit.tree / file_path

                    file_content = (
                        file_blob.data_stream
                        .read()
                        .decode("utf-8")
                    )

                    functions = self._get_changed_functions(
                        file_content,
                        changed_lines
                    )

                    changed_data[file_path]["functions"] = functions

                except Exception as e:
                    print(
                        f"Warning: Could not parse "
                        f"{file_path}: {e}"
                    )

        return changed_data

    def _parse_patch_lines(self, patch: str) -> list[int]:
        """
        Extract line numbers from the NEW version
        of the file that were added/modified.
        """

        changed_lines = []

        current_line = 0

        for line in patch.splitlines():

            # Example:
            # @@ -3,7 +3,7 @@
            if line.startswith("@@"):

                try:
                    # Find the + part
                    plus_part = line.split("+")[1]

                    # Get something like:
                    # 3,7
                    line_info = plus_part.split(" ")[0]

                    # Get starting line number
                    current_line = int(
                        line_info.split(",")[0]
                    )

                except (IndexError, ValueError):
                    continue

            # Added line
            elif line.startswith("+") and not line.startswith("+++"):

                changed_lines.append(current_line)

                current_line += 1

            # Removed line
            elif line.startswith("-") and not line.startswith("---"):

                # Removed lines don't exist in the NEW file,
                # so we don't add them.
                continue

            # Normal unchanged line
            elif not line.startswith("\\"):

                current_line += 1

        return changed_lines

    def _get_changed_functions(
        self,
        file_content: str,
        changed_lines: list[int]
    ) -> list[str]:
        """
        Find functions/classes that contain changed lines.
        """

        changed_functions = set()

        try:

            tree = ast.parse(file_content)

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef
                    )
                ):

                    # Check whether any changed line
                    # falls inside this function/class
                    if hasattr(node, "end_lineno"):

                        for line in changed_lines:

                            if node.lineno <= line <= node.end_lineno:

                                changed_functions.add(
                                    node.name
                                )

                                break

        except SyntaxError:
            print("Warning: Could not parse Python file.")

        return sorted(changed_functions)


# ============================================================
# TEST THE CHANGE ANALYZER
# ============================================================

if __name__ == "__main__":

    analyzer = ChangeAnalyzer(
        "data/synthetic/demo_repo"
    )

    # Get commits from newest to oldest
    commits = list(
        analyzer.repo.iter_commits()
    )

    print("Commits found:")

    for commit in commits:
        print(
            commit.hexsha,
            commit.message.strip()
        )

    if len(commits) >= 2:

        # Newest commit
        new_commit = commits[0].hexsha

        # Previous commit
        old_commit = commits[1].hexsha

        print("\nOld commit:")
        print(old_commit)

        print("\nNew commit:")
        print(new_commit)

        # Run analyzer
        info = analyzer.get_diff_info(
            old_commit,
            new_commit
        )

        print("\nChange Analyzer Output:")

        print(
            json.dumps(
                info,
                indent=2
            )
        )

    else:

        print(
            "Not enough commits to compare!"
        )