from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from App.employee import schema, services
from App import models
from App import db

router = APIRouter(tags=["Employee"], prefix="/employees")


@router.post("/", response_model=schema.Employee)
async def create_new_employee(emp: schema.EmployeeCreate, db: Session = Depends(db.get_db), ):
    db_emp = await services.get_employee_by_email(db=db, emp_email=emp.email)
    if db_emp:
        raise HTTPException(status_code=400, detail=f"The email {emp.email} already exist")
    new_emp = await services.create_employee(db=db, employee=emp)
    return new_emp


@router.get("/{employee_id}", response_model=schema.Employee)
async def get_employee_by_id(emp_id: int, db: Session = Depends(db.get_db)):
    emp_get = await services.get_employee_by_id(employee_id=emp_id, db=db)

    if not emp_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The employee with {emp_id} is not found")
    return emp_get


@router.get("/", response_model=List[schema.Employee])
async def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    all_emp = await services.get_employee(db=db, skip=skip, limit=limit)
    return all_emp

@router.get("/{email}", response_model=schema.Employee)
async def get_employee_by_email(email: str, db: Session = Depends(db.get_db)):
    emp_email = await services.get_employee_by_email(db=db, emp_email=email)
    return emp_email

@router.delete("/{emp_id}")
async def delete_position(emp_id: int, db: Session = Depends(db.get_db)):
    emp = await services.delete_employee_by_id(db=db, emp_id=emp_id)
    return emp


@router.patch("/{emp_id}")
async def update_employee(emp: schema.EmployeeCreate, emp_id: int, db: Session = Depends(db.get_db)):
    employee = await services.update_employee(db=db, emp_id=emp_id, emp=emp)
    return employee
