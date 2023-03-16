from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from App.department import schema, services
from App import models
from App import db

router = APIRouter(tags=["Department"], prefix="/department")


@router.post("/", response_model=schema.Department)
async def create_department(dept: schema.DepartmentCreate, db: Session = Depends(db.get_db)):
    db_dept = await services.get_department_by_name(db=db, department_name=dept.name)
    if db_dept:
        raise HTTPException(status_code=400, detail=f"The department name {dept.name} already exist")
    new_dept = await services.create_department(db=db, dept=dept)
    return new_dept


@router.get("/{dept_id}", response_model=schema.Department)
async def get_department_by_id(dept_id: int, db: Session = Depends(db.get_db)):
    dept = await services.get_department_by_id(department_id=dept_id, db=db)
    return dept


@router.get("/{dept_name}")
async def get_department_by_name(dept_name: str, db: Session = Depends(db.get_db)):
    dept_new = await services.get_department_by_name(db=db, department_name=dept_name)
    return dept_new


@router.get("/", response_model=List[schema.Department])
async def get_all_department(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    dept_all = await services.get_department(db=db, skip=skip, limit=limit)
    return dept_all


@router.delete("/{dept_id}")
async def delete_department(dept_id: int, db: Session = Depends(db.get_db)):
    dept = await services.delete_department_by_id(db=db, dept_id=dept_id)
    return dept


@router.patch("/{dept_id}")
async def update_department(dept: schema.DepartmentCreate, dept_id: int, db: Session = Depends(db.get_db)):
    department = await services.update_department(db=db, dept_id=dept_id, dept=dept)
    return department
