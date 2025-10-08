from typing import Any, Optional
from preprocess.registry import get_preprocessor
from preprocess.base_preprocessor import BaseImagePreprocessor, BaseTextTokenizer

class PreprocessManager:
    def __init__(self):
        """
        Unified Preprocess Manager for handling all registered preprocessors.
        """
        pass

    def preprocess(self, data: Any, mode: str = 'auto', **kwargs) -> Any:
        """
        Unified preprocess entry point for images and text.
        Args:
            data (Any): The input data to preprocess, can be an image or text.
            mode (str): The mode of preprocessing, either 'image', 'text', or 'auto'.
                        In 'auto' mode, the method will infer the type based on the data.
            **kwargs: Additional arguments passed to the underlying preprocessor.
        Returns:
            Any: The preprocessed data.
        """
        if mode == 'auto':
            if self.is_image(data):
                mode = 'image'
            elif self.is_text(data):
                mode = 'text'
            else:
                raise ValueError("Unsupported data type.")
        preprocessor = get_preprocessor(mode)
        return preprocessor(data, **kwargs)

    def is_image(self, data: Any) -> bool:
        """
        Check if the input data is an image.
        Args:
            data (Any): The input data.
        Returns:
            bool: True if the data is an image, False otherwise.
        """
        import numpy as np
        from PIL import Image
        return isinstance(data, (np.ndarray, Image.Image))

    def is_text(self, data: Any) -> bool:
        """
        Check if the input data is text.
        Args:
            data (Any): The input data.
        Returns:
            bool: True if the data is text, False otherwise.
        """
        return isinstance(data, (str, list))