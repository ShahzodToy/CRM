from sqlalchemy import select, update, delete, and_, func, case, cast, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, schemas



class IncomeExepnseDal:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_income_data(self,body:schemas.CreateIncomeStudent):
        query = models.IncomeData(
            name = body.name,
            real_price = body.real_price,
            pay_price=body.pay_price,
            date_paied=body.date_paid,
            position=body.position,
            type='from_student'
        )

        self.db_session.add(query)

        await self.db_session.commit()

        return query
    
    async def get_list_income_student(self):
        query = select(models.IncomeData).where(models.IncomeData.type=='from_student')

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def delete_income_student(self, income_student_id:int):
        query = delete(models.IncomeData).where(and_(models.IncomeData.type=='from_student'),(models.IncomeData.id==income_student_id))

        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False
    
    async def update_income_student(self, income_student_id:int, **kwargs):
        query = update(models.IncomeData).where(and_(models.IncomeData.type=='from_student'),(models.IncomeData.id==income_student_id)).values(**kwargs).returning(models.IncomeData)

        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
    
    async def create_income_project(self,body:schemas.CreateIncomeProject):
        query = models.IncomeData(
            project_id = body.project_id,
            pay_price=body.pay_price,
            type='from_project'
        )


        self.db_session.add(query)

        await self.db_session.commit()

        return query
    
    async def get_list_income_project(self):
        query = select(models.IncomeData).where(models.IncomeData.type=='from_project')

        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def delete_income_project(self, income_project_id:int):
        query = delete(models.IncomeData).where(and_(models.IncomeData.type=='from_project'),(models.IncomeData.id==income_project_id))

        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False
    
    async def update_income_project(self, income_project_id:int, pay_price:str):

        query = update(models.IncomeData).where(and_(models.IncomeData.type=='from_project'),(models.IncomeData.id==income_project_id)).values(pay_price=pay_price).returning(models.IncomeData)

        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
    
    async def get_income_statistics(self):
        query = (
            select(
                func.sum(
                    case(
                        (models.IncomeData.type == "from_student", cast(models.IncomeData.pay_price, Integer)),
                        else_=0,
                    )
                ).label("total_from_student"),
                func.sum(
                    case(
                        (models.IncomeData.type == "from_project", cast(models.IncomeData.pay_price, Integer)),
                        else_=0,
                    )
                ).label("total_from_project"),
                func.sum(cast(models.IncomeData.pay_price, Integer)).label("grand_total")
            )
        )

        result = await self.db_session.execute(query)
        stats = result.one()

        return stats
    
    async def create_expene_by_type(self,body:schemas.CreateNewExpence):
        query = models.ExpenseData(
            name=body.name,
            description=body.description,
            price_paid=body.price_paid,
            date_paied=body.date_paied,
            real_price=body.real_price,
            type=body.type
        )

        self.db_session.add(query)
        await self.db_session.commit()

        return query
    
    async def get_list_expense(self,status):
        query = select(models.ExpenseData).where(models.ExpenseData.type==status)

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def delete_expense(self, expense_id):
        query = delete(models.ExpenseData).where(models.ExpenseData.id==expense_id)
        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False


    




