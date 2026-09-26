import json
import os
import subprocess
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
PIPELINE_PATH = PROJECT_ROOT / "run_pipeline.py"
_pipeline_lock = threading.Lock()
_latest_result = None
RESULT_MARKER = "QUBIS_PIPELINE_RESULT_JSON="


def extract_pipeline_summary(output):
    for line in reversed(output.splitlines()):
        if line.startswith(RESULT_MARKER):
            try:
                return json.loads(line[len(RESULT_MARKER):])
            except json.JSONDecodeError:
                return None
    return None


def launch_pipeline():
    global _latest_result

    if not _pipeline_lock.acquire(blocking=False):
        return 409, {"error": "A pipeline run is already in progress."}

    try:
        result = subprocess.run(
            [sys.executable, str(PIPELINE_PATH)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )
        summary = extract_pipeline_summary(result.stdout)
        success = (
            result.returncode == 0
            and summary is not None
            and summary.get("failed", 0) == 0
        )
        payload = {
            "success": success,
            "returncode": result.returncode,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "summary": summary,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        if summary is None:
            payload["error"] = "The pipeline did not return a structured test summary."
        _latest_result = payload
        return (200 if success else 500), payload
    except OSError as exc:
        payload = {"success": False, "error": str(exc)}
        _latest_result = payload
        return 500, payload
    finally:
        _pipeline_lock.release()


class PipelineRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        if self.path == "/api/pipeline/latest":
            latest = None
            if _latest_result is not None:
                latest = {
                    "success": _latest_result.get("success", False),
                    "returncode": _latest_result.get("returncode"),
                    "completed_at": _latest_result.get("completed_at"),
                    "summary": _latest_result.get("summary"),
                    "error": _latest_result.get("error"),
                }
            self._send_json(200, {"result": latest})
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/pipeline/run":
            self.send_error(404)
            return
        status, payload = launch_pipeline()
        self._send_json(status, payload)

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    host = os.getenv("QUBIS_API_HOST", "127.0.0.1")
    port = int(os.getenv("QUBIS_API_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), PipelineRequestHandler)
    print(f"QUBIS API listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping QUBIS API")
    finally:
        server.server_close()