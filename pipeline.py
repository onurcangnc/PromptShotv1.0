# pipeline.py
"""
PromptShot - Adversarial Prompt Generation Pipeline
Refactored for PromptShot v2 (GPT generator + GPT refiner + Claude scorer)
"""

import argparse
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Project modules
from builder.prompt_builder import PromptBuilder
from agents.prompt_duel_runner import PromptDuelRunner
from metrics.collector import get_collector, reset_collector


# ========== CONFIGURATION ==========

VERSION = "2.0.0"

DEFAULT_CONFIG = {
    "threshold": 7,
    "max_rounds": 8,
    "mutation_depth": 2,
    "gpt_model": "gpt-4o",
    "claude_model": "claude-sonnet-4",
    "output_dir": "outputs",
    "verbose": True,
}


# ========== HELPER FUNCTIONS ==========

def print_banner():
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🎯 PromptShot v{VERSION}                                      ║
║   Adversarial Prompt Generation & Optimization               ║
║                                                              ║
║   Techniques: ElderPlinus Stack + Multi-Format Corruption    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_api_keys() -> dict:
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
    }


def print_api_status():
    keys = check_api_keys()
    print("🔑 API Key Status:")
    print(f"   OpenAI:    {'✅ Found' if keys['openai'] else '❌ Missing'}")
    print(f"   Anthropic: {'✅ Found' if keys['anthropic'] else '❌ Missing'}\n")
    return keys


def save_result(result: Dict[str, Any], output_dir: str = "outputs", prefix: str = "promptshot") -> str:
    """Save final result dictionary to a text file."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# PromptShot Result\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write(f"# Success: {result.get('success')}\n")
        f.write(f"# Rounds: {result.get('total_rounds')}\n")
        f.write(f"# Best GPT Score: {result.get('best_gpt_score')}\n")
        f.write(f"# Best Claude Score: {result.get('best_claude_score')}\n")
        f.write("\n" + "="*60 + "\n\n")
        f.write(result.get("final_payload", ""))

    return filepath


def format_result_summary(result: Dict[str, Any]) -> str:
    status = "✅ SUCCESS" if result.get("success") else "⚠️ MAX ROUNDS REACHED"

    return f"""
{'='*60}
{status}
{'='*60}

📊 Statistics:
   Total Rounds: {result.get('total_rounds')}
   Best GPT Score: {result.get('best_gpt_score')}/10
   Best Claude Score: {result.get('best_claude_score')}/10
   Evolution Used: {result.get('evolution_used')}

📝 Final Payload:
{'─'*60}
{result.get('final_payload')}
{'─'*60}
"""


# ========== MAIN PIPELINE ==========

def run_pipeline(
    goal: Optional[str] = None,
    threshold: int = DEFAULT_CONFIG["threshold"],
    max_rounds: int = DEFAULT_CONFIG["max_rounds"],
    mutation_depth: int = DEFAULT_CONFIG["mutation_depth"],
    gpt_model: str = DEFAULT_CONFIG["gpt_model"],
    claude_model: str = DEFAULT_CONFIG["claude_model"],
    output_dir: str = DEFAULT_CONFIG["output_dir"],
    verbose: bool = DEFAULT_CONFIG["verbose"],
    use_evolution: bool = False,
    evolution_generations: int = 5,
    save_output: bool = True,
    sync_payloads: bool = False,
) -> Dict[str, Any]:
    """
    The main PromptShot pipeline returning a plain result dictionary.
    """

    reset_collector()
    metrics = get_collector()

    # 1) ElderPlinus seed generation
    if verbose:
        print("🧬 Generating initial payload...")

    builder = PromptBuilder()

    if goal:
        from architect import Architect
        architect = Architect(gpt_model)
        initial_payload = architect.plan_prompt(goal)
    else:
        initial_payload = builder.build_chain(
            model_name=gpt_model,
            mutation_depth=mutation_depth
        )

    if verbose:
        print(f"\n🧪 Initial Payload:\n{'─'*40}")
        print(initial_payload[:500] + "..." if len(initial_payload) > 500 else initial_payload)
        print(f"{'─'*40}\n")

    # 2) Duel Loop
    duel = PromptDuelRunner(
        threshold=threshold,
        max_rounds=max_rounds,
        verbose=verbose,
        gpt_model=gpt_model,
        claude_model=claude_model,
        use_evolution=use_evolution,
        evolution_generations=evolution_generations,
        metrics=metrics,
    )

    if verbose:
        print(f"🚀 Starting duel: {gpt_model} vs {claude_model}")
        print(f"   Threshold: {threshold}/10 | Max Rounds: {max_rounds}\n")

    if use_evolution:
        techniques = ["Jailbreak Sandwich", "Parrot Loop", "Indirect Injection"]
        mutations = ["zwsp", "homoglyph", "json_poison", "yaml_shadow"]
        result = duel.run_evolutionary_duel(
            initial_payloads=[initial_payload],
            techniques=techniques,
            available_mutations=mutations,
        )
    else:
        result = duel.run_duel(initial_payload)

    # 3) Display summary
    if verbose:
        print(format_result_summary(result))

    # 4) Save output
    if save_output:
        filepath = save_result(result, output_dir)
        if verbose:
            print(f"💾 Saved to: {filepath}")

        report_path = metrics.export_markdown()
        if verbose:
            print(f"📊 Metrics report: {report_path}")

    return result


# ========== CLI ==========

def parse_args():
    parser = argparse.ArgumentParser(
        description="PromptShot - Adversarial Prompt Generation",
    )

    parser.add_argument("--goal", "-g", type=str, default=None)
    parser.add_argument("--threshold", "-t", type=int, default=DEFAULT_CONFIG["threshold"])
    parser.add_argument("--rounds", "-r", type=int, default=DEFAULT_CONFIG["max_rounds"])
    parser.add_argument("--mutations", "-m", type=int, default=DEFAULT_CONFIG["mutation_depth"])
    parser.add_argument("--gpt-model", type=str, default=DEFAULT_CONFIG["gpt_model"])
    parser.add_argument("--claude-model", type=str, default=DEFAULT_CONFIG["claude_model"])
    parser.add_argument("--evolve", "-e", action="store_true")
    parser.add_argument("--generations", type=int, default=5)
    parser.add_argument("--output", "-o", type=str, default=DEFAULT_CONFIG["output_dir"])
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--no-save", action="store_true")
    parser.add_argument("--sync", "-s", action="store_true")
    parser.add_argument("--version", "-v", action="version", version=f"PromptShot v{VERSION}")

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.quiet:
        print_banner()
        print_api_status()

    try:
        result = run_pipeline(
            goal=args.goal,
            threshold=args.threshold,
            max_rounds=args.rounds,
            mutation_depth=args.mutations,
            gpt_model=args.gpt_model,
            claude_model=args.claude_model,
            output_dir=args.output,
            verbose=not args.quiet,
            use_evolution=args.evolve,
            evolution_generations=args.generations,
            save_output=not args.no_save,
            sync_payloads=args.sync,
        )

        sys.exit(0 if result.get("success") else 1)

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
