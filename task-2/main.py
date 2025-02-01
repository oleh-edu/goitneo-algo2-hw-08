#!/usr/bin/env python

import time
import random
from typing import Dict

# Class for rate limiter
class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.user_last_message_time: Dict[str, float] = {}

    # Method for checking if the user can send a message
    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        last_message_time = self.user_last_message_time.get(user_id, 0)
        return (current_time - last_message_time) >= self.min_interval

    # Method for recording a message
    def record_message(self, user_id: str) -> bool:
        if self.can_send_message(user_id):
            self.user_last_message_time[user_id] = time.time()
            return True
        return False

    # Method for calculating the time until the next allowed message
    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        last_message_time = self.user_last_message_time.get(user_id, 0)
        return max(0.0, self.min_interval - (current_time - last_message_time))


# Function for printing
def print_message_status(message_id, user_id, result, wait_time):
    print(f"Message {message_id:2d} | User {user_id} | "
          f"{'✓' if result else f'× (waiting {wait_time:.1f}с)'}")


# Function for testing
def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Message flow simulation (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print_message_status(message_id, user_id, result, wait_time)
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting for 10 seconds...")
    time.sleep(10)

    print("\n=== New series of messages after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print_message_status(message_id, user_id, result, wait_time)
        time.sleep(random.uniform(0.1, 1.0))


# Work demonstration
if __name__ == "__main__":
    test_throttling_limiter()
