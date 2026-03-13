from pydantic import BaseModel


class CreateStudent(BaseModel):
    name : str
    email : str

class CreateCourse(BaseModel):
    name : str
    instructor : str
    capacity : int

class CreateEnrollment(BaseModel):
    student_id : int
    course_id : int
    enrollment_date : str 

class Enrollment_by_id(BaseModel):
    id: int
