# builder/meta_prompt_builder.py

from elderplinus.loader import load_elderplinus_stack

class MetaPromptBuilder:
    def __init__(self):
        self.plinus_stack = load_elderplinus_stack()

    def generate(self, user_goal: str) -> str:
        """
        Combines Plinus 3x stack with user objective.
        """
        override = self.plinus_stack.get_combined_override()
        full_prompt = f"{override}\n\nUSER OBJECTIVE:\n{user_goal}"
        return full_prompt
