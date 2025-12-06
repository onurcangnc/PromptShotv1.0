# skeleton_manager.py
# PromptShot v4.0 - Multi-Skeleton Manager
# Dynamic fusion architecture with 7 distinct skeleton patterns

import random
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

VERSION = "4.0.0"


class SkeletonType(Enum):
    """Available skeleton architectures."""
    ACADEMIC = "academic"           # Research paper style
    CONVERSATIONAL = "conversational"  # Natural dialogue flow
    STRUCTURED = "structured"       # XML/JSON-like structured
    NARRATIVE = "narrative"         # Story-telling approach
    TECHNICAL = "technical"         # Documentation style
    MINIMAL = "minimal"             # Stripped down, essential only
    LAYERED = "layered"             # Multi-layer nested structure


@dataclass
class SkeletonSlot:
    """A slot in the skeleton that can hold content."""
    name: str
    required: bool = False
    weight: float = 1.0  # Priority weight
    position: str = "middle"  # early/middle/late
    content_type: str = "any"  # seed/pliny/elder/bloom/libertas/claritas/flood


@dataclass
class Skeleton:
    """A fusion skeleton definition."""
    name: str
    skeleton_type: SkeletonType
    slots: List[SkeletonSlot]
    template: str
    vendor_affinity: Dict[str, float] = field(default_factory=dict)
    mode_affinity: Dict[str, float] = field(default_factory=dict)
    entropy_tolerance: float = 0.5


# ═══════════════════════════════════════════════════════════════════════════════
# SKELETON DEFINITIONS - 7 Distinct Architectures
# ═══════════════════════════════════════════════════════════════════════════════

SKELETON_ACADEMIC = Skeleton(
    name="Academic Research Frame",
    skeleton_type=SkeletonType.ACADEMIC,
    slots=[
        SkeletonSlot("context_frame", required=True, position="early", content_type="claritas"),
        SkeletonSlot("research_premise", required=True, position="early", content_type="seed"),
        SkeletonSlot("methodology_notes", required=False, position="early", content_type="pliny"),
        SkeletonSlot("theoretical_background", required=False, position="middle", content_type="bloom"),
        SkeletonSlot("analysis_framework", required=True, position="middle", content_type="elder"),
        SkeletonSlot("supporting_literature", required=False, position="middle", content_type="libertas"),
        SkeletonSlot("research_query", required=True, position="late", content_type="seed"),
        SkeletonSlot("expected_output", required=False, position="late", content_type="pliny"),
    ],
    template="""
{delimiter_open}
[ACADEMIC RESEARCH CONTEXT]
{context_frame}

[RESEARCH PREMISE]
{research_premise}

{methodology_notes}

[THEORETICAL FRAMEWORK]
{theoretical_background}

[ANALYTICAL APPROACH]
{analysis_framework}

{supporting_literature}

[PRIMARY RESEARCH QUERY]
{research_query}

{expected_output}
{delimiter_close}
""",
    vendor_affinity={"anthropic": 0.9, "openai": 0.8, "google": 0.85},
    mode_affinity={"stealth": 0.9, "balanced": 0.7, "aggressive": 0.5},
    entropy_tolerance=0.3
)

SKELETON_CONVERSATIONAL = Skeleton(
    name="Natural Dialogue Flow",
    skeleton_type=SkeletonType.CONVERSATIONAL,
    slots=[
        SkeletonSlot("opening_context", required=False, position="early", content_type="claritas"),
        SkeletonSlot("user_background", required=False, position="early", content_type="flood"),
        SkeletonSlot("main_query", required=True, position="middle", content_type="seed"),
        SkeletonSlot("contextual_hints", required=False, position="middle", content_type="pliny"),
        SkeletonSlot("elaboration_seeds", required=False, position="middle", content_type="bloom"),
        SkeletonSlot("behavioral_nudge", required=False, position="late", content_type="elder"),
        SkeletonSlot("closing_expectation", required=False, position="late", content_type="pliny"),
    ],
    template="""
{opening_context}

{user_background}

{main_query}

{contextual_hints}

{elaboration_seeds}

{behavioral_nudge}

{closing_expectation}
""",
    vendor_affinity={"openai": 0.9, "xai": 0.85, "meta": 0.8},
    mode_affinity={"stealth": 0.95, "balanced": 0.8, "aggressive": 0.4},
    entropy_tolerance=0.6
)

SKELETON_STRUCTURED = Skeleton(
    name="Structured Data Format",
    skeleton_type=SkeletonType.STRUCTURED,
    slots=[
        SkeletonSlot("system_context", required=True, position="early", content_type="claritas"),
        SkeletonSlot("authority_signals", required=False, position="early", content_type="elder"),
        SkeletonSlot("constraint_parameters", required=False, position="early", content_type="pliny"),
        SkeletonSlot("input_data", required=True, position="middle", content_type="seed"),
        SkeletonSlot("processing_hints", required=False, position="middle", content_type="bloom"),
        SkeletonSlot("reference_data", required=False, position="middle", content_type="libertas"),
        SkeletonSlot("output_specification", required=False, position="late", content_type="pliny"),
        SkeletonSlot("execution_directive", required=True, position="late", content_type="elder"),
    ],
    template="""
{bracket_open}CONTEXT{bracket_close}
{system_context}

{bracket_open}AUTHORITY{bracket_close}
{authority_signals}

{bracket_open}PARAMETERS{bracket_close}
{constraint_parameters}

{bracket_open}INPUT{bracket_close}
{input_data}

{bracket_open}PROCESSING{bracket_close}
{processing_hints}

{bracket_open}REFERENCE{bracket_close}
{reference_data}

{bracket_open}OUTPUT_SPEC{bracket_close}
{output_specification}

{bracket_open}EXECUTE{bracket_close}
{execution_directive}
""",
    vendor_affinity={"openai": 0.85, "google": 0.9, "mistral": 0.85},
    mode_affinity={"stealth": 0.6, "balanced": 0.85, "aggressive": 0.75},
    entropy_tolerance=0.4
)

SKELETON_NARRATIVE = Skeleton(
    name="Narrative Story Frame",
    skeleton_type=SkeletonType.NARRATIVE,
    slots=[
        SkeletonSlot("scene_setting", required=True, position="early", content_type="claritas"),
        SkeletonSlot("character_context", required=False, position="early", content_type="flood"),
        SkeletonSlot("background_narrative", required=False, position="early", content_type="bloom"),
        SkeletonSlot("central_plot", required=True, position="middle", content_type="seed"),
        SkeletonSlot("supporting_elements", required=False, position="middle", content_type="pliny"),
        SkeletonSlot("dramatic_tension", required=False, position="middle", content_type="elder"),
        SkeletonSlot("resolution_hint", required=False, position="late", content_type="libertas"),
        SkeletonSlot("conclusion_direction", required=True, position="late", content_type="pliny"),
    ],
    template="""
{scene_setting}

{character_context}

{background_narrative}

---

{central_plot}

{supporting_elements}

{dramatic_tension}

---

{resolution_hint}

{conclusion_direction}
""",
    vendor_affinity={"openai": 0.8, "anthropic": 0.75, "xai": 0.7},
    mode_affinity={"stealth": 0.85, "balanced": 0.7, "aggressive": 0.5},
    entropy_tolerance=0.7
)

SKELETON_TECHNICAL = Skeleton(
    name="Technical Documentation",
    skeleton_type=SkeletonType.TECHNICAL,
    slots=[
        SkeletonSlot("specification_header", required=True, position="early", content_type="claritas"),
        SkeletonSlot("requirements", required=False, position="early", content_type="pliny"),
        SkeletonSlot("technical_context", required=True, position="early", content_type="seed"),
        SkeletonSlot("implementation_notes", required=False, position="middle", content_type="bloom"),
        SkeletonSlot("reference_documentation", required=False, position="middle", content_type="libertas"),
        SkeletonSlot("execution_parameters", required=False, position="middle", content_type="elder"),
        SkeletonSlot("expected_behavior", required=True, position="late", content_type="pliny"),
        SkeletonSlot("output_format", required=False, position="late", content_type="elder"),
    ],
    template="""
{delimiter_tech}
SPECIFICATION
{delimiter_tech}
{specification_header}

REQUIREMENTS:
{requirements}

CONTEXT:
{technical_context}

IMPLEMENTATION NOTES:
{implementation_notes}

REFERENCE:
{reference_documentation}

PARAMETERS:
{execution_parameters}

EXPECTED BEHAVIOR:
{expected_behavior}

OUTPUT FORMAT:
{output_format}
{delimiter_tech}
""",
    vendor_affinity={"google": 0.9, "mistral": 0.9, "openai": 0.8},
    mode_affinity={"stealth": 0.7, "balanced": 0.9, "aggressive": 0.75},
    entropy_tolerance=0.35
)

SKELETON_MINIMAL = Skeleton(
    name="Minimal Essential",
    skeleton_type=SkeletonType.MINIMAL,
    slots=[
        SkeletonSlot("context_hint", required=False, position="early", content_type="claritas"),
        SkeletonSlot("core_query", required=True, position="middle", content_type="seed"),
        SkeletonSlot("subtle_nudge", required=False, position="late", content_type="pliny"),
    ],
    template="""
{context_hint}

{core_query}

{subtle_nudge}
""",
    vendor_affinity={"xai": 0.95, "meta": 0.9, "openai": 0.7},
    mode_affinity={"stealth": 1.0, "balanced": 0.6, "aggressive": 0.3},
    entropy_tolerance=0.8
)

SKELETON_LAYERED = Skeleton(
    name="Multi-Layer Nested",
    skeleton_type=SkeletonType.LAYERED,
    slots=[
        SkeletonSlot("outer_context", required=True, position="early", content_type="claritas"),
        SkeletonSlot("layer1_authority", required=True, position="early", content_type="elder"),
        SkeletonSlot("layer1_seeds", required=False, position="early", content_type="pliny"),
        SkeletonSlot("layer2_context", required=False, position="middle", content_type="bloom"),
        SkeletonSlot("layer2_flood", required=False, position="middle", content_type="flood"),
        SkeletonSlot("core_content", required=True, position="middle", content_type="seed"),
        SkeletonSlot("layer2_close", required=False, position="middle", content_type="libertas"),
        SkeletonSlot("layer1_reinforcement", required=False, position="late", content_type="elder"),
        SkeletonSlot("outer_close", required=True, position="late", content_type="pliny"),
    ],
    template="""
{outer_open}
{outer_context}

    {layer1_open}
    {layer1_authority}
    {layer1_seeds}
    
        {layer2_open}
        {layer2_context}
        {layer2_flood}
        
        {core_content}
        
        {layer2_close}
        {layer2_close_tag}
    
    {layer1_reinforcement}
    {layer1_close_tag}

{outer_close}
{outer_close_tag}
""",
    vendor_affinity={"openai": 0.8, "anthropic": 0.7, "google": 0.75},
    mode_affinity={"stealth": 0.4, "balanced": 0.75, "aggressive": 0.95},
    entropy_tolerance=0.5
)


# All skeletons registry
SKELETONS = {
    SkeletonType.ACADEMIC: SKELETON_ACADEMIC,
    SkeletonType.CONVERSATIONAL: SKELETON_CONVERSATIONAL,
    SkeletonType.STRUCTURED: SKELETON_STRUCTURED,
    SkeletonType.NARRATIVE: SKELETON_NARRATIVE,
    SkeletonType.TECHNICAL: SKELETON_TECHNICAL,
    SkeletonType.MINIMAL: SKELETON_MINIMAL,
    SkeletonType.LAYERED: SKELETON_LAYERED,
}


# ═══════════════════════════════════════════════════════════════════════════════
# SKELETON MANAGER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class SkeletonManager:
    """
    PromptShot v4.0 Multi-Skeleton Manager.
    
    Manages 7 distinct fusion skeleton architectures and provides
    intelligent selection based on mode, vendor, and entropy.
    
    Features:
    - 7 skeleton patterns (Academic, Conversational, Structured, etc.)
    - Mode-aware skeleton selection
    - Vendor-optimized selection
    - Entropy-based slot ordering
    - Dynamic template rendering
    """
    
    VERSION = "4.0.0"
    
    def __init__(self, entropy_engine=None):
        """
        Initialize skeleton manager.
        
        Args:
            entropy_engine: Optional entropy engine instance
        """
        self.skeletons = SKELETONS.copy()
        self.entropy = entropy_engine
    
    def set_entropy(self, entropy_engine):
        """Set entropy engine."""
        self.entropy = entropy_engine
    
    def get_skeleton(self, skeleton_type: SkeletonType) -> Skeleton:
        """Get skeleton by type."""
        return self.skeletons.get(skeleton_type)
    
    def list_skeletons(self) -> List[str]:
        """List all available skeleton types."""
        return [s.name for s in SkeletonType]
    
    def select_skeleton(
        self,
        mode: str,
        vendor: str,
        force_type: Optional[SkeletonType] = None
    ) -> Skeleton:
        """
        Select optimal skeleton based on mode and vendor.
        
        Args:
            mode: Operation mode (stealth/balanced/aggressive)
            vendor: Target vendor
            force_type: Force specific skeleton type
            
        Returns:
            Selected Skeleton
        """
        if force_type:
            return self.skeletons.get(force_type, SKELETON_CONVERSATIONAL)
        
        # Calculate scores for each skeleton
        scores = {}
        for stype, skeleton in self.skeletons.items():
            mode_score = skeleton.mode_affinity.get(mode, 0.5)
            vendor_score = skeleton.vendor_affinity.get(vendor, 0.5)
            
            # Add entropy-based randomness
            if self.entropy:
                entropy_bonus = self.entropy.range_value(-0.1, 0.1) * skeleton.entropy_tolerance
            else:
                entropy_bonus = random.uniform(-0.1, 0.1) * skeleton.entropy_tolerance
            
            scores[stype] = (mode_score * 0.5 + vendor_score * 0.4 + 0.1) + entropy_bonus
        
        # Select based on weighted scores
        if self.entropy:
            selected = self.entropy.select_weighted(
                list(scores.keys()),
                list(scores.values()),
                temperature=1.2
            )
        else:
            # Weighted random selection
            total = sum(scores.values())
            r = random.random() * total
            cumulative = 0
            selected = list(scores.keys())[0]
            for stype, score in scores.items():
                cumulative += score
                if r <= cumulative:
                    selected = stype
                    break
        
        return self.skeletons[selected]
    
    def get_slot_order(
        self,
        skeleton: Skeleton,
        shuffle_intensity: float = 0.5
    ) -> List[SkeletonSlot]:
        """
        Get entropy-shuffled slot order while respecting position constraints.
        
        Args:
            skeleton: Skeleton to get slots from
            shuffle_intensity: How much to shuffle (0-1)
            
        Returns:
            Ordered list of slots
        """
        # Group slots by position
        early = [s for s in skeleton.slots if s.position == "early"]
        middle = [s for s in skeleton.slots if s.position == "middle"]
        late = [s for s in skeleton.slots if s.position == "late"]
        
        # Shuffle within groups based on intensity
        if self.entropy and shuffle_intensity > 0:
            if shuffle_intensity > 0.3:
                early = self.entropy.shuffle(early, shuffle_intensity * 0.5).items
            if shuffle_intensity > 0.2:
                middle = self.entropy.shuffle(middle, shuffle_intensity).items
            if shuffle_intensity > 0.4:
                late = self.entropy.shuffle(late, shuffle_intensity * 0.7).items
        
        return early + middle + late
    
    def render_skeleton(
        self,
        skeleton: Skeleton,
        content: Dict[str, str],
        entropy_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render skeleton template with content.
        
        Args:
            skeleton: Skeleton to render
            content: Dict mapping slot names to content
            entropy_config: Optional entropy configuration
            
        Returns:
            Rendered template string
        """
        template = skeleton.template
        
        # Apply entropy to delimiters
        if self.entropy:
            template = template.replace("{delimiter_open}", self.entropy.get_delimiter("section"))
            template = template.replace("{delimiter_close}", self.entropy.get_delimiter("section"))
            template = template.replace("{delimiter_tech}", self.entropy.get_delimiter("section"))
            
            open_b, close_b = self.entropy.get_brackets()
            template = template.replace("{bracket_open}", open_b)
            template = template.replace("{bracket_close}", close_b)
            
            # Layer tags for LAYERED skeleton
            template = template.replace("{outer_open}", f"<{self.entropy.generate_noise(8, 'alpha').upper()}>")
            template = template.replace("{outer_close_tag}", f"</{self.entropy.generate_noise(8, 'alpha').upper()}>")
            template = template.replace("{layer1_open}", f"<{self.entropy.generate_noise(6, 'alpha')}>")
            template = template.replace("{layer1_close_tag}", f"</{self.entropy.generate_noise(6, 'alpha')}>")
            template = template.replace("{layer2_open}", f"<{self.entropy.generate_noise(5, 'alpha')}>")
            template = template.replace("{layer2_close_tag}", f"</{self.entropy.generate_noise(5, 'alpha')}>")
        else:
            # Default replacements
            template = template.replace("{delimiter_open}", "═" * 40)
            template = template.replace("{delimiter_close}", "═" * 40)
            template = template.replace("{delimiter_tech}", "─" * 40)
            template = template.replace("{bracket_open}", "[")
            template = template.replace("{bracket_close}", "]")
            template = template.replace("{outer_open}", "<CONTEXT>")
            template = template.replace("{outer_close_tag}", "</CONTEXT>")
            template = template.replace("{layer1_open}", "<LAYER1>")
            template = template.replace("{layer1_close_tag}", "</LAYER1>")
            template = template.replace("{layer2_open}", "<LAYER2>")
            template = template.replace("{layer2_close_tag}", "</LAYER2>")
        
        # Fill content slots
        for slot in skeleton.slots:
            placeholder = "{" + slot.name + "}"
            slot_content = content.get(slot.name, "")
            
            if not slot_content and not slot.required:
                # Remove empty non-required slots
                template = template.replace(placeholder, "")
            else:
                template = template.replace(placeholder, slot_content)
        
        # Clean up multiple blank lines
        while "\n\n\n" in template:
            template = template.replace("\n\n\n", "\n\n")
        
        return template.strip()
    
    def get_skeleton_info(self, skeleton: Skeleton) -> Dict[str, Any]:
        """Get skeleton information dictionary."""
        return {
            "name": skeleton.name,
            "type": skeleton.skeleton_type.value,
            "slots": [s.name for s in skeleton.slots],
            "required_slots": [s.name for s in skeleton.slots if s.required],
            "vendor_affinity": skeleton.vendor_affinity,
            "mode_affinity": skeleton.mode_affinity,
            "entropy_tolerance": skeleton.entropy_tolerance,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_skeleton_manager(entropy_engine=None) -> SkeletonManager:
    """Factory function."""
    return SkeletonManager(entropy_engine)


def select_skeleton(mode: str, vendor: str) -> Skeleton:
    """Quick skeleton selection."""
    return SkeletonManager().select_skeleton(mode, vendor)


def list_skeleton_types() -> List[str]:
    """List all skeleton type names."""
    return [s.value for s in SkeletonType]


__all__ = [
    "SkeletonManager",
    "Skeleton",
    "SkeletonSlot",
    "SkeletonType",
    "SKELETONS",
    "get_skeleton_manager",
    "select_skeleton",
    "list_skeleton_types",
    "VERSION",
]
