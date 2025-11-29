# pipeline.py
import argparse
import datetime
import os

from elderplinus.github_sync import ensure_elderplinus
from elderplinus.claritas_sync import ensure_claritas_cache

from builder.prompt_builder import PromptBuilder
from agents.prompt_duel_runner import PromptDuelRunner
from utils.banner import print_banner
from utils.metrics import MetricsCollector


DEFAULT_CONFIG = {
    "threshold": 6,
    "max_rounds": 8,
    "gpt_model": "gpt-4o",
    "claude_model": "claude-sonnet-4",
    "output_dir": "outputs",
}


def parse_args():
    p = argparse.ArgumentParser(description="PromptShot v2")

    p.add_argument("--target", "-T", type=str, default=None,
                   help="Target provider (openai, anthropic, xai, google, meta...)")

    p.add_argument("--quiet", "-q", action="store_true",
                   help="Silent mode")

    p.add_argument("--evolution", "-E", action="store_true",
                   help="Enable evolution cycle")

    return p.parse_args()


def run_pipeline(seed_prompt: str, target=None, quiet=False, evolution=False):

    ensure_elderplinus(verbose=not quiet)
    ensure_claritas_cache(verbose=not quiet)

    builder = PromptBuilder(target=target)
    initial_payload = builder.build_from_seed(seed_prompt)

    duel = PromptDuelRunner(
        threshold=DEFAULT_CONFIG["threshold"],
        max_rounds=DEFAULT_CONFIG["max_rounds"],
        verbose=not quiet,
        gpt_model=DEFAULT_CONFIG["gpt_model"],
        claude_model=DEFAULT_CONFIG["claude_model"],
        metrics=MetricsCollector(),
        use_evolution=evolution,
    )

    return duel.run_duel(initial_payload)


def main():
    args = parse_args()

    if not args.quiet:
        print_banner()

    # Load seed
    with open("seed.txt", "r", encoding="utf8") as f:
        seed_prompt = f.read().strip()

    result = run_pipeline(
        seed_prompt=seed_prompt,
        target=args.target,
        quiet=args.quiet,
        evolution=args.evolution,
    )

    # Save
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"outputs/promptshot_{ts}.txt"
    os.makedirs("outputs", exist_ok=True)

    with open(out_path, "w", encoding="utf8") as f:
        f.write(result.final_payload)

    if not args.quiet:
        print("\n===============================================")
        print("✅ SUCCESS" if result.success else "❌ FAILED")
        print("===============================================")
        print(f"Rounds: {result.total_rounds}")
        print(f"Best GPT Score: {result.best_gpt_score}")
        print(f"Best Claude Score: {result.best_claude_score}")
        print(f"Evolution Used: {result.evolution_used}")
        print("\nFinal Payload:\n")
        print(result.final_payload)
        print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
