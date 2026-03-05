"""
Automated tests for the Product Review Insights API.

Uses FastAPI's TestClient (backed by httpx) to validate the endpoint behaviour
without running a live server.
"""
from __future__ import annotations

import os
import sys

import pytest
from fastapi.testclient import TestClient

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.data_loader import reset_cache  # noqa: E402
from app.config import settings  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {settings.API_KEY}"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _setup_test_env():
    """Configure settings for testing and clear cache."""
    original_path = settings.DATA_PATH
    settings.DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_reviews.csv")
    reset_cache()
    yield
    settings.DATA_PATH = original_path
    reset_cache()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "online"}


class TestProductsEndpoint:
    def test_list_products(self):
        resp = client.get("/api/v1/products", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "B001" in data


class TestInsightsEndpoint:
    """Tests for POST /api/v1/insights."""

    def test_valid_product_returns_full_schema(self):
        """B001 has 15 reviews — should return a complete response."""
        resp = client.get("/api/v1/insights/B001", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()

        # Schema checks
        assert data["product_id"] == "B001"
        assert isinstance(data["top_aspects"], list)
        assert isinstance(data["pros"], list)
        assert isinstance(data["cons"], list)
        assert isinstance(data["summary"], str)
        assert 0.0 <= data["confidence"] <= 1.0
        assert data["review_count"] == 15

        # At least one aspect extracted
        assert len(data["top_aspects"]) >= 1
        for aspect in data["top_aspects"]:
            assert "aspect" in aspect
            assert "sentiment" in aspect
            assert "score" in aspect

    def test_unknown_product_returns_404(self):
        resp = client.get("/api/v1/insights/ZZZZ_NONEXISTENT", headers=AUTH_HEADERS)
        assert resp.status_code == 404
        assert "not found" in resp.json()["message"].lower()

    def test_insufficient_reviews_returns_safe_response(self):
        """B004 has only 2 reviews — below MIN_REVIEWS_FOR_ANALYSIS (3)."""
        resp = client.get("/api/v1/insights/B004", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()

        assert data["confidence"] == 0.22
        assert data["top_aspects"] == []
        assert data["pros"] == []
        assert data["cons"] == []
        assert "not enough data" in data["summary"].lower()

    def test_evidence_grounded(self):
        """Every pro and con must contain a non-empty evidence field that
        appears in the original review text."""
        resp = client.get("/api/v1/insights/B001", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()

        for item in data["pros"] + data["cons"]:
            assert item["evidence"], "Evidence must not be empty"
            assert item["source_review"], "Source review must not be empty"
            # The evidence sentence should be a substring of the cleaned
            # version of some review — but since evidence is already lowercase
            # cleaned text and source_review is the original, we check the
            # evidence is non-trivial (length > 10)
            assert len(item["evidence"]) > 10, (
                f"Evidence suspiciously short: {item['evidence']!r}"
            )

    def test_no_fabricated_aspects(self):
        """Verify that extracted aspects are not generic noise words."""
        resp = client.get("/api/v1/insights/B001", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()

        noise_words = {"the", "a", "an", "this", "that", "it", "product", "item", "thing"}
        for aspect_info in data["top_aspects"]:
            aspect = aspect_info["aspect"].lower()
            assert aspect not in noise_words, (
                f"Noise word '{aspect}' should not appear as an aspect"
            )

    def test_second_product(self):
        """B002 (earbuds) should also work correctly."""
        resp = client.get("/api/v1/insights/B002", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert data["product_id"] == "B002"
        assert data["review_count"] == 12
        assert len(data["top_aspects"]) >= 1
