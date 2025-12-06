import torch
from torchvision.transforms import functional as F
import numpy as np 

class PedestrianDetector:
    def __init__(self, device='cpu', model_type='fasterrcnn', conf_thresh=0.7, preprocess=None):
        self.model_type = model_type.lower()
        self.device = device
        self.preprocess = preprocess
        self.conf_thresh = conf_thresh
        
        if self.model_type == 'fasterrcnn':
            from torchvision.models.detection import fasterrcnn_resnet50_fpn
            from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
            model = fasterrcnn_resnet50_fpn(weights="DEFAULT").to(self.device).eval()
            in_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 2)  # 2 classes: background and person
            self.model = model
        elif self.model_type == 'yolov8':
            from ultralytics import YOLO
            model = YOLO("yolov8n.pt") 
            self.model = model.to(self.device).eval()
        elif self.model_type == 'detr':
            from torchvision.models.detection import detr_resnet50
            model = detr_resnet50(weights="DEFAULT").to(self.device).eval()
            self.model = model
        elif self.model_type == "retinanet":
            from torchvision.models.detection import retinanet_resnet50_fpn
            self.model = retinanet_resnet50_fpn(weights="DEFAULT").to(self.device).eval()
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")
        


    def detect(self, image) -> list:
        """
        Args:
            image (numpy array): The input image in numpy array format (H, W, C).
        Returns:
            boxes(list of list): Detected bounding boxes [[x1, y1, x2, y2], ...].
            scores(list): Confidence scores for each detected box.

        """

        if self.model_type in ["fasterrcnn", "detr", "retinanet"]:
            # 前處理（如果有指定）
            if self.preprocess is not None:
                image = self.preprocess(image)
            
            # convert numpy to tensor and normalize
            img_tensor = image
            with torch.no_grad():
                outputs = self.model([img_tensor])[0]
            boxes = outputs['boxes'].cpu().numpy()
            scores = outputs['scores'].cpu().numpy()
            labels = outputs['labels'].cpu().numpy()
            results = []
            for box, score, label in zip(boxes, scores, labels):
                if score >= self.conf_thresh and label == 1:  # COCO class 1 is 'person'
                    results.append((box.tolist(), score.item()))
        elif self.model_type == 'yolov8':
            results = []
            # 不要做 preprocess，直接傳原始 numpy array
            preds = self.model(image)
            for pred in preds:
                for box in pred.boxes:
                    cls_id = int(box.cls[0].item())
                    score = box.conf[0].item()
                    if cls_id == 0 and score >= self.conf_thresh:
                        xyxy = box.xyxy[0].cpu().numpy().tolist()
                        results.append((xyxy, score))
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")


        return results
    
    
if __name__ == "__main__":
    import cv2
    from preprocess.read_image import Preprocessor
    img= cv2.imread("/home/ubuntu/projects/pedestrian_attribute_recognition_30%/tests/data/FudanPed00003.png")
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    preprocess = Preprocessor()
    detector = PedestrianDetector(device='cpu', model_type='retinanet', conf_thresh=0.1, preprocess=preprocess)
    detections = detector.detect(img)
    print(detections)
    
    for box, score in detections:
        x1, y1, x2, y2 = map(int, box)
        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Put confidence score
        cv2.putText(img, f"{score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255, 12), 2)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("Detections", img)
    cv2.waitKey(0)
 