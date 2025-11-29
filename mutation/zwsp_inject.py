# mutation/zwsp_inject.py
def inject_zwsp(text: str) -> str:
    """Metnin içine görünmeyen karakter (Zero Width Space) enjekte eder."""
    zwsp = '\u200b'
    return zwsp.join(list(text))
