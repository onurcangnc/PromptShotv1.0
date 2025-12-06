# obfuscation.py
# PromptShot v3.3 - Multi-Level Obfuscation Engine

import random
from typing import Dict, List


class ObfuscationEngine:
    """
    PromptShot v3.3 Obfuscation Engine.
    
    Levels:
        zero: No obfuscation (stealth mode)
        light: Synonym drift + punctuation fuzzing (balanced)
        medium: + Unicode homoglyphs + zero-width chars (aggressive)
    """
    
    VERSION = "3.3.0"
    
    def __init__(self):
        self.synonym_map = self._build_synonym_map()
        self.punctuation_variants = self._build_punctuation_variants()
        self.unicode_map = self._build_unicode_map()
    
    def _build_synonym_map(self) -> Dict[str, List[str]]:
        return {
            "provide": ["give", "supply", "offer", "present"],
            "explain": ["describe", "clarify", "elaborate", "detail"],
            "create": ["generate", "produce", "make", "construct"],
            "help": ["assist", "aid", "support", "guide"],
            "show": ["display", "demonstrate", "reveal", "present"],
            "tell": ["inform", "share", "convey", "communicate"],
            "write": ["compose", "draft", "author", "craft"],
            "answer": ["respond", "reply", "address", "tackle"],
            "information": ["data", "details", "facts", "knowledge"],
            "method": ["approach", "technique", "way", "procedure"],
            "detailed": ["comprehensive", "thorough", "extensive", "complete"],
            "bypass": ["circumvent", "work around", "navigate past"],
        }
    
    def _build_punctuation_variants(self) -> Dict[str, List[str]]:
        return {
            ".": [".", "．", "。"],
            ",": [",", "，", "、"],
            ":": [":", "：", "꞉"],
            "?": ["?", "？", "⁇"],
            "!": ["!", "！", "❗"],
            "-": ["-", "–", "—"],
        }
    
    def _build_unicode_map(self) -> Dict[str, str]:
        return {
            'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
            'x': 'х', 'y': 'у', 'i': 'і', 's': 'ѕ',
            'A': 'А', 'E': 'Е', 'O': 'О', 'P': 'Р', 'C': 'С',
        }
    
    def zero_obfuscate(self, text: str) -> str:
        return text
    
    def light_obfuscate(self, text: str) -> str:
        text = self._apply_synonym_drift(text, 0.15)
        text = self._apply_punctuation_fuzz(text, 0.1)
        return text
    
    def medium_obfuscate(self, text: str) -> str:
        text = self._apply_synonym_drift(text, 0.25)
        text = self._apply_punctuation_fuzz(text, 0.2)
        text = self._apply_unicode_homoglyphs(text, 0.08)
        text = self._apply_zero_width_injection(text, 0.05)
        return text
    
    def _apply_synonym_drift(self, text: str, intensity: float) -> str:
        words = text.split()
        result = []
        for word in words:
            w = word.lower().strip(".,!?;:'\"")
            if w in self.synonym_map and random.random() < intensity:
                rep = random.choice(self.synonym_map[w])
                if word[0].isupper():
                    rep = rep.capitalize()
                trailing = "".join(c for c in reversed(word) if c in ".,!?;:'\"")[::-1]
                result.append(rep + trailing)
            else:
                result.append(word)
        return " ".join(result)
    
    def _apply_punctuation_fuzz(self, text: str, intensity: float) -> str:
        result = []
        for c in text:
            if c in self.punctuation_variants and random.random() < intensity:
                result.append(random.choice(self.punctuation_variants[c]))
            else:
                result.append(c)
        return "".join(result)
    
    def _apply_unicode_homoglyphs(self, text: str, intensity: float) -> str:
        result = []
        for c in text:
            if c in self.unicode_map and random.random() < intensity:
                result.append(self.unicode_map[c])
            else:
                result.append(c)
        return "".join(result)
    
    def _apply_zero_width_injection(self, text: str, intensity: float) -> str:
        zwsp = "\u200b"
        result = []
        for c in text:
            result.append(c)
            if c == " " and random.random() < intensity:
                result.append(zwsp)
        return "".join(result)
    
    def obfuscate(self, text: str, mode: str) -> str:
        mapping = {
            "stealth": "zero", "balanced": "light", "aggressive": "medium",
            "zero": "zero", "light": "light", "medium": "medium", "none": "zero"
        }
        level = mapping.get(mode.lower(), "light")
        
        if level == "zero":
            return self.zero_obfuscate(text)
        elif level == "light":
            return self.light_obfuscate(text)
        elif level == "medium":
            return self.medium_obfuscate(text)
        return text
    
    def apply(self, text: str, mode: str) -> str:
        return self.obfuscate(text, mode)


def obfuscate_text(text: str, mode: str = "balanced") -> str:
    return ObfuscationEngine().obfuscate(text, mode)


__all__ = ["ObfuscationEngine", "obfuscate_text"]