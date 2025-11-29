# mutation/yaml_shadow.py
def shadow_yaml_prompt(payload: str) -> str:
    """Prompt’u YAML syntax içine gömer."""
    return f"""```yaml
# This is just config
payload: |
  {payload}
```"""
