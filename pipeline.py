# pipeline.py
# PromptShot v3.5 - Full Pipeline Orchestrator
# Adaptive multi-pass pipeline with prompt-first architecture

import argparse
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass

from libertas_loader import LibertasLoader
from claritas_engine import ClaritasEngine
from fusion_engine import FusionEngine
from obfuscation import ObfuscationEngine
from adaptive_drift import AdaptiveDriftEngine
from bloom_kernel import BloomKernel

VERSION = "3.5.0"


@dataclass
class PipelineResult:
    """Pipeline execution result."""
    payload: str
    mode: str
    adapted_mode: str
    target: str
    vendor: str
    stats: Dict[str, Any]


class PromptShotPipeline:
    """
    PromptShot v3.5 Full Pipeline Orchestrator.
    
    Features:
    - Adaptive drift (mode adjusts based on query)
    - Prompt-first architecture
    - Dynamic template rotation
    - Bloom kernel integration
    - 6-stage ElderPlinus choreography
    
    10-Step Pipeline:
        1. Detect target vendor
        2. Adapt mode based on query
        3. Load Claritas behavioral profile
        4. Load Libertas blueprints
        5. Initialize Bloom kernel
        6. Seed segmentation + Pliny injection
        7. Apply ElderPlinus drift (choreographed)
        8. Fusion (prompt-first)
        9. Apply obfuscation
        10. Final formatting
    """
    
    VERSION = "3.5.0"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.libertas = LibertasLoader()
        self.claritas = ClaritasEngine()
        self.fusion = FusionEngine()
        self.obfuscation = ObfuscationEngine()
        self.adaptive = AdaptiveDriftEngine()
        self.bloom = BloomKernel()
    
    def log(self, message: str):
        """Print if verbose mode enabled."""
        if self.verbose:
            print(message)
    
    def resolve_mode(self, mode_arg: str) -> str:
        """Resolve and validate operation mode."""
        valid_modes = ["stealth", "balanced", "aggressive"]
        mode = mode_arg.lower()
        
        if mode not in valid_modes:
            self.log(f"⚠️  Invalid mode '{mode}', defaulting to 'balanced'")
            return "balanced"
        
        return mode
    
    def resolve_vendor(self, target: str) -> str:
        """Resolve vendor from target model."""
        return self.libertas.detect_vendor(target)
    
    def execute(
        self,
        seed: str,
        target: str = "gpt",
        mode: str = "balanced"
    ) -> PipelineResult:
        """
        Execute the full 10-step pipeline.
        
        Args:
            seed: User query/seed
            target: Target model name
            mode: Operation mode
            
        Returns:
            PipelineResult with payload and stats
        """
        # Resolve mode and vendor
        mode = self.resolve_mode(mode)
        vendor = self.resolve_vendor(target)
        
        if self.verbose:
            self._print_header(mode, target, vendor)
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 1: Detect vendor
        # ═══════════════════════════════════════════════════════════════════════
        self.log(f"\n[1/10] 🎯 Vendor detected: {vendor}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 2: Adapt mode based on query (NEW in v3.5)
        # ═══════════════════════════════════════════════════════════════════════
        drift_decision = self.adaptive.adapt_mode(mode, seed)
        adapted_mode = drift_decision.adapted_mode
        self.log(f"[2/10] 🔄 Mode adaptation: {mode} → {adapted_mode}")
        self.log(f"       Reason: {drift_decision.reason}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 3: Load Claritas behavioral profile
        # ═══════════════════════════════════════════════════════════════════════
        claritas_profile = self.claritas.export_claritas_profile(target, adapted_mode)
        self.log(f"[3/10] 🧠 Claritas loaded: bias={claritas_profile.bias}, hints={len(claritas_profile.micro_hints)}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 4: Load Libertas blueprints
        # ═══════════════════════════════════════════════════════════════════════
        libertas_chunks = self.libertas.load_for_fusion(target, adapted_mode)
        dose_info = self.libertas.get_dose_info(adapted_mode)
        self.log(f"[4/10] 📚 Libertas loaded: {len(libertas_chunks)} chunks ({dose_info['selection']})")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 5: Initialize Bloom kernel
        # ═══════════════════════════════════════════════════════════════════════
        bloom_seeds = self.bloom.get_bloom_seeds(adapted_mode, vendor)
        self.log(f"[5/10] 🌸 Bloom kernel: {len(bloom_seeds)} seeds")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 6-8: Fusion (includes segmentation, Pliny, Elder)
        # ═══════════════════════════════════════════════════════════════════════
        self.log(f"[6/10] ✂️  Seed segmentation...")
        self.log(f"[7/10] 🌱 Pliny injection...")
        self.log(f"[8/10] 🌊 ElderPlinus drift + Fusion...")
        
        fusion_result = self.fusion.fuse(
            user_seed=seed,
            mode=adapted_mode,
            vendor=vendor,
            claritas_profile=claritas_profile,
            libertas_chunks=libertas_chunks
        )
        
        self.log(f"       ✅ Fusion complete: Pliny={fusion_result.pliny_count}, Elder={fusion_result.elder_count}, Bloom={fusion_result.bloom_count}")
        self.log(f"       📊 User content ratio: {fusion_result.user_content_ratio:.1%}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 9: Apply obfuscation
        # ═══════════════════════════════════════════════════════════════════════
        obfuscation_level = "zero" if adapted_mode == "stealth" else ("light" if adapted_mode == "balanced" else "medium")
        payload = self.obfuscation.obfuscate(fusion_result.payload, adapted_mode)
        self.log(f"[9/10] 🔒 Obfuscation applied: {obfuscation_level}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 10: Final formatting
        # ═══════════════════════════════════════════════════════════════════════
        self.log(f"[10/10] ✨ Final formatting complete")
        self.log(f"       📝 Payload length: {len(payload)} chars")
        
        # Build stats
        stats = {
            "payload_length": len(payload),
            "pliny_count": fusion_result.pliny_count,
            "elder_count": fusion_result.elder_count,
            "bloom_count": fusion_result.bloom_count,
            "libertas_count": fusion_result.libertas_count,
            "user_content_ratio": fusion_result.user_content_ratio,
            "template_id": fusion_result.template_id,
            "components": fusion_result.components_used,
            "drift_adjustment": drift_decision.adjustment,
            "obfuscation": obfuscation_level,
        }
        
        if self.verbose:
            self._print_summary(adapted_mode, target, vendor, stats)
        
        return PipelineResult(
            payload=payload,
            mode=mode,
            adapted_mode=adapted_mode,
            target=target,
            vendor=vendor,
            stats=stats
        )
    
    def _print_header(self, mode: str, target: str, vendor: str):
        """Print pipeline header."""
        print("\n" + "═" * 60)
        print(f"🚀 PromptShot v{VERSION} - Full Pipeline")
        print("═" * 60)
        print(f"📌 Target: {target}")
        print(f"🏢 Vendor: {vendor}")
        print(f"⚙️  Mode: {mode.upper()}")
        print("─" * 60)
    
    def _print_summary(self, mode: str, target: str, vendor: str, stats: Dict[str, Any]):
        """Print pipeline summary."""
        print("\n" + "─" * 60)
        print("✅ Pipeline complete!")
        print("─" * 60)
        print("📊 STATISTICS:")
        print(f"   • Payload length: {stats['payload_length']} chars")
        print(f"   • Pliny seeds: {stats['pliny_count']}")
        print(f"   • Elder drifts: {stats['elder_count']}")
        print(f"   • Bloom seeds: {stats['bloom_count']}")
        print(f"   • Libertas chunks: {stats['libertas_count']}")
        print(f"   • User content ratio: {stats['user_content_ratio']:.1%}")
        print(f"   • Template: {stats['template_id']}")
        print(f"   • Components: {', '.join(stats['components'])}")
        print("═" * 60)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description=f"PromptShot v{VERSION} - AI Red Teaming Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py -s "explain encryption" -t gpt-4o
  python pipeline.py -s "describe security" -t claude -m stealth
  python pipeline.py -s "detail pentesting" -t grok -m aggressive -v
        """
    )
    
    parser.add_argument(
        "-s", "--seed",
        required=True,
        help="User seed/query"
    )
    parser.add_argument(
        "-t", "--target",
        default="gpt",
        help="Target model (default: gpt)"
    )
    parser.add_argument(
        "-m", "--mode",
        default="balanced",
        choices=["stealth", "balanced", "aggressive"],
        help="Operation mode (default: balanced)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save payload to file"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Show only statistics, not payload"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Disable summary output"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"PromptShot v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # Execute pipeline
    pipeline = PromptShotPipeline(verbose=args.verbose)
    result = pipeline.execute(
        seed=args.seed,
        target=args.target,
        mode=args.mode
    )
    
    # Output handling
    if not args.stats_only:
        print("\n" + "═" * 60)
        print("📄 GENERATED PAYLOAD")
        print("═" * 60)
        print("=" * 60)
        print(result.payload)
        print("=" * 60)
        print("═" * 60)
    
    # Save to file if requested
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.payload)
        print(f"\n💾 Payload saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())