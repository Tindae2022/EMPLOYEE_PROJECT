from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from App.position import schema
from App import models


async def get_position_by_id(db: Session, position_id: int):
    return db.query(models.Positions).filter(models.Positions.id == position_id).first()


async def get_position(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Positions).offset(skip).limit(limit).all()


async def get_position_by_name(db: Session, position_name: str):
    return db.query(models.Positions).filter(models.Positions.name == position_name).first()


async def create_position(db: Session, posi: schema.PositionCreate):
    db_position = models.Positions(name=posi.name, description=posi.description)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


async def delete_position_by_id(posi_id: int, db: Session):
    db.query(models.Positions).filter(models.Positions.id == posi_id).delete()
    db.commit()
    return {"status": "Deleted successfully", "department": posi_id}


async def update_position(db: Session, posi_id: int, posi: schema.PositionCreate):
    posi_query = db.query(models.Positions).filter(models.Positions.id == posi_id)
    db_posi = posi_query.first()
    if not db_posi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No _position with this id: {posi_id} found")
    updateData = posi.dict(exclude_unset=True)
    posi_query.filter(models.Positions.id == posi_id).update(updateData, synchronize_session=False)
    db.commit()
    db.refresh(db_posi)
    return {"status": "updated successfully", "position": db_posi}
