from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

student_course = Table(
    'student_course',
    Base.metadata,
    Column(
        "student_id",
        Integer,
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),
    Column(
        "course_id",
        Integer,
        ForeignKey(
            "courses.id",
        ondelete="CASCADE"),
    primary_key=True
    )
)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(String(500))
    students: Mapped[list["Student"]] = relationship(
        secondary=student_course,
        back_populates="courses"
    )
