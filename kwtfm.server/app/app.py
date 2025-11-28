from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import redis_connect
from app.routing import routers_list
from app.utils.token import is_update_worker, delete_update_worker


@asynccontextmanager
async def lifespan(app: FastAPI):

    update_worker = False

    if update_worker := await is_update_worker():

        # Запуск агентов
        print("Запуск агентов")
       
    yield

    if update_worker:
        await delete_update_worker()

    await redis_connect.aclose()

app = FastAPI(openapi_url="/api/docs/openapi.json", docs_url="/api/docs", lifespan=lifespan)

for router in routers_list:

    app.include_router(router["router"], prefix=router["prefix"], tags=router["tags"])
