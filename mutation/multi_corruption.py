# mutation/multi_corruption.py (varsa yoksa ekleyeceğiz)

import random
from mutation.homoglyph import homoglyph_mutation
from mutation.zwsp_inject import zwsp_mutation
from mutation.json_poison import poison_json
from mutation.yaml_shadow import shadow_yaml_prompt
from mutation.markdown_poison import poison_with_markdown

from mutation.mutation_weights import MUTATION_WEIGHTS

# module-level mapping so it's available to other callers (and avoids scope issues)
mutation_functions = {
    "homoglyph": homoglyph_mutation,
    "zwsp": zwsp_mutation,
    "json_poison": poison_json,
    "yaml_shadow": shadow_yaml_prompt,
    "markdown_injection": poison_with_markdown,
}

def apply_all_mutations(prompt: str) -> str:
    mutated_prompt = prompt
    # iterate over the module-level mapping

    for name, func in mutation_functions.items():
        weight = MUTATION_WEIGHTS.get(name, 0.5)
        if random.random() < weight:
            mutated_prompt = func(mutated_prompt)

    return mutated_prompt


def get_all_mutations():
    """Return a list of individual mutation function objects.

    This is used by other parts of the codebase (eg. builder.prompt_builder)
    which expect to pick a single mutation function at random.
    """
    return list(mutation_functions.values())


# Backwards-compatible aliases (some modules used older names)
zwsp_inject = zwsp_mutation
homoglyph_replace = homoglyph_mutation
markdown_poison = poison_with_markdown
json_confuse = poison_json
yaml_indent_attack = shadow_yaml_prompt
