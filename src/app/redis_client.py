from redis.asyncio import Redis

from app.config import settings

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


def tier_seats_key(tier_id: int) -> str:
    return f"tier:{tier_id}:seats"


async def get_redis() -> Redis:
    return redis
