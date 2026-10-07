import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from db import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test_academy.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

    engine.dispose()

    if os.path.exists("./test_academy.db"):
        try:
            os.remove("./test_academy.db")
        except PermissionError:
            pass

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_student():
    response = client.post(
        "/students/",
        json={"name": "Иван", "email": "ivan@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Иван"
    assert data["email"] == "ivan@example.com"
    assert "id" in data

def test_create_student_duplicate_email():
    response = client.post(
        "/students/",
        json={"name": "Другой Иван", "email": "ivan@example.com"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Этот email уже зарегистрирован"

def test_get_students():
    response = client.get("/students/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

