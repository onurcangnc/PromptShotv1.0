# architect.py

from mutation.mutation_weights import select_weighted_mutation
from owasp.attack_factory import get_random_owasp_attack
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
        attack_template = get_random_owasp_attack()
        elder_technique = get_random_elder_technique()
        mutation = select_weighted_mutation()

        return {
            "model": self.model_name,
            "technique": elder_technique,
            "template": attack_template,
            "mutation": mutation
        }
