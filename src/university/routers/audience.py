from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import audience


router = APIRouter(
    prefix="/audiences",
    tags=["audiences"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.AudienceBase])
def get_audiences(db: Session = Depends(get_db)):
    db_audience = audience.get_objs(db=db)

    return db_audience


@router.get("/{id}", response_model=schemas.AudienceBase)
def get_audience(id: int, db: Session = Depends(get_db)):
    db_audience = audience.get_obj(db=db, id=id)

    if db_audience is None:
        raise HTTPException(status_code=404, detail="Audience not found")
    return db_audience


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_audience(payload: schemas.AudienceBase, db: Session = Depends(get_db)):
    new_audience = audience.get_obj(db=db, id=payload.audience_number)
    if new_audience:
        raise HTTPException(status_code=400, detail="This number audience is exist")

    new_audience = audience.create_obj(db=db, new_object=payload)
    return {"status": "success", "object": new_audience}