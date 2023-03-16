import datetime
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from App.db import Base
from sqlalchemy.orm import relationship


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    location = Column(String(50), index=False)

    employees = relationship("Employees", back_populates="department")


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    departments_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    salary = Column(Float, nullable=False)
    hireDate = Column(DateTime, default=datetime.datetime.now())

    department = relationship("Departments", back_populates="employees")
    position = relationship("Positions", back_populates="employees")


class Positions(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(50))

    employees = relationship("Employees", back_populates="position")
