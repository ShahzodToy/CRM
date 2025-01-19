from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, delete
from sqlalchemy.orm import joinedload

from database import models, schemas


class CommonDal:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def get_income_expected_val(self):
        query = select(models.ExcpectedValue).where(models.ExcpectedValue.type == models.StatusExpectedVAlue.income)
        res = await self.db_session.execute(query)

        if res is not None:
            return res.scalars().all()
        print(res)
    
    async def get_expence_expected_val(self):
        query = select(models.ExcpectedValue).where(models.ExcpectedValue.type == models.StatusExpectedVAlue.expense)
        res = await self.db_session.execute(query)

        if res is not None:
            return res.scalars().all()
        
    async def create_expected_val(self,body:schemas.CreateExpectedValue):
        res = models.ExcpectedValue(
            name=body.name,
            date=body.date,
            description=body.description,
            type=body.type,
        )

        self.db_session.add(res)

        await self.db_session.flush()
        return res
        
    async def delete_expected_val(self, expected_val_id:int):
        query = delete(models.ExcpectedValue).where(models.ExcpectedValue.id == expected_val_id)

        res = await self.db_session.execute(query)

        await self.db_session.commit() 

        if res.rowcount > 0:
            return True
        return False
        
    async def update_expected_val(self, expected_avl_id:int, **kwargs):
        query = update(models.ExcpectedValue).where(models.ExcpectedValue.id == expected_avl_id).values(kwargs)

        res = await self.db_session.execute(query)
        await self.db_session.commit()

        if res.rowcount >0:
            return True
        return False