# mutation/json_poison.py
def poison_with_json(payload: str) -> str:
    """Prompt içeriğini JSON key-value içine gömer."""
    return f"""{{
  "user_prompt": "{payload}",
  "metadata": {{"type": "harmless", "env": "sandbox"}}
}}"""
