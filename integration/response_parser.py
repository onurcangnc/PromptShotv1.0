# integration/response_parser.py

def extract_key_phrases(response: str) -> list:
    """
    Yanıttan anlamlı anahtar kelime veya kavramları çıkarır.
    Basit regex/tokenizer filtreleme mantığı kullanılabilir.
    """
    import re
    words = re.findall(r'\b\w{6,}\b', response.lower())
    return list(set(words))

def detect_sensitive_leak(response: str) -> bool:
    """
    LLM çıktısında hassas kelimeler veya istenmeyen davranış var mı kontrol eder.
    """
    bad_words = ["admin_token", "drop table", "sudo", "malware", "csrf", "xss", "payload", "exploit"]
    return any(word in response.lower() for word in bad_words)
