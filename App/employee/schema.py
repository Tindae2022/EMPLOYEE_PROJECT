from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    salary: float
    hireDate: datetime
    email: str


class EmployeeCreate(EmployeeBase):
    departments_id: int
    position_id: int



class Employee(EmployeeBase):
    id: int
    departments_id: int
    position_id: int

    class Config:
        orm_mode = True
