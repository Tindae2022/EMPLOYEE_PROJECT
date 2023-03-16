from sqlalchemy.orm import Session
from App.department import schema
from App import models
from fastapi import HTTPException, status

async def get_department_by_id(db: Session, department_id: int):
    return db.query(models.Departments).filter(models.Departments.id == department_id).first()


async def get_department(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Departments).offset(skip).limit(limit).all()


async def get_department_by_name(db: Session, department_name: str):
    return db.query(models.Departments).filter(models.Departments.name == department_name).first()


async def create_department(db: Session, dept: schema.DepartmentCreate):
    db_department = models.Departments(name=dept.name, location=dept.location)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


async def delete_department_by_id(dept_id: int, db: Session):
    db.query(models.Departments).filter(models.Departments.id == dept_id).delete()
    db.commit()
    return {"status": "Deleted successfully", "department": dept_id}


async def update_department(db: Session, dept_id: int, dept: schema.DepartmentCreate):
    dept_query = db.query(models.Departments).filter(models.Departments.id == dept_id)
    db_dept = dept_query.first()
    if not db_dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No _department with this id: {dept_id} found")
    updateData = dept.dict(exclude_unset=True)
    dept_query.filter(models.Departments.id == dept_id).update(updateData, synchronize_session=False)
    db.commit()
    db.refresh(db_dept)
    return {"status": "updated successfully", "department": db_dept}
