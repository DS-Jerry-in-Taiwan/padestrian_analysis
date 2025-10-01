import torch
import matplotlib.pyplot as plt
import torch.nn as nn
from torchvision import transforms as T, models
from typing import Any, List
import numpy as np
from .attribute_analyzer_base import AttributeAnalyzerBase
from preprocess.read_image import Preprocessor
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""


class ResNet50AttributeAnalyzer(AttributeAnalyzerBase):
    def __init__(self, attribute_names: list[str], device: torch.device, preprocess: Preprocessor):
        self.model = models.resnet50(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, len(attribute_names))
        self.model = self.model.to(device)
        self.model.eval()
        self.attribute_names = attribute_names
        self.device = device
        self.preprocess = preprocess

        
    def analyze(self, image: Any, boxes: List[List[float]]) -> List[dict[str, float]]:
        """
        Args:
            image (numpy array): The input image.
            boxes (list of list of float): List of bounding boxes, each defined by [x1, y1, x2, y2].
        Returns:
            list of dict: Each dict contains attribute names as keys and their corresponding probabilities as values.   
        """
        crops = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            crop = image[y1:y2, x1:x2, :]
            crop = self.preprocess(crop)
            crops.append(crop)
        if not crops:
            return []
        batch = torch.stack(crops).to(self.device)
        with torch.no_grad():
            outputs = self.model(batch)
            probs = torch.sigmoid(outputs).cpu().numpy()
        results = []
        for pred in probs:
            result = {name: float(value) for name, value in zip(self.attribute_names, ped)}
            results.append(result)
        return results
    
class VitAttributeAnalyzer(AttributeAnalyzerBase):
    def __init__(self, attribute_names: list[str], device: torch.device, preprocess: Preprocessor):
        self.model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)
        in_features = self.model.heads[0].in_features
        self.model.heads = nn.Linear(in_features, len(attribute_names))
        self.model = self.model.to(device)
        self.model.eval()
        self.attribute_names = attribute_names
        self.device = device
        self.preprocess = preprocess

    def analyze(self, image: Any, boxes: List[list[float]]) -> List[dict[str, float]]:
        """
        Args:
            image (numpy array): The input image.
            boxes (list of list of float): List of bounding boxes, each defined by [x1, y1, x2, y2].
        Returns:
            list of dict: Each dict contains attribute names as keys and their corresponding probabilities as values.
        """
        crops = []
        for box in boxes:
            if isinstance(box, (tuple, list)) and len(box) == 2:
                coords, _ = box
            else:
                coords = box
            x1, y1, x2, y2 = map(int, coords)
            crop = image[y1:y2, x1:x2, :]
            crop = self.preprocess(crop)
            crops.append(crop)
        if not crops:
            return []
        batch = torch.stack(crops).to(self.device)
        with torch.no_grad():
            outputs = self.model(batch)
            probs = torch.sigmoid(outputs).cpu().numpy()
        results = []
        for pred in probs:
            result = {name: float(value) for name, value in zip(self.attribute_names, pred)}
            results.append(result)
        return results


if __name__ == "__main__":
    import torch
    from models.pedestrian_detector import PedestrianDetector
    import cv2
    import os
    import random

    
    # set image path
    img_dir = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/PA-100K/data"
    # number of images to process
    num_samples = 100

    if os.path.exists(img_dir):
        img_list = os.listdir(img_dir)
        sample_img = random.sample(img_list, num_samples)
        for img in sample_img:
            img_path = os.path.join(img_dir, img)
            print("Processing image:", img_path)
            img = cv2.imread(img_path)
            label_str = "Female,AgeOver60,Age18-60,AgeLess18,Front,Side,Back,Hat,Glasses,HandBag,ShoulderBag,Backpack,HoldObjectsInFront,ShortSleeve,LongSleeve,UpperStride,UpperLogo,UpperPlaid,UpperSplice,LowerStripe,LowerPattern,LongCoat,Trousers,Shorts,Skirt&Dress,boots"
            attribute_names = label_str.split(",")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            device = "cpu"
            # cv2.imshow("Image Window", img)  # "Image Window" 是視窗名稱，img 是你的影像
            # cv2.waitKey(0)                  # 等待按鍵（0 表示無
            # cv2.destroyAllWindows()         # 關閉所有 OpenCV 視窗限等待）
            
            preprocess = Preprocessor()
            detector = PedestrianDetector(device=device,model_type='yolov8', preprocess=preprocess, conf_thresh=0.3)
            analyzer = VitAttributeAnalyzer(attribute_names=attribute_names, device=device, preprocess=preprocess)
            boxes = detector.detect(img)
            print("boxes:", boxes)
            results = analyzer.analyze(img, boxes)
            for i, res in enumerate(results):
                print(f"Person {i+1}:")
                for attr, prob in res.items():
                    print(f"  {attr}: {prob:.4f}")
                    
            # --- 畫框與屬性 ---
            img_show = img.copy()
            for i, (box, res) in enumerate(zip(boxes, results)):
                coords = box[0] if isinstance(box, (tuple, list)) and len(box) == 2 else box
                x1, y1, x2, y2 = map(int, coords)
                cv2.rectangle(img_show, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # --- 用 matplotlib 顯示圖片與屬性 ---
            img_rgb = cv2.cvtColor(img_show, cv2.COLOR_BGR2RGB)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [3, 2]})
            ax1.imshow(img_rgb)
            ax1.axis('off')
            ax1.set_title("Detection Result")

            # 準備屬性文字
            attr_lines = []
            for i, res in enumerate(results):
                attr_lines.append(f"Person {i+1}:")
                for attr, prob in res.items():
                    attr_lines.append(f"  {attr}: {prob:.2f}")
                attr_lines.append("")  # 空行分隔

            attr_text = "\n".join(attr_lines)
            ax2.text(0, 1, attr_text, fontsize=12, va='top', family='monospace')
            ax2.axis('off')
            ax2.set_title("Attributes")

            plt.tight_layout()
            plt.show()
    else:
        print(f"Image path {img_path} does not exist.")
    
    

    