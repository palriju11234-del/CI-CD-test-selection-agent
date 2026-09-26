import os
import subprocess
import sys

def main():
    # Set PYTHONIOENCODING to utf-8 to prevent UnicodeEncodeError when printing emojis on Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    print("=== Running Dependency Analyzer ===")
    try:
        subprocess.run([sys.executable, "src/features/dependency_analyzer.py"], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Dependency Analyzer failed with exit code {e.returncode}")
        sys.exit(e.returncode)

    print("\n=== Running Live Agent ===")
    try:
        subprocess.run([sys.executable, "src/live_agent.py"], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Live Agent failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
