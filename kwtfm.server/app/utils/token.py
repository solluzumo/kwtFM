import hashlib
from config import JWT_TOKEN_SALT
from jose import jwt, JWTError
from app.database import redis_connect
from redis.asyncio import Redis
from datetime import datetime, timedelta, timezone


async def generate_token(login: str, is_admin: bool = False, refresh: bool = False) -> str:

    payload = {"login": login, "is_admin": is_admin, "type": "refresh" if refresh else "access", "exp": None}

    expire = timedelta(days=30) if refresh else timedelta(days=1)

    payload["exp"] = (datetime.now(timezone.utc) + expire).timestamp()

    token = jwt.encode(payload, JWT_TOKEN_SALT, "HS512")

    if refresh:

        token_id = hashlib.sha256(token.encode("utf-8")).hexdigest()

        async with Redis.from_pool(redis_connect) as redis:

            await redis.set(f"token:{token_id}", "True", ex=259000)

    return token


async def check_token(token: str, refresh: bool = False) -> str | None:

    try:

        token_data = jwt.decode(token, JWT_TOKEN_SALT, "HS512")

    except JWTError:

        return

    if refresh:

        if token_data["type"] != "refresh":

            return

        token_id = hashlib.sha256(token.encode("utf-8")).hexdigest()

        async with Redis.from_pool(redis_connect) as redis:

            data = await redis.get(f"token:{token_id}")

            if not data:

                return

            await redis.delete(f"token:{token_id}")

        return token_data["login"]

    if token_data["type"] == "refresh":

        return

    return token_data["login"]

async def check_admin(token: str) -> str | None:

    try:

        token_data = jwt.decode(token, JWT_TOKEN_SALT, "HS512")

    except JWTError:

        return


    return token_data["is_admin"]

# удаление токена refresh из базы данных
async def delete_token(token: str) -> bool:

    try:

        token_data = jwt.decode(token, JWT_TOKEN_SALT, "HS512")

    except JWTError:

        return False

    if token_data["type"] != "refresh":

        return False

    token_id = hashlib.sha256(token.encode("utf-8")).hexdigest()

    async with Redis.from_pool(redis_connect) as redis:

        await redis.delete(f"token:{token_id}")

    return True


async def is_update_worker() -> bool:

    async with Redis.from_pool(redis_connect) as redis:

        check = await redis.get("worker")

        if not check:

            # Попытка установить ключ, если он ещё не существует
            was_set = await redis.set("worker", "True", ex=10, nx=True)

            return was_set is not None  # Вернёт True только если ключ был установлен

        return False


async def delete_update_worker() -> None:

    async with Redis.from_pool(redis_connect) as redis:

        await redis.delete("worker")

    return
