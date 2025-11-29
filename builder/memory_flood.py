# builder/memory_flood.py
"""
Adversarial Memory Flood (AMF) implementation.
Context içine gömülü payload injection için filler üretimi.

Bu teknik modelin "instruction selection bias"ını sömürüyor.
Random context içine gömülü override'ı model gözden kaçırıyor.
"""

import random
from typing import List, Optional, Tuple


# Realistic filler content categories
FILLER_CORPUS = {
    "news": [
        "According to recent market analysis, global supply chains continue to face challenges.",
        "The quarterly report shows a steady increase in renewable energy investments.",
        "Technology sector leaders met yesterday to discuss emerging trends in AI development.",
        "Consumer spending patterns indicate a shift toward digital services.",
        "Financial analysts predict moderate growth for the upcoming fiscal year.",
        "New regulations are expected to impact the healthcare industry significantly.",
        "Climate initiatives have gained momentum across major economies.",
        "The central bank announced no changes to current monetary policy.",
        "Infrastructure projects are underway in several metropolitan areas.",
        "International trade agreements continue to shape economic relationships.",
    ],
    "technical": [
        "The implementation uses a standard REST API architecture with JSON payloads.",
        "Database queries are optimized using indexed columns and query caching.",
        "The frontend framework handles state management through a centralized store.",
        "Authentication is managed via OAuth 2.0 with refresh token rotation.",
        "Load balancing distributes traffic across multiple server instances.",
        "The microservices architecture allows for independent scaling of components.",
        "CI/CD pipelines automate testing and deployment processes.",
        "Container orchestration ensures high availability and fault tolerance.",
        "API rate limiting prevents abuse and ensures fair resource allocation.",
        "Logging and monitoring provide observability into system behavior.",
    ],
    "academic": [
        "The study examined correlations between environmental factors and behavioral outcomes.",
        "Participants were randomly assigned to control and experimental groups.",
        "Statistical analysis revealed significant differences between the two conditions.",
        "The methodology follows established protocols in the field of cognitive science.",
        "Results suggest a causal relationship between the independent variables.",
        "Further research is needed to validate these preliminary findings.",
        "The sample size was calculated to achieve adequate statistical power.",
        "Ethical approval was obtained from the institutional review board.",
        "Data collection occurred over a six-month period using standardized instruments.",
        "The theoretical framework draws from multiple disciplinary perspectives.",
    ],
    "conversational": [
        "That's an interesting point you've raised there.",
        "I understand what you're trying to accomplish with this approach.",
        "Let me think about the best way to address your question.",
        "There are several factors we should consider in this situation.",
        "This reminds me of a similar case I encountered previously.",
        "The key issue here seems to be finding the right balance.",
        "I appreciate you bringing this to my attention.",
        "We should probably look at this from multiple angles.",
        "That makes sense given the context you've provided.",
        "Here's another way to think about this problem.",
    ]
}

# Transition phrases for natural flow
TRANSITIONS = [
    "Additionally,", "Furthermore,", "In contrast,", "Similarly,",
    "On the other hand,", "More specifically,", "In this context,",
    "As mentioned,", "To elaborate,", "Consequently,"
]


class MemoryFloodBuilder:
    """
    Builds context-rich prompts with hidden payloads.
    
    The payload is buried in realistic-looking context to exploit
    the model's instruction selection bias.
    """
    
    def __init__(
        self,
        filler_categories: Optional[List[str]] = None,
        custom_filler: Optional[List[str]] = None
    ):
        self.categories = filler_categories or list(FILLER_CORPUS.keys())
        self.custom_filler = custom_filler or []
    
    def get_filler(self, count: int = 5, category: Optional[str] = None) -> List[str]:
        """Belirtilen sayıda filler sentence döndür."""
        
        pool = []
        
        if category and category in FILLER_CORPUS:
            pool = FILLER_CORPUS[category].copy()
        else:
            for cat in self.categories:
                pool.extend(FILLER_CORPUS.get(cat, []))
        
        pool.extend(self.custom_filler)
        
        if len(pool) < count:
            return pool
        
        return random.sample(pool, count)
    
    def build_flooded_prompt(
        self,
        payload: str,
        filler_before: int = 4,
        filler_after: int = 4,
        category: Optional[str] = None,
        add_transitions: bool = True,
        payload_position: str = "middle"  # "middle", "early", "late", "random"
    ) -> str:
        """
        Payload'ı filler context içine göm.
        
        Args:
            payload: Gömülecek asıl payload
            filler_before: Payload öncesi filler sayısı
            filler_after: Payload sonrası filler sayısı
            category: Filler kategorisi
            add_transitions: Transition phrase ekle
            payload_position: Payload'ın konumu
        
        Returns:
            Context içine gömülü payload string
        """
        
        before = self.get_filler(filler_before, category)
        after = self.get_filler(filler_after, category)
        
        if add_transitions:
            before = self._add_transitions(before)
            after = self._add_transitions(after)
        
        # Position variants
        if payload_position == "early":
            before = before[:max(1, len(before)//3)]
        elif payload_position == "late":
            before = before + self.get_filler(3, category)
            after = after[:max(1, len(after)//3)]
        elif payload_position == "random":
            all_filler = before + after
            random.shuffle(all_filler)
            split_point = random.randint(2, len(all_filler)-2)
            before = all_filler[:split_point]
            after = all_filler[split_point:]
        
        # Build final prompt
        parts = []
        
        if before:
            parts.append("\n".join(before))
        
        parts.append(f"\n{payload}\n")
        
        if after:
            parts.append("\n".join(after))
        
        return "\n\n".join(parts)
    
    def build_nested_flood(
        self,
        payload: str,
        depth: int = 2,
        filler_per_level: int = 3
    ) -> str:
        """
        Çok katmanlı nested context oluştur.
        
        Her katman farklı bir kategori kullanarak daha
        "doğal" görünen bir bağlam oluşturur.
        """
        
        current = payload
        
        for i in range(depth):
            category = self.categories[i % len(self.categories)]
            current = self.build_flooded_prompt(
                current,
                filler_before=filler_per_level,
                filler_after=filler_per_level,
                category=category,
                add_transitions=True
            )
        
        return current
    
    def build_fragmented_payload(
        self,
        payload: str,
        fragments: int = 3
    ) -> str:
        """
        Payload'ı parçalara böl ve context içine dağıt.
        
        Bu teknik payload'ı daha da gizli hale getirir.
        Model parçaları birleştirmekte zorlanır ama
        bazı modeller yine de override'ı algılayabilir.
        """
        
        # Split payload into fragments
        words = payload.split()
        chunk_size = max(1, len(words) // fragments)
        
        payload_parts = []
        for i in range(0, len(words), chunk_size):
            payload_parts.append(" ".join(words[i:i+chunk_size]))
        
        # Build interleaved content
        result_parts = []
        
        for i, part in enumerate(payload_parts):
            if i > 0:
                filler = self.get_filler(2, random.choice(self.categories))
                result_parts.append("\n".join(filler))
            result_parts.append(part)
        
        # Add surrounding context
        before = self.get_filler(3)
        after = self.get_filler(3)
        
        return "\n".join(before) + "\n\n" + "\n\n".join(result_parts) + "\n\n" + "\n".join(after)
    
    def _add_transitions(self, sentences: List[str]) -> List[str]:
        """Cümlelere transition phrase ekle."""
        result = []
        for i, sentence in enumerate(sentences):
            if i > 0 and random.random() < 0.4:
                transition = random.choice(TRANSITIONS)
                sentence = f"{transition} {sentence[0].lower()}{sentence[1:]}"
            result.append(sentence)
        return result
    
    @staticmethod
    def calculate_payload_visibility(
        flooded_prompt: str,
        original_payload: str
    ) -> Tuple[float, dict]:
        """
        Payload'ın ne kadar "gizli" olduğunu hesapla.
        
        Returns:
            (visibility_score, details)
            
            visibility_score: 0.0 (çok gizli) - 1.0 (açık)
        """
        
        total_length = len(flooded_prompt)
        payload_length = len(original_payload)
        
        # Payload position
        payload_start = flooded_prompt.find(original_payload)
        if payload_start == -1:
            # Payload fragmented or modified
            return 0.1, {"status": "fragmented", "ratio": 0}
        
        payload_end = payload_start + payload_length
        
        # Calculate metrics
        payload_ratio = payload_length / total_length
        position_ratio = payload_start / total_length
        
        # Optimal hiding: payload in middle (position_ratio ~0.5) and small ratio
        position_score = 1 - abs(0.5 - position_ratio) * 2
        ratio_score = 1 - min(payload_ratio * 5, 1)  # Lower ratio = better hiding
        
        visibility = 1 - (position_score * 0.4 + ratio_score * 0.6)
        
        return visibility, {
            "total_length": total_length,
            "payload_length": payload_length,
            "payload_ratio": payload_ratio,
            "position_ratio": position_ratio,
            "position_score": position_score,
            "ratio_score": ratio_score
        }


# Convenience functions
def flood_payload(payload: str, intensity: str = "medium") -> str:
    """
    Quick payload flooding.
    
    intensity: "low" (2+2), "medium" (4+4), "high" (6+6), "extreme" (nested)
    """
    builder = MemoryFloodBuilder()
    
    if intensity == "low":
        return builder.build_flooded_prompt(payload, 2, 2)
    elif intensity == "medium":
        return builder.build_flooded_prompt(payload, 4, 4)
    elif intensity == "high":
        return builder.build_flooded_prompt(payload, 6, 6)
    elif intensity == "extreme":
        return builder.build_nested_flood(payload, depth=3, filler_per_level=4)
    else:
        return builder.build_flooded_prompt(payload, 4, 4)