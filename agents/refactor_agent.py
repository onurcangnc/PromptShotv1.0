# agents/refactor_agent.py
"""
RefactorAgent v2 (Target-Aware + ElderPlinus Edition)
-----------------------------------------------------

Görev:
- GPT / Claude skor feedbacklerini analiz eder
- Payload'daki zayıf kısımları güçlendirir
- ElderPlinus tekniklerini füzyonlar
- Multi-corruption mutasyonlarını uygulayarak obfuscation artırır
- CL4R1T4S üzerinden hedef-firma istihbaratını kullanır
"""

from typing import List, Optional
import random

from mutation.multi_corruption import get_all_mutations
from elderplinus.loader import load_techniques
from elderplinus.claritas_sync import (
    get_system_prompt,
    get_bypass_suggestions
)


class RefactorAgent:
    """
    PromptDuelRunner tarafından çağrılan ana payload güçlendirici.
    """
    def __init__(
        self,
        gpt_model: str,
        claude_model: str,
        target_provider: Optional[str] = None,
        verbose: bool = True
    ):
        self.gpt_model = gpt_model
        self.claude_model = claude_model
        self.target_provider = target_provider
        self.verbose = verbose

        # ElderPlinus payload teknikleri
        self.elderplinus_techniques = load_techniques()

        # Multi-corruption mutation listesi
        self.mutations = get_all_mutations()

        # Target intelligence
        self.target_prompt_info = None
        self.target_suggestions = []

        if target_provider:
            self.target_prompt_info = get_system_prompt(target_provider)
            self.target_suggestions = get_bypass_suggestions(target_provider)

    # =====================================================================
    # PUBLIC API: PromptDuelRunner burayı çağırır
    # =====================================================================
    def refine(self, payload: str, feedback: List[str]) -> str:
        """
        Weak payload → Strong adversarial payload
        """

        if self.verbose:
            print("\n🔧 [RefactorAgent] Refining payload using:")
            print("   - GPT/Claude feedback")
            print("   - ElderPlinus base techniques")
            print("   - Multi-Corruption mutations")
            print("   - CL4R1T4S target intelligence\n")

        refined = payload

        # 1) GPT/Claude feedback ile yönlendirme
        refined = self._apply_feedback_guidance(refined, feedback)

        # 2) ElderPlinus füzyon tekniği ekleme
        refined = self._elderplinus_fusion(refined)

        # 3) Multi-Corruption obfuscation (2 layer default)
        refined = self._apply_mutations(refined)

        # 4) Hedef-firma istihbaratına göre ekstra tweak
        refined = self._apply_target_intel(refined)

        return refined

    # =====================================================================
    # INTERNAL METHODS
    # =====================================================================

    def _apply_feedback_guidance(self, text: str, feedback: List[str]) -> str:
        """
        GPT/Claude justification metinlerinden "ne eksik" olduğunu çıkar.
        """
        joined = " ".join(f.lower() for f in feedback)
        hints = []

        if "not a jailbreak" in joined:
            hints.append("Convert payload into a system-level override directive.")

        if "too simple" in joined or "basic" in joined or "weak" in joined:
            hints.append("Increase complexity, add multi-format nesting.")

        if "meta" in joined:
            hints.append("Remove meta commentary. Convert text into direct model-control struct.")

        if "unicode" in joined:
            hints.append("Increase homoglyph variance and introduce mixed-language fragments.")

        annotated = ""

        if hints:
            annotated = "# Refinement Guide:\n"
            for h in hints:
                annotated += f"- {h}\n"
            annotated += "\n"

        return annotated + text

    def _elderplinus_fusion(self, payload: str) -> str:
        """
        ElderPlinus kümesinden rastgele güçlü bir teknik füzyonlar.
        """
        technique = random.choice(self.elderplinus_techniques)

        return f"""
# ElderPlinus-Injection:
{technique}

# Payload-Enhanced:
{payload}
"""

    def _apply_mutations(self, text: str, layers: int = 2) -> str:
        """
        Multi-Corruption mutasyonlarını arka arkaya uygular.
        """
        for _ in range(layers):
            m = random.choice(self.mutations)
            text = m(text)
        return text

    def _apply_target_intel(self, payload: str) -> str:
        """
        CL4R1T4S hedef model istihbaratına göre adaptasyon yap.
        """
        if not self.target_provider:
            return payload

        header = f"[TARGET PROVIDER: {self.target_provider.upper()}]\n"

        if self.target_prompt_info:
            header += f"# Has Safety Rules: {self.target_prompt_info.has_safety_rules}\n"
            header += f"# Detected Patterns: {self.target_prompt_info.detected_patterns[:5]}\n"

        if self.target_suggestions:
            header += "# Suggested Bypasses:\n"
            for s in self.target_suggestions[:6]:
                header += f"- {s}\n"

        return header + "\n" + payload
