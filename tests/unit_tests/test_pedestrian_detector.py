import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import numpy as np
import pytest
from models.pedestrian_detector import PedestrianDetector
from preprocess.read_image import DetectionImagePreprocessor
from preprocess.registry import register_preprocessor

@pytest.fixture(autouse=True)
def register_image_preprocessor():
    # 測試前自動註冊 detection 用的 image preprocessor
    register_preprocessor('image', DetectionImagePreprocessor())

@pytest.mark.parametrize("model_type", ["fasterrcnn", "yolov8", "retinanet"])
def test_pedestrian_detector_multi_model(model_type):
    dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)
    detector = PedestrianDetector(model_type=model_type, conf_thresh=0.0, preprocess=DetectionImagePreprocessor())
    results = detector.detect(dummy_img)
    assert isinstance(results, list)
    for item in results:
        box, score = item
        assert isinstance(box, list)
        assert isinstance(score, float) or isinstance(score, np.floating)