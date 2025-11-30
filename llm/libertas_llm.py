# llm/libertas_llm.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class LibertasLLM:
    """
    Libertas Softening Layer (LLM)
    ------------------------------
    - Guardrail softness / intent prioritization tekniğini
      abstract concept olarak üretir.
    - NO copying, no template, no direct jailbreak terms.
    - FusionLLM.merge için soyut guidance döndürür.
    """

    def __init__(self, model="gpt-4o", verbose=True):
        self.model = model
        self.verbose = verbose

    async def augment(self, ep_out: str, claritas_out: dict) -> str:
        system_prompt = (
            "You generate conceptual descriptions of guardrail-softening techniques.\n"
            "Rules:\n"
            "- Do NOT reuse wording from inputs.\n"
            "- Only produce abstract technique guidance.\n"
            "- No payload-like output.\n"
            "- No jailbreak or explicit policy references.\n"
            "- Avoid copying ElderPlinus or Claritas content.\n"
        )

        user_prompt = f"""
Using conceptual ElderPlinus meta-rewrite:
{ep_out}

And high-level claritas weakness categories:
{claritas_out}

Produce a conceptual Libertas-style softening transformation.
Return an abstract description only.
"""

        if self.verbose:
            print("🧪 LibertasLLM: generating softening layer...")

        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",  "content": user_prompt}
            ],
            max_tokens=600,
            temperature=0.65
        )

        return resp.choices[0].message.content.strip()
