from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Student, Course
from schemas import CourseCreate, StudentCreate


def create_student(db: Session, student: StudentCreate):
    existing_student = db.scalars(select(Student).where(Student.email == student.email)).first()
    if existing_student:
        return None
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    result = db.scalars(select(Student).offset(skip).limit(limit)).all()
    return result


def create_course(db: Session, course: CourseCreate):
    db_course = Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_student_by_id(db: Session, student_id: int):
    return db.get(Student, student_id)


def get_course_by_id(db: Session, course_id: int):
    return db.get(Course, course_id)


def enroll_course_by_id(db: Session, student_id: int, course_id: int):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    course = get_course_by_id(db, course_id)
    if not course:
        return None
    student.courses.append(course)
    db.commit()
    db.refresh(student)
    return student