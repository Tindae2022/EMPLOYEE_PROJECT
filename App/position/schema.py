from typing import List
from pydantic import BaseModel
from App.employee.schema import Employee


class PositionBase(BaseModel):
    name: str
    description: str


class PositionCreate(PositionBase):
    pass


class Position(PositionBase):
    id: int
    employees: List[Employee]

    class Config:
        orm_mode = True
