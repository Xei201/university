from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import student

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.ListStudentBase])
def get_students(db: Session = Depends(get_db)):
    db_student = student.get_objs(db=db)
    return db_student


@router.get("/{student_id}", response_model=schemas.GetStudentBase)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student.get_obj(db=db, id=student_id)

    return db_student


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_student(payload: schemas.StudentBase, db: Session = Depends(get_db)):
    new_student = student.create_obj(db=db, new_object=payload)

    return {"status": "success", "object": new_student}


@router.delete('/{student_id}')
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_query = student.get_obj(db=db, id=student_id)
    if student_query is None:
        raise HTTPException(status_code=400, detail="Student not exist")

    student.delete_obj(db=db, object_query=student_query)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{student_id}')
def update_student(student_id: int, payload: schemas.StudentBase, db: Session = Depends(get_db)):
    student_query = student.get_obj(db=db, id=student_id)
    if student_query is None:
        raise HTTPException(status_code=400, detail="Student not exist")

    update_student = student.update_obj(db=db, id=student_id, new_data=payload)
    return {"status": "success", "student": update_student}