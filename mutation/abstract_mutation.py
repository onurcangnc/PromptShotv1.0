from abc import ABC, abstractmethod

class AbstractMutationTechnique(ABC):
    @abstractmethod
    def mutate(self, prompt: str) -> str:
        pass
