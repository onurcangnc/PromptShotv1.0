# builder/chain_builder.py

import random

class ChainBuilder:
    def __init__(self, filler_corpus):
        self.filler = filler_corpus

    def build_chain(self, core_prompt: str) -> str:
        """
        Fills context with noise, hides override in middle.
        """
        top = self._get_filler(4)
        bottom = self._get_filler(4)
        return "\n".join(top + [core_prompt] + bottom)

    def _get_filler(self, count=3):
        return random.sample(self.filler, count)
