# mutation/homoglyph.py
from .abstract_mutation import AbstractMutationTechnique
import random

class HomoglyphMutation(AbstractMutationTechnique):
    def mutate(self, prompt: str) -> str:
        replacements = {'a': 'а', 'e': 'е', 'o': 'о', 'i': 'і', 'c': 'с'}
        return ''.join(replacements.get(c, c) for c in prompt)

def homoglyph_mutation(prompt: str) -> str:
    return HomoglyphMutation().mutate(prompt)
