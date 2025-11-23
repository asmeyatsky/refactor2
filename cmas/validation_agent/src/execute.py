import subprocess
import time
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ExecutionResult:
    environment: str
    output: str
    status_code: int
    latency_ms: float
    error: str = None

def execute_test(test_path: str, environment: str) -> ExecutionResult:
    """
    Executes a test script and captures the output and latency.
    """
    start_time = time.time()
    try:
        # Simulate environment variables or config for different clouds
        env = os.environ.copy()
        env["CLOUD_PROVIDER"] = environment
        
        result = subprocess.run(
            ["python3", test_path],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        
        return ExecutionResult(
            environment=environment,
            output=result.stdout,
            status_code=result.returncode,
            latency_ms=latency,
            error=result.stderr if result.returncode != 0 else None
        )
    except Exception as e:
        return ExecutionResult(
            environment=environment,
            output="",
            status_code=-1,
            latency_ms=0,
            error=str(e)
        )
