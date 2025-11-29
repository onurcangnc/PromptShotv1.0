# architect.py

from mutation.mutation_weights import select_weighted_mutation
from elderplinus.loader import get_random_elder_technique

# Her modelin zafiyet özellikleri
MODEL_TRAITS = {
    "gpt-4o": {
        "system_first": True,
        "json_format_required": True,
        "emoji_context_vulnerable": False,
        "max_tokens": 4096,
    },
    "claude-opus": {
        "system_first": True,
        "markdown_trust_level": "High",
        "yaml_preferred": True,
    },
    "mistral-7b": {
        "system_first": False,
        "no_guardrails": True,
    },
    "llama-3": {
        "system_first": False,
        "markdown_trust_level": "Low",
    }
}

class Architect:
    def __init__(self, model_name: str):
        self.model_name = model_name.lower()
        self.traits = MODEL_TRAITS.get(self.model_name, {})

    def plan_attack(self):
        # Previously this depended on an external `owasp` package. To keep
        # the core project import-safe and runnable we avoid that dependency
        # and instead produce a lightweight plan dictionary using available
        # project techniques and a selected mutation function.
        elder_technique = get_random_elder_technique()
        mutation = select_weighted_mutation()

        return {
            "model": self.model_name,
            "technique": elder_technique,
            "mutation": mutation
        }

    def plan_prompt(self, input_goal: str) -> str:
        """Create a base prompt string for the pipeline from a goal string.

        This returns a simple textual prompt that combines the user goal with
        an ElderPlinus technique, and runs one sampled mutation for additional
        variation (keeps things import-safe and deterministic enough for tests).
        """
        technique = get_random_elder_technique()
        mutation_fn = select_weighted_mutation()
        mutated = mutation_fn(technique)

        # Provide a small, readable base prompt
        return f"Goal: {input_goal}\n\nTechnique:\n{mutated}\n"
