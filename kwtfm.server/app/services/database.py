from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Type, Any, TypeVar, Generic

from app.schemas.BaseSchema import BaseSchema
from app.schemas.SortItemSchema import SortItemSchema
from app.schemas.FilterItemSchema import FilterItemSchema
from app.utils.listOperators import apply_filters, apply_sorting

T = TypeVar("T", bound=BaseSchema)


class DBService(Generic[T]):
    def __init__(
        self,
        model: Type,
        session: AsyncSession,
        schema: Type[T],
    ):
        self.session = session
        self.model = model
        self.schema = schema

    # single insert
    async def create(self, data: Any) -> T:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)  # Обновляем объект модели
        return data

    # select with pagination and sorting and filtering for data table
    async def select(
        self,
        sorting: list[SortItemSchema],
        filtering: list[FilterItemSchema],
        page: int,
        pageSize: int,
    ):

        query = select(self.model)

        if filtering:

            query = apply_filters(query, filtering, self.model)

        if sorting:

            query = apply_sorting(query, sorting, self.model)

        result = await self.session.execute(query.offset(pageSize * page).limit(pageSize))

        items = [row for row in result.scalars().all()]

        count_query = select(func.count()).select_from(self.model)

        if filtering:

            count_query = apply_filters(count_query, filtering, self.model)

        total_rows = await self.session.execute(count_query)
        total_count: int = total_rows.scalar() or 0

        return {"rows": items, "totalRows": total_count}

    # single select by any unique field
    async def getOneBy(self, field: str, value: Any) -> Any | None:
        query = select(self.model).where(getattr(self.model, field) == value)

        return await self.session.scalar(query)

    async def batch_insert(self, data: list[Any]) -> List[Any]:
        new_data = [self.model(**item) for item in data]
        self.session.add_all(new_data)
        await self.session.commit()

        # получаем список созданных моделей
        query = select(self.model).where(self.model.id.in_([item.id for item in new_data]))
        new_data = await self.session.execute(query)
        result: List[Type] = [row for row in new_data.scalars().all()]

        return result

    async def batch_update(self, data: list[Any]) -> List[Any]:

        for item in data:
            query = select(self.model).where(self.model.id == item["id"])
            model = await self.session.scalar(query)

            if model:

                for key, value in item.items():
                    setattr(model, key, value)

        await self.session.commit()

        # получаем список обновленных моделей
        query = select(self.model).where(self.model.id.in_([item["id"] for item in data]))
        new_data = await self.session.execute(query)
        result: List[Type] = [row for row in new_data.scalars().all()]

        return result

    async def batch_delete(self, data: list[int]) -> list[int]:
        query = select(self.model).where(self.model.id.in_(data))
        models = await self.session.execute(query)
        models = models.scalars().all()

        result = []
        for model in models:
            result.append(model.id)
            await self.session.delete(model)

            await self.session.commit()

        return result
