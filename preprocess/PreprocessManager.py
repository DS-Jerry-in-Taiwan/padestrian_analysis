from typing import Any, Optional
from preprocess.base_preprocessor import BaseImagePreprocessor, BaseTextTokenizer

class PreprocessManager:
    def __init__(self, image_preprocessor: Optional[BaseImagePreprocessor] = None, text_tokenizer: Optional[BaseTextTokenizer] = None):
        """
            Unified Preprocess Manager for handling image and text preprocessing
            Args:
                image_preprocessor (Optional[BaseImagePreprocessor]): An image preprocessing object with a `preprocess` method.
                text_tokenizer (Optional[BaseTextTokenizer]): A text tokenizer object with a `tokenize` method.
        """
        self.image_preprocessor = image_preprocessor
        self.text_tokenizer = text_tokenizer

    def preprocess(self, data: Any, mode: str = 'auto', **kwargs) -> Any:
        """
            Unified preprocess entry point for images and text
            Args:
                data (Any): The input data to preprocess, can be an image or text.
                mode (str): The mode of preprocessing, either 'image', 'text', or 'auto'.
                            In 'auto' mode, the method will infer the type based on the data.
            Returns:
                Any: The preprocessed data.
        """
        if mode == 'image' or (mode == 'auto' and self.is_image(data)):
            if self.image_preprocessor is None:
                raise ValueError("Image preprocessor is not provided.")
            return self.image_preprocessor(data, **kwargs)
        elif mode == 'text' or (mode == 'auto' and self.is_text(data)):
            if self.text_tokenizer is None:
                raise ValueError("Text tokenizer is not provided.")
            return self.text_tokenizer(data, **kwargs)
        else:
            raise ValueError("Unsupported mode. Choose from 'image', 'text'.")
        
    def is_image(self, data: Any) -> bool:
        import numpy as np
        from PIL import Image
        return isinstance(data, (np.ndarray, Image.Image))
    
    def is_text(self, data: Any) -> bool:
        return isinstance(data, (str, list))