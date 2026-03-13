from fastapi import FastAPI, HTTPException
from schemes.models import CreateStudent, CreateCourse, CreateEnrollment, Enrollment_by_id
from database.database import (create_tables, insert_student, insert_course, get_all_courses, get_all_students, get_all_enrollments, get_student_by_id, enroll_student, get_course_by_id, get_enrollment_count, check_if_enrolled, delete_enrollment)

app = FastAPI()

create_tables()

@app.get("/students")
def read_students():
    return get_all_students()

@app.post("/students")
def add_student(student: CreateStudent):
    insert_student(student.name, student.email)
    return {"message": "the following user has been successfully created:",
            "user": {"name": student.name, "email": student.email}}

@app.get("/courses")
def read_courses():
    return get_all_courses()

@app.post("/course")
def add_course(course: CreateCourse):
    insert_course(course.name, course.instructor, course.capacity)
    return {"message": "the following course has been successfully created:",
            "course": {"name": course.name, "instructor": course.instructor, "capacity": course.capacity}}


@app.get("/enrollments")
def read_enrollments():
    return get_all_enrollments()

@app.post("/enrollments")
def add_enrollment(enrl: CreateEnrollment):
    if not get_student_by_id(enrl.student_id):
        raise HTTPException(status_code=404, detail="The entered student doesn't exist")
    if not get_course_by_id(enrl.course_id):
        raise HTTPException(status_code=404, detail="The entered course doesn't exist")
    if get_enrollment_count(enrl.course_id) == get_course_by_id(enrl.course_id)["capacity"]:
        raise HTTPException(status_code=400, detail="the choosen course has already reached its maximum capacity.")
    if check_if_enrolled(enrl.student_id, enrl.course_id):
        raise HTTPException(status_code=400, detail="The student is already enrolled in the specified course.")
    enrollment = enroll_student(enrl.student_id, enrl.course_id, enrl.enrollment_date)
    return {"message": "the following enrollment has been successfully created:",
            "course": {"student_name": enrollment["student_name"], "course_name": enrollment["course_name"], "enrollment_date": enrollment["enrollment_date"]}}
@app.delete("/enrollments/{enrl_id}")
def delete_enrll(enrl_id: int):
    enrollment = delete_enrollment(enrl_id)
    return {"message": "the following enrollment has been successfully deleted:",
            "enrollment_details": enrollment}
