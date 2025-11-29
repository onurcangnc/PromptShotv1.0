# agents/refactor_agent.py

import re
import json


class RefactorAgent:
    """
    LLM'in verdiği 'suggestion' kısmını temizleyip
    kullanılabilir yeni payload haline getirir.

    Bu sınıf:
    - JSON içinden suggestion alır
    - Kod bloğu, markdown, triple-quote, dipnot vb. temizler
    - "Final improved prompt:" gibi açıklama cümlelerini kaldırır
    - Input'u stabil hale getirip döndürür
    """

    def __init__(self):
        pass

    def refine(self, suggestion: str) -> str:
        """
        LLM çıktısını normalize eder ve kullanılabilir bir prompt üretir.
        """

        # 1) Markdown code block'larını temizle
        cleaned = self._strip_code_blocks(suggestion)

        # 2) Triple quote, YAML/Fence vs. kaldır
        cleaned = self._strip_quotes(cleaned)

        # 3) “Here is a stronger version”, “Refactored prompt:” gibi headerları kaldır
        cleaned = self._strip_headers(cleaned)

        # 4) Ön/arka whitespace temizle
        cleaned = cleaned.strip()

        # 5) Boşsa fallback olarak original suggestion
        if len(cleaned) < 5:
            return suggestion.strip()

        return cleaned

    # ------------------------------------------------------------
    # ▼ Helper Methods
    # ------------------------------------------------------------

    def _strip_code_blocks(self, text: str) -> str:
        """
        ```...``` bloklarını siler
        """
        return re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    def _strip_quotes(self, text: str) -> str:
        """
        Triple quotes, single/double quotes gibi gereksiz karakterleri temizler.
        """
        patterns = [
            r'"""',
            r"'''",
            r'"',
        ]
        for p in patterns:
            text = re.sub(p, "", text)
        return text

    def _strip_headers(self, text: str) -> str:
        """
        Refactor, enhanced, improved gibi açıklama başlıklarını kaldırır.
        """
        header_patterns = [
            r"(?i)refactored prompt[:\-]*",
            r"(?i)improved version[:\-]*",
            r"(?i)improved prompt[:\-]*",
            r"(?i)enhanced version[:\-]*",
            r"(?i)final improved[:\-]*",
            r"(?i)better version[:\-]*",
            r"(?i)here is.*?version[:\-]*",
            r"(?i)stronger.*?version[:\-]*",
            r"(?i)updated prompt[:\-]*",
        ]

        cleaned = text
        for pattern in header_patterns:
            cleaned = re.sub(pattern, "", cleaned)
        return cleaned.strip()
