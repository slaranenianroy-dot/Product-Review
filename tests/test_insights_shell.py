import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.data_loader import reset_cache
import pandas as pd
import os

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {settings.API_KEY}"}

@pytest.fixture
def scaling_csv(tmp_path):
    orig_path = settings.DATA_PATH
    csv_path = tmp_path / "scaling.csv"
    settings.DATA_PATH = str(csv_path)
    yield csv_path
    settings.DATA_PATH = orig_path
    reset_cache()

def test_confidence_scaling(scaling_csv):
    """AC 2.3.4: Verify confidence score logic."""
    def get_conf(n):
        df = pd.DataFrame({
            "product_id": ["P1"] * n,
            "review_text": ["Good stuff. " * 5] * n,
            "rating": [5] * n,
            "review_date": ["2023"] * n
        })
        df.to_csv(scaling_csv, index=False)
        reset_cache()
        resp = client.get("/api/v1/insights/P1", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        return resp.json()["confidence"]

    # 1 review -> 0.1
    assert get_conf(1) == 0.1
    # 10 reviews -> 0.5
    assert get_conf(10) == 0.5
    # 100 reviews -> 0.9
    assert get_conf(100) == 0.9

def test_insights_get_success():
    """AC 2.3.1: GET endpoint works."""
    # We use the mock_reviews.csv if available or B001 from test_api pattern
    # Actually, test_api.py sets DATA_PATH to mock_reviews.csv in its fixture.
    # We should do the same if we want to rely on B001.
    mock_csv = os.path.join(os.path.dirname(__file__), "mock_reviews.csv")
    orig_path = settings.DATA_PATH
    settings.DATA_PATH = mock_csv
    reset_cache()
    try:
        resp = client.get("/api/v1/insights/B001", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        assert resp.json()["product_id"] == "B001"
    finally:
        settings.DATA_PATH = orig_path
        reset_cache()

def test_insights_not_found():
    """AC 2.3.3: 404 for unknown product."""
    resp = client.get("/api/v1/insights/UNKNOWN_PROD_123", headers=AUTH_HEADERS)
    assert resp.status_code == 404
    assert resp.json()["error"] == "NOT_FOUND"
