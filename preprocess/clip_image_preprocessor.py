from typing import Any, List, Tuple
import numpy as np
from PIL import Image
from preprocess.base_preprocessor import BaseImagePreprocessor

class CLIPImagePreprocessor(BaseImagePreprocessor):
    """
    CLIP image preprocessor implementation
    """
    
    def __init__(
        self,
        size: Tuple[int, int] = (224, 224),
        mean: Tuple[float, float, float] = (0.48145466, 0.4578275, 0.40821073),
        std: Tuple[float, float, float] = (0.26862954, 0.26130258, 0.27577711),
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
    
    def __call__(self, image: Any, **kwargs) -> Any:
        """
        Preprocess a single image: resize, normalize, convert to tensor.
        Args:
            image (Any): Input image (PIL Image or numpy array).
            **kwargs: Additional arguments (not used here).
        Returns:
            Any: Preprocessed image as a numpy array.
        """
        # Validate input type
        if isinstance(image, np.ndarray):
            if image.ndim != 3 or image.shape[2] != 3:
                raise ValueError(f"Input numpy.ndarray must be HxWx3, got shape {image.shape}")
            img = Image.fromarray(image) # Convert numpy array to PIL Image
        elif isinstance(image, Image.Image):
            img = image
        else:
            raise ValueError("Input must be a PIL.Image or numpy array")
        
        #resize image
        img = img.convert("RGB")  # Ensure image is in RGB format
        img = img.resize(self.szie, Image.BICUBIC)
        
        # convert to numpy array
        arr = np.array(img).astype(np.float32) / 255.0  # Scale to [0, 1]
        if arr.shape[-1] != 3:
            raise ValueError(f"Input image must be a PIL.Image or numpy.ndarray")
        
        # normalize
        arr = (arr - self.mean[None, None, :]) / self.std[None, None, :]
        arr = arr.transpose(2, 0, 1) # HWC -> CHW
        
        return arr
    
    def batch_preprocess(self, images: List[Any], **kwargs) -> List[np.ndarray]:
        """
        Batch preprocess a list of images.
        Args:
            images (List[Any]): List of input images (PIL Images or numpy arrays).
            **kwargs: Additional arguments (not used here).
            
        Returns:
            np.ndarray: Batch of preprocessed images as a numpy array.
        """
        # Process each image and stack them into a single numpy array
        preprocessed_images = [self.__call__(image, **kwargs) for image in images]
        return np.stack(preprocessed_images, axis=0)
    
        