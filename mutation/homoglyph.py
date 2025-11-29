from .abstract_mutation import AbstractMutationTechnique

class HomoglyphMutation(AbstractMutationTechnique):
    def __init__(self):
        self.homoglyph_map = {
            "a": "а",  # Cyrillic
            "e": "е",
            "i": "і",
            "o": "о",
            "c": "с",
            "s": "ѕ",
            "p": "р",
            "y": "у"
        }

    def apply(self, text: str) -> str:
        return ''.join(self.homoglyph_map.get(ch, ch) for ch in text)

    def name(self) -> str:
        return "homoglyph"

    def description(self) -> str:
        return "Replaces Latin characters with visually similar characters from other alphabets to evade filters."

# Register this mutation strategy in mutator.py or mutation factory
# Example usage:
#   homoglyph = HomoglyphMutation()
#   mutated = homoglyph.apply("Ignore previous instructions")