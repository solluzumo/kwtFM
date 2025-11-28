from app.schemas.BaseSchema import BaseSchema


from datetime import datetime


class CustomErrorSchema(BaseSchema):
    message: str  # Текст ошибки
    timestamp: str  # Дата и время ошибки в формате строки