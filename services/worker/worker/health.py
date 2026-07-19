"""Container healthcheck: worker heartbeat freshness in Redis (D3-2).

Healthy only when the heartbeat key exists, is fresh, and Redis is
reachable — so a stopped Redis or a dead worker loop both flip the
container to unhealthy.

Traceability: REQ-048, AC-001.
"""

import os
import sys
import time

import redis

from worker.main import HEARTBEAT_KEY

MAX_AGE_SECONDS = 15


def main() -> int:
    url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    try:
        value = redis.Redis.from_url(url, socket_timeout=2).get(HEARTBEAT_KEY)
    except redis.RedisError as exc:
        print(f"unhealthy: redis unreachable: {exc}")
        return 1
    if value is None:
        print("unhealthy: heartbeat key missing or expired")
        return 1
    age = time.time() - float(value)
    if age > MAX_AGE_SECONDS:
        print(f"unhealthy: heartbeat stale ({age:.1f}s)")
        return 1
    print(f"healthy: heartbeat {age:.1f}s old")
    return 0


if __name__ == "__main__":
    sys.exit(main())
