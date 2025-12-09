import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_pipeline_inference_success():
    # 假設 /api/pipeline 路由接受 POST 並回傳推論結果
    payload = {
        "image_url": "../data/CrowdHuman/crowdhuman/images/train/273271,1a0d6000b9e1f5b7.jpg",
        "attributes": ["gender", "age"]
    }
    response = client.post("/api/pipeline", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], dict)
    for v in data["results"].values():
        assert isinstance(v, list)

def test_pipeline_inference_invalid_input():
    # 缺少必要欄位，應回傳 422
    payload = {"image_url": ""}
    response = client.post("/api/pipeline", json=payload)
    assert response.status_code == 422

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_analyze_endpoint():
    payload = {
        "image_url": "https://exaple.com/test.jpg",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], dict)
    
def test_analyze_invalid_input():
    payload = {"image_url": ""}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422
    
def test_detect_endpoint():
    payload = {
        "image_url": "https://example.com/test.jpg"
    }
    response = client.post("/api/detect", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    
def test_detect_invalid_input():
    payload = {"image_url": ""}
    response = client.post("/api/detect", json=payload)
    assert response.status_code == 422