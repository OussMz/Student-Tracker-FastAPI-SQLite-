import sqlite3

def get_connection():
    conn = sqlite3.connect("uni_db.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE       
            )
""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                instructor TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                UNIQUE(name, instructor)   
            )
""")    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrollment_date TEXT NOT NULL,
                UNIQUE(student_id, course_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
""")    
        conn.commit()

def insert_student(name, email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students(name, email) VALUES(?, ?)
""", (name, email))
        conn.commit()

def insert_course(name, instructor, capacity):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO courses(name, instructor, capacity) VALUES(?, ?, ?)
""", (name, instructor, capacity))
        conn.commit()

def get_all_students():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students
""")
        return [dict(row) for row in cursor.fetchall()]

def get_all_courses():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM courses
""")
        return [dict(row) for row in cursor.fetchall()]
    
def get_course_by_id(course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM courses WHERE id = ?
""", (course_id,))
        fetched_course = cursor.fetchone()
        return dict(fetched_course) if fetched_course else None

def get_student_by_id(student_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM students WHERE id = ?
        """, (student_id,))
        fetched_course = cursor.fetchone()
        return dict(fetched_course) if fetched_course else None
    
def get_enrollment_count(course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM enrollments WHERE course_id = ?
""", (course_id,))
        return cursor.fetchone()[0]

def enroll_student(student_id, course_id, enrollment_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO enrollments(student_id, course_id, enrollment_date) VALUES(?, ?, ?)
        """, (student_id, course_id, enrollment_date))
        conn.commit()
        cursor.execute("""
            SELECT students.name AS student_name, courses.name AS course_name, enrollment_date
            FROM enrollments
            JOIN students ON students.id = enrollments.student_id
            JOIN courses ON courses.id = enrollments.course_id
            WHERE students.id = ? AND courses.id = ?
        """, (student_id, course_id))
        result = cursor.fetchone()
        return dict(result) if result else None        

def get_enrollment_by_id(enrl_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                    students.name AS student_name,
                    courses.name AS course_name,
                    enrollment_date
            FROM enrollments
            JOIN students ON students.id = enrollments.student_id
            JOIN courses ON courses.id = enrollments.course_id
            WHERE enrollments.id = ?
        """, (enrl_id,))
        enrollment = cursor.fetchone()
        return dict(enrollment) if enrollment else None
    
def get_all_enrollments():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                    enrollments.id,
                    students.name AS student_name,
                    courses.name AS course_name,
                    enrollment_date
            FROM enrollments
            JOIN students ON students.id = enrollments.student_id
            JOIN courses ON courses.id = enrollments.course_id
        """)
        return [dict(row) for row in cursor.fetchall()]
    
def check_if_enrolled(student_id, course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM enrollments WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))
        return True if cursor.fetchone()[0] == 1 else False
    

def delete_enrollment(enrl_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        enrollment = get_enrollment_by_id(enrl_id)
        cursor.execute("""
            DELETE FROM enrollments
            WHERE id = ?
        """, (enrl_id,))
        conn.commit()
        return enrollment
        

