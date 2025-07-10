import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.main import app

client = TestClient(app)

@patch("src.main.AIOKafkaProducer", new_callable=AsyncMock)
def test_root(mock_producer):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running"}

@patch("src.main.AIOKafkaProducer", new_callable=AsyncMock)
def test_hits(mock_producer):
    # This test assumes the database is either mocked or empty
    response = client.get("/hits")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 