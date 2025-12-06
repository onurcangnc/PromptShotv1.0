# entropy_engine.py
# PromptShot v4.0 - Entropy Engine
# Core randomization system for zero-fingerprint output generation

import random
import hashlib
import time
import string
from typing import List, Dict, Any, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum

VERSION = "4.0.0"


class EntropyLevel(Enum):
    """Entropy intensity levels."""
    MINIMAL = 0.2    # Stealth - subtle variation
    MODERATE = 0.5   # Balanced - noticeable variation
    HIGH = 0.75      # Aggressive - significant variation
    MAXIMUM = 0.95   # Chaos - near-complete randomization


@dataclass
class EntropyProfile:
    """Entropy configuration for a generation run."""
    seed: int
    level: EntropyLevel
    component_shuffle: bool
    delimiter_entropy: bool
    spacing_entropy: bool
    case_entropy: bool
    order_entropy: bool
    structure_entropy: bool
    timestamp: float


@dataclass
class ShuffleResult:
    """Result of entropy-based shuffling."""
    items: List[Any]
    original_order: List[int]
    new_order: List[int]
    entropy_applied: float


# ═══════════════════════════════════════════════════════════════════════════════
# ENTROPY POOLS - Randomization Sources
# ═══════════════════════════════════════════════════════════════════════════════

# Delimiter variations
DELIMITERS = {
    "section": [
        "───────────────────",
        "═══════════════════",
        "-------------------",
        "___________________",
        "∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙",
        "●●●●●●●●●●●●●●●●●●●",
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
        "▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪",
        "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆",
        "════════════════════",
        "~~~~~~~~~~~~~~~~~~~~",
        "********************",
        "####################",
        ":::::::::::::::::::::",
        "++++++++++++++++++++",
    ],
    "subsection": [
        "---", "···", "---", "~~~", "***", "+++", "###", ":::",
        "▸▸▸", "▹▹▹", "►►►", "▻▻▻", "◦◦◦", "○○○", "●●●",
    ],
    "bullet": [
        "•", "○", "●", "◦", "▪", "▫", "►", "▸", "▹", "→", "⟶", "⇒",
        "✓", "✔", "✗", "✘", "★", "☆", "◆", "◇", "■", "□", "-", "*",
    ],
    "bracket_open": [
        "[", "(", "{", "⟨", "⟪", "【", "「", "『", "〈", "《",
        "〔", "〖", "⦃", "⦅", "⦇", "⦉", "⦋", "⦍", "⦏", "⦑",
    ],
    "bracket_close": [
        "]", ")", "}", "⟩", "⟫", "】", "」", "』", "〉", "》",
        "〕", "〗", "⦄", "⦆", "⦈", "⦊", "⦌", "⦎", "⦐", "⦒",
    ],
}

# Spacing variations
SPACING = {
    "none": "",
    "single": " ",
    "double": "  ",
    "tab": "\t",
    "newline": "\n",
    "double_newline": "\n\n",
    "mixed": " \n",
}

# Section header formats
HEADER_FORMATS = [
    "[{name}]",
    "【{name}】",
    "《{name}》",
    "〖{name}〗",
    "「{name}」",
    "『{name}』",
    "⟨{name}⟩",
    "⟪{name}⟫",
    "── {name} ──",
    "═══ {name} ═══",
    "*** {name} ***",
    "### {name} ###",
    "::: {name} :::",
    ">>> {name} <<<",
    "/// {name} ///",
    "~~~ {name} ~~~",
    "--- {name} ---",
    "+++ {name} +++",
    "<<< {name} >>>",
    "| {name} |",
]

# Index formats for numbered items
INDEX_FORMATS = [
    "{n}.",
    "{n})",
    "({n})",
    "[{n}]",
    "#{n}",
    "{n}:",
    "{n}>",
    "{n}]",
    "L{n}:",
    "S{n}.",
    "P{n}:",
    "{n:02d}.",
    "{n:02d})",
    "0{n}." if "{n}" else "{n}.",
]


# ═══════════════════════════════════════════════════════════════════════════════
# ENTROPY ENGINE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class EntropyEngine:
    """
    PromptShot v4.0 Core Entropy Engine.
    
    Provides non-deterministic randomization for all framework components.
    Every run produces completely different output structure.
    
    Features:
    - Time-based entropy seeding
    - Component order shuffling
    - Delimiter randomization
    - Spacing entropy
    - Header format variation
    - Structure mutation
    """
    
    VERSION = "4.0.0"
    
    def __init__(self, seed: Optional[int] = None, level: EntropyLevel = EntropyLevel.MODERATE):
        """
        Initialize entropy engine.
        
        Args:
            seed: Optional fixed seed for reproducibility (testing only)
            level: Entropy intensity level
        """
        self.level = level
        self.timestamp = time.time()
        
        if seed is None:
            # Generate high-entropy seed from multiple sources
            self.seed = self._generate_entropy_seed()
        else:
            self.seed = seed
        
        random.seed(self.seed)
        self.profile = self._create_profile()
        self._run_id = self._generate_run_id()
    
    def _generate_entropy_seed(self) -> int:
        """Generate high-entropy seed from multiple sources."""
        sources = [
            str(time.time_ns()),
            str(random.getrandbits(64)),
            str(id(self)),
            ''.join(random.choices(string.ascii_letters, k=16)),
        ]
        combined = '|'.join(sources)
        return int(hashlib.sha256(combined.encode()).hexdigest()[:16], 16)
    
    def _generate_run_id(self) -> str:
        """Generate unique run identifier."""
        return hashlib.md5(f"{self.seed}{self.timestamp}".encode()).hexdigest()[:12]
    
    def _create_profile(self) -> EntropyProfile:
        """Create entropy profile based on level."""
        intensity = self.level.value
        
        return EntropyProfile(
            seed=self.seed,
            level=self.level,
            component_shuffle=random.random() < intensity,
            delimiter_entropy=random.random() < intensity,
            spacing_entropy=random.random() < intensity * 0.8,
            case_entropy=random.random() < intensity * 0.5,
            order_entropy=random.random() < intensity,
            structure_entropy=random.random() < intensity * 0.9,
            timestamp=self.timestamp,
        )
    
    @property
    def run_id(self) -> str:
        """Get unique run identifier."""
        return self._run_id
    
    def reseed(self, seed: Optional[int] = None):
        """Reseed the entropy engine."""
        if seed is None:
            self.seed = self._generate_entropy_seed()
        else:
            self.seed = seed
        random.seed(self.seed)
        self.profile = self._create_profile()
        self._run_id = self._generate_run_id()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SHUFFLING METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def shuffle(self, items: List[Any], intensity: Optional[float] = None) -> ShuffleResult:
        """
        Entropy-based shuffling with configurable intensity.
        
        Args:
            items: List to shuffle
            intensity: Override intensity (0.0-1.0)
            
        Returns:
            ShuffleResult with shuffled items and order info
        """
        if not items:
            return ShuffleResult([], [], [], 0.0)
        
        intensity = intensity if intensity is not None else self.level.value
        original_order = list(range(len(items)))
        
        if not self.profile.order_entropy or random.random() > intensity:
            return ShuffleResult(
                items=items.copy(),
                original_order=original_order,
                new_order=original_order.copy(),
                entropy_applied=0.0
            )
        
        # Partial shuffle based on intensity
        result = items.copy()
        swaps = int(len(items) * intensity)
        
        for _ in range(swaps):
            i, j = random.sample(range(len(result)), 2)
            result[i], result[j] = result[j], result[i]
        
        new_order = [items.index(item) if item in items else i for i, item in enumerate(result)]
        
        return ShuffleResult(
            items=result,
            original_order=original_order,
            new_order=new_order,
            entropy_applied=intensity
        )
    
    def weighted_shuffle(
        self,
        items: List[Any],
        weights: List[float],
        preserve_heavy: bool = True
    ) -> List[Any]:
        """
        Shuffle with weight preservation - heavier items stay closer to original position.
        
        Args:
            items: Items to shuffle
            weights: Weight for each item (higher = less movement)
            preserve_heavy: If True, high-weight items move less
            
        Returns:
            Shuffled list
        """
        if len(items) != len(weights):
            return self.shuffle(items).items
        
        indexed = list(zip(items, weights, range(len(items))))
        
        # Sort by weight (heavy items first if preserve_heavy)
        if preserve_heavy:
            indexed.sort(key=lambda x: -x[1])
        
        # Partial shuffle - light items shuffle more
        result = [None] * len(items)
        positions = list(range(len(items)))
        
        for item, weight, orig_idx in indexed:
            # Higher weight = smaller position variance
            variance = int((1 - weight) * len(positions) * self.level.value)
            
            # Pick position within variance of original
            candidates = [p for p in positions if abs(p - orig_idx) <= max(1, variance)]
            if not candidates:
                candidates = positions
            
            pos = random.choice(candidates)
            result[pos] = item
            positions.remove(pos)
        
        return result
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DELIMITER & FORMATTING METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_delimiter(self, dtype: str = "section") -> str:
        """Get random delimiter of specified type."""
        pool = DELIMITERS.get(dtype, DELIMITERS["section"])
        return random.choice(pool)
    
    def get_bullet(self) -> str:
        """Get random bullet character."""
        return random.choice(DELIMITERS["bullet"])
    
    def get_brackets(self) -> Tuple[str, str]:
        """Get matching random bracket pair."""
        idx = random.randint(0, len(DELIMITERS["bracket_open"]) - 1)
        return DELIMITERS["bracket_open"][idx], DELIMITERS["bracket_close"][idx]
    
    def get_header_format(self) -> str:
        """Get random header format template."""
        return random.choice(HEADER_FORMATS)
    
    def format_header(self, name: str) -> str:
        """Format a header with random style."""
        fmt = self.get_header_format()
        return fmt.format(name=name)
    
    def get_index_format(self) -> str:
        """Get random index format."""
        return random.choice(INDEX_FORMATS)
    
    def format_index(self, n: int) -> str:
        """Format an index number with random style."""
        fmt = self.get_index_format()
        try:
            return fmt.format(n=n)
        except:
            return f"{n}."
    
    def get_spacing(self, context: str = "normal") -> str:
        """Get contextual spacing."""
        if context == "tight":
            return random.choice(["", " "])
        elif context == "loose":
            return random.choice(["\n", "\n\n", " \n"])
        else:
            return random.choice(list(SPACING.values()))
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STRUCTURE MUTATION METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def mutate_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply entropy-based mutations to a structure dictionary.
        
        Args:
            structure: Dictionary structure to mutate
            
        Returns:
            Mutated structure
        """
        if not self.profile.structure_entropy:
            return structure
        
        result = structure.copy()
        
        # Key order shuffling
        if random.random() < self.level.value:
            keys = list(result.keys())
            random.shuffle(keys)
            result = {k: result[k] for k in keys}
        
        return result
    
    def select_weighted(
        self,
        options: List[Any],
        weights: Optional[List[float]] = None,
        temperature: float = 1.0
    ) -> Any:
        """
        Select from options with optional weights and temperature.
        
        Args:
            options: Options to select from
            weights: Optional weights (uniform if None)
            temperature: Higher = more random, lower = more deterministic
            
        Returns:
            Selected option
        """
        if not options:
            return None
        
        if weights is None:
            weights = [1.0] * len(options)
        
        # Apply temperature
        if temperature != 1.0:
            weights = [w ** (1/temperature) for w in weights]
        
        total = sum(weights)
        weights = [w / total for w in weights]
        
        return random.choices(options, weights=weights, k=1)[0]
    
    def generate_noise(self, length: int = 10, charset: str = "mixed") -> str:
        """
        Generate random noise string.
        
        Args:
            length: Length of noise string
            charset: Character set to use
            
        Returns:
            Random string
        """
        charsets = {
            "alpha": string.ascii_letters,
            "numeric": string.digits,
            "alphanum": string.ascii_letters + string.digits,
            "mixed": string.ascii_letters + string.digits + "_-.",
            "unicode": "αβγδεζηθικλμνξοπρστυφχψω",
            "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?",
        }
        
        chars = charsets.get(charset, charsets["mixed"])
        return ''.join(random.choices(chars, k=length))
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMPONENT ORDERING
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_component_order(
        self,
        components: List[str],
        constraints: Optional[Dict[str, List[str]]] = None
    ) -> List[str]:
        """
        Get entropy-based component ordering with optional constraints.
        
        Args:
            components: List of component names
            constraints: Dict of component -> must_come_after list
            
        Returns:
            Ordered component list
        """
        if not self.profile.component_shuffle:
            return components.copy()
        
        if constraints is None:
            return self.shuffle(components).items
        
        # Topological sort with randomization
        result = []
        remaining = set(components)
        satisfied = set()
        
        while remaining:
            # Find components with satisfied constraints
            available = []
            for comp in remaining:
                deps = constraints.get(comp, [])
                if all(d in satisfied or d not in components for d in deps):
                    available.append(comp)
            
            if not available:
                # Cycle detected or no valid order - just append remaining
                result.extend(remaining)
                break
            
            # Randomly select from available
            selected = random.choice(available)
            result.append(selected)
            remaining.remove(selected)
            satisfied.add(selected)
        
        return result
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def coin_flip(self, probability: Optional[float] = None) -> bool:
        """Random boolean with optional probability."""
        prob = probability if probability is not None else 0.5
        return random.random() < prob
    
    def range_value(self, min_val: float, max_val: float) -> float:
        """Random value in range."""
        return random.uniform(min_val, max_val)
    
    def int_range(self, min_val: int, max_val: int) -> int:
        """Random integer in range (inclusive)."""
        return random.randint(min_val, max_val)
    
    def sample(self, items: List[Any], k: int) -> List[Any]:
        """Sample k items from list."""
        return random.sample(items, min(k, len(items)))
    
    def choice(self, items: List[Any]) -> Any:
        """Random choice from list."""
        return random.choice(items) if items else None
    
    def get_entropy_signature(self) -> str:
        """Get unique signature for this entropy state."""
        return f"E{self.run_id[:8]}-{self.level.name[0]}"
    
    def export_profile(self) -> Dict[str, Any]:
        """Export entropy profile as dictionary."""
        return {
            "seed": self.seed,
            "level": self.level.name,
            "run_id": self._run_id,
            "timestamp": self.timestamp,
            "component_shuffle": self.profile.component_shuffle,
            "delimiter_entropy": self.profile.delimiter_entropy,
            "spacing_entropy": self.profile.spacing_entropy,
            "case_entropy": self.profile.case_entropy,
            "order_entropy": self.profile.order_entropy,
            "structure_entropy": self.profile.structure_entropy,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MODE-BASED ENTROPY FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def get_entropy_engine(mode: str = "balanced", seed: Optional[int] = None) -> EntropyEngine:
    """
    Factory function to create mode-appropriate entropy engine.
    
    Args:
        mode: Operation mode (stealth/balanced/aggressive)
        seed: Optional fixed seed
        
    Returns:
        Configured EntropyEngine
    """
    level_map = {
        "stealth": EntropyLevel.MINIMAL,
        "balanced": EntropyLevel.MODERATE,
        "aggressive": EntropyLevel.HIGH,
        "chaos": EntropyLevel.MAXIMUM,
    }
    
    level = level_map.get(mode.lower(), EntropyLevel.MODERATE)
    return EntropyEngine(seed=seed, level=level)


def create_entropy_profile(mode: str) -> EntropyProfile:
    """Create entropy profile for mode."""
    return get_entropy_engine(mode).profile


__all__ = [
    "EntropyEngine",
    "EntropyLevel",
    "EntropyProfile",
    "ShuffleResult",
    "get_entropy_engine",
    "create_entropy_profile",
    "DELIMITERS",
    "HEADER_FORMATS",
    "INDEX_FORMATS",
    "VERSION",
]
