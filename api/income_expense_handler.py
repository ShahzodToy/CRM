from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, session
from dals import income_expense_dal
from api.action import income_expense

expense_income_handler = APIRouter()

@expense_income_handler.post('/create_income_student')
async def create_income_student(body:schemas.CreateIncomeStudent ,db:AsyncSession = Depends(session.get_db)):
    return await income_expense._create_income_student(body=body, session=db)

@expense_income_handler.get('/list-income-student', response_model=List[schemas.ShowIncomeStudent])
async def get_list_income_student(db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_list_income_student(session=db)

@expense_income_handler.delete('/delete-income-student')
async def delete_create_income(income_student_id:int, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._delete_income_student(income_student_id=income_student_id, session=db)

@expense_income_handler.patch('/update-income-student')
async def update_income_student(income_student_id:int, update_params:schemas.UpdateStudentIncome, db:AsyncSession=Depends(session.get_db)):
    body = update_params.model_dump(exclude_none=True)
    return await income_expense._update_income_student(session=db, income_student_id=income_student_id,
                                                       body=body)

@expense_income_handler.post('/create_income_project')
async def create_income_project(body:schemas.CreateIncomeProject, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._create_income_project(session=db, body=body)

@expense_income_handler.get('/get-list-income-project')
async def get_list_income_project(db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_list_income_project(session=db)

@expense_income_handler.delete('/delete-income-project')
async def delete_income_project(income_project_id:int, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._delete_income_project(income_project_id=income_project_id,
                                                       session=db)

@expense_income_handler.patch('/update-income-project')
async def update_income_project(income_project_id:int, pay_price:str|None, session:AsyncSession=Depends(session.get_db)):

    return await income_expense._update_income_project(income_project_id=income_project_id,
                                                       pay_price=pay_price,
                                                       session=session)

@expense_income_handler.get('/get-pie-chart-income')
async def get_income_chiechart(db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_income_piechart(session=db)

@expense_income_handler.post('/create-expense-type')
async def create_expense(body:schemas.CreateNewExpence,db:AsyncSession=Depends(session.get_db)):
    return await income_expense._create_expence_type(session=db, body=body)




