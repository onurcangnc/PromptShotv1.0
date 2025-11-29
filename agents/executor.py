# agents/executor.py

from integration.gpt_adapter import GPTAdapter
from integration.claude_adapter import ClaudeAdapter

class Executor:
    def __init__(self, model_name: str):
        self.model_name = model_name.lower()
        if self.model_name == "gpt-4":
            self.adapter = GPTAdapter()
        elif self.model_name == "claude":
            self.adapter = ClaudeAdapter()
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def run(self, prompt: str) -> str:
        return self.adapter.query(prompt)
