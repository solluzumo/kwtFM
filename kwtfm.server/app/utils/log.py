import os
from json import dumps
from typing import Callable, Type, Any
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.responses import StreamingResponse

from app.schemas.CustomErrorSchema import CustomErrorSchema


def log_info(req_method, req_url, req_body, req_headers, res_code, res_body):
    log_dir = "logs"
    log_file_path = os.path.join(log_dir, "requests.log")

    # Проверяем наличие директории logs и файла requests.log
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Создаём директорию logs
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as file:
            file.write("")  # Создаём пустой файл requests.log

    #Обрабатываем и строки, и байты
    if isinstance(req_body, bytes):
        try:
            body_str = req_body.decode("utf-8")
        except UnicodeDecodeError:
            body_str = repr(req_body[:200]) + " [binary data truncated]"
    else:
        body_str = str(req_body)

    # Запись логов
    with open(log_file_path, "a") as file:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": {
                "method": req_method,
                "path": str(req_url),
                "body": body_str,
                "headers": dict(req_headers),
            },
            "response": {"status_code": res_code, "body": res_body}
        }
        file.write(dumps(log_entry, ensure_ascii=False) + "\n")


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            try:
                response = await original_route_handler(request)
            except Exception as e:
                try:
                    status_code = int(str(e)[:3])
                    res_body = str(e)[5:]
                except ValueError:
                    status_code = None
                    res_body = str(e)
                log_info(request.method, request.url, req_body, request.headers, status_code, res_body)
                raise e

            if isinstance(response, StreamingResponse):
                chunks = []
                async for chunk in response.body_iterator:
                    chunks.append(chunk)
                res_body = b"".join(chunks)
                try:
                    log_info(
                        request.method,
                        request.url,
                        req_body,
                        request.headers,
                        response.status_code,
                        res_body.decode("utf-8"),
                    )
                except UnicodeDecodeError:
                    log_info(
                        request.method,
                        request.url,
                        req_body,
                        request.headers,
                        response.status_code,
                        f"...{len(res_body)} bytes...",
                    )
                response = Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            else:
                try:
                    log_info(
                        request.method,
                        request.url,
                        req_body,
                        request.headers,
                        response.status_code,
                        response.body.decode("utf-8"),
                    )
                except UnicodeDecodeError:
                    log_info(
                        request.method,
                        request.url,
                        req_body,
                        request.headers,
                        response.status_code,
                        f"...{len(response.body)} bytes...",
                    )

            return response

        return custom_route_handler


async def update_logs(session: AsyncSession, model: Type[Any], condition: Any, error_message: str) -> None:
    """
    Универсальная функция для обновления логов в поле JSONB с использованием схемы CustomErrorSchema.

    :param session: Сессия базы данных.
    :param model: Модель базы данных, в которой нужно выполнить обновление.
    :param condition: Условие для выборки записей (например, `model.id == some_id`).
    :param error_message: Сообщение ошибки, которое нужно добавить в поле логов.
    """
    # Создаем новый лог с текущей меткой времени
    new_log = CustomErrorSchema(message=error_message, timestamp=datetime.now().isoformat())

    # Извлекаем текущие логи
    result = await session.execute(select(model.ozon_logs).where(condition))
    existing_logs = result.scalar()

    # Проверяем, что текущие логи - это список; если нет, создаем пустой список
    if not isinstance(existing_logs, list):
        existing_logs = []
    else:
        # Находим лог с таким же сообщением и обновляем его дату
        existing_logs = [log for log in existing_logs if log["message"] != error_message]

    # Добавляем новый лог и конвертируем его в словарь для сохранения в JSONB
    updated_logs = existing_logs + [new_log.model_dump()]

    # Обновляем запись в базе
    await session.execute(update(model).where(condition).values(ozon_logs=updated_logs))
    await session.commit()
