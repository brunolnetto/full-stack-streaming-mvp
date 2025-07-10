import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app

client = TestClient(app)

@patch("main.AIOKafkaProducer", new_callable=AsyncMock)
def test_root(mock_producer):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running"}

@patch("main.engine.connect")
@patch("main.AIOKafkaProducer", new_callable=AsyncMock)
def test_hits(mock_producer, mock_connect):
    # Mock the DB connection and query result
    mock_conn = MagicMock()
    mock_result = [("/", 5), ("/about", 3)]
    mock_conn.execute.return_value = mock_result
    mock_connect.return_value.__enter__.return_value = mock_conn

    response = client.get("/hits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{"route": "/", "count": 5}, {"route": "/about", "count": 3}]

@patch("main.AIOKafkaProducer", new_callable=AsyncMock)
def test_lifespan_and_middleware(mock_producer_class):
    from main import app as test_app
    test_client = TestClient(test_app)
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running"} 