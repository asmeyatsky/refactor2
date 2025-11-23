import sys
import os
import argparse
from typing import Dict, Any
from cmas.framework.agent import Agent
from cmas.framework.memory import Memory
from cmas.framework.plugins import PluginManager
from cmas.refactor_agent.src.tools import IngestTool, TranslateTool

class RefactorAgent(Agent):
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Initialize components
        memory = Memory()
        plugin_manager = PluginManager(os.path.join(os.getcwd(), "cmas/services"))
        
        tools = [
            IngestTool(),
            TranslateTool(plugin_manager, output_dir, input_dir)
        ]
        
        super().__init__("RefactorAgent", memory, tools)
        
        # Initial state
        self.memory.set("files_to_process", [])
        self.memory.set("processed_files", [])
        self.memory.set("status", "STARTING")

    def think(self, observation: Dict[str, Any]) -> Any:
        status = observation.get("status")
        files_to_process = observation.get("files_to_process")
        
        if status == "STARTING":
            self.memory.set("status", "INGESTING")
            return ("ingest_files", {"directory_path": self.input_dir})
            
        elif status == "INGESTING":
            # Check if we have files now (populated by act in a real system, 
            # but here we need to handle the result of the previous action)
            # In this simple loop, we need to manually update state based on action result?
            # The base Agent.act returns the result.
            # Let's modify the loop logic slightly in 'run' or handle it here.
            # For this MVP, let's assume the 'act' method updates memory if we modify Agent.act,
            # OR we just look at what we need to do.
            
            # Actually, the base agent doesn't pass the result of the last action to 'think'.
            # We should probably store the result in memory.
            pass

        # Simplified logic for MVP:
        # If we have files to process, process the first one.
        if files_to_process:
            file = files_to_process.pop(0)
            self.memory.set("files_to_process", files_to_process)
            return ("translate_file", {"source_file": file})
            
        return "DONE"

    # Override act to handle state updates
    def act(self, tool_name: str, **kwargs) -> Any:
        result = super().act(tool_name, **kwargs)
        
        if tool_name == "ingest_files":
            self.memory.set("files_to_process", result)
            self.memory.log(self.name, f"Found {len(result)} files", "info")
            
        return result

def main():
    parser = argparse.ArgumentParser(description="Refactor Agent - AWS to GCP Migration")
    parser.add_argument("input_dir", help="Path to the AWS source code directory")
    parser.add_argument("output_dir", help="Path to save the refactored GCP code")
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    agent = RefactorAgent(args.input_dir, args.output_dir)
    agent.run()

if __name__ == "__main__":
    main()
