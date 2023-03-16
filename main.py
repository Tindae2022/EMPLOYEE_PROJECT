from fastapi import FastAPI
from App.department.router import router as dept_router
from App.position.router import router as posi_router
from App.employee.router import router as emp_router

app = FastAPI(title="Tindae Company", version="0.0.1")

app.include_router(dept_router)
app.include_router(posi_router)
app.include_router(emp_router)
