"""
Rate Limiter for Gemini API
Implements a simple request queue to prevent overwhelming the API
"""

import time
import threading
from collections import deque
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter using token bucket algorithm
    """
    
    def __init__(self, requests_per_minute: int = 10, requests_per_day: int = 1500):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests allowed per minute
            requests_per_day: Maximum requests allowed per day (for free tier)
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        
        self.minute_window = deque()
        self.day_window = deque()
        
        self.lock = threading.Lock()
        
    def can_proceed(self) -> tuple[bool, float]:
        """
        Check if a request can proceed
        
        Returns:
            (can_proceed, wait_time_seconds)
        """
        with self.lock:
            now = time.time()
            
            # Clean up old entries
            minute_ago = now - 60
            day_ago = now - 86400
            
            while self.minute_window and self.minute_window[0] < minute_ago:
                self.minute_window.popleft()
                
            while self.day_window and self.day_window[0] < day_ago:
                self.day_window.popleft()
            
            # Check minute limit
            if len(self.minute_window) >= self.requests_per_minute:
                wait_time = 60 - (now - self.minute_window[0])
                return False, max(wait_time, 0)
            
            # Check day limit
            if len(self.day_window) >= self.requests_per_day:
                wait_time = 86400 - (now - self.day_window[0])
                return False, max(wait_time, 0)
            
            return True, 0
    
    def record_request(self):
        """Record that a request was made"""
        with self.lock:
            now = time.time()
            self.minute_window.append(now)
            self.day_window.append(now)
    
    def wait_if_needed(self) -> float:
        """
        Wait if rate limit is hit
        
        Returns:
            Time waited in seconds
        """
        can_proceed, wait_time = self.can_proceed()
        
        if not can_proceed:
            logger.warning(f"Rate limit reached. Waiting {wait_time:.2f}s before proceeding...")
            time.sleep(wait_time)
            return wait_time
        
        return 0


# Global rate limiter instance (initialized by CredifyAgent)
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        # Fallback initialization
        _rate_limiter = RateLimiter(requests_per_minute=10, requests_per_day=1500)
    return _rate_limiter


def rate_limited_call(func: Callable, *args, **kwargs) -> Any:
    """
    Execute a function with rate limiting
    
    Args:
        func: Function to call
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Function result
    """
    limiter = get_rate_limiter()
    
    # Wait if needed
    wait_time = limiter.wait_if_needed()
    if wait_time > 0:
        logger.info(f"Waited {wait_time:.2f}s due to rate limiting")
    
    # Execute function
    try:
        result = func(*args, **kwargs)
        limiter.record_request()
        return result
    except Exception as e:
        # Still record the request even if it failed
        limiter.record_request()
        raise e
