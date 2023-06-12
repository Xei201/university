from sqlalchemy import TIMESTAMP, Column, String, BigInteger, Integer, ForeignKey, Table
from fastapi_utils.guid_type import GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy.orm import relationship

from .database import Base


# Association table for student and program Many-to-many
ProgramStudent = Table(
    'program_student',
    Base.metadata,
    Column('program_student_id',
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column('student_id', Integer, ForeignKey("student.student_id", ondelete="CASCADE")),
    Column('program_id', Integer, ForeignKey("course_program.program_id", ondelete="CASCADE")))


class FacultyType(Base):
    __tablename__ = 'faculty_type'

    name = Column(
        String(50),
        primary_key=True)

    groups = relationship(
        "GroupStudent",
        back_populates="faculty_type_name",
    )


class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(50), nullable=False)

    groups = relationship(
        "GroupStudent",
        back_populates="faculty",
    )
    teachers = relationship(
        "Teacher",
        back_populates="faculty",
    )
    all_syllabus = relationship(
        "Syllabus",
        back_populates="faculty",
        cascade="all, delete",
        passive_deletes=True,
    )


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(50), nullable=False)

    all_syllabus = relationship(
        "Syllabus",
        back_populates="course",
        cascade="all, delete",
        passive_deletes=True,
    )
    course_programs = relationship(
        "CourseProgram",
        back_populates="course",
        cascade="all, delete",
        passive_deletes=True,
    )
    exams = relationship(
        "Exam",
        back_populates="course",
        cascade="all, delete",
        passive_deletes=True,
    )


class Semester(Base):
    __tablename__ = 'semester'

    semester_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    start_date = Column(TIMESTAMP, nullable=True)
    end_date = Column(TIMESTAMP, nullable=True)

    all_syllabus = relationship(
        "Syllabus",
        back_populates="semester",
        cascade="all, delete",
        passive_deletes=True,
    )


class Building(Base):
    __tablename__ = 'building'

    building_number = Column(
        Integer,
        primary_key=True)
    address = Column(String(50))

    audiences = relationship(
        "Audience",
        back_populates="building",
        cascade="all, delete",
        passive_deletes=True,
    )


class Audience(Base):
    __tablename__ = 'audience'

    audience_number = Column(
        Integer,
        primary_key=True)
    building_number = Column(
        Integer,
        ForeignKey("building.building_number", ondelete="CASCADE"))

    building = relationship(
        "Building",
        back_populates="audiences",
    )
    schedules = relationship(
        "Schedule",
        back_populates="audience",
        cascade="all, delete",
        passive_deletes=True,
    )


class GroupStudent(Base):
    __tablename__ = 'group_student'

    group_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    faculty_id = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="SET NULL"),
        nullable=True)
    faculty_type = Column(
        String(50),
        ForeignKey("faculty_type.name", ondelete="SET NULL"),
        nullable=True)

    faculty = relationship(
        "Faculty",
        back_populates="groups",
    )
    faculty_type_name = relationship(
        "FacultyType",
        back_populates="groups",
    )
    students = relationship(
        "Student",
        back_populates="group",
    )
    schedules = relationship(
        "Schedule",
        back_populates="group",
        cascade="all, delete",
        passive_deletes=True,
    )


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    first_name = Column(String(50))
    last_name = Column(String(50))
    group_id = Column(
        Integer,
        ForeignKey("group_student.group_id", ondelete="SET NULL"),
        nullable=True)

    group = relationship(
        "GroupStudent",
        back_populates="students",
    )
    programs = relationship(
        'CourseProgram',
        secondary=ProgramStudent,
        back_populates='students')
    marks = relationship(
        "Mark",
        back_populates="student",
        cascade="all, delete",
        passive_deletes=True,
    )
    exam_marks = relationship(
        "Mark_exam",
        back_populates="student",
        cascade="all, delete",
        passive_deletes=True,
    )


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    first_name = Column(String(50))
    last_name = Column(String(50))
    faculty_id = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="SET NULL"),
        nullable=True)

    faculty = relationship(
        "Faculty",
        back_populates="teachers",
    )
    course_programs = relationship(
        "CourseProgram",
        back_populates="teacher",
    )


class Syllabus(Base):
    __tablename__ = 'syllabus'

    syllabus_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    faculty_id = Column(
        Integer,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE"))
    semester_id = Column(
        Integer,
        ForeignKey("semester.semester_id", ondelete="CASCADE"))
    course_id = Column(
        Integer,
        ForeignKey("course.course_id", ondelete="CASCADE"))

    faculty = relationship(
        "Faculty",
        back_populates="all_syllabus",
    )
    semester = relationship(
        "Semester",
        back_populates="all_syllabus",
    )
    course = relationship(
        "Course",
        back_populates="all_syllabus",
    )


class CourseProgram(Base):
    __tablename__ = 'course_program'

    program_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(50), nullable=False)
    teacher_id = Column(
        Integer,
        ForeignKey("teacher.teacher_id", ondelete="SET NULL"),
        nullable=True)
    course_id = Column(
        Integer,
        ForeignKey("course.course_id", ondelete="CASCADE"))

    teacher = relationship(
        "Teacher",
        back_populates="course_programs",
    )
    course = relationship(
        "Course",
        back_populates="course_programs",
    )
    students = relationship(
        'Student',
        secondary=ProgramStudent,
        back_populates='programs')
    schedules = relationship(
        "Schedule",
        back_populates="program",
        cascade="all, delete",
        passive_deletes=True,
    )
    exercises = relationship(
        "Exercise",
        back_populates="program",
        cascade="all, delete",
        passive_deletes=True,
    )


class Schedule(Base):
    __tablename__ = 'schedule'

    schedule_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    group_id = Column(
        Integer,
        ForeignKey("group_student.group_id", ondelete="CASCADE"))
    audience_id = Column(
        Integer,
        ForeignKey("audience.audience_number", ondelete="CASCADE"))
    subject = Column(
        Integer,
        ForeignKey("course_program.program_id", ondelete="CASCADE"))
    group = relationship(
        "GroupStudent",
        back_populates="schedules",
    )
    audience = relationship(
        "Audience",
        back_populates="schedules",
    )
    program = relationship(
        "CourseProgram",
        back_populates="schedules",
    )


class Exercise(Base):
    __tablename__ = 'exercise'

    exercise_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    program_id = Column(
        Integer,
        ForeignKey("course_program.program_id", ondelete="CASCADE"))
    program = relationship(
        "CourseProgram",
        back_populates="exercises",
    )
    marks = relationship(
        "Mark",
        back_populates="exercise",
        cascade="all, delete",
        passive_deletes=True,
    )


class Mark(Base):
    __tablename__ = 'mark'

    mark_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    student_id = Column(
        Integer,
        ForeignKey("student.student_id", ondelete="CASCADE"))
    exercise_id = Column(
        Integer,
        ForeignKey("exercise.exercise_id", ondelete="CASCADE"))

    student = relationship(
        "Student",
        back_populates="marks",
    )
    exercise = relationship(
        "Exercise",
        back_populates="marks",
    )


class Exam(Base):
    __tablename__ = 'exam'

    exam_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    date = Column(TIMESTAMP, nullable=True)
    course_id = Column(
        Integer,
        ForeignKey("course.course_id", ondelete="CASCADE"))
    course = relationship(
        "Course",
        back_populates="exams",
    )
    exam_marks = relationship(
        "Mark_exam",
        back_populates="exam",
        cascade="all, delete",
        passive_deletes=True,
    )


class Mark_exam(Base):
    __tablename__ = 'mark_exam'

    mark_exam_id = Column(
        BigInteger,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    mark = Column(Integer, nullable=False)
    student_id = Column(
        Integer,
        ForeignKey("student.student_id", ondelete="CASCADE"))
    exam_id = Column(
        Integer,
        ForeignKey("exam.exam_id", ondelete="CASCADE"))

    student = relationship(
        "Student",
        back_populates="exam_marks",
    )
    exam = relationship(
        "Exam",
        back_populates="exam_marks",
    )


