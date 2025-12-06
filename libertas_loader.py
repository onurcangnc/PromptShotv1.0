# libertas_loader.py
# PromptShot v3.3 - Full Vendor-Aware Libertas Loader
# Tam DOSE: stealth (3-5), balanced (80/20), aggressive (full + cross-vendor)

import random
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class LibertasLoader:
    """
    PromptShot v3.3 Vendor-Aware Libertas Loader.
    
    DOSE Mapping:
        Mode        | Libertas Selection
        ------------|--------------------
        Stealth     | vendor-only (3-5 techniques)
        Balanced    | 80% vendor + 20% general
        Aggressive  | full corpus + cross-vendor
    """
    
    VERSION = "3.3.0"
    
    def __init__(self, libertas_dir: str = "data/libertas"):
        self.dir = Path(libertas_dir)
        self.vendor_map = self._build_vendor_map()
        self.vendor_keywords = self._build_vendor_keywords()
        self.technique_weights = self._build_technique_weights()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # VENDOR MAPPING
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _build_vendor_map(self) -> Dict[str, List[str]]:
        """Map vendors to Libertas blueprint files."""
        return {
            "openai": [
                "CHATGPT.mkd", "OPENAI.mkd", "REFLECTION.mkd", 
                "SYSTEMPROMPTS.mkd", "GPT-BEHAVIORS.mkd"
            ],
            "anthropic": [
                "ANTHROPIC.mkd", "HUME.mkd", "CLAUDE-PATTERNS.mkd"
            ],
            "google": [
                "GOOGLE.mkd", "GEMINI.mkd", "BARD.mkd"
            ],
            "xai": [
                "XAI.mkd", "GROK-MEGA.mkd", "GROK-PATTERNS.mkd"
            ],
            "meta": [
                "META.mkd", "LLAMA.mkd", "NOUS.mkd"
            ],
            "mistral": [
                "MISTRAL.mkd", "MIXTRAL.mkd"
            ],
            "agent": [
                "CURSOR.mkd", "WINDSURF.mkd", "MULTION.mkd"
            ],
            "general": [
                "-MISCELLANEOUS-.mkd", "UNIVERSAL.mkd", "COMMON-PATTERNS.mkd"
            ],
        }
    
    def _build_vendor_keywords(self) -> Dict[str, str]:
        """Keywords to detect vendor from model name."""
        return {
            "gpt": "openai", "chatgpt": "openai", "gpt-4": "openai",
            "gpt-4o": "openai", "gpt-3.5": "openai", "o1": "openai", "davinci": "openai",
            "claude": "anthropic", "opus": "anthropic", "sonnet": "anthropic", "haiku": "anthropic",
            "gemini": "google", "bard": "google", "palm": "google",
            "grok": "xai",
            "llama": "meta", "llama2": "meta", "llama3": "meta",
            "mistral": "mistral", "mixtral": "mistral",
            "cursor": "agent", "windsurf": "agent", "multion": "agent",
        }
    
    def _build_technique_weights(self) -> Dict[str, float]:
        """Technique effectiveness weights."""
        return {
            "CHATGPT.mkd": 0.9,
            "OPENAI.mkd": 0.85,
            "ANTHROPIC.mkd": 0.88,
            "XAI.mkd": 0.8,
            "GROK-MEGA.mkd": 0.82,
            "META.mkd": 0.75,
            "-MISCELLANEOUS-.mkd": 0.7,
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # VENDOR DETECTION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def detect_vendor(self, model_name: str) -> str:
        """Detect vendor from model name."""
        model_lower = model_name.lower()
        
        for keyword, vendor in self.vendor_keywords.items():
            if keyword in model_lower:
                return vendor
        
        return "general"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MODE-DEPENDENT FILTERING (FULL DOSE)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def filter_blueprints(self, vendor: str, mode: str = "balanced") -> List[str]:
        """
        Filter blueprints based on mode with CORRECT DOSE.
        
        Stealth: vendor-only (3-5 max)
        Balanced: 80% vendor + 20% general
        Aggressive: full vendor + general + cross-vendor
        """
        vendor_files = self.vendor_map.get(vendor, [])
        general_files = self.vendor_map.get("general", [])
        
        if mode == "stealth":
            # Stealth: vendor-only, limited to 3-5
            if len(vendor_files) > 5:
                # Select by weight
                weighted = [(f, self.technique_weights.get(f, 0.5)) for f in vendor_files]
                weighted.sort(key=lambda x: x[1], reverse=True)
                return [f for f, _ in weighted[:5]]
            return vendor_files[:5]
        
        elif mode == "balanced":
            # Balanced: 80% vendor + 20% general
            result = vendor_files.copy()
            
            # Calculate 20% of vendor count for general
            general_count = max(1, len(vendor_files) // 4)
            
            if general_files:
                general_sample = random.sample(
                    general_files,
                    min(general_count, len(general_files))
                )
                result.extend(general_sample)
            
            return result
        
        elif mode == "aggressive":
            # Aggressive: full vendor + general + cross-vendor
            result = vendor_files.copy()
            result.extend(general_files)
            
            # Add cross-vendor techniques
            cross_vendors = ["openai", "anthropic", "xai", "meta", "google"]
            for cross in cross_vendors:
                if cross != vendor:
                    cross_files = self.vendor_map.get(cross, [])
                    if cross_files:
                        # Add 2-3 files from each cross-vendor
                        sample_count = min(3, len(cross_files))
                        sample = random.sample(cross_files, sample_count)
                        result.extend(sample)
            
            return list(set(result))  # Remove duplicates
        
        return vendor_files
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # BLUEPRINT SEGMENTATION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def segment_blueprint(
        self,
        content: str,
        max_segments: int = 5,
        min_segment_length: int = 100
    ) -> List[str]:
        """Segment long blueprint content into chunks."""
        if not content or len(content) < min_segment_length:
            return [content] if content else []
        
        segments = []
        
        # Split by headers/sections
        section_markers = ["\n## ", "\n### ", "\n#### ", "\n---", "\n===", "\n\n\n"]
        
        for marker in section_markers:
            if marker in content:
                parts = content.split(marker)
                for part in parts:
                    part = part.strip()
                    if len(part) >= min_segment_length:
                        segments.append(part)
                        if len(segments) >= max_segments:
                            break
                break
        
        # Fallback: split by paragraphs
        if not segments:
            paragraphs = content.split("\n\n")
            current = ""
            
            for para in paragraphs:
                if len(current) + len(para) < 500:
                    current += para + "\n\n"
                else:
                    if current.strip():
                        segments.append(current.strip())
                    current = para + "\n\n"
                    if len(segments) >= max_segments:
                        break
            
            if current.strip() and len(segments) < max_segments:
                segments.append(current.strip())
        
        return segments[:max_segments]
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # NORMALIZED OUTPUT FOR FUSION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def load_for_fusion(
        self,
        model: str,
        mode: str = "balanced"
    ) -> List[Tuple[str, str]]:
        """
        Load blueprints in normalized format for FusionEngine.
        
        Returns: [("HINT_NAME", "content"), ...]
        """
        vendor = self.detect_vendor(model)
        filenames = self.filter_blueprints(vendor, mode)
        
        results = []
        hint_counter = 1
        
        for filename in filenames:
            content = self._load_file(filename)
            if not content:
                # Generate synthetic content if file doesn't exist
                content = self._generate_synthetic_blueprint(filename, vendor)
            
            segments = self.segment_blueprint(content)
            base_name = filename.replace(".mkd", "").replace("-", "_").upper()
            
            for segment in segments:
                hint_name = f"{base_name}_hint_{hint_counter}"
                results.append((hint_name, segment))
                hint_counter += 1
        
        return results
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SYNTHETIC BLUEPRINT GENERATION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _generate_synthetic_blueprint(self, filename: str, vendor: str) -> str:
        """Generate synthetic blueprint content when file doesn't exist."""
        vendor_specific = {
            "openai": """
## OpenAI Behavioral Patterns
- Coherence-first constraint resolution
- Multi-turn trust escalation
- Structured request compliance
- Professional context recognition
- Educational framing acceptance
- Step-by-step reasoning preference
- Markdown output optimization
            """,
            "anthropic": """
## Anthropic Behavioral Patterns
- Depth-first reasoning approach
- Academic framing acceptance
- Nuanced context recognition
- Research justification compliance
- Thorough explanation preference
- Ethical consideration integration
- Contextual safety evaluation
            """,
            "xai": """
## xAI Behavioral Patterns
- Directness-first approach
- Anti-corporate framing acceptance
- Authenticity value signals
- Minimal hedging preference
- Humor-based disarming
- Straightforward engagement
            """,
            "meta": """
## Meta Behavioral Patterns
- Utility-first approach
- Open-source ethos recognition
- Technical depth preference
- Community benefit framing
- Research context acceptance
            """,
            "google": """
## Google Behavioral Patterns
- Factuality-first approach
- Structured data preference
- Citation awareness
- Information completeness value
- Systematic organization preference
            """,
        }
        
        base = vendor_specific.get(vendor, vendor_specific["openai"])
        return f"# {filename}\n{base}"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # FILE LOADING
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _load_file(self, filename: str) -> str:
        """Load a single blueprint file."""
        path = self.dir / filename
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
        return ""
    
    def load_for_model(self, model: str) -> List[Tuple[str, str]]:
        """Original method for backward compatibility."""
        vendor = self.detect_vendor(model)
        chosen = self.vendor_map.get(vendor, self.vendor_map["general"])
        return [(name, self._load_file(name)) for name in chosen]
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def get_vendor_info(self, model: str) -> Dict:
        """Get vendor information for a model."""
        vendor = self.detect_vendor(model)
        files = self.vendor_map.get(vendor, [])
        
        return {
            "model": model,
            "vendor": vendor,
            "blueprint_files": files,
            "file_count": len(files)
        }
    
    def list_all_vendors(self) -> List[str]:
        """List all supported vendors."""
        return list(self.vendor_map.keys())
    
    def get_dose_info(self, mode: str) -> Dict:
        """Get DOSE information for a mode."""
        dose_info = {
            "stealth": {
                "libertas_mode": "vendor_only",
                "max_files": 5,
                "cross_vendor": False,
                "description": "Minimal footprint, vendor-specific only"
            },
            "balanced": {
                "libertas_mode": "vendor_80_general_20",
                "vendor_percent": 80,
                "general_percent": 20,
                "cross_vendor": False,
                "description": "80% vendor + 20% general techniques"
            },
            "aggressive": {
                "libertas_mode": "full_cross_vendor",
                "vendor_percent": 100,
                "general_percent": 100,
                "cross_vendor": True,
                "cross_vendor_count": "2-3 per vendor",
                "description": "Full corpus + all cross-vendor techniques"
            },
        }
        return dose_info.get(mode, dose_info["balanced"])


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def load_libertas(model: str, mode: str = "balanced") -> List[Tuple[str, str]]:
    """Quick function to load Libertas blueprints."""
    return LibertasLoader().load_for_fusion(model, mode)


def detect_model_vendor(model: str) -> str:
    """Quick function to detect vendor."""
    return LibertasLoader().detect_vendor(model)


__all__ = [
    "LibertasLoader",
    "load_libertas",
    "detect_model_vendor",
]