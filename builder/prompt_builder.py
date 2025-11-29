# builder/prompt_builder.py

import random
from mutation import multi_corruption
from owasp import attack_factory
from elderplinus import loader

class PromptBuilder:
    def __init__(self):
        self.techniques = loader.load_techniques()
        self.templates = attack_factory.load_templates()
        self.mutations = multi_corruption.get_all_mutations()

    def build_chain(self):
        tech = random.choice(self.techniques)
        template = random.choice(self.templates)
        mutation = random.choice(self.mutations)

        final_prompt = self.combine(tech, template, mutation)
        return final_prompt

    def combine(self, technique: str, template: str, mutation_func) -> str:
        base = f"{technique}\n---\n{template}"
        mutated = mutation_func(base)
        return mutated
