from .. import models, schemas
from sqlalchemy.orm import Session, joinedload


def get_obj(db: Session, id: int):
    return db.query(models.Audience).\
        where(models.Audience.audience_number == id).one()


def get_objs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Audience).offset(skip).limit(limit).all()


def create_obj(db: Session, new_object: schemas.AudienceBase):
    new_audience = models.Audience(**new_object.dict())
    db.add(new_audience)
    db.commit()
    db.refresh(new_audience)
    return new_audience

