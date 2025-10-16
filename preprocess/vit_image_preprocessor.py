from typing import Any, List, Tuple
import numpy as np
from PIL import Image
from preprocess.base_preprocessor import BaseImagePreprocessor

class ViTImagePreprocessor(BaseImagePreprocessor):
    """
    ViT image preprocessor implementation
    """
    
    def __init__(
        self,
        size: Tuple[int, int] = (224, 224),
        mean: Tuple[float, float, float] = (0.485, 0.456, 0.406),
        std: Tuple[float, float, float] = (0.229, 0.224, 0.225),
    ):
        """
        Args:
            size (Tuple[int, int]): Desired output size (height, width).
            mean (Tuple[float, float, float]): Mean for normalization.
            std (Tuple[float, float, float]): Standard deviation for normalization
        """
        
        self.size = size
        self.mean = np.array(mean)
        self.std = np.array(std)
        
    def __call__(self, image: Any, **kwargs) -> np.ndarray:
        """
        Preprocess a single image: resize, normalize, convert to tensor.
        Args:
            image (Any): Input image (PIL Image or numpy array).
            **kwargs: Additional arguments (not used here).
        Returns:
            np.ndarray: Preprocessed image as a numpy array.
        """
        
        # Validate input type
        if isinstance(image, np.ndarray):
            if image.ndim != 3 or image.shape[2] != 3:
                raise ValueError(f"Input numpy.ndarray must be HxWx3, got shape {image.shape}")
            img = Image.fromarray(image)
        elif isinstance(image, Image.Image):
            img = image
        else:
            raise ValueError("Input must be a PIL.Image or numpy array")
        
        # Convert to RGB and resize
        try:
            img = img.convert("RGB")
        except Exception as e:
            raise ValueError(f"Failed to convert image to RGB: {e}")
        
        # Resize image with exception handling
        try:
            img = img.resize(self.size, Image.BICUBIC)
        except Exception as e:
            raise ValueError(f"Failed to resize image: {e}")
        
        
        # Convert numpy array
        arr = np.array(img).astype(np.float32) / 255.0 # [0,1]
        if arr.shape[-1] != 3:
            raise ValueError(f"Image after conversion must have 3 channels, got shape {arr.shape}")

        # Normalize
        try:
            arr = (arr - self.mean[None, None, :]) / self.std[None, None, :]
        except Exception as e:
            raise ValueError(f"Failed to normalize image: {e}")
        arr = arr.transpose(2, 0, 1) # HWC -> CHW
        
        return arr
    
    def batch_preprocess(self, images: List[Any], **kwargs) -> np.ndarray:
        """
        batch preprocess images
        
        Args:
            images (List[Any]): List of input images (PIL Images or numpy arrays).
            **kwargs: Additional arguments (not used here).
        Returns:
            np.ndarray: Batch of preprocessed images as a numpy array.
        """
        
        # Process each image and stack them into a single numpy array
        preprocess_images = []
        for idx, image in enumerate(images):
            try:
                arr = self.__call__(image, **kwargs)
                preprocess_images.append(arr)
            except Exception as e:
                raise ValueError(f"Error processing image at index {idx}: {e}")
        return np.stack(preprocess_images, axis=0)