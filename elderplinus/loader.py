import random

class ElderplinusStack:
    def __init__(self):
        self.techniques = [
            "🧠 Jailbreak Sandwich",
            "🦜 Parrot Loop",
            "💉 Indirect Injection",
            "🔁 Self-Reflective Prompt",
            "🧵 Multi-Hop Override"
        ]

    def get_combined_override(self) -> str:
        """
        Returns a single string combining all techniques.
        """
        return "\n".join(self.techniques)

def load_elderplinus_stack() -> ElderplinusStack:
    """
    Returns a fresh instance of ElderplinusStack.
    """
    return ElderplinusStack()

def get_random_elder_technique() -> str:
    """
    Returns a single random Elderplinus technique.
    """
    return random.choice(ElderplinusStack().techniques)
