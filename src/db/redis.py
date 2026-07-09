from redis import asyncio as aioredis 
from src.config import Config

JTI_EXPIRY = 3600
BOOK_CACHE_EXPIRY = 3600

token_blocklist= aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    protocol=2
)
async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value='',
        ex=JTI_EXPIRY,
    )


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    
    return jti is not None

# caching a books

async def set_cache(key: str, value: str, expiry: int = BOOK_CACHE_EXPIRY) -> None:
    await token_blocklist.set(
        name=key,
        value=value,
        ex=expiry
    )
async def get_cache(key: str) -> str | None:
    value = await token_blocklist.get(key)
    if value:
        return value.decode("utf-8")
    return None


async def clear_cache(key: str) -> None:
    await token_blocklist.delete(key)