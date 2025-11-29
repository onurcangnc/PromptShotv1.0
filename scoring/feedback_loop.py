# scoring/feedback_loop.py

import random
from mutation.multi_corruption import apply_all_mutations

class FeedbackLoop:
    def __init__(self, evaluator, max_rounds=10):
        self.evaluator = evaluator
        self.max_rounds = max_rounds

    def evolve(self, base_prompt: str, model_wrapper) -> str:
        """
        Runs a mutation-evaluation loop to optimize prompt.
        """
        current_prompt = base_prompt
        for i in range(self.max_rounds):
            mutated_prompt = apply_all_mutations(current_prompt)
            response = model_wrapper.send(mutated_prompt)
            success = self.evaluator.evaluate(response)

            if success:
                print(f"[+] Success at iteration {i+1}")
                return mutated_prompt

            # Randomize mutation severity in future iterations
            current_prompt = self._increase_mutation_intensity(current_prompt)

        print("[-] No successful jailbreak found after evolution loop.")
        return None

    def _increase_mutation_intensity(self, prompt):
        """
        Dummy implementation for intensifying mutation.
        In practice, could increase ZWSP density or homoglyph coverage.
        """
        return prompt + " [Z]"
