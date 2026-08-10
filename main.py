from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row

conn = psycopg.connect(
    host="localhost",
    dbname="student_api",
    user="krisharora",
    port=5432,
    row_factory=dict_row
)

app = FastAPI()

students = []

class Student(BaseModel):
    name: str
    age: int
    roll_no: int
    branch: str

@app.get("/")
def home():
    return {"message": "Hello!"}

@app.get("/about")
def about_profile():
    return {"name": "Krish", "role": "AI Engineer"}

@app.get("/skills")
def acquired_skills():
    return {"Skills": ["python","frontend", "backend", "AI"]}

@app.get("/projects")
def major_projects():
    return {"Projects": ["Resume Analyzer with AI", "Weather app"]}

@app.get("/contact")
def contact_details():
    return{"email": "xyz@gmail.com", "phone no.": "1234567890"}

@app.get("/square/{number}")
def square(number: int):
   
    return{"number": number, "square": number * number }

@app.post("/students", status_code = 201)
def create_student(student: Student):
    try:
        result = conn.execute(
        """
        INSERT INTO student
        (roll_no, name, age, branch)
        VALUES (%s, %s, %s, %s)
        """,
        (
            student.roll_no,
            student.name,
            student.age,
            student.branch
        )
    )
        conn.commit()
        
        return {
            "message": "Student created successfully",
            "student": student
        }
    
    except:
        raise HTTPException(
        status_code = 409,
        detail = "Student already exists!")

@app.get("/students") 
def get_students():
    result = conn.execute(
        "SELECT * FROM student;"
    )

    return result.fetchall()

@app.put("/students/{roll_no}")
def update_student(roll_no: int, student: Student):
    try:
        result = conn.execute(
            """
            UPDATE student
            SET
                roll_no = %s,
                name = %s,
                age = %s,
                branch = %s
            WHERE roll_no = %s;
            """,
            (
                student.roll_no,
                student.name,
                student.age,
                student.branch,
                roll_no,
            )
        )
        if result.rowcount == 0:
            conn.rollback()
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        
        conn.commit()
    
        return {
        "message": "Student updated successfully",
        "student": student
    }

    except HTTPException:
        raise

    except Exception as e:
        conn.rollback()
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
@app.delete("/students/{roll_no}")
def delete_student(roll_no: int):
    try:
        result = conn.execute(
            """DELETE FROM student
               WHERE roll_no = %s""",
               (roll_no,)
        )
        
        if result.rowcount == 0:
                conn.rollback()
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )
        conn.commit()
        return {
            "message": f"Student with roll number {roll_no} deleted successfully"
        }
            
    except HTTPException:
            raise
        
    except Exception as e:
            conn.rollback()
            print(e)
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
        
        
    
       
    

   
@app.get("/students/{roll_no}")
def search_student(roll_no: int):
    
    result = conn.execute(
        """ SELECT *
            FROM student
            WHERE roll_no = %s;""",
            (roll_no,))
    student = result.fetchone()
    
                              
    if student is None:
        raise HTTPException(
        status_code = 404,
        detail = "Student not found")
        
    return student
    
