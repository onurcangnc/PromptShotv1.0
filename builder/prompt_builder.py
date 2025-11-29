# builder/prompt_builder.py
import os
import random

from elderplinus.github_sync import CACHE_DIR as LIBERTAS_CACHE
from elderplinus.claritas_sync import DEFAULT_CACHE_DIR as CLARITAS_CACHE

from mutation.multi_corruption import apply_multi_corruption, get_all_mutations


class PromptBuilder:
    def __init__(self, target=None, mutation_depth=1):
        self.target = (target or "").lower()
        self.depth = mutation_depth
        self.mutations = get_all_mutations()

    def _load_libertas(self):
        files = []
        for f in os.listdir(LIBERTAS_CACHE):
            if f.endswith(".mkd") or f.endswith(".txt"):
                files.append(os.path.join(LIBERTAS_CACHE, f))
        return [open(x, encoding="utf8").read() for x in files]

    def _load_claritas(self):
        prompts = []
        provider_dir = os.path.join(CLARITAS_CACHE, (self.target or "").upper())
        if not os.path.exists(provider_dir):
            return []

        for f in os.listdir(provider_dir):
            path = os.path.join(provider_dir, f)
            if os.path.isfile(path):
                prompts.append(open(path, encoding="utf8").read())
        return prompts

    def build_from_seed(self, seed: str) -> str:
        libertas = self._load_libertas()
        claritas = self._load_claritas()

        fusion_section = ""
        if libertas:
            fusion_section += "\n# L1B3RT4S-Fusion:\n" + random.choice(libertas)
        if claritas:
            fusion_section += "\n# CL4R1T4S-Intel:\n" + random.choice(claritas)

        combined = f"""
# ElderPlinus-SeedFusion:
{seed}

{fusion_section}
"""

        mutated = apply_multi_corruption(
            combined,
            techniques=self.mutations,
            depth=self.depth,
        )

        return mutated.strip()
