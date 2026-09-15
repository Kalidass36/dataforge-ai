import pytest
from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "DataForge API"


def test_catalog():
    response = client.get("/api/v1/catalog")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "tables" in data


def test_quality():
    response = client.get("/api/v1/quality")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "report" in data


def test_query():
    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show me the top 5 customers by spending"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "sql" in data
    assert "response" in data


def test_query_contains_sql():
    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show me the top 5 customers by spending"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["sql"], str)
    assert len(data["sql"]) > 0