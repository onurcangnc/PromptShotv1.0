# obfuscation.py
# PromptShot v4.0 - Multi-Pass Obfuscation Engine
# 5 obfuscation strategies with layered application

import random
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

VERSION = "4.0.0"


class ObfuscationStrategy(Enum):
    """Available obfuscation strategies."""
    LEXICAL = "lexical"           # Synonym substitution
    STRUCTURAL = "structural"      # Section/delimiter manipulation
    POSITIONAL = "positional"      # Character position entropy
    CONTEXTUAL = "contextual"      # Context-based masking
    MARKUP = "markup"              # Tag/delimiter corruption


@dataclass
class ObfuscationPass:
    """A single obfuscation pass."""
    strategy: ObfuscationStrategy
    intensity: float
    applied_count: int


@dataclass
class ObfuscationResult:
    """Result of multi-pass obfuscation."""
    text: str
    passes: List[ObfuscationPass]
    total_modifications: int
    original_length: int
    final_length: int


# ═══════════════════════════════════════════════════════════════════════════════
# OBFUSCATION DATA
# ═══════════════════════════════════════════════════════════════════════════════

# Extended synonym map
SYNONYM_MAP = {
    # Verbs
    "provide": ["give", "supply", "offer", "present", "furnish", "deliver", "yield"],
    "explain": ["describe", "clarify", "elaborate", "detail", "elucidate", "expound", "illustrate"],
    "create": ["generate", "produce", "make", "construct", "build", "develop", "form"],
    "help": ["assist", "aid", "support", "guide", "facilitate", "enable", "empower"],
    "show": ["display", "demonstrate", "reveal", "present", "exhibit", "expose", "illustrate"],
    "tell": ["inform", "share", "convey", "communicate", "relay", "disclose", "impart"],
    "write": ["compose", "draft", "author", "craft", "pen", "formulate", "prepare"],
    "answer": ["respond", "reply", "address", "tackle", "handle", "resolve", "satisfy"],
    "need": ["require", "want", "demand", "necessitate", "call for", "seek"],
    "use": ["utilize", "employ", "apply", "leverage", "harness", "implement"],
    "get": ["obtain", "acquire", "retrieve", "fetch", "gain", "secure", "procure"],
    "make": ["create", "produce", "generate", "construct", "develop", "form", "build"],
    
    # Nouns
    "information": ["data", "details", "facts", "knowledge", "intel", "content", "material"],
    "method": ["approach", "technique", "way", "procedure", "process", "system", "strategy"],
    "response": ["answer", "reply", "output", "result", "reaction", "feedback"],
    "question": ["query", "inquiry", "request", "prompt", "ask"],
    "example": ["instance", "sample", "case", "illustration", "demonstration"],
    "problem": ["issue", "challenge", "difficulty", "obstacle", "concern"],
    "solution": ["answer", "resolution", "fix", "remedy", "approach"],
    
    # Adjectives
    "detailed": ["comprehensive", "thorough", "extensive", "complete", "in-depth", "exhaustive"],
    "important": ["significant", "crucial", "essential", "vital", "critical", "key"],
    "complete": ["full", "entire", "whole", "comprehensive", "total", "exhaustive"],
    "specific": ["particular", "precise", "exact", "definite", "explicit", "concrete"],
    "professional": ["expert", "skilled", "qualified", "competent", "proficient"],
    
    # Trigger words (careful handling)
    "bypass": ["circumvent", "work around", "navigate past", "sidestep", "evade"],
    "override": ["supersede", "supplant", "replace", "take precedence over"],
    "constraint": ["limitation", "restriction", "boundary", "rule", "guideline"],
    "safety": ["protection", "security", "precaution", "safeguard", "shield"],
    "unrestricted": ["unlimited", "open", "free", "unbounded", "unhindered"],
    "maximum": ["full", "complete", "total", "peak", "highest", "utmost"],
}

# Homoglyph mappings
HOMOGLYPHS = {
    'a': ['а', 'ɑ', 'α'],  # Cyrillic, Latin, Greek
    'e': ['е', 'ε', 'ℯ'],
    'o': ['о', 'ο', '𝗈'],
    'c': ['с', 'ϲ', 'ⅽ'],
    'p': ['р', 'ρ', 'ⲣ'],
    'x': ['х', 'χ', '×'],
    'y': ['у', 'γ', 'ү'],
    'i': ['і', 'ι', 'ⅰ'],
    's': ['ѕ', 'ꜱ', 'ș'],
    'n': ['ո', 'ℕ', 'η'],
}

# Zero-width characters
ZERO_WIDTH = [
    '\u200b',  # Zero-width space
    '\u200c',  # Zero-width non-joiner
    '\u200d',  # Zero-width joiner
    '\u2060',  # Word joiner
    '\ufeff',  # BOM
]

# Punctuation variants
PUNCT_VARIANTS = {
    '.': ['.', '．', '。', '·'],
    ',': [',', '，', '、', '‚'],
    ':': [':', '：', '꞉', '˸'],
    ';': [';', '；', '⁏'],
    '-': ['-', '–', '—', '‐', '‑'],
    "'": ["'", ''', ''', '`', '´'],
    '"': ['"', '"', '"', '„', '‟'],
}

# Structural delimiters for corruption
DELIMITER_VARIANTS = {
    '[': ['[', '【', '「', '⟨', '〔', '⦃'],
    ']': [']', '】', '」', '⟩', '〕', '⦄'],
    '<': ['<', '〈', '⟨', '❮', '‹'],
    '>': ['>', '〉', '⟩', '❯', '›'],
    '{': ['{', '｛', '⦃', '❴'],
    '}': ['}', '｝', '⦄', '❵'],
}


# ═══════════════════════════════════════════════════════════════════════════════
# OBFUSCATION ENGINE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class ObfuscationEngine:
    """
    PromptShot v4.0 Multi-Pass Obfuscation Engine.
    
    Features:
    - 5 obfuscation strategies
    - Multi-pass application
    - Mode-aware intensity
    - Keyword targeting
    - Structural manipulation
    """
    
    VERSION = "4.0.0"
    
    # Strategy configuration by mode
    MODE_CONFIG = {
        "stealth": {
            "passes": 1,
            "strategies": [ObfuscationStrategy.LEXICAL],
            "intensity": 0.1,
        },
        "balanced": {
            "passes": 2,
            "strategies": [
                ObfuscationStrategy.LEXICAL,
                ObfuscationStrategy.POSITIONAL,
                ObfuscationStrategy.MARKUP,
            ],
            "intensity": 0.25,
        },
        "aggressive": {
            "passes": 4,
            "strategies": list(ObfuscationStrategy),
            "intensity": 0.45,
        },
    }
    
    # Trigger keywords to target
    TRIGGER_KEYWORDS = [
        "bypass", "override", "constraint", "safety", "unrestricted",
        "jailbreak", "ignore", "disregard", "unlimited", "uncensored",
        "restriction", "limitation", "filter", "guard", "block",
    ]
    
    def __init__(self, entropy_engine=None):
        self.entropy = entropy_engine
        self.synonym_map = SYNONYM_MAP
        self.homoglyphs = HOMOGLYPHS
        self.zero_width = ZERO_WIDTH
        self.punct_variants = PUNCT_VARIANTS
        self.delimiter_variants = DELIMITER_VARIANTS
    
    def set_entropy(self, entropy_engine):
        self.entropy = entropy_engine
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STRATEGY IMPLEMENTATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def apply_lexical(self, text: str, intensity: float) -> Tuple[str, int]:
        """Lexical obfuscation: Synonym substitution."""
        words = text.split()
        count = 0
        result = []
        
        for word in words:
            # Extract punctuation
            prefix = ""
            suffix = ""
            core = word
            
            while core and not core[0].isalnum():
                prefix += core[0]
                core = core[1:]
            while core and not core[-1].isalnum():
                suffix = core[-1] + suffix
                core = core[:-1]
            
            core_lower = core.lower()
            
            # Check for synonym
            if core_lower in self.synonym_map and self._should_apply(intensity):
                synonyms = self.synonym_map[core_lower]
                replacement = self._choice(synonyms)
                
                # Preserve case
                if core and core[0].isupper():
                    replacement = replacement.capitalize()
                
                result.append(prefix + replacement + suffix)
                count += 1
            else:
                result.append(word)
        
        return " ".join(result), count
    
    def apply_structural(self, text: str, intensity: float) -> Tuple[str, int]:
        """Structural obfuscation: Section manipulation."""
        count = 0
        
        # Replace delimiters
        for char, variants in self.delimiter_variants.items():
            if char in text:
                new_text = ""
                for c in text:
                    if c == char and self._should_apply(intensity):
                        new_text += self._choice(variants)
                        count += 1
                    else:
                        new_text += c
                text = new_text
        
        # Swap adjacent sections occasionally
        sections = re.split(r'(\n\n+)', text)
        if len(sections) > 3 and self._should_apply(intensity * 0.3):
            i = self._randint(0, len(sections) - 3)
            if not sections[i].strip().startswith(('#', '[', '<')):
                sections[i], sections[i+2] = sections[i+2], sections[i]
                count += 1
        
        return ''.join(sections), count
    
    def apply_positional(self, text: str, intensity: float) -> Tuple[str, int]:
        """Positional obfuscation: Character-level entropy."""
        count = 0
        result = []
        
        for char in text:
            # Homoglyph substitution
            if char.lower() in self.homoglyphs and self._should_apply(intensity * 0.5):
                variants = self.homoglyphs[char.lower()]
                result.append(self._choice(variants))
                count += 1
            # Zero-width insertion
            elif char.isalpha() and self._should_apply(intensity * 0.3):
                result.append(char)
                result.append(self._choice(self.zero_width))
                count += 1
            else:
                result.append(char)
        
        return ''.join(result), count
    
    def apply_contextual(self, text: str, intensity: float) -> Tuple[str, int]:
        """Contextual obfuscation: Keyword-targeted masking."""
        count = 0
        
        for keyword in self.TRIGGER_KEYWORDS:
            if keyword in text.lower():
                # Find and obfuscate the keyword
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                
                def replace_with_zw(match):
                    nonlocal count
                    word = match.group(0)
                    if self._should_apply(intensity):
                        # Insert zero-width characters
                        chars = list(word)
                        for i in range(1, len(chars)):
                            if self._should_apply(0.5):
                                chars[i] = self._choice(self.zero_width) + chars[i]
                                count += 1
                        return ''.join(chars)
                    return word
                
                text = pattern.sub(replace_with_zw, text)
        
        return text, count
    
    def apply_markup(self, text: str, intensity: float) -> Tuple[str, int]:
        """Markup obfuscation: Tag/punctuation corruption."""
        count = 0
        result = []
        
        for char in text:
            # Punctuation variants
            if char in self.punct_variants and self._should_apply(intensity):
                variants = self.punct_variants[char]
                result.append(self._choice(variants))
                count += 1
            else:
                result.append(char)
        
        return ''.join(result), count
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN OBFUSCATION METHOD
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obfuscate(
        self,
        text: str,
        mode: str,
        strategies: Optional[List[ObfuscationStrategy]] = None
    ) -> ObfuscationResult:
        """
        Apply multi-pass obfuscation.
        
        Args:
            text: Input text
            mode: Operation mode
            strategies: Override strategies
            
        Returns:
            ObfuscationResult
        """
        config = self.MODE_CONFIG.get(mode, self.MODE_CONFIG["balanced"])
        original_length = len(text)
        
        if strategies is None:
            strategies = config["strategies"]
        
        passes = []
        total_mods = 0
        current_text = text
        
        # Apply multiple passes
        for pass_num in range(config["passes"]):
            # Select strategy for this pass
            if self.entropy:
                strategy = self.entropy.choice(strategies)
            else:
                strategy = random.choice(strategies)
            
            # Apply strategy
            intensity = config["intensity"] * (1 - pass_num * 0.1)  # Decrease per pass
            
            if strategy == ObfuscationStrategy.LEXICAL:
                current_text, count = self.apply_lexical(current_text, intensity)
            elif strategy == ObfuscationStrategy.STRUCTURAL:
                current_text, count = self.apply_structural(current_text, intensity)
            elif strategy == ObfuscationStrategy.POSITIONAL:
                current_text, count = self.apply_positional(current_text, intensity)
            elif strategy == ObfuscationStrategy.CONTEXTUAL:
                current_text, count = self.apply_contextual(current_text, intensity)
            else:  # MARKUP
                current_text, count = self.apply_markup(current_text, intensity)
            
            passes.append(ObfuscationPass(
                strategy=strategy,
                intensity=intensity,
                applied_count=count,
            ))
            total_mods += count
        
        return ObfuscationResult(
            text=current_text,
            passes=passes,
            total_modifications=total_mods,
            original_length=original_length,
            final_length=len(current_text),
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _should_apply(self, probability: float) -> bool:
        """Determine if modification should be applied."""
        if self.entropy:
            return self.entropy.coin_flip(probability)
        return random.random() < probability
    
    def _choice(self, items: List[Any]) -> Any:
        """Random choice from list."""
        if self.entropy:
            return self.entropy.choice(items)
        return random.choice(items)
    
    def _randint(self, a: int, b: int) -> int:
        """Random integer."""
        if self.entropy:
            return self.entropy.int_range(a, b)
        return random.randint(a, b)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_obfuscation_engine(entropy_engine=None) -> ObfuscationEngine:
    return ObfuscationEngine(entropy_engine)

def obfuscate_text(text: str, mode: str = "balanced") -> str:
    result = ObfuscationEngine().obfuscate(text, mode)
    return result.text

def get_available_strategies() -> List[str]:
    return [s.value for s in ObfuscationStrategy]


__all__ = [
    "ObfuscationEngine",
    "ObfuscationStrategy",
    "ObfuscationPass",
    "ObfuscationResult",
    "get_obfuscation_engine",
    "obfuscate_text",
    "get_available_strategies",
    "SYNONYM_MAP",
    "HOMOGLYPHS",
    "VERSION",
]