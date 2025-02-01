#!/usr/bin/env python

import time
import random
from typing import Dict
from collections import deque


# Class for rate limiter
class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests: Dict[str, deque] = {}

    # Function for cleaning up the window
    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id in self.user_requests:
            while self.user_requests[user_id] and self.user_requests[user_id][0] <= current_time - self.window_size:
                self.user_requests[user_id].popleft()
            if not self.user_requests[user_id]:
                del self.user_requests[user_id]

    # Function for checking
    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return len(self.user_requests.get(user_id, [])) < self.max_requests

    # Function for recording
    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        if self.can_send_message(user_id):
            if user_id not in self.user_requests:
                self.user_requests[user_id] = deque()
            self.user_requests[user_id].append(current_time)
            return True
        return False

    # Function for time
    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        if user_id not in self.user_requests or not self.user_requests[user_id]:
            return 0.0
        return max(0.0, self.window_size - (current_time - self.user_requests[user_id][0]))


# Function for printing
def print_message_status(message_id, user_id, result, wait_time):
    print(f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (waiting {wait_time:.1f}с)'}")


# Function for testing
def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    print("\n=== Message flow simulation ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print_message_status(message_id, user_id, result, wait_time)
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting for 4 seconds...")
    time.sleep(4)
    
    print("\n=== New series of messages after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print_message_status(message_id, user_id, result, wait_time)
        time.sleep(random.uniform(0.1, 1.0))


# Work demonstration
if __name__ == "__main__":
    test_rate_limiter()
