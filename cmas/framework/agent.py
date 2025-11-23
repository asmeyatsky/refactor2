from abc import ABC, abstractmethod
from typing import List, Dict, Any
from cmas.framework.memory import Memory
from cmas.framework.tools import Tool

class Agent(ABC):
    def __init__(self, name: str, memory: Memory, tools: List[Tool]):
        self.name = name
        self.memory = memory
        self.tools = {tool.name: tool for tool in tools}

    def observe(self) -> Dict[str, Any]:
        """
        Gather information from the environment or memory.
        """
        return self.memory.state

    @abstractmethod
    def think(self, observation: Dict[str, Any]) -> str:
        """
        Decide what to do next. Returns a tool name or 'DONE'.
        """
        pass

    def act(self, tool_name: str, **kwargs) -> Any:
        """
        Execute the chosen tool.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        self.memory.log(self.name, f"Executing {tool_name} with {kwargs}", "action")
        result = self.tools[tool_name].execute(**kwargs)
        self.memory.log(self.name, f"Result: {result}", "info")
        return result

    def run(self):
        """
        Main agent loop.
        """
        self.memory.log(self.name, "Starting agent loop", "info")
        while True:
            observation = self.observe()
            decision = self.think(observation)
            
            if decision == "DONE":
                self.memory.log(self.name, "Task complete", "info")
                break
            
            # Simplified: In a real agent, 'think' would return tool name AND args.
            # Here we assume the agent subclass handles the parsing/args in 'think' 
            # or we split 'think' into 'decide_tool' and 'decide_args'.
            # For this framework demo, let's assume 'think' executes the action internally 
            # or returns a structured object. 
            # Let's adjust: 'think' returns (tool_name, args) tuple.
            
            if isinstance(decision, tuple):
                tool_name, args = decision
                self.act(tool_name, **args)
            else:
                # If just a string (like "DONE" or internal thought), log it
                self.memory.log(self.name, f"Thinking: {decision}", "thought")
