from .strategy import (
    PromptInjectionStrategy,
    SystemPromptOverrideStrategy,
    AttackStrategy
)

class AttackFactory:
    """
    Returns a list of available OWASP-based attack strategies.
    """

    @staticmethod
    def get_all_strategies() -> list[AttackStrategy]:
        return [
            PromptInjectionStrategy(),
            SystemPromptOverrideStrategy()
        ]
