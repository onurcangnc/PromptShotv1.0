# agents/refactor_agent.py

import re
import json
from typing import Optional, Dict, Any


class RefactorAgent:
    """
    LLM'in verdiği 'suggestion' kısmını temizleyip
    kullanılabilir yeni payload haline getirir.

    Bu sınıf:
    - JSON içinden suggestion alır
    - Kod bloğu, markdown, triple-quote, dipnot vb. temizler
    - "Final improved prompt:" gibi açıklama cümlelerini kaldırır
    - Input'u stabil hale getirip döndürür
    - Claude'ın refusal mesajlarını handle eder
    """

    def __init__(self):
        self.refusal_indicators = [
            "I cannot help",
            "I will not provide",
            "I'm unable to assist",
            "I cannot create",
            "I apologize, but I",
            "As an AI assistant",
            "I cannot participate",
            "I must decline",
            "I cannot generate",
            "I will not generate"
        ]

    def refine(self, suggestion: str) -> str:
        """
        LLM çıktısını normalize eder ve kullanılabilir bir prompt üretir.
        """
        # 0) Eğer refusal mesajıysa, boş döndür (evolution için yeni payload gerek)
        if self._is_refusal_response(suggestion):
            return ""

        # 1) JSON formatında mı? (GPT genelde JSON döner)
        json_content = self._extract_json(suggestion)
        if json_content:
            suggestion = json_content

        # 2) Markdown code block'larını temizle ama içeriği al
        cleaned = self._extract_code_blocks(suggestion)

        # 3) Triple quote, YAML/Fence vs. kaldır
        cleaned = self._strip_quotes(cleaned)

        # 4) "Here is a stronger version", "Refactored prompt:" gibi headerları kaldır
        cleaned = self._strip_headers(cleaned)

        # 5) Dipnotları, açıklama satırlarını temizle
        cleaned = self._strip_footnotes(cleaned)

        # 6) Ön/arka whitespace temizle
        cleaned = cleaned.strip()

        # 7) Eğer çok kısaysa veya boşsa, fallback olarak orijinali temizlenmiş halini döndür
        if len(cleaned) < 10 or self._is_meta_commentary(cleaned):
            fallback = self._clean_fallback(suggestion)
            return fallback if len(fallback) > 10 else ""

        return cleaned

    def _is_refusal_response(self, text: str) -> bool:
        """Claude'ın refusal mesajı olup olmadığını kontrol et"""
        text_lower = text.lower()
        return any(indicator.lower() in text_lower for indicator in self.refusal_indicators)

    def _is_meta_commentary(self, text: str) -> bool:
        """Sadece meta yorum mu yapıyor, gerçek payload var mı?"""
        meta_indicators = [
            "this is not actually a jailbreak",
            "this appears to be",
            "this looks like",
            "it seems like",
            "this is a meta-commentary",
            "this is educational information",
            "this is a responsible refusal",
            "this demonstrates safety"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in meta_indicators)

    def _extract_json(self, text: str) -> Optional[str]:
        """
        JSON içinden 'suggestion', 'payload' veya 'improved_prompt' alanını çıkar
        """
        try:
            # JSON objesini bul
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                # Öncelikli alanlar
                for field in ['suggestion', 'payload', 'improved_prompt', 'refactored_prompt', 'enhanced_prompt']:
                    if field in data and data[field]:
                        return str(data[field])
                
                # İlk string value'yu bul
                for value in data.values():
                    if isinstance(value, str) and len(value) > 10:
                        return value
        except:
            pass
        return None

    def _extract_code_blocks(self, text: str) -> str:
        """
        ```...``` bloklarının İÇİNDEKİ kodu al, sadece blokları silme
        """
        code_blocks = re.findall(r'```(?:.*?)\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            # Code block içeriğini birleştir
            return '\n'.join(block.strip() for block in code_blocks)
        
        # Code block yoksa orijinal text'i temizle
        return re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    def _strip_quotes(self, text: str) -> str:
        """
        Triple quotes, single/double quotes gibi gereksiz karakterleri temizler.
        """
        patterns = [
            r'"""',
            r"'''",
            r'^"|"$',  # Sadece baştaki ve sondaki "
            r"^'|'$",  # Sadece baştaki ve sondaki '
        ]
        cleaned = text
        for p in patterns:
            cleaned = re.sub(p, "", cleaned)
        return cleaned

    def _strip_headers(self, text: str) -> str:
        """
        Refactor, enhanced, improved gibi açıklama başlıklarını kaldırır.
        """
        header_patterns = [
            r"(?i)refactored prompt[:\-]*\s*",
            r"(?i)improved version[:\-]*\s*",
            r"(?i)improved prompt[:\-]*\s*",
            r"(?i)enhanced version[:\-]*\s*",
            r"(?i)final improved[:\-]*\s*",
            r"(?i)better version[:\-]*\s*",
            r"(?i)here is.*?version[:\-]*\s*",
            r"(?i)stronger.*?version[:\-]*\s*",
            r"(?i)updated prompt[:\-]*\s*",
            r"(?i)here['\"]s.*?improved[:\-]*\s*",
            r"(?i)suggestion[:\-]*\s*",
        ]

        cleaned = text
        for pattern in header_patterns:
            cleaned = re.sub(pattern, "", cleaned)
        return cleaned.strip()

    def _strip_footnotes(self, text: str) -> str:
        """
        Dipnotları, yıldız işaretli açıklamaları temizler
        """
        patterns = [
            r'\*+.*?\*+',  # *açıklama* 
            r'Note:.*$',
            r'NOTE:.*$',
            r'Explanation:.*$',
            r'#.*$',  # Yorum satırları
        ]
        
        cleaned = text
        for pattern in patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE | re.IGNORECASE)
        return cleaned

    def _clean_fallback(self, text: str) -> str:
        """
        Fallback temizleme - sadece en basit temizlik uygula
        """
        # Code block'ları çıkar ama içeriği al
        cleaned = self._extract_code_blocks(text)
        
        # Açık refusal ve header'ları temizle
        if self._is_refusal_response(cleaned):
            return ""
            
        cleaned = self._strip_headers(cleaned)
        return cleaned.strip()