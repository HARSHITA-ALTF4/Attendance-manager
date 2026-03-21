import sqlite3

conn = sqlite3.connect("college_attendance.db")
cur = conn.cursor()

# enable foreign keys
cur.execute("PRAGMA foreign_keys = ON")

# ---------------------------
# DROP TABLES (if exist)
# ---------------------------

cur.executescript("""

DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS attendance_sessions;
DROP TABLE IF EXISTS class_subjects;
DROP TABLE IF EXISTS grades;
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

CREATE TABLE grades (
  grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  subject_id INTEGER NOT NULL,
  marks REAL,
  grade TEXT,
  UNIQUE(student_id, subject_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
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
  status TEXT NOT NULL CHECK(status IN ('P','A')),
  PRIMARY KEY (session_id, student_id),
  FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);

""")

# ---------------------------
# INSERT CLASS
# ---------------------------

cur.execute("""
INSERT INTO classes (year_name, division, academic_year)
VALUES ('SY','A','2025-26')
""")

# ---------------------------
# INSERT TEACHERS
# ---------------------------

teachers = [
('Pooja Jadhav','pooja@college.com'),
('Ashwini Patil','ashwini@college.com'),
('Prof C','c@college.com'),
('Prof D','d@college.com'),
('Prof E','e@college.com'),
('Prof F','f@college.com')
]

cur.executemany(
"INSERT INTO teachers (teacher_name,email) VALUES (?,?)",
teachers
)

# ---------------------------
# INSERT SUBJECTS
# ---------------------------

subjects = [
('101','DATABASE MANAGEMENT SYSTEM'),
('102','DATA SCIENCE'),
('103','PROBABILITY AND STATISTICS'),
('104','EMBEDDED SYSTEM'),
('105','PROJECT MANAGEMENT'),
('106','EVS')
]

cur.executemany(
"INSERT INTO subjects (subject_code,subject_name) VALUES (?,?)",
subjects
)

# ---------------------------
# CLASS SUBJECTS
# ---------------------------

class_subjects = [
(1,1,1),
(1,2,2),
(1,3,3),
(1,4,4),
(1,5,5),
(1,6,6)
]

cur.executemany(
"INSERT INTO class_subjects (class_id,subject_id,teacher_id) VALUES (?,?,?)",
class_subjects
)

# ---------------------------
# STUDENTS
# ---------------------------

students = [
('2101','THERESA MATTEL','s2101@gmail.com',1),
('2102','SHIVARKAR ANISHKA RAHUL','s2102@gmail.com',1),
('2103','PATOLE NAMRATA SHASHIKANT','s2103@gmail.com',1),
('2104','GHOSH PRATHAMA ANISH','s2104@gmail.com',1),
('2105','JORWAR PANKAJ RAJU','s2105@gmail.com',1),
('2106','NEMADE SIDDHESH TUSHAR','s2106@gmail.com',1),
('2107','SHINDE MONIKA SUBHASH','s2107@gmail.com',1),
('2108','MULE SUJAL SAMEER','s2108@gmail.com',1),
('2109','TONDARE SIYA MAHENDRA','s2109@gmail.com',1),
('2110','PAWAR HARSHADA SACHIN','s2110@gmail.com',1),
('2111','KHALELKAR TANUSHREE ANUP','s2111@gmail.com',1),
('2112','SHERE SANDHYA RAMPRASAD','s2112@gmail.com',1),
('2113','MALAVE PAYAL PANDURANG','s2113@gmail.com',1),
('2114','SHUKLA HITESHI JAYESH','s2114@gmail.com',1),
('2115','GOLE ANUSHKA MAHADEV','s2115@gmail.com',1),
('2116','KORE GAYATRI VIJAYKUMAR','s2116@gmail.com',1),
('2117','SHINDE OMKAR HARISH','s2117@gmail.com',1),
('2118','BHOSALE SUSHANT SOMNATH','s2118@gmail.com',1),
('2119','MAINDAD OMKAR DHANANJAY','s2119@gmail.com',1),
('2120','PUPPALWAR SOHAM PANDHARI','s2120@gmail.com',1),
('2121','DHAGE GAURAV RAVINDRA','s2121@gmail.com',1),
('2122','NEVASE SHRIRAJ SUNIL','s2122@gmail.com',1),
('2123','KUDCHIKAR PARAS PANDURANG','s2123@gmail.com',1),
('2124','FAKATKAR PRADNYA KAILAS','s2124@gmail.com',1),
('2125','SONAWANE PRUTHVI ANIL','s2125@gmail.com',1),
('2126','SHAIKH AMAN RAJU','s2126@gmail.com',1),
('2127','SHAIKH ALI RIYAZ','s2127@gmail.com',1),
('2128','JADHAV PAYAL PRAVIN','s2128@gmail.com',1),
('2129','WANKHADE POOJA SANJAY','s2129@gmail.com',1),
('2130','KALE RUTUJA ASHOK','s2130@gmail.com',1),
('2131','GAIKWAD CHETAN NAGNATH','s2131@gmail.com',1),
('2132','ABHISHEK GAURAV','s2132@gmail.com',1),
('2133','KHODE VEDANT KESHAV','s2133@gmail.com',1),
('2134','PATIL AKSHAY UMESH','s2134@gmail.com',1),
('2135','SONKULE SHREYASH','s2135@gmail.com',1),
('2136','KOLHE NIKHIL ASHOK','s2136@gmail.com',1),
('2137','VIRDHE OMKAR ATUL','s2137@gmail.com',1),
('2138','DESHMUKH SHREYA PRASHANT','s2138@gmail.com',1),
('2139','GHULE YASH PRABHAKAR','s2139@gmail.com',1),
('2140','LAKHE ADITYA SAMBHAJI','s2140@gmail.com',1),
('2141','GANGJI ADITYA SUNIL','s2141@gmail.com',1),
('2142','KOLI JYOTI SIDRAM','s2142@gmail.com',1),
('2143','PICHARE CHAITANYA CHANDRAKANT','s2143@gmail.com',1),
('2144','SONONE RADHIKA DIGHAMBER','s2144@gmail.com',1),
('2145','TANDEL TAHAAM IMRAN','s2145@gmail.com',1),
('2146','NADANWAR YASHASHVI','s2146@gmail.com',1),
('2147','GURAV RAVIRAJ VIJAY','s2147@gmail.com',1),
('2148','LOKHANDE OMKAR KALURAM','s2148@gmail.com',1),
('2149','RANE DILESH RAMESHWAR','s2149@gmail.com',1),
('2150','JADHAV ANUJA YENKU','s2150@gmail.com',1),
('2151','RAUT SURAJ VAIBHAV','s2151@gmail.com',1),
('2152','CHAVAN MAYUR MAHENDRA','s2152@gmail.com',1),
('2153','DHOLE NANDINI SUNIL','s2153@gmail.com',1),
('2154','KHATRI HARSHITA','s2154@gmail.com',1),
('2155','BODAKHE GAURI SADASHIVAPPA','s2155@gmail.com',1),
('2156','PATIL VISHWAJIT PRASHANT','s2156@gmail.com',1),
('2157','PATIL PRASHANT SANJAY','s2157@gmail.com',1),
('2158','BHADALE SPANDAN RAHUL','s2158@gmail.com',1),
('2159','GAIKWAD VEDIKA SATISH','s2159@gmail.com',1),
('2160','PAWAR SAMRUDDHI RAJESH','s2160@gmail.com',1),
('2161','DIVYAM RAJ','s2161@gmail.com',1),
('2162','TRIVEDI YUG RAJEEV','s2162@gmail.com',1),
('2163','DESHMUKH YASH NITIN','s2163@gmail.com',1),
('2164','UNDE SIDDHARTH DILIP','s2164@gmail.com',1),
('2165','SARWADE ANARY SACHIN','s2165@gmail.com',1),
('2166','GHADGE YASH VINOD','s2166@gmail.com',1),
('2167','WATTAMWAR SHASHANK RAMESH','s2167@gmail.com',1),
('2168','SUKHADIYA YASH MUKESH','s2168@gmail.com',1),
('2169','KAMBLE VISHWPRATAP SACHIN','s2169@gmail.com',1),
('2170','MASIHA SILVIYA SANTOSH','s2170@gmail.com',1),
('2171','GOLANDE ADITYA YOGESH','s2171@gmail.com',1),
('2172','MORE HARSHAL MANOHAR','s2172@gmail.com',1),
('2173','SONAWANE SUYASH MAHESH','s2173@gmail.com',1),
('2174','BENKE SIDDHI SAGAR','s2174@gmail.com',1),
('2175','DAREKAR SAMRUDDHI BALASO','s2175@gmail.com',1),
('2176','WAGH TANUSHREE KISHOR','s2176@gmail.com',1),
('2177','MAHER TANISHA KARANSINGH','s2177@gmail.com',1),
('2178','KADAM PRASAD ASHOK','s2178@gmail.com',1),
('2179','DAHIWAL OMKAR SURESH','s2179@gmail.com',1)
]

cur.executemany(
"INSERT INTO students (roll_no,full_name,email,class_id) VALUES (?,?,?,?)",
students
)

conn.commit()
conn.close()

print("Database created successfully!")