from typing import List, Dict, Any, Callable
import torch
from PIL import Image
import numpy as np
from preprocess.read_image import Preprocessor
from models.attribute_analyzer_base import AttributeAnalyzerBase

class PromptBasedAttributeAnalyzer(AttributeAnalyzerBase):
    def __init__(self, model, attribute_names: List[str], device: torch.device, preprocess: Preprocessor, prompt: List[str]):
        """
            Args:
                model: pre-trained model for attribute analysis.
                attribute_names (list of str): List of attribute names to analyze.
                device (torch.device): Device to run the model on.
                preprocess (Preprocessor): Preprocessing function for input images.
                prompt (str): Prompt template for the model.    
        """
        self.model = model
        self.prompt = prompt
        self.model = self.model.to(device)
        self.model.eval()
        self.attribute_names = attribute_names
        self.device = device
        self.preprocess = preprocess
        
    def analyze(self, image: Any, boxes: List[List[float]]) -> List[Dict[str, float]]:
        """
        Args:
            image (numpy array): The input image
            boxes (list of list of float): List of bounding boxes, each defined by
        Returns:
            list of dict: Each dict contains attribute names as keys and their corresponding probabilities as values.
        """
        # Crop image based on boxes
        crops = []
        for box in boxes:
            x1,x2,y1,y2 = map(int, box)
            crop = image[x1:x2, y1:y2, :]  # Assuming image is a numpy array
            crops.append(crop)
        
        # preprocess batch of images
        input = self.preprocess(crops).to(self.device)
        
        # preprocess prompt
        prompts = prompts if prompts is not None else self.prompts
        
        #tokenize prompts
        


        # calculate probabilities
        with torch.no_grad():
            outputs = self.model(inputs, prompts)
            prob = torch.sigmoid(outputs).cpu().numpy()
            results = []
            for p in prob:
                result = {attr: float(prob) for attr, prob in zip(self.attribute_names, p)}
                results.append(result)
                
        return results