from typing import List, Dict, Any, Callable
import torch
from PIL import Image
import numpy as np
from preprocess.read_image import Preprocessor
from models.attribute_analyzer_base import AttributeAnalyzerBase

class PromptBasedAttributeAnalyzer(AttributeAnalyzerBase):
    def __init__(self, model, attribute_names: List[str], device: torch.device,
                 preprocess: Preprocessor,tokenizer: Callable, prompts: List[str]):
        """
            Args:
                model: The prompt-based model for attribute analysis.
                attribute_names (List[str]): List of attribute names to analyze.
                device (torch.device): The device to run the model on.
                preprocess (Preprocessor): The image preprocessor.
                tokenizer (Callable): The tokenizer for processing prompts.
                prompt (List[str]): List of prompts corresponding to attributes.
        """
        self.model = model.to(device)
        self.model.eval()
        self.attribute_names = attribute_names
        self.device = device
        self.preprocess = preprocess
        self.tokenizer = tokenizer
        self.prompts = prompts

    def analyze(self, image: Any, boxes: List[List[float]], prompts: List[str] = None) -> List[Dict[str, float]]:
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
        #Tokenize prompts
        prompts = prompts if prompts is not None else self.prompts
        tokenized_prompts = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
        for k in tokenized_prompts:
            tokenized_prompts[k] = tokenized_prompts[k].to(self.device)
        # calculate probabilities
        with torch.no_grad():
            outputs = self.model(inputs, tokenized_prompts)
            prob = torch.sigmoid(outputs).cpu().numpy()
            results = []
            for p in prob:
                result = {attr: float(prob) for attr, prob in zip(self.attribute_names, p)}
                results.append(result)
                
        return results
    
    def save_checkpoint(self, filepath: str, optimizer: Any = None, epoch: int = None, extra: dict = None) -> None:
        """
        save model checkpoint
        """
        try:
            checkpoint = {
                "model_state_dict": self.model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict() if optimizer else None,
                "epoch": epoch,
                "extra": extra
            }
            if optimizer is not None:
                checkpoint["optimizer_state_dict"] = optimizer.state_dict()
            torch.save(checkpoint, filepath)
        except Exception as e:
            raise RuntimeError(f"Error saving checkpoint to {filepath}: {e}")

    def load_checkpoint(self, filepath: str, optimizer: Any = None) -> dict:
        """
        load model checkpoint
        """
        try:
            checkpoint = torch.load(filepath, map_location=self.device)
            self.model.load_state_dict(checkpoint["model_state_dict"])
            if optimizer is not None and checkpoint.get("optimizer_state_dict") is not None:
                optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            self.attribute_names = checkpoint.get("attribute_names", self.attribute_names)
            self.prompts = checkpoint.get("prompts", self.prompts)
            return checkpoint
        except Exception as e:
            raise RuntimeError(f"Error loading checkpoint from {filepath}: {e}")