from .. import models, schemas
from sqlalchemy.orm import Session, joinedload


def get_obj(db: Session, id: int):
    return db.query(models.Mark_exam). \
        filter(models.Mark_exam.mark_exam_id == id).first()


def create_obj(db: Session, new_object: schemas.CreateMarkExamBase):
    new_mark = models.Mark_exam(**new_object.dict())
    db.add(new_mark)
    db.commit()
    db.refresh(new_mark)

    return new_mark


def update_obj(db: Session, id: int, new_data: schemas.MarkExamBase):
    update_data = new_data.dict(exclude_unset=True)
    update_mark = db.query(models.Mark_exam).filter(models.Mark_exam.mark_exam_id == id)
    update_mark.update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(update_mark.first())

    return update_mark.first()

