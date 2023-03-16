from pydantic import BaseModel
from typing import List
from App.employee.schema import Employee


class DepartmentBase(BaseModel):
    name: str
    location: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int
    employees: List[Employee]

    class Config:
        orm_mode = True
