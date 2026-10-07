from pydantic import BaseModel, EmailStr, ConfigDict


class CourseCreate(BaseModel):
    title: str
    description: str | None


class CourseResponse(CourseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    name: str
    email: EmailStr


class StudentResponse(StudentCreate):
    id: int
    courses: list[CourseResponse] = []

    model_config = ConfigDict(from_attributes=True)

