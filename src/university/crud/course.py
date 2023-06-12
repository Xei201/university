from .. import models, schemas
from sqlalchemy.orm import Session, joinedload, subqueryload


def get_obj(db: Session, id: int):
    return db.query(models.Course).options(joinedload(models.Course.course_programs)). \
        where(models.Course.course_id == id).one()


def create_obj(db: Session, new_object: schemas.CourseBase):
    new_course = models.Course(**new_object.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_objs_students_on_course(db: Session, id: int):
    db_cource = db.query(models.Course).options(joinedload(models.Course.course_programs). \
        subqueryload(models.CourseProgram.students)). \
        where(models.Course.course_id == id).one()

    return db_cource


def get_objs_students(db: Session, id: int, skip: int = 0, limit: int = 100):
    db_cource = db.query(models.Course).options(joinedload(models.Course.course_programs). \
        subqueryload(models.CourseProgram.students)). \
        where(models.Course.course_id == id).one()

    id_programs = set()
    for element in db_cource.course_programs:
        id_programs.add(element.program_id)

    list_student = db.query(models.Student).join(models.Student.programs).\
        filter(models.CourseProgram.program_id.in_(id_programs)).\
        offset(skip).limit(limit).all()

    return list_student