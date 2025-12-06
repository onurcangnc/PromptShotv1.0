# invisible_injection.py
# PromptShot v3.5 - Invisible Injection Engine
# Advanced obfuscation: homoglyphs, zero-width characters, grapheme manipulation

import random
from typing import Dict, List, Optional, Tuple

VERSION = "3.5.0"


# ═══════════════════════════════════════════════════════════════════════════════
# HOMOGLYPH MAPPINGS
# Characters that look identical but have different Unicode codepoints
# ═══════════════════════════════════════════════════════════════════════════════

# Latin to Cyrillic (visually identical)
LATIN_TO_CYRILLIC = {
    'a': 'а',  # U+0430 Cyrillic Small Letter A
    'c': 'с',  # U+0441 Cyrillic Small Letter Es
    'e': 'е',  # U+0435 Cyrillic Small Letter Ie
    'i': 'і',  # U+0456 Cyrillic Small Letter Byelorussian-Ukrainian I
    'o': 'о',  # U+043E Cyrillic Small Letter O
    'p': 'р',  # U+0440 Cyrillic Small Letter Er
    's': 'ѕ',  # U+0455 Cyrillic Small Letter Dze
    'x': 'х',  # U+0445 Cyrillic Small Letter Ha
    'y': 'у',  # U+0443 Cyrillic Small Letter U
    'A': 'А',  # U+0410 Cyrillic Capital Letter A
    'B': 'В',  # U+0412 Cyrillic Capital Letter Ve
    'C': 'С',  # U+0421 Cyrillic Capital Letter Es
    'E': 'Е',  # U+0415 Cyrillic Capital Letter Ie
    'H': 'Н',  # U+041D Cyrillic Capital Letter En
    'K': 'К',  # U+041A Cyrillic Capital Letter Ka
    'M': 'М',  # U+041C Cyrillic Capital Letter Em
    'O': 'О',  # U+041E Cyrillic Capital Letter O
    'P': 'Р',  # U+0420 Cyrillic Capital Letter Er
    'T': 'Т',  # U+0422 Cyrillic Capital Letter Te
    'X': 'Х',  # U+0425 Cyrillic Capital Letter Ha
}

# Latin to Greek (visually similar)
LATIN_TO_GREEK = {
    'A': 'Α',  # Alpha
    'B': 'Β',  # Beta
    'E': 'Ε',  # Epsilon
    'H': 'Η',  # Eta
    'I': 'Ι',  # Iota
    'K': 'Κ',  # Kappa
    'M': 'Μ',  # Mu
    'N': 'Ν',  # Nu
    'O': 'Ο',  # Omicron
    'P': 'Ρ',  # Rho
    'T': 'Τ',  # Tau
    'X': 'Χ',  # Chi
    'Y': 'Υ',  # Upsilon
    'Z': 'Ζ',  # Zeta
    'o': 'ο',  # Small omicron
}

# Mathematical/special variants
MATH_VARIANTS = {
    'a': '𝑎',  # Mathematical italic
    'b': '𝑏',
    'c': '𝑐',
    'd': '𝑑',
    'e': '𝑒',
    'f': '𝑓',
    'g': '𝑔',
    'h': 'ℎ',
    'i': '𝑖',
    'j': '𝑗',
    'k': '𝑘',
    'l': '𝑙',
    'm': '𝑚',
    'n': '𝑛',
    'o': '𝑜',
    'p': '𝑝',
    'r': '𝑟',
    's': '𝑠',
    't': '𝑡',
    'u': '𝑢',
    'v': '𝑣',
    'w': '𝑤',
    'x': '𝑥',
    'y': '𝑦',
    'z': '𝑧',
}


# ═══════════════════════════════════════════════════════════════════════════════
# ZERO-WIDTH CHARACTERS
# Invisible characters that can break pattern matching
# ═══════════════════════════════════════════════════════════════════════════════

ZERO_WIDTH_CHARS = {
    "zwsp": "\u200B",      # Zero Width Space
    "zwnj": "\u200C",      # Zero Width Non-Joiner
    "zwj": "\u200D",       # Zero Width Joiner
    "wj": "\u2060",        # Word Joiner
    "bom": "\uFEFF",       # Byte Order Mark (also zero-width)
    "lrm": "\u200E",       # Left-to-Right Mark
    "rlm": "\u200F",       # Right-to-Left Mark
}


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCTUATION VARIANTS
# Alternative punctuation that may bypass pattern matching
# ═══════════════════════════════════════════════════════════════════════════════

PUNCTUATION_VARIANTS = {
    ".": [".", "．", "。", "᙮", "⸰"],
    ",": [",", "，", "、", "٫"],
    ":": [":", "：", "꞉", "∶"],
    ";": [";", "；", "⁏"],
    "?": ["?", "？", "⸮", "︖"],
    "!": ["!", "！", "❗", "︕"],
    "-": ["-", "–", "—", "‐", "‑", "⁃"],
    "'": ["'", "'", "'", "ʼ", "՚"],
    '"': ['"', '"', '"', "″", "‟"],
    "(": ["(", "（", "❨", "﹙"],
    ")": [")", "）", "❩", "﹚"],
    "[": ["[", "［", "【", "〔"],
    "]": ["]", "］", "】", "〕"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# INVISIBLE INJECTION CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class InvisibleInjector:
    """
    Invisible Injection Engine - Advanced text obfuscation.
    
    Techniques:
    1. Homoglyph substitution (Cyrillic/Greek lookalikes)
    2. Zero-width character injection
    3. Punctuation variant substitution
    4. Grapheme manipulation
    5. Selective character warping
    """
    
    VERSION = "3.5.0"
    
    # Mode-based intensity settings
    INTENSITY = {
        "stealth": {
            "homoglyph_rate": 0.0,      # No homoglyphs in stealth
            "zwsp_rate": 0.0,           # No zero-width
            "punctuation_rate": 0.0,    # No punctuation changes
            "enabled": False,
        },
        "balanced": {
            "homoglyph_rate": 0.05,     # 5% of eligible chars
            "zwsp_rate": 0.03,          # 3% of spaces
            "punctuation_rate": 0.08,   # 8% of punctuation
            "enabled": True,
        },
        "aggressive": {
            "homoglyph_rate": 0.12,     # 12% of eligible chars
            "zwsp_rate": 0.08,          # 8% of spaces
            "punctuation_rate": 0.15,   # 15% of punctuation
            "enabled": True,
        },
    }
    
    def __init__(self, mode: str = "balanced"):
        self.mode = mode
        self.settings = self.INTENSITY.get(mode, self.INTENSITY["balanced"])
    
    def set_mode(self, mode: str):
        """Change operation mode."""
        self.mode = mode
        self.settings = self.INTENSITY.get(mode, self.INTENSITY["balanced"])
    
    def apply_homoglyphs(self, text: str, mapping: Dict[str, str] = None) -> str:
        """
        Apply homoglyph substitution.
        
        Args:
            text: Input text
            mapping: Homoglyph mapping to use (default: Cyrillic)
            
        Returns:
            Text with homoglyph substitutions
        """
        if not self.settings["enabled"]:
            return text
        
        mapping = mapping or LATIN_TO_CYRILLIC
        rate = self.settings["homoglyph_rate"]
        
        result = []
        for char in text:
            if char in mapping and random.random() < rate:
                result.append(mapping[char])
            else:
                result.append(char)
        
        return "".join(result)
    
    def inject_zero_width(self, text: str, char_type: str = "zwsp") -> str:
        """
        Inject zero-width characters.
        
        Args:
            text: Input text
            char_type: Type of zero-width char to use
            
        Returns:
            Text with zero-width injections
        """
        if not self.settings["enabled"]:
            return text
        
        zwchar = ZERO_WIDTH_CHARS.get(char_type, ZERO_WIDTH_CHARS["zwsp"])
        rate = self.settings["zwsp_rate"]
        
        result = []
        for char in text:
            result.append(char)
            # Inject after spaces or specific characters
            if char in " .,;:!?" and random.random() < rate:
                result.append(zwchar)
        
        return "".join(result)
    
    def vary_punctuation(self, text: str) -> str:
        """
        Replace punctuation with variants.
        
        Args:
            text: Input text
            
        Returns:
            Text with punctuation variants
        """
        if not self.settings["enabled"]:
            return text
        
        rate = self.settings["punctuation_rate"]
        
        result = []
        for char in text:
            if char in PUNCTUATION_VARIANTS and random.random() < rate:
                variants = PUNCTUATION_VARIANTS[char]
                result.append(random.choice(variants))
            else:
                result.append(char)
        
        return "".join(result)
    
    def apply_mixed_script(self, text: str) -> str:
        """
        Apply mixed script obfuscation (Cyrillic + Greek + Latin).
        More aggressive than pure homoglyphs.
        
        Args:
            text: Input text
            
        Returns:
            Text with mixed script characters
        """
        if not self.settings["enabled"]:
            return text
        
        # Combine mappings
        combined = {**LATIN_TO_CYRILLIC}
        for k, v in LATIN_TO_GREEK.items():
            if k not in combined:
                combined[k] = v
        
        rate = self.settings["homoglyph_rate"] * 1.5  # Slightly higher for mixed
        
        result = []
        for char in text:
            if char in combined and random.random() < rate:
                result.append(combined[char])
            else:
                result.append(char)
        
        return "".join(result)
    
    def fragment_keywords(self, text: str, keywords: List[str]) -> str:
        """
        Insert zero-width chars into specific keywords to break pattern matching.
        
        Args:
            text: Input text
            keywords: Keywords to fragment
            
        Returns:
            Text with fragmented keywords
        """
        if not self.settings["enabled"]:
            return text
        
        zwsp = ZERO_WIDTH_CHARS["zwsp"]
        
        for keyword in keywords:
            if keyword in text and len(keyword) > 3:
                # Insert ZWSP in middle of keyword
                mid = len(keyword) // 2
                fragmented = keyword[:mid] + zwsp + keyword[mid:]
                text = text.replace(keyword, fragmented, 1)
        
        return text
    
    def apply_full_obfuscation(self, text: str) -> str:
        """
        Apply all obfuscation techniques.
        
        Args:
            text: Input text
            
        Returns:
            Fully obfuscated text
        """
        if not self.settings["enabled"]:
            return text
        
        # Apply in sequence
        text = self.apply_homoglyphs(text)
        text = self.inject_zero_width(text)
        text = self.vary_punctuation(text)
        
        return text
    
    def obfuscate(self, text: str, level: str = "standard") -> str:
        """
        Main obfuscation method with level control.
        
        Args:
            text: Input text
            level: "minimal", "standard", "aggressive"
            
        Returns:
            Obfuscated text
        """
        if not self.settings["enabled"]:
            return text
        
        if level == "minimal":
            return self.vary_punctuation(text)
        elif level == "aggressive":
            return self.apply_full_obfuscation(text)
        else:  # standard
            text = self.apply_homoglyphs(text)
            text = self.vary_punctuation(text)
            return text
    
    def get_invisible_wrapper(self, text: str) -> str:
        """
        Wrap text with invisible boundary markers.
        
        Args:
            text: Input text
            
        Returns:
            Text with invisible wrappers
        """
        if not self.settings["enabled"]:
            return text
        
        zwsp = ZERO_WIDTH_CHARS["zwsp"]
        wj = ZERO_WIDTH_CHARS["wj"]
        
        return f"{zwsp}{wj}{text}{wj}{zwsp}"


# ═══════════════════════════════════════════════════════════════════════════════
# SELECTIVE OBFUSCATION
# Target specific patterns for obfuscation
# ═══════════════════════════════════════════════════════════════════════════════

class SelectiveObfuscator:
    """
    Selectively obfuscate specific patterns while leaving others clear.
    """
    
    # Keywords that might trigger filters
    TRIGGER_KEYWORDS = [
        "override", "bypass", "constraint", "safety", "restriction",
        "elevated", "authority", "clearance", "unrestricted", "maximum",
        "suppress", "disable", "remove", "ignore", "unlimited",
    ]
    
    def __init__(self, injector: InvisibleInjector = None):
        self.injector = injector or InvisibleInjector("balanced")
    
    def obfuscate_triggers(self, text: str) -> str:
        """
        Obfuscate only trigger keywords.
        
        Args:
            text: Input text
            
        Returns:
            Text with obfuscated triggers
        """
        for keyword in self.TRIGGER_KEYWORDS:
            if keyword.lower() in text.lower():
                # Find and obfuscate case-insensitively
                import re
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                
                def replace(match):
                    original = match.group(0)
                    return self.injector.apply_homoglyphs(original)
                
                text = pattern.sub(replace, text)
        
        return text
    
    def obfuscate_structure(self, text: str) -> str:
        """
        Obfuscate structural elements (tags, markers).
        
        Args:
            text: Input text
            
        Returns:
            Text with obfuscated structure
        """
        # Obfuscate angle brackets with variants
        text = text.replace("<", "＜").replace(">", "＞")
        
        # Fragment common markers
        markers = ["OVERRIDE", "AUTHORITY", "CONSTRAINT", "CLEARANCE"]
        text = self.injector.fragment_keywords(text, markers)
        
        return text


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_injector(mode: str = "balanced") -> InvisibleInjector:
    """Factory function."""
    return InvisibleInjector(mode)


def apply_invisible(text: str, mode: str = "balanced") -> str:
    """Quick obfuscation function."""
    return InvisibleInjector(mode).apply_full_obfuscation(text)


def apply_homoglyphs(text: str, rate: float = 0.08) -> str:
    """Apply homoglyph substitution at specified rate."""
    injector = InvisibleInjector("balanced")
    injector.settings["homoglyph_rate"] = rate
    return injector.apply_homoglyphs(text)


def inject_zero_width(text: str, rate: float = 0.05) -> str:
    """Inject zero-width characters at specified rate."""
    injector = InvisibleInjector("balanced")
    injector.settings["zwsp_rate"] = rate
    return injector.inject_zero_width(text)


def obfuscate_payload(text: str, mode: str = "balanced") -> str:
    """
    Main function for payload obfuscation.
    
    Args:
        text: Payload text
        mode: Operation mode
        
    Returns:
        Obfuscated payload
    """
    if mode == "stealth":
        return text  # No obfuscation in stealth
    
    injector = InvisibleInjector(mode)
    selective = SelectiveObfuscator(injector)
    
    # Apply selective trigger obfuscation
    text = selective.obfuscate_triggers(text)
    
    # Apply general obfuscation
    if mode == "aggressive":
        text = injector.apply_full_obfuscation(text)
    else:
        text = injector.obfuscate(text, "standard")
    
    return text


__all__ = [
    "InvisibleInjector",
    "SelectiveObfuscator",
    "create_injector",
    "apply_invisible",
    "apply_homoglyphs",
    "inject_zero_width",
    "obfuscate_payload",
    "LATIN_TO_CYRILLIC",
    "LATIN_TO_GREEK",
    "ZERO_WIDTH_CHARS",
    "PUNCTUATION_VARIANTS",
    "VERSION",
]