from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass
