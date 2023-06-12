from .. import models
from sqlalchemy.orm import Session, joinedload


def get_obj(db: Session, id: int):
    return db.query(models.Teacher).options(joinedload(models.Teacher.faculty)). \
        options(joinedload(models.Teacher.course_programs)). \
        where(models.Teacher.teacher_id == id).one()


def get_objs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

