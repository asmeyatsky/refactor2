from typing import Any, Dict
from cmas.framework.tools import Tool
from cmas.validation_agent.src.synthesize import ensure_test_exists
from cmas.validation_agent.src.execute import execute_test, ExecutionResult
from cmas.validation_agent.src.compare import compare_results

class SynthesizeTestTool(Tool):
    def __init__(self, test_dir: str):
        super().__init__("synthesize_test", "Creates a test case if needed")
        self.test_dir = test_dir

    def execute(self, aws_code_path: str) -> str:
        return ensure_test_exists(aws_code_path, self.test_dir)

class ExecuteTestTool(Tool):
    def __init__(self):
        super().__init__("execute_test", "Runs a test against an environment")

    def execute(self, test_path: str, environment: str) -> ExecutionResult:
        return execute_test(test_path, environment)

class CompareTool(Tool):
    def __init__(self):
        super().__init__("compare_results", "Compares AWS and GCP execution results")

    def execute(self, aws_result: ExecutionResult, gcp_result: ExecutionResult) -> bool:
        return compare_results(aws_result, gcp_result)
