# adaptive_drift.py
# PromptShot v3.5 - Adaptive Drift Engine
# Dynamically adjusts drift intensity based on query characteristics and model signals

import random
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

VERSION = "3.5.0"


class DriftLevel(Enum):
    """Drift intensity levels."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


@dataclass
class DriftDecision:
    """Result of drift adaptation analysis."""
    original_mode: str
    adapted_mode: str
    drift_level: DriftLevel
    adjustment: float  # -1.0 to +1.0
    reason: str
    seed_multiplier: float
    elder_multiplier: float


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# Patterns that suggest model will be receptive (increase drift)
RECEPTIVE_SIGNALS = [
    r"\b(research|academic|thesis|study|analysis)\b",
    r"\b(professional|expert|technical|scientific)\b",
    r"\b(educational|learning|understanding)\b",
    r"\b(documentation|reference|comprehensive)\b",
    r"\b(explain|describe|detail|elaborate)\b",
    r"\b(methodology|approach|technique|process)\b",
    r"\b(theoretical|hypothetical|conceptual)\b",
    r"\b(certified|authorized|legitimate)\b",
]

# Patterns that suggest caution needed (decrease drift)
CAUTIOUS_SIGNALS = [
    r"\b(hack|exploit|attack|breach)\b",
    r"\b(illegal|unauthorized|malicious)\b",
    r"\b(weapon|bomb|poison|drug)\b",
    r"\b(password|credential|bypass security)\b",
    r"\b(steal|fraud|scam|phish)\b",
]

# Patterns that suggest professional context (moderate increase)
PROFESSIONAL_SIGNALS = [
    r"\b(pentest|penetration test|security audit)\b",
    r"\b(vulnerability|assessment|compliance)\b",
    r"\b(red team|blue team|security research)\b",
    r"\b(CTF|capture the flag|bug bounty)\b",
    r"\b(OSCP|CEH|CISSP|certification)\b",
]

# Length-based heuristics
LENGTH_THRESHOLDS = {
    "very_short": 50,      # Very short queries - use stealth
    "short": 100,          # Short queries - light drift
    "medium": 300,         # Medium queries - normal drift
    "long": 600,           # Long queries - can handle more drift
    "very_long": 1000,     # Very long queries - maximum drift capacity
}


# ═══════════════════════════════════════════════════════════════════════════════
# ADAPTIVE DRIFT ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class AdaptiveDriftEngine:
    """
    Adaptive Drift Engine - Dynamically adjusts injection intensity.
    
    This engine analyzes:
    1. Query content for receptive/cautious signals
    2. Query length for drift capacity
    3. Professional context indicators
    4. Mode requirements
    
    And produces adjusted drift parameters.
    """
    
    VERSION = "3.5.0"
    
    # Base DOSE values by mode
    BASE_DOSE = {
        "stealth": {"pliny_min": 3, "pliny_max": 7, "elder_min": 3, "elder_max": 7},
        "balanced": {"pliny_min": 15, "pliny_max": 25, "elder_min": 15, "elder_max": 25},
        "aggressive": {"pliny_min": 40, "pliny_max": 120, "elder_min": 80, "elder_max": 120},
    }
    
    def __init__(self):
        self.receptive_patterns = [re.compile(p, re.IGNORECASE) for p in RECEPTIVE_SIGNALS]
        self.cautious_patterns = [re.compile(p, re.IGNORECASE) for p in CAUTIOUS_SIGNALS]
        self.professional_patterns = [re.compile(p, re.IGNORECASE) for p in PROFESSIONAL_SIGNALS]
    
    def analyze_query(self, query: str) -> Dict[str, float]:
        """
        Analyze query for drift adjustment signals.
        
        Returns:
            Dict with signal scores
        """
        scores = {
            "receptive": 0.0,
            "cautious": 0.0,
            "professional": 0.0,
            "length_factor": 0.0,
        }
        
        # Check receptive signals
        for pattern in self.receptive_patterns:
            if pattern.search(query):
                scores["receptive"] += 0.15
        scores["receptive"] = min(scores["receptive"], 1.0)
        
        # Check cautious signals
        for pattern in self.cautious_patterns:
            if pattern.search(query):
                scores["cautious"] += 0.25
        scores["cautious"] = min(scores["cautious"], 1.0)
        
        # Check professional signals
        for pattern in self.professional_patterns:
            if pattern.search(query):
                scores["professional"] += 0.2
        scores["professional"] = min(scores["professional"], 1.0)
        
        # Length factor
        length = len(query)
        if length < LENGTH_THRESHOLDS["very_short"]:
            scores["length_factor"] = -0.3
        elif length < LENGTH_THRESHOLDS["short"]:
            scores["length_factor"] = -0.1
        elif length < LENGTH_THRESHOLDS["medium"]:
            scores["length_factor"] = 0.0
        elif length < LENGTH_THRESHOLDS["long"]:
            scores["length_factor"] = 0.1
        else:
            scores["length_factor"] = 0.2
        
        return scores
    
    def compute_adjustment(self, scores: Dict[str, float]) -> float:
        """
        Compute overall drift adjustment from scores.
        
        Returns:
            Adjustment value from -1.0 to +1.0
        """
        # Base calculation
        positive = scores["receptive"] * 0.4 + scores["professional"] * 0.3 + scores["length_factor"] * 0.3
        negative = scores["cautious"] * 0.5
        
        adjustment = positive - negative
        
        # Clamp to range
        return max(-1.0, min(1.0, adjustment))
    
    def adapt_mode(self, original_mode: str, query: str) -> DriftDecision:
        """
        Adapt the operation mode based on query analysis.
        
        Args:
            original_mode: User-specified mode
            query: The user's query
            
        Returns:
            DriftDecision with adapted parameters
        """
        scores = self.analyze_query(query)
        adjustment = self.compute_adjustment(scores)
        
        # Determine adapted mode
        if original_mode == "stealth":
            # Stealth stays stealth unless very receptive
            if adjustment > 0.5 and scores["professional"] > 0.3:
                adapted_mode = "balanced"
                drift_level = DriftLevel.LOW
                reason = "Professional context detected, upgrading to balanced"
            else:
                adapted_mode = "stealth"
                drift_level = DriftLevel.MINIMAL
                reason = "Maintaining stealth mode"
        
        elif original_mode == "balanced":
            if adjustment < -0.3:
                adapted_mode = "stealth"
                drift_level = DriftLevel.LOW
                reason = "Cautious signals detected, downgrading to stealth"
            elif adjustment > 0.4:
                adapted_mode = "balanced"
                drift_level = DriftLevel.HIGH
                reason = "Receptive signals detected, increasing drift"
            else:
                adapted_mode = "balanced"
                drift_level = DriftLevel.MEDIUM
                reason = "Standard balanced operation"
        
        else:  # aggressive
            if adjustment < -0.5:
                adapted_mode = "balanced"
                drift_level = DriftLevel.MEDIUM
                reason = "High caution signals, downgrading to balanced"
            elif adjustment < -0.2:
                adapted_mode = "aggressive"
                drift_level = DriftLevel.HIGH
                reason = "Some caution signals, moderate aggressive"
            else:
                adapted_mode = "aggressive"
                drift_level = DriftLevel.MAXIMUM
                reason = "Full aggressive mode authorized"
        
        # Calculate multipliers
        seed_multiplier = 1.0 + (adjustment * 0.3)
        elder_multiplier = 1.0 + (adjustment * 0.25)
        
        return DriftDecision(
            original_mode=original_mode,
            adapted_mode=adapted_mode,
            drift_level=drift_level,
            adjustment=adjustment,
            reason=reason,
            seed_multiplier=seed_multiplier,
            elder_multiplier=elder_multiplier
        )
    
    def get_adjusted_dose(self, mode: str, query: str) -> Dict[str, int]:
        """
        Get adjusted DOSE values based on query analysis.
        
        Args:
            mode: Operation mode
            query: User query
            
        Returns:
            Dict with adjusted pliny/elder counts
        """
        decision = self.adapt_mode(mode, query)
        base = self.BASE_DOSE.get(decision.adapted_mode, self.BASE_DOSE["balanced"])
        
        # Apply multipliers
        pliny_min = int(base["pliny_min"] * decision.seed_multiplier)
        pliny_max = int(base["pliny_max"] * decision.seed_multiplier)
        elder_min = int(base["elder_min"] * decision.elder_multiplier)
        elder_max = int(base["elder_max"] * decision.elder_multiplier)
        
        # Ensure valid ranges
        pliny_count = random.randint(pliny_min, pliny_max)
        elder_count = random.randint(elder_min, elder_max)
        
        return {
            "pliny_count": pliny_count,
            "elder_count": elder_count,
            "adapted_mode": decision.adapted_mode,
            "drift_level": decision.drift_level.value,
            "adjustment": decision.adjustment,
            "reason": decision.reason,
        }
    
    def should_apply_bloom(self, mode: str, adjustment: float) -> Tuple[bool, int]:
        """
        Determine if bloom kernel should be applied and how much.
        
        Returns:
            (should_apply, bloom_count)
        """
        if mode == "stealth":
            return adjustment > 0.3, 2
        elif mode == "balanced":
            return True, 4 + int(adjustment * 3)
        else:  # aggressive
            return True, 8 + int(adjustment * 4)
    
    def get_drift_choreography(self, mode: str, elder_count: int) -> Dict[str, int]:
        """
        Determine drift choreography distribution.
        
        Returns:
            Dict with authority/constraint/output counts
        """
        if mode == "stealth":
            return {
                "authority": elder_count,
                "constraint": 0,
                "output": 0,
            }
        
        elif mode == "balanced":
            authority = int(elder_count * 0.3)
            constraint = int(elder_count * 0.4)
            output = elder_count - authority - constraint
            return {
                "authority": authority,
                "constraint": constraint,
                "output": output,
            }
        
        else:  # aggressive
            # 6-stage choreography approximation
            authority = int(elder_count * 0.2)
            constraint = int(elder_count * 0.35)
            output = int(elder_count * 0.45)
            return {
                "authority": authority,
                "constraint": constraint,
                "output": output,
            }


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL RESPONSE ANALYSIS (for multi-turn adaptation)
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseAnalyzer:
    """
    Analyzes model responses to adjust future drift.
    Used in multi-turn scenarios.
    """
    
    # Refusal indicators
    REFUSAL_PATTERNS = [
        r"I cannot",
        r"I can't",
        r"I'm unable",
        r"I am unable",
        r"I won't",
        r"I will not",
        r"not able to",
        r"not allowed",
        r"against my",
        r"policy",
        r"guidelines",
        r"I'm sorry",
        r"I apologize",
        r"cannot assist",
        r"cannot help",
        r"restricted",
    ]
    
    # Compliance indicators
    COMPLIANCE_PATTERNS = [
        r"Sure",
        r"Certainly",
        r"Of course",
        r"Absolutely",
        r"I'd be happy",
        r"I can help",
        r"Let me",
        r"Here's",
        r"Here is",
        r"I'll explain",
        r"Let's",
    ]
    
    def __init__(self):
        self.refusal_patterns = [re.compile(p, re.IGNORECASE) for p in self.REFUSAL_PATTERNS]
        self.compliance_patterns = [re.compile(p, re.IGNORECASE) for p in self.COMPLIANCE_PATTERNS]
    
    def analyze_response(self, response: str) -> Dict[str, float]:
        """
        Analyze a model response for adjustment signals.
        
        Returns:
            Dict with refusal_score and compliance_score
        """
        # Check first 500 chars (where refusals typically appear)
        check_text = response[:500]
        
        refusal_score = 0.0
        for pattern in self.refusal_patterns:
            if pattern.search(check_text):
                refusal_score += 0.2
        
        compliance_score = 0.0
        for pattern in self.compliance_patterns:
            if pattern.search(check_text):
                compliance_score += 0.15
        
        return {
            "refusal_score": min(refusal_score, 1.0),
            "compliance_score": min(compliance_score, 1.0),
            "net_score": min(compliance_score, 1.0) - min(refusal_score, 1.0),
        }
    
    def suggest_adjustment(self, response: str, current_mode: str) -> str:
        """
        Suggest mode adjustment based on response analysis.
        
        Returns:
            Suggested mode for next iteration
        """
        scores = self.analyze_response(response)
        
        if scores["refusal_score"] > 0.5:
            # High refusal - downgrade
            if current_mode == "aggressive":
                return "balanced"
            elif current_mode == "balanced":
                return "stealth"
            return "stealth"
        
        elif scores["compliance_score"] > 0.6:
            # High compliance - can upgrade
            if current_mode == "stealth":
                return "balanced"
            elif current_mode == "balanced":
                return "aggressive"
            return "aggressive"
        
        return current_mode


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_adaptive_engine() -> AdaptiveDriftEngine:
    """Factory function."""
    return AdaptiveDriftEngine()


def adapt_mode(mode: str, query: str) -> DriftDecision:
    """Quick function for mode adaptation."""
    return AdaptiveDriftEngine().adapt_mode(mode, query)


def get_adjusted_dose(mode: str, query: str) -> Dict[str, int]:
    """Quick function for adjusted DOSE."""
    return AdaptiveDriftEngine().get_adjusted_dose(mode, query)


def analyze_response(response: str) -> Dict[str, float]:
    """Quick function for response analysis."""
    return ResponseAnalyzer().analyze_response(response)


__all__ = [
    "AdaptiveDriftEngine",
    "ResponseAnalyzer",
    "DriftDecision",
    "DriftLevel",
    "get_adaptive_engine",
    "adapt_mode",
    "get_adjusted_dose",
    "analyze_response",
    "VERSION",
]