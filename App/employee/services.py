from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from App.employee import schema
from App import models


async def get_employee_by_id(employee_id: int, db: Session):
    return db.query(models.Employees).filter(models.Employees.id == employee_id).first()


async def get_employee(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employees).offset(skip).limit(limit).all()


async def get_employee_by_email(db: Session, emp_email: str):
    return db.query(models.Employees).filter(models.Employees.email == emp_email).first()


async def create_employee(db: Session, employee: schema.EmployeeCreate):
    db_emp = models.Employees(name=employee.name, salary=employee.salary, hireDate=employee.hireDate,
                              email=employee.email, departments_id=employee.departments_id,
                              position_id=employee.position_id)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

async def delete_employee_by_id(emp_id: int, db: Session):
    db.query(models.Employees).filter(models.Employees.id == emp_id).delete()
    db.commit()
    return {"status": "Deleted successfully", "Employees": emp_id}


async def update_employee(db: Session, emp_id: int, emp: schema.EmployeeCreate):
    emp_query = db.query(models.Employees).filter(models.Employees.id == emp_id)
    db_emp = emp_query.first()
    if not db_emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No _employee with this id: {emp_id} found")
    updateData = emp.dict(exclude_unset=True)
    emp_query.filter(models.Positions.id == emp_id).update(updateData, synchronize_session=False)
    db.commit()
    db.refresh(db_emp)
    return {"status": "updated successfully", "product": db_emp}