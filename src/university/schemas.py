from pydantic import BaseModel, constr
from typing import List, Optional


# Faculty models
class FacultyBase(BaseModel):
    name: constr(max_length=50)

    class Config:
        orm_mode = True


class GetFacultyBase(FacultyBase):
    faculty_id: int


# Audience models
class AudienceBase(BaseModel):
    audience_number: int
    building_number: int

    class Config:
        orm_mode = True


# Building models
class BuildingBase(BaseModel):
    building_number: int
    address: constr(max_length=50)

    class Config:
        orm_mode = True


class GetBuildingBase(BuildingBase):
    audiences: List[AudienceBase]


# CourseProgram models
class CourseProgramBase(BaseModel):
    program_id: int
    name: constr(max_length=50)
    teacher_id: Optional[int]
    course_id: int

    class Config:
        orm_mode = True


# Separate student model to avoid recursion
class ProgramStudentBase(BaseModel):
    student_id: int
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    group_id: Optional[int]

    class Config:
        orm_mode = True


class GetCourseProgramBase(CourseProgramBase):
    students: List[ProgramStudentBase]


# Course models
class CourseBase(BaseModel):
    name: constr(max_length=50)

    class Config:
        orm_mode = True


class GetCourseBase(CourseBase):
    course_id: int
    course_programs: Optional[List[CourseProgramBase]]


class GetProgramCourseBase(CourseBase):
    course_id: int
    course_programs: List[GetCourseProgramBase]


# Student models
class StudentBase(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    group_id: Optional[int]

    class Config:
        orm_mode = True


class ListStudentBase(StudentBase):
    student_id: int


class GetStudentBase(ListStudentBase):
    programs: Optional[List[CourseProgramBase]]


# Teacher models
class TeacherBase(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    faculty_id: Optional[int]

    class Config:
        orm_mode = True


class ListTeacherBase(TeacherBase):
    teacher_id: int


class GetTeacherBase(ListTeacherBase):
    faculty: Optional[GetFacultyBase]
    course_programs: Optional[List[CourseProgramBase]]



