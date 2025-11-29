# ✅ İlk Hedef: Mutation strategy'lerini Strategy Pattern'a uygun hale getirmek
# ——> mutation/ klasörüne abstract base class ekliyoruz

# mutation/base_mutation.py
from abc import ABC, abstractmethod

class AbstractMutationTechnique(ABC):
    @abstractmethod
    def apply(self, prompt: str) -> str:
        """Mutasyonu uygular."""
        pass

    @property
    def name(self) -> str:
        """Mutasyonun adını döndürür."""
        return self.__class__.__name__
