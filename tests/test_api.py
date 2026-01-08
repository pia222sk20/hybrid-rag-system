"""
Test cases for Hybrid RAG System
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()


def test_stats_endpoint():
    """Test statistics endpoint"""
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "dense_chunks" in data
    assert "sparse_chunks" in data


def test_query_endpoint_validation():
    """Test query endpoint with invalid input"""
    # Empty question
    response = client.post(
        "/api/v1/query",
        json={"question": "", "top_k": 5}
    )
    assert response.status_code == 422  # Validation error
    
    # Invalid top_k
    response = client.post(
        "/api/v1/query",
        json={"question": "test", "top_k": 0}
    )
    assert response.status_code == 422


def test_query_endpoint_valid():
    """Test query endpoint with valid input"""
    response = client.post(
        "/api/v1/query",
        json={
            "question": "테스트 질문입니다",
            "top_k": 3,
            "include_sources": True
        }
    )
    
    # Should return 200 even if no documents are indexed
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
