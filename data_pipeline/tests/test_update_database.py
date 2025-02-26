from fastapi.testclient import TestClient
from app import app

base_url: str = "http://data-pipeline:8000"
client = TestClient(app, base_url=base_url)

def test_update_database_failure():
    from unittest.mock import patch
    with patch("app.run_all_process", side_effect=Exception("Something went wrong")):
        response = client.get("/updateDatabase")
        assert response.status_code == 500
        assert "Process failed" in response.json()["detail"]