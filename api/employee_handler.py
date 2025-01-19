import shutil
import os
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form

from sqlalchemy.ext.asyncio import AsyncSession

from api.action import employee
from api.login_handler import get_current_user_from_token
from datetime import datetime

from database import schemas, session, models


emp_router = APIRouter()

UPLOAD_DIRECTORY = "media/uploads"  # Directory to store uploaded files
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the directory exists

@emp_router.post('/create_user', response_model=schemas.ShowEmployee)
async def create_employee(
    date_of_birth: Optional[datetime] = Form(default=None),
    salary: int = Form(...),
    position_id: int = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    first_name: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    date_of_jobstarted: datetime = Form(...),
    db: AsyncSession = Depends(session.get_db),
    file: Optional[UploadFile] = File(None)
):
    
    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving the file.")
    
    employee_data = schemas.EmployeeCreate(
        date_of_birth=date_of_birth,
        salary=salary,
        position_id=position_id,
        last_name=last_name,
        username=username,
        first_name=first_name,
        phone_number=phone_number,
        password=password,
        date_of_jobstarted=date_of_jobstarted
    )
    return await employee._create_new_employee(body=employee_data, session=db, file_name=f'uploads/{file.filename}')


@emp_router.get('/list',response_model=List[schemas.ShowEmployee])
async def get_all_employee(position_id:Optional[int]=None ,db:AsyncSession = Depends(session.get_db)):
    return await employee._get_all_employee(db, position_id)
    
UPLOAD_DIRECTORY1 = 'media/projects'

@emp_router.post('/create_project',response_model=schemas.ShowProject)
async def create_project(
    name: str = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    progemmer_list: list[str] = Form(...),
    price: str = Form(...),
    db: AsyncSession = Depends(session.get_db),
    image: Optional[UploadFile] = File(None)
    ):

    try:
        print(progemmer_list)
        programmer_ids = [int(x) for x in progemmer_list[0] if x.isdigit()]
    except ValueError:
        raise HTTPException(
                status_code=400, detail="All elements in progemmer_list must be valid integers."
            )
        
    try:
        file_path = os.path.join(UPLOAD_DIRECTORY1, image.filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving the file.")
    
    body = schemas.CreateProject(
        name=name,
        start_date=start_date,
        end_date=end_date,
        programmer_ids=programmer_ids,
        price=price

    )
    return await employee._create_project(session=db, body=body,image=f'projects/{image.filename}')
    

@emp_router.get('/list-projects', response_model=List[schemas.ShowProject])
async def get_list_projects(db:AsyncSession = Depends(session.get_db)):
    return await employee._get_all_projects(db)

@emp_router.get('/detail-employee', response_model=schemas.ShowEmployeeDetail)
async def get_detail_employee(user_id:int, db:AsyncSession = Depends(session.get_db)):
    return await employee._get_detail_employee(user_id,db)

@emp_router.post('/create_operator', response_model=schemas.ShowOperator)
async def create_new_operator(body:schemas.CreateOperator, db:AsyncSession = Depends(session.get_db)):
    return await employee._create_new_operatoe(session=db, body=body)

@emp_router.get('/list-operator', response_model=List[schemas.ShowOperator])
async def get_all_operators(oper_type_id:Optional[int]=None, status:Optional[str]=None, db:AsyncSession = Depends(session.get_db)):
    return await employee._get_all_operators(operator_type_id=oper_type_id, session=db, status=status)

@emp_router.post('/change-status-operator')
async def change_operator_status(oper_id:int, status:str, db:AsyncSession = Depends(session.get_db)):
    return await employee._change_operator_status(oper_id=oper_id,
                                                  status=status,
                                                  session=db)
