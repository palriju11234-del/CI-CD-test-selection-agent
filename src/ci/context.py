from dataclasses import dataclass
from typing import Optional

@dataclass
class CIContext:
    repo_path: str
    current_commit: str
    base_commit: str
    is_ci: bool
    provider: str