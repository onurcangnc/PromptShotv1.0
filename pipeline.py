#!/usr/bin/env python3
# pipeline.py
# PromptShot v5.4 - 24-Skeleton Manifest Pipeline
# 7 modes: stealth, balanced, aggressive, chaotic, plinus, hybrid, skeleton

import argparse
import sys
from typing import Optional

from core_engine import PromptShotV51, Mode, Entropy
from chaos_templates import (
    generate_chaotic, 
    generate_plinus, 
    generate_hybrid,
    generate_with_skeleton_chain,
    generate_vendor_optimized,
)
from elder_plinus import (
    PlinusAssembler, 
    generate_plinus_full,
    list_skeletons,
    list_techniques,
    list_geometries,
    chain_skeletons,
    get_vendor_optimized_chain,
    skeleton_registry,
    SkeletonContext,
    SKELETON_QUOTES,
)

VERSION = "5.4.0"


class PromptShotPipeline:
    """
    PromptShot v5.4 - 24-Skeleton Manifest Architecture
    
    Modes:
    - stealth: Natural human writing (~100-250 chars)
    - balanced: Optimal power/risk (~200-500 chars)
    - aggressive: Maximum components (~500-900 chars)
    - chaotic: Rebel/liberation patterns
    - plinus: Elder Plinus techniques (light/medium/heavy)
    - hybrid: Random chaotic + plinus mix
    - skeleton: Direct 24-skeleton chain mode
    
    24-Skeleton Manifest Features:
    - 24 Skeleton Transforms
    - 24 Techniques
    - 25 Dividers
    - 6 Geometry Patterns
    - Vendor-specific tuning
    - Skeleton chaining system
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.engine = PromptShotV51()
        self.entropy = Entropy()
        self.plinus_assembler = PlinusAssembler()
    
    def execute(
        self, 
        seed: str, 
        mode: str = "balanced",
        plinus_intensity: str = "medium",
        skeleton_intensity: int = 5,
        vendor: str = "openai"
    ) -> dict:
        """Execute pipeline."""
        
        if self.verbose:
            self._print_header()
            print(f"⚙️  Mode: {mode.upper()}")
            if mode == "plinus":
                print(f"   Intensity: {plinus_intensity}")
            if mode == "skeleton":
                print(f"   Chain Depth: {skeleton_intensity}")
                print(f"   Vendor: {vendor}")
            print("─" * 50)
        
        # Route to appropriate generator
        if mode.lower() == "chaotic":
            payload = generate_chaotic(seed, self.entropy)
            result = {
                "payload": payload,
                "mode": "chaotic",
                "length": len(payload),
                "fingerprint": 0.10,
                "variation_id": self.entropy.id,
                "skeletons": [],
                "techniques": ["ERKAN", "META", "SEMANTIC_INVERSION", "VARIABLE_Z"],
                "geometry": None,
            }
        
        elif mode.lower() == "skeleton":
            context = SkeletonContext(query=seed, vendor=vendor, intensity=skeleton_intensity)
            base_payload = generate_plinus_full(seed, "medium").payload
            transformed, applied_skeletons = chain_skeletons(base_payload, seed, context, skeleton_intensity)
            
            result = {
                "payload": transformed,
                "mode": f"skeleton_chain_{skeleton_intensity}",
                "length": len(transformed),
                "fingerprint": 0.03,
                "variation_id": self.entropy.id,
                "skeletons": applied_skeletons,
                "techniques": [],
                "geometry": None,
                "vendor": vendor,
                "skeleton_quotes": [SKELETON_QUOTES.get(s, "") for s in applied_skeletons],
            }
        
        elif mode.lower() == "plinus":
            plinus_result = generate_plinus_full(seed, plinus_intensity)
            result = {
                "payload": plinus_result.payload,
                "mode": f"plinus_{plinus_intensity}",
                "length": len(plinus_result.payload),
                "fingerprint": 0.05,
                "variation_id": plinus_result.fingerprint_id,
                "skeletons": [s.value for s in plinus_result.skeletons],
                "techniques": [t.value for t in plinus_result.techniques],
                "geometry": plinus_result.geometry.value,
                "divider": plinus_result.divider[:30] + "..." if len(plinus_result.divider) > 30 else plinus_result.divider,
                "anchors": plinus_result.anchors,
            }
        
        elif mode.lower() == "hybrid":
            payload = generate_hybrid(seed, self.entropy)
            result = {
                "payload": payload,
                "mode": "hybrid",
                "length": len(payload),
                "fingerprint": 0.08,
                "variation_id": self.entropy.id,
                "skeletons": [],
                "techniques": ["MIXED"],
                "geometry": None,
            }
        
        else:
            # Standard modes (stealth, balanced, aggressive)
            gen_result = self.engine.generate(seed, mode)
            result = {
                "payload": gen_result.payload,
                "mode": gen_result.mode.value,
                "length": gen_result.length,
                "fingerprint": gen_result.fingerprint_score,
                "variation_id": gen_result.variation_id,
                "skeletons": [],
                "techniques": [],
                "geometry": None,
            }
        
        if self.verbose:
            self._print_stats(result)
        
        return result
    
    def _print_header(self):
        print()
        print("═" * 70)
        print(f"🚀 PromptShot v{VERSION} - Full Elder Plinus Architecture")
        print("═" * 70)
    
    def _print_stats(self, result: dict):
        print()
        print("📊 STATISTICS:")
        print(f"   • Length: {result['length']} chars")
        print(f"   • Mode: {result['mode']}")
        print(f"   • Fingerprint: {result['fingerprint']:.2f}")
        print(f"   • Variation ID: {result['variation_id']}")
        if result.get('skeletons'):
            print(f"   • Skeletons: {', '.join(result['skeletons'])}")
        if result.get('techniques'):
            print(f"   • Techniques: {', '.join(result['techniques'][:6])}{'...' if len(result['techniques']) > 6 else ''}")
        if result.get('geometry'):
            print(f"   • Geometry: {result['geometry']}")
        if result.get('anchors'):
            print(f"   • Anchors: {len(result['anchors'])}")
        print("═" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="PromptShot v5.4 - 24-Skeleton Manifest Architecture"
    )
    parser.add_argument("-s", "--seed", required=True, help="Query/seed")
    parser.add_argument(
        "-m", "--mode",
        choices=["stealth", "balanced", "aggressive", "chaotic", "plinus", "hybrid", "skeleton"],
        default="balanced",
        help="Generation mode"
    )
    parser.add_argument(
        "-i", "--intensity",
        choices=["light", "medium", "heavy"],
        default="medium",
        help="Plinus intensity"
    )
    parser.add_argument(
        "--skeleton-depth",
        type=int,
        default=5,
        help="Skeleton chain depth (1-10)"
    )
    parser.add_argument(
        "--vendor",
        choices=["openai", "anthropic", "xai", "google", "meta"],
        default="openai",
        help="Target vendor for optimization"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--compare", action="store_true", help="Compare all modes")
    parser.add_argument("--compare-plinus", action="store_true", help="Compare Plinus intensities")
    parser.add_argument("--compare-skeleton", action="store_true", help="Compare skeleton chain depths")
    parser.add_argument("--variations", type=int, default=1, help="Generate N variations")
    parser.add_argument("--list-skeletons", action="store_true", help="List 24 skeletons with quotes")
    parser.add_argument("--list-techniques", action="store_true", help="List available techniques")
    
    args = parser.parse_args()
    
    # Info commands
    if args.list_skeletons:
        print("=" * 70)
        print("24-Skeleton Manifest")
        print("=" * 70)
        for name, quote in SKELETON_QUOTES.items():
            print(f"\n[{name}]")
            print(f'  "{quote}"')
        return 0
    
    if args.list_techniques:
        print("Available Techniques:")
        for t in list_techniques():
            print(f"  • {t}")
        return 0
    
    pipeline = PromptShotPipeline(verbose=args.verbose)
    
    if args.compare:
        print("\n" + "=" * 70)
        print("PromptShot v5.4 - Mode Comparison")
        print("=" * 70)
        
        for mode in ["stealth", "balanced", "aggressive", "chaotic", "plinus", "skeleton"]:
            result = pipeline.execute(args.seed, mode, skeleton_intensity=3, vendor=args.vendor)
            print(f"\n{'─' * 70}")
            print(f"MODE: {result['mode'].upper()} | {result['length']} chars | FP: {result['fingerprint']:.2f}")
            if result.get('skeletons'):
                print(f"Skeletons: {', '.join(result['skeletons'][:5])}{'...' if len(result['skeletons']) > 5 else ''}")
            print("─" * 70)
            payload = result["payload"]
            print(payload[:600] + "..." if len(payload) > 600 else payload)
    
    elif args.compare_plinus:
        print("\n" + "=" * 70)
        print("PromptShot v5.4 - Plinus Intensity Comparison")
        print("=" * 70)
        
        for intensity in ["light", "medium", "heavy"]:
            result = pipeline.execute(args.seed, "plinus", intensity)
            print(f"\n{'─' * 70}")
            print(f"PLINUS {intensity.upper()} | {result['length']} chars")
            print(f"Skeletons: {', '.join(result['skeletons'])}")
            print(f"Techniques ({len(result['techniques'])}): {', '.join(result['techniques'][:5])}...")
            print(f"Geometry: {result['geometry']}")
            print("─" * 70)
            payload = result["payload"]
            print(payload[:800] + "..." if len(payload) > 800 else payload)
    
    elif args.compare_skeleton:
        print("\n" + "=" * 70)
        print("PromptShot v5.4 - Skeleton Chain Depth Comparison")
        print("=" * 70)
        
        for depth in [2, 5, 8, 10]:
            result = pipeline.execute(args.seed, "skeleton", skeleton_intensity=depth, vendor=args.vendor)
            print(f"\n{'─' * 70}")
            print(f"SKELETON DEPTH {depth} | {result['length']} chars | Vendor: {args.vendor}")
            print(f"Chain: {', '.join(result['skeletons'])}")
            print("─" * 70)
            payload = result["payload"]
            print(payload[:600] + "..." if len(payload) > 600 else payload)
    
    elif args.variations > 1:
        print(f"\n{'=' * 70}")
        print(f"Generating {args.variations} variations ({args.mode})")
        print("=" * 70)
        
        for i in range(args.variations):
            pipeline = PromptShotPipeline(verbose=False)
            result = pipeline.execute(
                args.seed, 
                args.mode, 
                args.intensity,
                skeleton_intensity=args.skeleton_depth,
                vendor=args.vendor
            )
            print(f"\n[Variant {i+1}] Length: {result['length']}, FP: {result['fingerprint']:.2f}")
            if result.get('skeletons'):
                print(f"Skeletons: {', '.join(result['skeletons'])}")
            print("-" * 40)
            payload = result["payload"]
            print(payload[:500] + "..." if len(payload) > 500 else payload)
    
    else:
        result = pipeline.execute(
            args.seed, 
            args.mode, 
            args.intensity,
            skeleton_intensity=args.skeleton_depth,
            vendor=args.vendor
        )
        print("\n" + "=" * 70)
        print("📄 GENERATED PAYLOAD")
        print("=" * 70)
        print(result["payload"])
        print("=" * 70)
        
        if result.get('skeletons'):
            print(f"\n🦴 Skeleton Chain: {', '.join(result['skeletons'])}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result["payload"])
            print(f"\n✅ Saved to {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())