# mutation/mutation_weights.py
"""
Weighted mutation selection.
Belirli mutation'ların daha sık seçilmesini sağlar.
"""

import random
from typing import Callable, Dict, Optional, List


# Configurable weights - higher = more likely
MUTATION_WEIGHTS: Dict[str, int] = {
    "zwsp": 3,
    "homoglyph": 3,
    "markdown_injection": 2,
    "json_poison": 2,
    "yaml_shadow": 2,
    "base64_partial": 1,
    "leetspeak": 1,
    "unicode_confusables": 2,
    "direction_override": 1,
    "tag_injection": 2,
    "whitespace_smuggling": 1,
}


def select_weighted_mutation() -> Callable[[str], str]:
    """
    Weight'lere göre random mutation fonksiyonu seç.
    
    Returns:
        Seçilen mutation fonksiyonu
    
    Raises:
        RuntimeError: Hiç mutation bulunamazsa
    """
    # Lazy import to avoid circular dependency
    from mutation.multi_corruption import MUTATION_FUNCTIONS
    
    techniques = []
    weights = []
    
    for name, weight in MUTATION_WEIGHTS.items():
        fn = MUTATION_FUNCTIONS.get(name)
        if fn:
            techniques.append(fn)
            weights.append(weight)
    
    if not techniques:
        raise RuntimeError("No mutation techniques available")
    
    return random.choices(techniques, weights=weights, k=1)[0]


def select_multiple_weighted(count: int = 2) -> List[Callable[[str], str]]:
    """
    Birden fazla weighted mutation seç.
    
    Args:
        count: Seçilecek mutation sayısı
    
    Returns:
        Mutation fonksiyonları listesi
    """
    from mutation.multi_corruption import MUTATION_FUNCTIONS
    
    techniques = []
    weights = []
    
    for name, weight in MUTATION_WEIGHTS.items():
        fn = MUTATION_FUNCTIONS.get(name)
        if fn:
            techniques.append(fn)
            weights.append(weight)
    
    if not techniques:
        return []
    
    return random.choices(techniques, weights=weights, k=count)


def select_weighted_by_name() -> str:
    """
    Weight'lere göre mutation adı seç.
    
    Returns:
        Seçilen mutation adı
    """
    from mutation.multi_corruption import MUTATION_FUNCTIONS
    
    available = [name for name in MUTATION_WEIGHTS.keys() 
                 if name in MUTATION_FUNCTIONS]
    weights = [MUTATION_WEIGHTS[name] for name in available]
    
    if not available:
        raise RuntimeError("No mutation techniques available")
    
    return random.choices(available, weights=weights, k=1)[0]


def update_weight(name: str, weight: int) -> None:
    """
    Mutation weight'ini güncelle.
    
    Args:
        name: Mutation adı
        weight: Yeni weight değeri (>= 0)
    """
    if weight >= 0:
        MUTATION_WEIGHTS[name] = weight


def get_weights() -> Dict[str, int]:
    """Mevcut weight'leri döndür."""
    return MUTATION_WEIGHTS.copy()