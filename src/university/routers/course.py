from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas
from ..crud import course


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{course_id}", response_model=schemas.GetCourseBase)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course.get_obj(db=db, id=course_id)
    print(db_course.name, db_course.course_id)
    return db_course


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_course(payload: schemas.CourseBase, db: Session = Depends(get_db)):
    new_course = course.create_obj(db=db, new_object=payload)
    return {"status": "success", "object": new_course}


@router.get("/{course_id}/students_on_program", response_model=schemas.GetProgramCourseBase)
def get_objs_course_students(course_id: int, db: Session = Depends(get_db)):
    db_course = course.get_objs_students_on_course(db=db, id=course_id)
    return db_course


@router.get("/{course_id}/students", response_model=List[schemas.StudentBase])
def get_objs_only_students(course_id: int, db: Session = Depends(get_db)):
    db_course = course.get_objs_students(db=db, id=course_id)
    return db_course