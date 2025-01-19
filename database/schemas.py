from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, constr, field_validator

class EmployeeCreate(BaseModel):
    last_name:str
    first_name:str
    phone_number:str
    date_of_birth:datetime
    date_of_jobstarted:datetime
    salary:int
    username:str
    position_id:int
    password:str

    class Config:
        orm_format = True

    @field_validator('date_of_birth', 'date_of_jobstarted')
    def make_datetimes_naive(cls, v):
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        return v
    

class ShowEmployee(BaseModel):
    id:int
    last_name: str
    first_name: str
    phone_number: str
    date_of_birth: Optional[datetime] = None
    date_of_jobstarted: datetime
    username:str
    salary: int
    user_type: str
    image: Optional[str] = None

    class Config:
        orm_format = True

class Token(BaseModel):
    access_token:str
    type:str


class CreateProject(BaseModel):
    name:str
    start_date:datetime
    end_date:datetime
    programmer_ids:List[int]
    price:str


class ProgrammerSchema(BaseModel):
    id: int
    first_name: str
    image: str
    last_name: str

    class Config:
        from_attributes = True


class ShowProject(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    image: str
    programmers: List[ProgrammerSchema]
    status:str
    price:str | None

    class Config:
        from_attributes = True


class ShowEmployeeDetail(BaseModel):
    id:int
    last_name: str
    first_name: str
    phone_number: str
    date_of_birth: Optional[datetime] = None
    date_of_jobstarted: datetime
    username:str
    salary: int
    user_type: str
    image: Optional[str] = None
    projects: List[ShowProject] = []

    class Config:
        from_attributes = True


class CreateOperator(BaseModel):
    full_name:str
    phone_number:str
    description:str
    operator_type_id:int


class ShowOperator(BaseModel):
    id:int
    full_name:str
    phone_number:str
    description:str
    operator_type_id:int
    operator_type:Optional[str]
    status:str

    class Config:
        from_attributes = True

class ShowExpectedValue(BaseModel):
    id:int
    name:str
    date:datetime
    description:str
    type:Optional[str] = None

    class Config:
        from_attributes = True

class CreateExpectedValue(BaseModel):
    name:str
    date:datetime
    description:str
    type:str

class UpdateExpectedValue(BaseModel):
    name:Optional[str] = None
    date:Optional[datetime] = None
    description:Optional[str] =None
    