from dals import income_expense_dal,  user_dal

from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, models


async def _create_income_student(session:AsyncSession, body:schemas.CreateIncomeStudent):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        income_student = await in_ex_dal.create_income_data(body=body)

        return schemas.ShowIncomeStudent(
            id=income_student.id,
            name=income_student.name,
            real_price=income_student.real_price,
            pay_price=income_student.real_price,
            left_price=int(income_student.real_price) - int(income_student.real_price),
            date_paied=income_student.date_paied,
            position=income_student.position,
            type=income_student.type
        )
    
async def _get_list_income_student(session:AsyncSession):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        income_students = await in_ex_dal.get_list_income_student()

        return [
            schemas.ShowIncomeStudent(
            id=income_student.id,
            name=income_student.name,
            real_price=income_student.real_price,
            pay_price=income_student.real_price,
            left_price=int(income_student.real_price) - int(income_student.real_price),
            date_paied=income_student.date_paied,
            position=income_student.position,
            type=income_student.type
        )
            for income_student in income_students
        ]
    
async def _delete_income_student(session:AsyncSession, income_student_id:int):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        income_student = await in_ex_dal.delete_income_student(income_student_id)

        if income_student:
            return {'success':True,
                    'message':'Muvvafaqiyatli ochirildi'}
        
async def _update_income_student(session:AsyncSession, income_student_id:int, body:dict):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        income_student = await in_ex_dal.update_income_student(income_student_id=income_student_id,
                                                               **body)
        
        return schemas.ShowIncomeStudent(
            id=income_student.id,
            name=income_student.name,
            real_price=income_student.real_price,
            pay_price=income_student.real_price,
            left_price=int(income_student.real_price) - int(income_student.real_price),
            date_paied=income_student.date_paied,
            position=income_student.position,
            type=income_student.type
        )
# ------------------------------------------------------------------------------------------------------------------

async def _create_income_project(session:AsyncSession, body:schemas.CreateIncomeProject):
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
        empl_dal = user_dal.EmployeeDal(session)

        income_project = await in_ex_dal.create_income_project(body=body)

        project_with_id = await empl_dal.get_project_id(project_id=body.project_id)

        return schemas.ShowIncomeProject(
            id=income_project.id,
            name=project_with_id.name,
            real_price=project_with_id.price,
            date_start=project_with_id.start_date,
            pay_price=income_project.pay_price,
            date_end=project_with_id.end_date,
            type=income_project.type,
            left_price=int(project_with_id.price) - int(income_project.pay_price),
            date_paied=income_project.date_paied,
            programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await empl_dal.get_programmers_by_project_id(project_with_id.id)],

        )
    
async def _get_list_income_project(session: AsyncSession):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
        empl_dal = user_dal.EmployeeDal(session)

        income_projects = await in_ex_dal.get_list_income_project()

        result = []
        for income_project in income_projects:
            project_with_id = await empl_dal.get_project_id(project_id=income_project.project_id)

            programmers = await empl_dal.get_programmers_by_project_id(project_with_id.id)

            result.append(
                schemas.ShowIncomeProject(
                    id=income_project.id,
                    name=project_with_id.name,
                    real_price=project_with_id.price,
                    date_start=project_with_id.start_date,
                    pay_price=income_project.pay_price,
                    date_end=project_with_id.end_date,
                    type=income_project.type,
                    left_price=int(project_with_id.price) - int(income_project.pay_price),
                    date_paied=income_project.date_paied,
                    programmers=[
                        schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers
                    ],
                )
            )

        return result

async def _delete_income_project(session:AsyncSession, income_project_id:int):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        income_project = await in_ex_dal.delete_income_project(income_project_id=income_project_id)

        if income_project:
            return {'success':True,
                    'message':'Muvvafaqiyatli ochirildi'}
        
async def _update_income_project(session:AsyncSession, income_project_id:int, pay_price:str):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
        empl_dal = user_dal.EmployeeDal(session)

        income_project = await in_ex_dal.update_income_project(income_project_id=income_project_id,
                                                               pay_price=pay_price)

        project_with_id = await empl_dal.get_project_id(project_id=income_project.project_id)

        return schemas.ShowIncomeProject(
            id=income_project.id,
            name=project_with_id.name,
            real_price=project_with_id.price,
            date_start=project_with_id.start_date,
            pay_price=income_project.pay_price,
            date_end=project_with_id.end_date,
            type=income_project.type,
            left_price=int(project_with_id.price) - int(income_project.pay_price),
            date_paied=income_project.date_paied,
            programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await empl_dal.get_programmers_by_project_id(project_with_id.id)],

        )

async def _get_income_piechart(session:AsyncSession):
    in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

    total = await in_ex_dal.get_income_statistics()

    return {
        'total_income_student':total.total_from_student,
        'total_income_project':total.total_from_project,
        'total':total.grand_total,
        'percentage_income_student':(total.total_from_student/total.grand_total)*100,
        'percentage_income_project':(total.total_from_project/total.grand_total)*100,
    }

async def _create_expence_type(session:AsyncSession,
                               body:schemas.CreateNewExpence):
    in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

    create_expense = await in_ex_dal.create_expene_by_type(body=body)

    return schemas.ShowExpenseType(
        id=create_expense.id,
        price_paid=create_expense.price_paid,
        description=create_expense.description,
        date_paied=create_expense.date_paied,
        type=create_expense.type
    )




