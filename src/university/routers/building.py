from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import building


router = APIRouter(
    prefix="/biuldings",
    tags=["biuldings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.GetBuildingBase])
def get_buildings(db: Session = Depends(get_db)):
    db_audience = building.get_objs(db=db)

    return db_audience


@router.get("/{id}", response_model=schemas.GetBuildingBase)
def get_building(id: int, db: Session = Depends(get_db)):
    db_audience = building.get_obj(db=db, id=id)

    if db_audience is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return db_audience


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_building(payload: schemas.BuildingBase, db: Session = Depends(get_db)):
    new_building = building.get_obj(db=db, id=payload.building_number)
    if new_building:
        raise HTTPException(status_code=400, detail="This number building is exist")

    new_building = building.create_obj(db=db, new_object=payload)
    return {"status": "success", "object": new_building}

