from datetime import datetime
from fastapi import File, UploadFile, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, delete, func, case
from sqlalchemy.orm import joinedload, selectinload

from database import models, schemas

from utils.hashing import Hasher


class EmployeeDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_employee(self, position_id):
        query = select(models.Employees).join(models.Position).where(models.Employees.is_active==True).options(
                        selectinload(models.Employees.position))
        if position_id:
            query = select(models.Employees).join(models.Position).where(and_(models.Employees.is_active==True, models.Employees.position_id == position_id)).options(
                        selectinload(models.Employees.position))
        res = await self.db_session.execute(query)

        all_user = res.scalars().all()
        return all_user
    
    async def create_employee(self, first_name:str, last_name:str,
                              password:str, position_id: int,phone_number:str,
                              date_of_birth:datetime, date_of_jobstarted, salary:int,username:str,
                              image:str):
        
        new_employee = models.Employees(
            first_name=first_name,
            last_name=last_name,
            password=Hasher.get_password_hash(password),
            position_id=position_id,
            phone_number=phone_number,
            date_of_jobstarted=date_of_jobstarted,
            date_of_birth=date_of_birth,
            username=username,
            salary=salary,
            image=image
        )

        self.db_session.add(new_employee)
        await self.db_session.flush()
        return new_employee

    async def get_username(self, username:str):
        query = (
            select(models.Employees).where(models.Employees.username == username)
        )
        res = await self.db_session.execute(query)

        username = res.fetchone()
        if username is not None:
            return username[0]

    async def create_project(self, name:str, 
                            start_date:datetime,
                            end_date:datetime, 
                            image:str,
                            programmer_ids: list[str],
                            price: str):
        
        new_project = models.Project(
            name=name,
            start_date=start_date,
            end_date=end_date,
            image=image,
            price=price
        )
        self.db_session.add(new_project)
        await self.db_session.flush() 

        project_programmers = [
            models.ProjectProgrammer(
                project_id=new_project.id,
                programmer_id=int(programmer_id)
            )
            for programmer_id in programmer_ids
        ]
        self.db_session.add_all(project_programmers)

        await self.db_session.commit()

        await self.db_session.refresh(new_project)

        return new_project
    
    async def get_programmers_by_project_id(self, project_id: int):
        result = await self.db_session.execute(
            select(models.Employees).join(models.ProjectProgrammer).where(models.ProjectProgrammer.project_id == project_id)
        )
        return result.scalars().all()

    async def get_al_projects(self):
        query = select(models.Project).where(models.Project.is_deleted==False)
        res = await self.db_session.execute(query)
        all_projects = res.scalars().all()

        return all_projects
    
    async def get_project_id(self, project_id):
        query = select(models.Project).where(and_(models.Project.is_deleted==False),(models.Project.id == project_id))
        res = await self.db_session.execute(query)
        all_projects = res.scalar_one_or_none()

        return all_projects


    async def get_employee_detail(self, user_id):
        query = select(models.Employees).where(models.Employees.id==user_id)
        query_2 = (
            select(models.Project)
            .options(joinedload(models.Project.programmers)) 
            .where(and_(models.Project.programmers.any(models.Employees.id == user_id)),(models.Project.is_deleted==False))
        )
        result_user_info = await self.db_session.execute(query)
        result_user_projects = await self.db_session.execute(query_2)

        user_info = result_user_info.scalar_one()
        user_projects = result_user_projects.unique().scalars().all() 
        
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user_info is not None and user_projects is not None:
            return (user_info, user_projects)

    async def create_operator(self,full_name:str, 
                              phone_number:str, 
                              description:str,operator_type_id:int):
        query = models.Operator(
            full_name=full_name,
            phone_number=phone_number,
            description=description,
            operator_type_id=operator_type_id,
        )

        self.db_session.add(query)
        await self.db_session.flush()  # Commit the session to persist the data
        # await self.db_session.refresh(query)  # Refresh to access relationships
        return query
    
    async def get_operator_type_by_id(self,op_id:int):
        query = (
            select(models.OperatorType)
            .where(models.OperatorType.id == op_id)
        )
        result = await self.db_session.execute(query)
        operator_with_type = result.scalar_one()
        return operator_with_type.name
    
    async def get_all_operator(self, oper_type_id:int,status:str):
        query = select(models.Operator)

        if oper_type_id and status:
            query = select(models.Operator).where(and_(models.Operator.operator_type_id == oper_type_id, models.Operator.status == status))
        if oper_type_id:
            query = select(models.Operator).where(models.Operator.operator_type_id == oper_type_id)
        elif status:
            query = select(models.Operator).where(models.Operator.status == status)

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def change_operator_status(self,oper_id:int, status:str):
        if status not in models.StatusOperator.__members__.values():
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.values())}")
        
        try:
            status_enum = models.StatusOperator[status]  # Convert string to StatusOperator enum
        except KeyError:
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.keys())}")

        query = (
            update(models.Operator)
            .values(status=status_enum)
            .filter_by(id = oper_id)
            .returning(models.Operator) 
        )

        res = await self.db_session.execute(query) 
  
        return res.scalar_one_or_none()

    async def delete_created_project(self, project_id:int):
        query = update(models.Project).where(models.Project.id == project_id).values(is_deleted=True)

        res = await self.db_session.execute(query)
        self.db_session.commit()

        if res.rowcount > 0:
            return True
        return False

    async def update_created_project(self, project_id:int,image:str|None, body:schemas.UpdateProject):
    
        preject_update = (
                update(models.Project)
                .where(models.Project.id == project_id)
                .values(
                    name=body.name,
                    start_date=body.start_date,
                    end_date=body.end_date,
                    image=image,
                    price=body.price
                )
            ).returning(models.Project)
        res = await self.db_session.execute(preject_update)
        task_result = res.scalar_one_or_none()

        if not task_result:
            return None
        
        await self.db_session.execute(
            delete(models.ProjectProgrammer).where(models.ProjectProgrammer.project_id == project_id)
        )
        for programmer_id in body.programmers:
            project_programmer = models.ProjectProgrammer(
                project_id=project_id,
                programmer_id=programmer_id,
            )
            self.db_session.add(project_programmer)

            
        await self.db_session.commit()

        return task_result
    
    async def update_status_project(self, project_id:int, status:str):
        project_update = update(models.Project).where(models.Project.id == project_id).values(status=status).returning(models.Project)

        result = await self.db_session.execute(project_update)

        return result.scalar_one_or_none()
        
    async def get_list_position(self):
        query = select(models.Position)

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def create_position(self, name):
        query = models.Position(name=name)

        self.db_session.add(query)

        await self.db_session.commit()
        return query

    