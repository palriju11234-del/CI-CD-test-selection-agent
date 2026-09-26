import subprocess
import sys
import json
from unittest.mock import patch

from web_api import PIPELINE_PATH, PROJECT_ROOT, launch_pipeline


def test_launch_pipeline_runs_pipeline_script_from_project_root():
    summary = {"total_tests": 1, "executed": 1, "passed": 1, "failed": 0, "tests": []}
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=f"QUBIS_PIPELINE_RESULT_JSON={json.dumps(summary)}\npipeline output",
        stderr="",
    )

    with patch("web_api.subprocess.run", return_value=completed) as run:
        status, payload = launch_pipeline()

    assert status == 200
    assert payload["success"] is True
    assert payload["summary"] == summary
    assert payload["stderr"] == ""
    run.assert_called_once()
    command = run.call_args.args[0]
    options = run.call_args.kwargs
    assert command == [sys.executable, str(PIPELINE_PATH)]
    assert PIPELINE_PATH.name == "run_pipeline.py"
    assert options["cwd"] == str(PROJECT_ROOT)
    assert options["check"] is False


def test_launch_pipeline_reports_failure_exit_code():
    summary = {"total_tests": 1, "executed": 1, "passed": 0, "failed": 1, "tests": []}
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=f"QUBIS_PIPELINE_RESULT_JSON={json.dumps(summary)}",
        stderr="",
    )

    with patch("web_api.subprocess.run", return_value=completed):
        status, payload = launch_pipeline()

    assert status == 500
    assert payload["returncode"] == 0
    assert payload["success"] is False
    assert payload["summary"]["failed"] == 1