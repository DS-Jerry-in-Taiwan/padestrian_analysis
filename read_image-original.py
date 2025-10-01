from PIL import Image
import os
import torchvision.transforms as transforms
import numpy as np

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
        img = Image.open(file_path)
        img = img.convert('RGB')
        return img
    except Exception as e:
        raise IOError(f"An error occurred while reading the image: {e}")
        return None
    
def read_images(file_path):
    """
    Reads batch of images from the specified file path and returns a list of image objects.
    
    Returns:
        list: A list of image objects read from the files.
    """
    
    images = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The directory {file_path} does not exist.")
    try:
        img_list = os.listdir(file_path)[:20]
        for img_name in img_list:
            img = read_image(os.path.join(file_path, img_name))
            images.append(img)
    except Exception as e:
        raise IOError(f"An error occurred while reading the images: {e}")
    return images

def resize_image(img, size, interpolation=Image.BILINEAR):
    """
    Resizes the given image to the specified size.
    
    Args:
        img (Image object): The image to be resized.
        size (tuple): The desired size as (width, height).
        
    Returns:
        Image object: The resized image.
    """
    if not isinstance(img, Image.Image):
        raise TypeError("The provided img is not a valid Image object.")
    if not (isinstance(size, tuple) and len(size) == 2):
        raise ValueError("Size must be a tuple of (width, height).")

    return img.resize(size, interpolation)

def resize_images(img_list, size, interpolation=Image.BILINEAR):
    """
    Resizes a list of images to the specified size.
    
    Args:
        img_list (list): A list of Image objects to be resized.
        size (tuple): The desired size as (width, height).
        
    Returns:
        list: A list of resized Image objects.
    """
    if not isinstance(img_list, list):
        raise TypeError("img_list must be a list of Image objects.")
    
    resized_images = []
    for img in img_list:
        resized_img = resize_image(img, size, interpolation)
        resized_images.append(resized_img)
    
    return resized_images




if __name__ == "__main__":
    img_path = "/home/ubuntu/projects/pedestrian_attribute_recognition_0%/data/PA-100K/data"
    img_list = read_images(img_path)
    img_list = normalize_image(img_list, mode="0-1")
    for img in img_list[:1]:
        img = resize_image(img, (256, 256))
        img.show()
        # print(f"Image {img_name} read successfully with size {img.size}")
