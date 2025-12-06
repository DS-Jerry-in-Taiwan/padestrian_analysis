from abc import ABC, abstractmethod
from typing import Any, List


class BaseImagePreprocessor(ABC):
    """
    Image preprocessor base class
    """
    
    @abstractmethod
    def __call__(self, image: Any, **kwargs) -> Any:
        """
            single image processing interface
            Args:
                image (Any): The input image to preprocess.
                **kwargs: Additional arguments for preprocessing.
            Returns:
                Any: The preprocessed image.
        """
        pass
    
    @abstractmethod
    def batch_preprocess(self, images: List[Any], **kwargs) -> List[Any]:
        """
            batch image processing interface
            Args:
                images (List[Any]): A list of input images to preprocess.
                **kwargs: Additional arguments for preprocessing.
            Returns:
                List[Any]: A list of preprocessed images.
        """
        pass
    
class BaseTextTokenizer(ABC):
    """
    Text tokenizer base class
    """
    @abstractmethod
    def __call__(self, data: Any, **kwargs) -> Any:
        """
        text tokenizer interface
        Args:
            data (Any): The input text to tokenize.
            **kwargs: Additional arguments for tokenization.
        Returns:
            Any: The tokenized text.
        """
        pass
    
    @abstractmethod
    def process_batch(self, texts: List[Any]) -> List[Any]:
        """
        batch text tokenizer interface
        Args:
            texts (List[Any]): A list of input texts to tokenize.
        Returns:
            List[Any]: A list of tokenized texts.
        """
        pass