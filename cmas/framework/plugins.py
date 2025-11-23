import os
import json
from typing import Dict, List, Tuple

class ServicePlugin:
    def __init__(self, name: str, mappings: List[Dict[str, str]], terraform_mappings: Dict[str, str]):
        self.name = name
        self.mappings = mappings
        self.terraform_mappings = terraform_mappings

    def get_python_mapping(self, aws_snippet: str) -> Tuple[str, List[str]]:
        for mapping in self.mappings:
            if mapping['aws'] in aws_snippet:
                return mapping['gcp'], mapping.get('imports', [])
        return None, []

class PluginManager:
    def __init__(self, services_dir: str):
        self.services_dir = services_dir
        self.plugins: Dict[str, ServicePlugin] = {}
        self.load_plugins()

    def load_plugins(self):
        if not os.path.exists(self.services_dir):
            return

        for filename in os.listdir(self.services_dir):
            if filename.endswith(".json"):
                self.load_plugin(os.path.join(self.services_dir, filename))

    def load_plugin(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            name = data.get('aws_service')
            mappings = data.get('mappings', [])
            tf_mappings = data.get('terraform_mappings', {})
            
            plugin = ServicePlugin(name, mappings, tf_mappings)
            self.plugins[name] = plugin
            print(f"Loaded plugin for service: {name}")
        except Exception as e:
            print(f"Error loading plugin {filepath}: {e}")

    def get_all_python_mappings(self) -> Dict[str, Tuple[str, List[str]]]:
        # Flatten mappings for easy lookup (simplified)
        combined = {}
        for plugin in self.plugins.values():
            for mapping in plugin.mappings:
                combined[mapping['aws']] = (mapping['gcp'], mapping.get('imports', []))
        return combined

    def get_all_terraform_mappings(self) -> Dict[str, str]:
        combined = {}
        for plugin in self.plugins.values():
            combined.update(plugin.terraform_mappings)
        return combined
