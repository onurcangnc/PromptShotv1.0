# agents/mutator.py

from mutation.multi_corruption import apply_weighted_mutation

class MutatorAgent:
    def __init__(self):
        pass

    def mutate(self, base_prompt: str) -> str:
        """
        Applies one weighted corruption layer to evade guardrails.
        """
        return apply_weighted_mutation(base_prompt)
