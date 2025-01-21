import pytest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de prédiction pour la détection de fraudes"}

def test_predict_valid():
    valid_payload = {
        "V1": -1.359807,
        "V2": -0.072781,
        "V3": 2.536346,
        "V4": 1.378155,
        "V5": -0.338321,
        "V6": 0.462388,
        "V7": 0.239599,
        "V8": 0.098698,
        "V9": 0.363787,
        "V10": 0.090794,
        "V11": -0.551600,
        "V12": -0.617801,
        "V13": -0.991390,
        "V14": -0.311169,
        "V15": 1.468177,
        "V16": -0.470400,
        "V17": 0.207971,
        "V18": 0.025791,
        "V19": 0.403993,
        "V20": 0.251412,
        "V21": -0.018307,
        "V22": 0.277838,
        "V23": -0.110474,
        "V24": 0.066928,
        "V25": 0.128539,
        "V26": -0.189115,
        "V27": 0.133558,
        "V28": -0.021053,
        "Amount": 149.62
    }
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "prediction" in response_data, "Missing 'prediction' in response."
    assert "probability" in response_data, "Missing 'probability' in response."
    assert isinstance(response_data["prediction"], int), "'prediction' should be an integer."
    assert isinstance(response_data["probability"], float), "'probability' should be a float."

def test_predict_invalid():
    invalid_payload = {
        "V1": -1.359807,
        "V2": -0.072781,
        "V3": "invalid",  # Donnée invalide
        "V4": 1.378155,
        "Amount": 149.62
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422, f"Expected 422 but got {response.status_code}. Response: {response.text}"
    assert "detail" in response.json(), "Missing 'detail' in error response."

def test_predict_missing():
    missing_payload = {
        "V1": -1.359807,
        "V2": -0.072781,
        "V3": 2.536346,
        "V4": 1.378155
        # Certaines colonnes manquent
    }
    response = client.post("/predict", json=missing_payload)
    assert response.status_code == 422, f"Expected 422 but got {response.status_code}. Response: {response.text}"
    assert "detail" in response.json(), "Missing 'detail' in error response."
