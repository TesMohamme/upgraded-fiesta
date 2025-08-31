from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentals=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== الموديلات ======
class Student(BaseModel):
    id: int
    name: str
    grade: int

class StudentCreate(BaseModel):
    name: str
    grade: int

# ====== "قاعدة بيانات" في الذاكرة ======
students_db: list[Student] = [
    Student(id=1, name="Mohammed Adm", grade=5),
    Student(id=2, name="Almez Mohamed", grade=5),
]

# ====== المسارات ======
@app.get("/students/")
def read_students() -> list[Student]:
    return students_db

@app.get("/students/{student_id}")
def read_student(student_id: int) -> Student:
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students/", status_code=201)
def create_student(new_student: StudentCreate) -> Student:
    # توليد id تلقائي بسيط
    new_id = (max((s.id for s in students_db), default=0) + 1)
    student = Student(id=new_id, **new_student.model_dump())
    students_db.append(student)
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated: Student) -> Student:
    # PUT = استبدال كامل للسجل (id في الـ body يجب يطابق المسار أو نتجاهله)
    for index, student in enumerate(students_db):
        if student.id == student_id:
            # نحافظ على id المسار لكي يكون المصدر الوحيد للحقيقة
            students_db[index] = Student(id=student_id, name=updated.name, grade=updated.grade)
            return students_db[index]
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            students_db.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Student not found")
