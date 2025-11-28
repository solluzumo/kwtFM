import asyncio
from datetime import datetime
from logging.config import fileConfig

from alembic import context

# Импортируйте ваш асинхронный движок
from app.database import engine

# Добавляем модели для генерации миграции
from app.models.DBModelBase import DBModelBase
from app.models.users import UserModel

# Устанавливаем метаданные целевой модели для 'autogenerate' поддержки
target_metadata = DBModelBase.metadata

# В файле alembic/env.py после определения target_metadata
print(str(datetime.now()) + " alembic:", target_metadata.tables.keys())


def run_migrations_offline():
    """Запуск миграций в офлайн-режиме."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в онлайн-режиме с асинхронным движком."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
