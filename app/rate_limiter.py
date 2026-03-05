import time
from collections import defaultdict

class RateLimiter:
    """
    In-memory rate limiter using a sliding window algorithm.
    Tracks requests per API key.
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Dictionary mapping api_key -> list of timestamps
        self._history = defaultdict(list)

    def is_allowed(self, api_key: str) -> tuple[bool, int, int]:
        """
        Check if a request is allowed for the given API key.
        Returns: (is_allowed, requests_remaining, retry_after_seconds)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean up old timestamps
        history = self._history[api_key]
        self._history[api_key] = [t for t in history if t > window_start]
        
        current_history = self._history[api_key]
        
        if len(current_history) < self.max_requests:
            self._history[api_key].append(now)
            remaining = self.max_requests - len(self._history[api_key])
            return True, remaining, 0
        else:
            # Calculate retry after (time until the oldest timestamp in the window expires)
            oldest_ts = current_history[0]
            retry_after = int(oldest_ts + self.window_seconds - now) + 1
            return False, 0, max(1, retry_after)

    def reset(self, api_key: str | None = None):
        """Reset the rate limit state (globally or for a specific key)."""
        if api_key:
            if api_key in self._history:
                del self._history[api_key]
        else:
            self._history.clear()
