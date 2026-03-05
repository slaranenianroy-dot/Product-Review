import time
import pytest
from fastapi.testclient import TestClient
from app.main import app, rate_limiter
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {settings.API_KEY}"}


class TestRateLimiter:
    """Unit tests for the RateLimiter class."""

    def test_rate_limiter_allows_requests_within_limit(self):
        """Test that requests within the limit are allowed."""
        limiter = rate_limiter
        limiter.reset("test-key-1")
        
        for i in range(settings.RATE_LIMIT_PER_MINUTE):
            allowed, remaining, retry_after = limiter.is_allowed("test-key-1")
            assert allowed, f"Request {i+1} should be allowed"
            assert retry_after == 0, f"Request {i+1} should have retry_after=0"
            assert remaining == settings.RATE_LIMIT_PER_MINUTE - i - 1

    def test_rate_limiter_blocks_requests_over_limit(self):
        """Test that requests over the limit are blocked."""
        limiter = rate_limiter
        limiter.reset("test-key-2")
        
        # Make max requests
        for _ in range(settings.RATE_LIMIT_PER_MINUTE):
            allowed, _, _ = limiter.is_allowed("test-key-2")
            assert allowed
        
        # Next request should be blocked
        allowed, remaining, retry_after = limiter.is_allowed("test-key-2")
        assert not allowed, "Request over limit should be blocked"
        assert remaining == 0, "Remaining should be 0"
        assert retry_after > 0, "retry_after should be positive"

    def test_rate_limiter_per_key_isolation(self):
        """Test that rate limits are isolated per API key."""
        limiter = rate_limiter
        limiter.reset("key-a")
        limiter.reset("key-b")
        
        # Make max requests with key-a
        for _ in range(settings.RATE_LIMIT_PER_MINUTE):
            allowed, _, _ = limiter.is_allowed("key-a")
            assert allowed
        
        # key-a is now blocked
        allowed, _, _ = limiter.is_allowed("key-a")
        assert not allowed
        
        # But key-b should still have allowance
        allowed, remaining, _ = limiter.is_allowed("key-b")
        assert allowed, "key-b should not be affected by key-a's limit"
        assert remaining == settings.RATE_LIMIT_PER_MINUTE - 1


class TestRateLimitingEndpoints:
    """Integration tests for rate limiting on API endpoints."""

    def test_rate_limit_enforcement(self):
        """AC 1.4.1 & 1.4.2: Enforce 10 requests per minute, then return 429."""
        # Send max allowed requests
        for i in range(settings.RATE_LIMIT_PER_MINUTE):
            response = client.get("/api/v1/products", headers=AUTH_HEADERS)
            assert response.status_code == 200, f"Request {i+1} failed"
        
        # The next request should fail with 429
        response = client.get("/api/v1/products", headers=AUTH_HEADERS)
        assert response.status_code == 429
        data = response.json()
        assert data["error"] == "RATE_LIMIT_EXCEEDED"
        assert "Retry-After" in response.headers

    def test_rate_limit_retry_after_header(self):
        """AC 1.4.2: Verify Retry-After header is present in 429 response."""
        # Exhaust rate limit
        for _ in range(settings.RATE_LIMIT_PER_MINUTE):
            client.get("/api/v1/products", headers=AUTH_HEADERS)
        
        # Next request should include Retry-After header
        response = client.get("/api/v1/products", headers=AUTH_HEADERS)
        assert response.status_code == 429
        assert "Retry-After" in response.headers
        retry_after = int(response.headers["Retry-After"])
        assert 1 <= retry_after <= 60, "Retry-After should be between 1 and 60 seconds"

    def test_health_exempt_from_rate_limit(self):
        """AC 1.4.4: /health is exempt from rate limiting."""
        # Send more than the limit to /health
        for _ in range(settings.RATE_LIMIT_PER_MINUTE + 5):
            response = client.get("/health")
            assert response.status_code == 200

    def test_insights_endpoint_rate_limiting(self):
        """Test that /api/v1/insights also enforces rate limiting."""
        product_id = "B001"
        
        # Make max allowed requests
        for i in range(settings.RATE_LIMIT_PER_MINUTE):
            response = client.get(
                f"/api/v1/insights/{product_id}",
                headers=AUTH_HEADERS
            )
            # Response can be 200 or 404 depending on product, but not 429
            assert response.status_code in [200, 404], f"Request {i+1} should not be rate limited"
        
        # Next request should be rate limited
        response = client.get(
            f"/api/v1/insights/{product_id}",
            headers=AUTH_HEADERS
        )
        assert response.status_code == 429

    def test_missing_auth_header_returns_401_not_429(self):
        """Test that missing auth header returns 401, not 429."""
        # Make many requests without auth header
        for _ in range(settings.RATE_LIMIT_PER_MINUTE + 5):
            response = client.get("/api/v1/products")
            assert response.status_code == 401, "Missing auth should return 401, not 429"
            assert response.json()["error"] == "UNAUTHORIZED"
