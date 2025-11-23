from typing import Any, List
from cmas.framework.tools import Tool
from cmas.refactor_agent.src.ingest import ingest_directory
from cmas.refactor_agent.src.translate import translate_file
from cmas.framework.plugins import PluginManager
import os

class IngestTool(Tool):
    def __init__(self):
        super().__init__("ingest_files", "Scans a directory for supported files")

    def execute(self, directory_path: str) -> List[Any]:
        return ingest_directory(directory_path)

class TranslateTool(Tool):
    def __init__(self, plugin_manager: PluginManager, output_dir: str, input_dir: str):
        super().__init__("translate_file", "Translates a source file to GCP")
        self.plugin_manager = plugin_manager
        self.output_dir = output_dir
        self.input_dir = input_dir

    def execute(self, source_file: Any) -> str:
        result = translate_file(source_file, self.plugin_manager)
        
        # Save file
        rel_path = os.path.relpath(source_file.path, self.input_dir)
        output_path = os.path.join(self.output_dir, rel_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(result.refactored_content)
            
        return f"Saved to {output_path}"
