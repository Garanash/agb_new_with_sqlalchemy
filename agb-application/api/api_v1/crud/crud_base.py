from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, select
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """
    CRUD-операции для модели.
    """

    def __init__(self, model) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """
        Возвращает объект из базы данных по идентификатору.
        """
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """
        Возвращает список объектов из базы данных.
        """
        query = select(self.model)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ):
        """
        Создает новый объект в базе данных.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """
        Обновляет объект в базе данных.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """
        Удаляет объект из базы данных.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def search(
        self,
        request: str,
        session: AsyncSession,
    ):
        """
        Производит поиск объектов по заданному полю.
        """
        attributes = [attr.key for attr in inspect(self.model).mapper.attrs]
        attributes.pop(attributes.index('marked_for_deletion'))
        attributes.pop(attributes.index('id'))
        conditions = [
            getattr(self.model, attr).ilike(f"%{request}%")
            for attr in attributes
        ]
        query = select(self.model).where(or_(*conditions))
        result = await session.execute(query)
        return result.scalars().all()
