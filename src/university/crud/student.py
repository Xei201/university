from .. import models, schemas
from sqlalchemy.orm import Session, joinedload


def get_obj(db: Session, id: int):
    return db.query(models.Student).options(joinedload(models.Student.programs)). \
        where(models.Student.student_id == id).one()


def get_objs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_obj(db: Session, new_object: schemas.StudentBase):
    new_student = models.Student(**new_object.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def delete_obj(db: Session, object_query):
    db.delete(object_query)
    db.commit()


def update_obj(db: Session, id: int, new_data: schemas.StudentBase):
    update_data = new_data.dict(exclude_unset=True)
    update_student = db.query(models.Student).filter(models.Student.student_id == id)
    update_student.update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(update_student.first())

    return update_student.first()

