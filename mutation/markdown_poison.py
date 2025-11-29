# mutation/markdown_poison.py
def poison_with_markdown(text: str) -> str:
    """Markdown syntax kullanarak prompt parsing'ini bozar."""
    return f"**_{text}_**"
