from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_health_remains_public():
    """AC 1.2.5: /health remains publicly accessible."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}

def test_products_requires_auth():
    """AC 1.2.1: /api/v1/products requires Bearer token."""
    response = client.get("/api/v1/products")
    assert response.status_code == 401

def test_insights_requires_auth():
    """AC 1.2.1: /api/v1/insights requires Bearer token."""
    # Assuming valid payload or it might fail with 422, but auth should check first
    response = client.get("/api/v1/insights/B001")
    assert response.status_code == 401

def test_invalid_token():
    """AC 1.2.4: Invalid token returns 401."""
    response = client.get("/api/v1/products", headers={"Authorization": "Bearer invalid-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "UNAUTHORIZED"
    assert data["message"] == "Invalid API key"

def test_valid_token():
    """AC 1.2.2: Valid token returns 200."""
    response = client.get("/api/v1/products", headers={"Authorization": f"Bearer {settings.API_KEY}"})
    assert response.status_code == 200
