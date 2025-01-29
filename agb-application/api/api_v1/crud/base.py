from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import (AccordingToTheDrawing, AdaptersAndPlugs,
                         Metiz, Project, PurchasedHydroperforator,
                         Purchased, RWD, User)


class CRUDBase:

    def __init__(self, model) -> None:
        self.model = model

    async def get(self, session: AsyncSession):
        stmt = select(self.model).order_by(self.model.id)
        result = await session.scalars(stmt)
        return result.all()

    async def create(self, session: AsyncSession, obj_in):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, session: AsyncSession, db_obj, obj_in):
        obj_in_data = obj_in.dict(exclude_unset=True)
        for field in obj_in_data:
            setattr(db_obj, field, obj_in_data[field])
        await session.commit()
        return db_obj

    async def delete(self, session: AsyncSession, db_obj):
        session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_all(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()


class AccordingToTheDrawingCRUD(CRUDBase):
    pass


class AdaptersAndPlugsCRUD(CRUDBase):
    pass


class MetizCRUD(CRUDBase):
    pass


class ProjectCRUD(CRUDBase):
    pass


class PurchasedCRUD(CRUDBase):
    pass


class PurchasedHydroperforatorCRUD(CRUDBase):
    pass


class RWDCRUD(CRUDBase):
    pass


class UserCRUD(CRUDBase):
    pass


# Usage
accordingtothedrawing_crud = AccordingToTheDrawingCRUD(AccordingToTheDrawing)
adaotersandplugs_crud = AdaptersAndPlugsCRUD(AdaptersAndPlugs)
metiz_crud = MetizCRUD(Metiz)
projects_crud = ProjectCRUD(Project)
purchased_crud = PurchasedCRUD(Purchased)
purchasedhydroperforator_crud = PurchasedHydroperforatorCRUD(PurchasedHydroperforator)
rwd_crud = RWDCRUD(RWD)
users_crud = UserCRUD(User)
