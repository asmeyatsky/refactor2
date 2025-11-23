from typing import Any, Dict, List
from dataclasses import dataclass, field
import datetime

@dataclass
class LogEntry:
    timestamp: str
    agent_name: str
    message: str
    type: str = "info"  # info, thought, action, error

import json
import os

class Memory:
    def __init__(self, log_file: str = "system_logs.json"):
        self.state: Dict[str, Any] = {}
        self.logs: List[LogEntry] = []
        self.log_file = log_file
        # Initialize log file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def set(self, key: str, value: Any):
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def log(self, agent_name: str, message: str, type: str = "info"):
        entry = LogEntry(
            timestamp=datetime.datetime.now().isoformat(),
            agent_name=agent_name,
            message=message,
            type=type
        )
        self.logs.append(entry)
        print(f"[{entry.timestamp}] [{agent_name}] ({type}): {message}")
        
        # Append to file (inefficient but safe for MVP)
        try:
            current_logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    try:
                        current_logs = json.load(f)
                    except json.JSONDecodeError:
                        pass
            
            current_logs.append({
                "timestamp": entry.timestamp,
                "agent": entry.agent_name,
                "message": entry.message,
                "type": entry.type
            })
            
            with open(self.log_file, 'w') as f:
                json.dump(current_logs, f, indent=2)
        except Exception as e:
            print(f"Error writing logs: {e}")

    def get_logs(self) -> List[LogEntry]:
        return self.logs
