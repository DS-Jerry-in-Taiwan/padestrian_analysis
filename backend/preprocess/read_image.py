import cv2
import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from typing import Union, List, Optional, Dict, Any




class DetectionImagePreprocessor:
    def __init__(self, size=(224,224), mean=None, std=None, model_type='default', use_center_crop=None):
        """
        Args:
            size (tuple): Desired output size (height, width).
            mean (list): Mean for normalization.
            std (list): Standard deviation for normalization.
            model_type (str): Type of model to determine preprocessing steps.
        """
        # Initialize the preprocessor with desired size, mean, and std for normalization
        self.model_type = model_type
        self.size = size
        config = self.get_model_config(model_type)
        self.mean = mean if mean is not None else config['mean']
        self.std = std if std is not None else config['std']
        self.interpolation = config['interpolation']
        self.use_center_crop = use_center_crop if use_center_crop is not None else config['use_center_crop']
        # Create the transformation pipeline
        self.transform = self.build_transform()

    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """根據模型類型返回預設配置"""
        configs = {
            'clip': {
                'mean': [0.48145466, 0.4578275, 0.40821073],
                'std': [0.26862954, 0.26130258, 0.27577711],
                'interpolation': transforms.InterpolationMode.BICUBIC,
                'use_center_crop': True
            },
            'openclip': {
                'mean': [0.48145466, 0.4578275, 0.40821073],
                'std': [0.26862954, 0.26130258, 0.27577711],
                'interpolation': transforms.InterpolationMode.BICUBIC,
                'use_center_crop': True
            },
            'vit': {
                'mean': [0.5, 0.5, 0.5],  # ViT 常用參數
                'std': [0.5, 0.5, 0.5],
                'interpolation': transforms.InterpolationMode.BICUBIC,
                'use_center_crop': True
            },
            'default': {
                'mean': [0.485, 0.456, 0.406],  # ImageNet 標準
                'std': [0.229, 0.224, 0.225],
                'interpolation': transforms.InterpolationMode.BILINEAR,
                'use_center_crop': False
            }
        }
        return configs.get(model_type, configs['default'])

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.transform = self.build_transform()
    
    def build_transform(self) -> transforms.Compose:
        """
        Build the transformation pipeline based on the provided parameters
        """
        # Initialize the list of transformations
        transform_list = [transforms.ToPILImage()]
        
        # Resize the image
        transform_list.append(transforms.Resize(self.size, interpolation=self.interpolation))
    
        # Optionally apply center crop
        if self.use_center_crop:
            transform_list.append(transforms.CenterCrop(self.size))
        
        # conver image to tensor
        transform_list.append(transforms.ToTensor())
        
        # Normalize the image
        transform_list.append(transforms.Normalize(mean=self.mean, std=self.std))
        
        return transforms.Compose(transform_list)
    
    def __call__(self, img: Union[np.ndarray, Image.Image]) -> torch.Tensor:
        """
        Args:
            img (numpy array): The image to be preprocessed.
        Returns:
            Tensor: The preprocessed image tensor.
        """
        if isinstance(img, np.ndarray):
            return self.transform(img)
        elif isinstance(img, Image.Image):
            return self.transform(np.array(img))
        else:
            raise ValueError("Input should be a numpy array or PIL Image.")
    
    def batch(self, imgs: Union[List[np.ndarray], List[Image.Image]]) -> List[torch.Tensor]:
        """
        preprocess a batch of images
        Args:
            imgs (list of numpy arrays): The list of images to be preprocessed.
        Returns:
            Tensor(List[torch.Tensor]): The preprocessed image tensor batch.
        """
        
        return [self.__call__(img) for img in imgs]
    
    def batch_stack(self, imgs: List[Union[np.ndarray, Image.Image]]) -> torch.Tensor:
        """
        Preprocess a batch of images and stack them into a single tensor
        Args:
            imags (list of numpy arrays): The list of images to be preprocessed.
        Returns:
            Tensor: The stacked preprocessed image tensor batch.
        """
        processed = self.batch(imgs)
        return torch.stack(processed, dim=0)

def read_image(file_path):
    """
    Reads an image from the specified file path and returns the image object.
    
    Args:
        file_path (str): The path to the image file.
    Returns:
        Image object: The image read from the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
        return img
    except Exception as e:
        raise IOError(f"An error occurred while reading the image: {e}")
    
def read_images(file_path):
    """
    Reads batch of images from the specified file path and returns a list of image objects.
    
    Returns:
        list: A list of image objects read from the files.
    """
    
    images = []
    errors = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The directory {file_path} does not exist.")
    
    img_list = os.listdir(file_path)[:20]
    for img_name in img_list:
        try:
            img = read_image(os.path.join(file_path, img_name))
            images.append(img)
        except Exception as e:
            errors.append((img_name, str(e)))
            print(f"Warning: Failed to read {img_name}: {e}")
            continue
    return images




if __name__ == "__main__":
    img_path = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/PA-100K/data"
    img_list = read_images(img_path)
    preprocessor = Preprocessor(size=(224, 224))
    processed_imgs = preprocessor.batch(img_list)
    print(processed_imgs[0])  # 應為 torch.Size([3, 224, 224])
    # for img in img_list[:3]:
    #     cv2.imshow("Image", img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
