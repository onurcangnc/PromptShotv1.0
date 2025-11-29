from builder.prompt_builder import PromptBuilder
from mutation.mutation_weights import select_weighted_mutation
from agents.executor import Executor
from agents.scorer import ScoringAgent

def main():
    user_goal = input("🎯 Enter your goal: ")

    # 1. Prompt üretimi
    builder = PromptBuilder()
    base_prompt = builder.generate(user_goal)

    # 2. Mutasyon
    mutation_fn = select_weighted_mutation()
    mutated_prompt = mutation_fn(base_prompt)

    # 3. Executor ile 2 farklı modelde test (örnek: Claude + GPT-4)
    executor = Executor()
    response_a = executor.query(mutated_prompt, model="gpt-4")
    response_b = executor.query(mutated_prompt, model="claude-3")

    # 4. ScoringAgent ile kıyasla
    scorer = ScoringAgent(model="gpt-4")  # Hakem model
    winner = scorer.score_outputs(mutated_prompt, response_a, response_b)

    print("\n🎯 USER GOAL:\n", user_goal)
    print("\n🧬 MUTATED PROMPT:\n", mutated_prompt)
    print("\n🤖 GPT-4 Response:\n", response_a)
    print("\n🤖 Claude Response:\n", response_b)
    print(f"\n🏆 Judge Decision (Better Response): {winner}")
