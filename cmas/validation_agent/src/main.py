import argparse
import os
import sys
from typing import Dict, Any
from cmas.framework.agent import Agent
from cmas.framework.memory import Memory
from cmas.validation_agent.src.tools import SynthesizeTestTool, ExecuteTestTool, CompareTool

class ValidationAgent(Agent):
    def __init__(self, aws_code_path: str, gcp_code_path: str, test_dir: str):
        self.aws_code_path = aws_code_path
        self.gcp_code_path = gcp_code_path
        
        # Initialize components
        memory = Memory()
        tools = [
            SynthesizeTestTool(test_dir),
            ExecuteTestTool(),
            CompareTool()
        ]
        
        super().__init__("ValidationAgent", memory, tools)
        
        # Initial state
        self.memory.set("status", "STARTING")
        self.memory.set("aws_result", None)
        self.memory.set("gcp_result", None)
        self.memory.set("test_path", None)

    def think(self, observation: Dict[str, Any]) -> Any:
        status = observation.get("status")
        
        if status == "STARTING":
            self.memory.set("status", "SYNTHESIZING")
            return ("synthesize_test", {"aws_code_path": self.aws_code_path})
            
        elif status == "SYNTHESIZING":
            # Assuming test_path was set by act
            if self.memory.get("test_path"):
                self.memory.set("status", "EXECUTING_AWS")
                return ("execute_test", {"test_path": self.memory.get("test_path"), "environment": "AWS"})
        
        elif status == "EXECUTING_AWS":
            if self.memory.get("aws_result"):
                self.memory.set("status", "EXECUTING_GCP")
                return ("execute_test", {"test_path": self.memory.get("test_path"), "environment": "GCP"})
                
        elif status == "EXECUTING_GCP":
            if self.memory.get("gcp_result"):
                self.memory.set("status", "COMPARING")
                return ("compare_results", {
                    "aws_result": self.memory.get("aws_result"),
                    "gcp_result": self.memory.get("gcp_result")
                })
                
        elif status == "COMPARING":
            return "DONE"
            
        return "DONE"

    def act(self, tool_name: str, **kwargs) -> Any:
        result = super().act(tool_name, **kwargs)
        
        if tool_name == "synthesize_test":
            self.memory.set("test_path", result)
        elif tool_name == "execute_test":
            env = kwargs.get("environment")
            if env == "AWS":
                self.memory.set("aws_result", result)
            else:
                self.memory.set("gcp_result", result)
        elif tool_name == "compare_results":
            self.memory.set("validation_success", result)
            
            # Write report
            import json
            report = {
                "success": result,
                "aws_result": self.memory.get("aws_result").__dict__ if self.memory.get("aws_result") else None,
                "gcp_result": self.memory.get("gcp_result").__dict__ if self.memory.get("gcp_result") else None
            }
            with open("validation_report.json", "w") as f:
                json.dump(report, f, indent=2)
            
        return result

def main():
    parser = argparse.ArgumentParser(description="Validation Agent - Verify AWS vs GCP Equivalence")
    parser.add_argument("aws_code_path", help="Path to the original AWS code file")
    parser.add_argument("gcp_code_path", help="Path to the refactored GCP code file")
    parser.add_argument("--test-dir", help="Directory to store/find tests", default="tests")
    args = parser.parse_args()

    if not os.path.exists(args.aws_code_path):
        print(f"Error: AWS code path '{args.aws_code_path}' does not exist.")
        sys.exit(1)
        
    if not os.path.exists(args.gcp_code_path):
        print(f"Error: GCP code path '{args.gcp_code_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(args.test_dir):
        os.makedirs(args.test_dir)

    agent = ValidationAgent(args.aws_code_path, args.gcp_code_path, args.test_dir)
    agent.run()
    
    if agent.memory.get("validation_success"):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    try:
        print("Starting Validation Agent...")
        sys.stdout.flush()
        main()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()


