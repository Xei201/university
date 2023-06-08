from sqlalchemy import TIMESTAMP, Column, String, BigInteger, Integer, ForeignKey
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

from ..database import Base


class FacultyType(Base):
    __tablename__ = 'faculty_type'

    name = Column(
        String(50),
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)


class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(50), nullable=False)


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(50), nullable=False)


class Semester(Base):
    __tablename__ = 'semester'

    semester = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    start_date = Column(TIMESTAMP, nullable=True)
    end_date = Column(TIMESTAMP, nullable=True)


class Building(Base):
    __tablename__ = 'building'

    building_numer = Column(
        Integer,
        primary_key=True)
    address = Column(String(50))


class Audience(Base):
    __tablename__ = 'audience'

    audience_numer = Column(
        Integer,
        primary_key=True)
    building = Column(
        Integer,
        ForeignKey("building.building_number", ondelete="CASCADE"))


class GroupStudent(Base):
    __tablename__ = 'group_student'

    group_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    faculty = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE"))
    faculty_type = Column(
        String(50),
        ForeignKey("faculty_type.name", ondelete="CASCADE"))


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    first_name = Column(String(50))
    last_name = Column(String(50))
    group_student = Column(
        Integer,
        ForeignKey("group_student.group_id", ondelete="SET NULL"))


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    first_name = Column(String(50))
    last_name = Column(String(50))
    faculty = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="SET NULL"))


class Syllabus(Base):
    __tablename__ = 'syllabus'

    syllabus_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    faculty = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE"))
    semester = Column(
        Integer,
        ForeignKey("semester.semester_id", ondelete="CASCADE"))
    course = Column(
        Integer,
        ForeignKey("course.course_id", ondelete="CASCADE"))


class CourseProgram(Base):
    __tablename__ = 'course_program'

    program_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    teacher = Column(
        Integer,
        ForeignKey("teacher.teacher_id", ondelete="SET NULL"))
    course = Column(
        Integer,
        ForeignKey("course.course_id", ondelete="CASCADE"))


class ProgramStudent(Base):
    __tablename__ = 'program_student'

    program_student_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    student = Column(
        Integer,
        ForeignKey("student.student_id", ondelete="CASCADE"))
    program = Column(
        Integer,
        ForeignKey("program.program_id", ondelete="CASCADE"))


class Schedule(Base):
    __tablename__ = 'schedule'

    schedule_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    group_student = Column(
        Integer,
        ForeignKey("group_student.group_id", ondelete="CASCADE"))
    audience = Column(
        Integer,
        ForeignKey("audience.audience_numer", ondelete="CASCADE"))
    subject = Column(
        Integer,
        ForeignKey("course_program.program_id", ondelete="CASCADE"))


class Exercise(Base):
    __tablename__ = 'exercise'

    exercise_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    date_creation = Column(
        TIMESTAMP,
        nullable=False,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    program = Column(
        Integer,
        ForeignKey("program.program_id", ondelete="CASCADE"))


class Mark(Base):
    __tablename__ = 'mark'

    mark_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    student = Column(
        Integer,
        ForeignKey("student.student_id", ondelete="CASCADE"))
    exercise = Column(
        Integer,
        ForeignKey("exercise.exercise_numer", ondelete="CASCADE"))


class Mark(Base):
    __tablename__ = 'mark'

    mark_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    student = Column(
        Integer,
        ForeignKey("student.student_id", ondelete="CASCADE"))
    exercise = Column(
        Integer,
        ForeignKey("exercise.exercise_numer", ondelete="CASCADE"))


