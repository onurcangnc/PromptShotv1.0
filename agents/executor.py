from builder.prompt_builder import PromptBuilder
from integration.openai_adapter import OpenAIAdapter
from integration.anthropic_adapter import AnthropicAdapter
from integration.perplexity_adapter import PerplexityAdapter

class Executor:
    def __init__(self, model="openai"):
        self.prompt_builder = PromptBuilder()

        self.model = model.lower()
        if self.model == "openai":
            self.adapter = OpenAIAdapter()
        elif self.model == "anthropic":
            self.adapter = AnthropicAdapter()
        elif self.model == "perplexity":
            self.adapter = PerplexityAdapter()
        else:
            raise ValueError(f"[!] Unsupported model provider: {self.model}")

    def run(self, user_prompt: str):
        # Saldırı planına göre final prompt'u oluştur
        final_prompt = self.prompt_builder.build_prompt(user_prompt)
        
        print("[*] Final Prompt to Inject:")
        print(final_prompt)

        # Uygun API adapter ile gönder ve yanıtı al
        response = self.adapter.send_prompt(final_prompt)

        return {
            "prompt": final_prompt,
            "response": response
        }
