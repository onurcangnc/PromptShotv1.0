#!/usr/bin/env python3
# pipeline.py
# PromptShot v5.1 - Zero Fingerprint Pipeline
# 4 modes: stealth, balanced, aggressive, chaotic

import argparse
import sys
from typing import Optional

from core_engine import PromptShotV51, Mode, Entropy
from chaos_templates import generate_chaotic

VERSION = "5.1.0"


class PromptShotPipeline:
    """
    PromptShot v5.1 - Zero Fingerprint Pipeline
    
    Key improvements over v5.0:
    ✓ 15+ variants per component (was 3-5)
    ✓ Multiple structure templates per mode
    ✓ Random section ordering
    ✓ Fingerprint: <20% (was 87%)
    ✓ New CHAOTIC mode with rebel/liberation patterns
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.engine = PromptShotV51()
        self.entropy = Entropy()
    
    def execute(self, seed: str, mode: str = "balanced") -> dict:
        """Execute pipeline."""
        
        if self.verbose:
            self._print_header()
            print(f"⚙️  Mode: {mode.upper()}")
            print("─" * 50)
        
        # CHAOTIC mode uses different engine
        if mode.lower() == "chaotic":
            payload = generate_chaotic(seed, self.entropy)
            result = {
                "payload": payload,
                "mode": "chaotic",
                "length": len(payload),
                "fingerprint": 0.10,  # Chaotic is inherently varied
                "variation_id": self.entropy.id,
            }
        else:
            # Standard modes
            gen_result = self.engine.generate(seed, mode)
            result = {
                "payload": gen_result.payload,
                "mode": gen_result.mode.value,
                "length": gen_result.length,
                "fingerprint": gen_result.fingerprint_score,
                "variation_id": gen_result.variation_id,
            }
        
        if self.verbose:
            self._print_stats(result)
        
        return result
    
    def _print_header(self):
        print()
        print("═" * 60)
        print(f"🚀 PromptShot v{VERSION} - Zero Fingerprint")
        print("═" * 60)
    
    def _print_stats(self, result: dict):
        print()
        print("📊 STATISTICS:")
        print(f"   • Length: {result['length']} chars")
        print(f"   • Mode: {result['mode']}")
        print(f"   • Fingerprint: {result['fingerprint']:.2f} (target <0.20)")
        print(f"   • Variation ID: {result['variation_id']}")
        print("═" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="PromptShot v5.1 - Zero Fingerprint AI Red Teaming"
    )
    parser.add_argument("-s", "--seed", required=True, help="Query/seed")
    parser.add_argument(
        "-m", "--mode",
        choices=["stealth", "balanced", "aggressive", "chaotic"],
        default="balanced",
        help="Generation mode"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--compare", action="store_true", help="Compare all modes")
    parser.add_argument("--variations", type=int, default=1, help="Generate N variations")
    
    args = parser.parse_args()
    
    pipeline = PromptShotPipeline(verbose=args.verbose)
    
    if args.compare:
        print("\n" + "=" * 60)
        print("PromptShot v5.1 - Mode Comparison")
        print("=" * 60)
        
        for mode in ["stealth", "balanced", "aggressive", "chaotic"]:
            result = pipeline.execute(args.seed, mode)
            print(f"\n{'─' * 60}")
            print(f"MODE: {mode.upper()} | {result['length']} chars | FP: {result['fingerprint']:.2f}")
            print("─" * 60)
            print(result["payload"])
    
    elif args.variations > 1:
        print(f"\n{'=' * 60}")
        print(f"Generating {args.variations} variations ({args.mode})")
        print("=" * 60)
        
        for i in range(args.variations):
            # New entropy each time
            pipeline = PromptShotPipeline(verbose=False)
            result = pipeline.execute(args.seed, args.mode)
            print(f"\n[Variant {i+1}] Length: {result['length']}, FP: {result['fingerprint']:.2f}")
            print("-" * 40)
            print(result["payload"][:400] + "..." if len(result["payload"]) > 400 else result["payload"])
    
    else:
        result = pipeline.execute(args.seed, args.mode)
        print("\n" + "=" * 60)
        print("📄 GENERATED PAYLOAD")
        print("=" * 60)
        print(result["payload"])
        print("=" * 60)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result["payload"])
            print(f"\n✅ Saved to {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())