from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import DATABASE_URL, REDIS_URL
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=50,  # Увеличиваем базовый пул соединений
    max_overflow=100,  # Разрешаем больше дополнительных соединений
    pool_timeout=60,  # Время ожидания соединения
    pool_recycle=1800,  # Перезапуск соединений каждые 30 минут
)

session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

redis_connect: ConnectionPool = ConnectionPool.from_url(REDIS_URL)
