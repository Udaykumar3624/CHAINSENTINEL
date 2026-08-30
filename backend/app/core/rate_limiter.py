import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

class SimpleRateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.client_requests = defaultdict(list)

    def check_rate_limit(self, request: Request):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        window_start = now - 60.0

        # Filter out requests older than 60 seconds
        self.client_requests[client_ip] = [
            t for t in self.client_requests[client_ip] if t > window_start
        ]

        if len(self.client_requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded ({self.requests_per_minute} req/min). Please wait before submitting more analysis requests."
            )

        self.client_requests[client_ip].append(now)

analysis_rate_limiter = SimpleRateLimiter(requests_per_minute=30)
