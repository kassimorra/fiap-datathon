from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_model_data():
    response = client.get("/api/model-data")
    assert response.status_code == 200
    assert "data" in response.json()

def test_invalid_endpoint():
    response = client.get("/api/invalid-endpoint")
    assert response.status_code == 404