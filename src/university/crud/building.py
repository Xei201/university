from .. import models, schemas
from sqlalchemy.orm import Session, joinedload


def get_obj(db: Session, id: int):
    return db.query(models.Building).options(joinedload(models.Building.audiences)).\
        where(models.Building.building_number == id).one()


def get_objs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).options(joinedload(models.Building.audiences)).offset(skip).limit(limit).all()


def create_obj(db: Session, new_object: schemas.BuildingBase):
    new_building = models.Building(**new_object.dict())
    db.add(new_building)
    db.commit()
    db.refresh(new_building)

    return new_building

