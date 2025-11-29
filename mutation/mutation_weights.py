import random

# Use canonical mutation names as keys to avoid import-time circular references.
MUTATION_WEIGHTS = {
    "zwsp": 3,
    "homoglyph": 2,
    "markdown_injection": 1,
    "json_poison": 2,
    "yaml_shadow": 2,
}

def select_weighted_mutation():
    """Return a mutation function chosen using the configured weights.

    We import `mutation.multi_corruption` lazily inside the function to avoid
    circular imports at module-import time.
    """
    import mutation.multi_corruption as mc

    techniques = []
    weights = []
    for name, w in MUTATION_WEIGHTS.items():
        fn = mc.mutation_functions.get(name)
        if fn:
            techniques.append(fn)
            weights.append(w)

    if not techniques:
        raise RuntimeError("No mutation techniques available to choose from")

    return random.choices(techniques, weights=weights, k=1)[0]
