# integration/anthropic_adapter.py

import anthropic

class AnthropicAdapter:
    def __init__(self, api_key, model="claude-2"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def send_prompt(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
