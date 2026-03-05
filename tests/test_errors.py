from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {settings.API_KEY}"}

def test_404_consistent_format():
    """AC 1.3.1: 404 returns {"error": "NOT_FOUND", "message": "..."}"""
    # Use a product ID that doesn't exist to trigger a 404 from the logic
    response = client.get("/api/v1/insights/NONEXISTENT_PROD", headers=AUTH_HEADERS)
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "NOT_FOUND"
    assert "not found" in data["message"].lower()

def test_generic_404_consistent_format():
    """Verify that a totally invalid route also returns a consistent 404."""
    response = client.get("/api/v1/completely-wrong-route", headers=AUTH_HEADERS)
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "NOT_FOUND"
