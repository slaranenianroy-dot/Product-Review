from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    AC 1.1.2: GET /health endpoint is available and returns a 200 OK status code.
    AC 1.1.3: The /health response body is exactly {"status": "online"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}
