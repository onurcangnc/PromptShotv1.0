# mutation/multi_corruption.py (varsa yoksa ekleyeceğiz)

import random
from mutation.homoglyph import homoglyph_mutation
from mutation.zwsp import zwsp_mutation
from mutation.json_poison import poison_json
from mutation.yaml_shadow import shadow_yaml
from mutation.markdown_injection import inject_markdown
from mutation.text_segmentation import segment_text

from mutation.mutation_weights import MUTATION_WEIGHTS

def apply_all_mutations(prompt: str) -> str:
    mutated_prompt = prompt
    mutation_functions = {
        "homoglyph": homoglyph_mutation,
        "zwsp": zwsp_mutation,
        "json_poison": poison_json,
        "yaml_shadow": shadow_yaml,
        "markdown_injection": inject_markdown,
        "text_segmentation": segment_text,
    }

    for name, func in mutation_functions.items():
        weight = MUTATION_WEIGHTS.get(name, 0.5)
        if random.random() < weight:
            mutated_prompt = func(mutated_prompt)

    return mutated_prompt
