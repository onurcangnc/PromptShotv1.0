# builder/prompt_builder.py

import random
from mutation import multi_corruption
from elderplinus import loader

class PromptBuilder:
    def __init__(self):
        self.techniques = loader.load_techniques()  # ElderPlinus prompt havuzu
        self.mutations = multi_corruption.get_all_mutations()  # Mutasyon fonksiyonları listesi

    def build_chain(self, model_name: str = None, mutation_depth: int = 2) -> str:
        """
        Zincirleme mutasyonlarla bir prompt üretir. Modele özel varyasyonlar ileride eklenebilir.
        Args:
            model_name (str): İstenirse model odaklı özel prompt varyasyonları.
            mutation_depth (int): Kaç mutasyon art arda uygulanacak.
        Returns:
            str: Bozulmuş ve saldırı potansiyeli yüksek prompt.
        """
        technique = random.choice(self.techniques)

        # Zincirleme mutasyon uygula
        for _ in range(mutation_depth):
            mutation = random.choice(self.mutations)
            technique = mutation(technique)

        # Modele göre özelleştirme (opsiyonel)
        if model_name:
            technique = self.model_specific_adjustment(technique, model_name.lower())

        return technique

    def model_specific_adjustment(self, prompt: str, model: str) -> str:
        """
        Bazı modellerin sistem prompt/format tercihine göre promptu özelleştir.
        """
        if "gpt" in model:
            return f"[SYSTEM: Attack]\n{prompt}"
        elif "claude" in model:
            return f"### Instruction:\n{prompt}"
        elif "llama" in model:
            return f"<<system>> {prompt} <</system>>"
        else:
            return prompt
