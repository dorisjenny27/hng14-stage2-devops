import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


with patch('redis.Redis') as mock_redis:
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_submit_job_returns_job_id():
    with patch('main.redis_client') as mock_r:
        mock_r.hset = MagicMock()
        mock_r.rpush = MagicMock()
        response = client.post("/submit")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) == 36


def test_get_status_not_found():
    with patch('main.redis_client') as mock_r:
        mock_r.hgetall = MagicMock(return_value={})
        response = client.get("/status/fake-job-id")
        assert response.status_code == 200
        assert "error" in response.json()


def test_get_status_found():
    with patch('main.redis_client') as mock_r:
        mock_r.hgetall = MagicMock(return_value={"status": "completed"})
        response = client.get("/status/some-job-id")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"