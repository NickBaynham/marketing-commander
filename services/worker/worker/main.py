"""Marketing Commander worker stub (plan/plan.md Phase 3, Increment 3.3).

Connects to Redis and writes a heartbeat key on an interval. No job
logic; the queue and worker execution model arrive in Phase 10.

Traceability: REQ-048, AC-001; decision D3-2 (heartbeat health).
"""

import os
import time

import redis

HEARTBEAT_KEY = "mc:worker:heartbeat"
INTERVAL_SECONDS = 5
TTL_SECONDS = 15


def main() -> None:
    url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    client = redis.Redis.from_url(url)
    print(
        f"worker stub started; heartbeat to {HEARTBEAT_KEY} "
        f"every {INTERVAL_SECONDS}s (ttl {TTL_SECONDS}s)"
    )
    while True:
        try:
            client.set(HEARTBEAT_KEY, str(time.time()), ex=TTL_SECONDS)
        except redis.RedisError as exc:
            print(f"heartbeat failed: {exc}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
