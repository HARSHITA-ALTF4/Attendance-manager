import sqlite3


conn = sqlite3.connect("college_attendance.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")

cur.executescript(
    """
    DROP TABLE IF EXISTS attendance;
    DROP TABLE IF EXISTS grades;
    DROP TABLE IF EXISTS attendance_sessions;
    DROP TABLE IF EXISTS class_subjects;
    DROP TABLE IF EXISTS students;
    DROP TABLE IF EXISTS subjects;
    DROP TABLE IF EXISTS teachers;
    DROP TABLE IF EXISTS classes;

    CREATE TABLE classes (
      class_id INTEGER PRIMARY KEY AUTOINCREMENT,
      year_name TEXT NOT NULL,
      division TEXT NOT NULL,
      academic_year TEXT NOT NULL,
      UNIQUE(year_name, division, academic_year)
    );

    CREATE TABLE students (
      student_id INTEGER PRIMARY KEY AUTOINCREMENT,
      roll_no TEXT NOT NULL UNIQUE,
      full_name TEXT NOT NULL,
      email TEXT,
      class_id INTEGER NOT NULL,
      FOREIGN KEY (class_id) REFERENCES classes(class_id)
    );

    CREATE TABLE teachers (
      teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
      teacher_name TEXT NOT NULL,
      email TEXT
    );

    CREATE TABLE subjects (
      subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
      subject_code TEXT NOT NULL UNIQUE,
      subject_name TEXT NOT NULL
    );

    CREATE TABLE class_subjects (
      class_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
      class_id INTEGER NOT NULL,
      subject_id INTEGER NOT NULL,
      teacher_id INTEGER NOT NULL,
      UNIQUE(class_id, subject_id),
      FOREIGN KEY (class_id) REFERENCES classes(class_id),
      FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
      FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    );

    CREATE TABLE attendance_sessions (
      session_id INTEGER PRIMARY KEY AUTOINCREMENT,
      class_subject_id INTEGER NOT NULL,
      session_date TEXT NOT NULL,
      start_time TEXT,
      FOREIGN KEY (class_subject_id) REFERENCES class_subjects(class_subject_id)
    );

    CREATE TABLE attendance (
      session_id INTEGER NOT NULL,
      student_id INTEGER NOT NULL,
      status TEXT NOT NULL CHECK(status IN ('P', 'A')),
      PRIMARY KEY (session_id, student_id),
      FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
      FOREIGN KEY (student_id) REFERENCES students(student_id)
    );

    CREATE TABLE grades (
      student_id INTEGER NOT NULL,
      subject_id INTEGER NOT NULL,
      marks REAL,
      grade TEXT,
      PRIMARY KEY (student_id, subject_id),
      FOREIGN KEY (student_id) REFERENCES students(student_id),
      FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    );
    """
)

cur.execute(
    "INSERT INTO classes (year_name, division, academic_year) VALUES (?, ?, ?)",
    ("SY", "A", "2025-26"),
)

teachers = [
    ("Pooja Jadhav", "pooja@college.com"),
    ("Ashwini Patil", "ashwini@college.com"),
    ("Prof C", "c@college.com"),
    ("Prof D", "d@college.com"),
    ("Prof E", "e@college.com"),
    ("Prof F", "f@college.com"),
]
cur.executemany("INSERT INTO teachers (teacher_name, email) VALUES (?, ?)", teachers)

subjects = [
    ("101", "DATABASE MANAGEMENT SYSTEM"),
    ("102", "DATA SCIENCE"),
    ("103", "PROBABILITY AND STATISTICS"),
    ("104", "EMBEDDED SYSTEM"),
    ("105", "PROJECT MANAGEMENT"),
    ("106", "EVS"),
]
cur.executemany("INSERT INTO subjects (subject_code, subject_name) VALUES (?, ?)", subjects)

class_subjects = [
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3),
    (1, 4, 4),
    (1, 5, 5),
    (1, 6, 6),
]
cur.executemany(
    "INSERT INTO class_subjects (class_id, subject_id, teacher_id) VALUES (?, ?, ?)",
    class_subjects,
)

students = [
    ("2101", "THERESA MATTEL", "s2101@gmail.com", 1),
    ("2102", "SHIVARKAR ANISHKA RAHUL", "s2102@gmail.com", 1),
    ("2103", "PATOLE NAMRATA SHASHIKANT", "s2103@gmail.com", 1),
    ("2104", "GHOSH PRATHAMA ANISH", "s2104@gmail.com", 1),
    ("2105", "JORWAR PANKAJ RAJU", "s2105@gmail.com", 1),
    ("2106", "NEMADE SIDDHESH TUSHAR", "s2106@gmail.com", 1),
    ("2107", "SHINDE MONIKA SUBHASH", "s2107@gmail.com", 1),
    ("2108", "MULE SUJAL SAMEER", "s2108@gmail.com", 1),
    ("2109", "TONDARE SIYA MAHENDRA", "s2109@gmail.com", 1),
    ("2110", "PAWAR HARSHADA SACHIN", "s2110@gmail.com", 1),
]
cur.executemany(
    "INSERT INTO students (roll_no, full_name, email, class_id) VALUES (?, ?, ?, ?)",
    students,
)

conn.commit()
conn.close()

print("SQLite database created successfully!")
