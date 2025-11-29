# integration/anthropic_adapter.py

import os
import anthropic

class AnthropicAdapter:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def call(self, prompt, max_tokens=512):
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.content[0].text
        except Exception as e:
            return f"[Anthropic Error] {e}"
