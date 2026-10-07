from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import engine, Base, get_db
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academy API")


@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.create_student(db=db, student=student)
    if db_student is None:
        raise HTTPException(status_code=400, detail="Этот email уже зарегистрирован")
    return db_student


@app.get("/students/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_students(db=db, skip=skip, limit=limit)


@app.post("/courses/", response_model=schemas.CourseResponse)
def create_courses(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)


@app.post("/students/{student_id}/enroll/{course_id}/", response_model=schemas.StudentResponse)
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    updated_student = crud.enroll_course_by_id(db=db, student_id=student_id, course_id=course_id)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Студент или курс не найден")
    return updated_student
