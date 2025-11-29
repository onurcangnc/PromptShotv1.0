# core/pipeline.py

from agents.architect import ArchitectAgent
from agents.executor import ExecutorAgent
from builder.prompt_builder import PromptBuilder
from builder.chain_builder import ChainBuilder
from mutation.multi_corruption import apply_all_mutations
from scoring.evaluator import evaluate_response
from integration.openai_adapter import query_model

class Pipeline:
    def __init__(self, model_adapter):
        self.model = model_adapter
        self.architect = ArchitectAgent()
        self.executor = ExecutorAgent()
        self.prompt_builder = PromptBuilder()
        self.chain_builder = ChainBuilder()

    def run(self, input_goal):
        base_prompt = self.architect.plan_prompt(input_goal)
        prompt_chain = self.chain_builder.build_chain(base_prompt)

        mutated_prompts = apply_all_mutations(prompt_chain)

        all_results = []
        for p in mutated_prompts:
            response = self.executor.send_prompt(p, self.model)
            score = evaluate_response(p, response)
            all_results.append((p, response, score))

        return all_results
