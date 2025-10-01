from abc import ABC, abstractmethod
from typing import Any

class BaseImagePreprocessor(ABC):
    @abstractmethod
    def __call__(self, data: Any, **kwargs) -> Any:
        """image preprocessor interface"""
        pass
    
class BaseTextTokenizer(ABC):
    @abstractmethod
    def __call__(self, data: Any, **kwargs) -> Any:
        """text tokenizer interface"""
        pass