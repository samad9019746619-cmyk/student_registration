from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# ---------------- DATABASE ----------------

def create_database():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()


# ---------------- HOME PAGE ----------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id DESC")

    students = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "students": students
        }
    )
# ---------------- REGISTER STUDENT ----------------

@app.post("/register")
def register_student(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    age: int = Form(...),
    course: str = Form(...)
):

    connection = sqlite3.connect("students.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, email, phone, age, course)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, age, course))

    connection.commit()
    connection.close()

    return RedirectResponse("/", status_code=303)


# ---------------- DELETE STUDENT ----------------

@app.get("/delete/{student_id}")
def delete_student(student_id: int):

    connection = sqlite3.connect("students.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse("/", status_code=303)