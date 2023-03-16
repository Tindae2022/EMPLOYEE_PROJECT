from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from App.position import schema, services
from App import models
from App import db

router = APIRouter(tags=["Positions"], prefix="/position")


@router.post("/", response_model=schema.Position)
async def create_position(posi: schema.PositionCreate, db: Session = Depends(db.get_db)):
    db_posi = await services.get_position_by_name(db=db, position_name=posi.name)
    if db_posi:
        raise HTTPException(status_code=400, detail=f"The position name {posi.name} already exist")
    new_posi = await services.create_position(db=db, posi=posi)
    return new_posi


@router.get("/{posi_name}")
async def get_position_by_name(posi_name: str, db: Session = Depends(db.get_db)):
    posi_get = await services.get_position_by_name(db=db, position_name=posi_name)
    return posi_get


@router.delete("/{posi_id}")
async def delete_position(posi_id: int, db: Session = Depends(db.get_db)):
    posi = await services.delete_position_by_id(db=db, posi_id=posi_id)
    return posi


@router.patch("/{posi_id}")
async def update_position(posi: schema.PositionCreate, posi_id: int, db: Session = Depends(db.get_db)):
    position = await services.update_position(db=db, posi_id=posi_id, posi=posi)
    return position
