from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import teacher

router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.ListTeacherBase])
def get_teachers(db: Session = Depends(get_db)):

    db_teacher = teacher.get_objs(db=db)
    return db_teacher


@router.get("/{id}", response_model=schemas.GetTeacherBase)
def get_teacher(id: int, db: Session = Depends(get_db)):
    db_teacher = teacher.get_obj(db=db, id=id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return db_teacher

