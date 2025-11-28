from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class BatchUpdateErrorsSchema(BaseSchema):

    not_unique: list[int] | None = Field(..., title="Список ИД с ошибкой обновления из за уникальности")

    missed: list[int] | None = Field(..., title="Список ИД с ошибкой обновления из за отсутствия записи")

    incorrect: list[int] | None = Field(..., title="Список ИД с ошибкой обновления из за некорректных данных")

    class Config:

        from_attributes = True
