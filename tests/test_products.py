import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.data_loader import reset_cache, load_reviews
import pandas as pd

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {settings.API_KEY}"}

@pytest.fixture(autouse=True)
def setup_data(tmp_path):
    """Set up a fresh test dataset."""
    original_path = settings.DATA_PATH
    csv_file = tmp_path / "test_products.csv"
    pd.DataFrame({
        "product_id": ["P3", "P1", "P2"],
        "review_text": ["A", "B", "C"],
        "rating": [5, 5, 5],
        "review_date": ["2023", "2023", "2023"]
    }).to_csv(csv_file, index=False)
    
    settings.DATA_PATH = str(csv_file)
    reset_cache()
    yield
    settings.DATA_PATH = original_path
    reset_cache()

def test_list_products_success():
    """AC 2.2.1: Return sorted naked JSON array."""
    resp = client.get("/api/v1/products", headers=AUTH_HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data == ["P1", "P2", "P3"]  # Alphabetical

def test_list_products_unauthorized():
    """AC 2.2.2: Return 401 without token."""
    resp = client.get("/api/v1/products")
    assert resp.status_code == 401
    assert resp.json()["error"] == "UNAUTHORIZED"

def test_list_products_empty(tmp_path):
    """AC 2.2.3: Return [] if empty."""
    csv_file = tmp_path / "empty.csv"
    pd.DataFrame(columns=["product_id", "review_text", "rating", "review_date"]).to_csv(csv_file, index=False)
    settings.DATA_PATH = str(csv_file)
    reset_cache()
    
    resp = client.get("/api/v1/products", headers=AUTH_HEADERS)
    assert resp.status_code == 200
    assert resp.json() == []
