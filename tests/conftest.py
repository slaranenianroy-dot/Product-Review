import pytest
from app.main import rate_limiter

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset the global rate limiter before each test to prevent cross-test interference."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()
