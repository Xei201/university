from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import exam_mark

router = APIRouter(
    prefix="/grades",
    tags=["grades"],
    responses={404: {"description": "Not found"}},
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_mark(payload: schemas.CreateMarkExamBase, db: Session = Depends(get_db)):
    new_mark = exam_mark.create_obj(db=db, new_object=payload)

    return {"status": "success", "object": new_mark}


@router.put('/{grade_id}')
def update_mark(grade_id: int, payload: schemas.MarkExamBase, db: Session = Depends(get_db)):
    grade_query = exam_mark.get_obj(db=db, id=grade_id)
    if grade_query is None:
        raise HTTPException(status_code=400, detail="Grade not exist")

    update_grade = exam_mark.update_obj(db=db, id=grade_id, new_data=payload)
    return {"status": "success", "student": update_grade}
