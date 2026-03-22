import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = "dev-secret"

# 1. Railway MySQL Environment Variables fallback to localhost
app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQLDATABASE', 'attendance')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT', 3306))

# Helper to manage connection
def get_conn():
    try:
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# ----------------------------
# INTRO PAGE
# ----------------------------
@app.route("/")
def intro():
    return render_template("intro.html")


# ----------------------------
# DASHBOARD / HOME
# ----------------------------
@app.route("/dashboard")
def home():
    return render_template("home.html")


# ----------------------------
# LIST + ADD STUDENTS
# ----------------------------
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = get_conn()
    if not conn:
        flash("Database connection failed!")
        return redirect(url_for('home'))
    cur = conn.cursor()

    # find first class row
    cur.execute("SELECT class_id, year_name, division, academic_year FROM classes LIMIT 1")
    klass = cur.fetchone()

    if not klass:
        conn.close()
        return "No class found. Please insert a class row in classes table first."

    if request.method == "POST":
        roll_no = request.form["roll_no"].strip()
        full_name = request.form["full_name"].strip()
        email = request.form.get("email", "").strip() or None

        try:
            cur.execute(
                "INSERT INTO students (roll_no, full_name, email, class_id) VALUES (%s, %s, %s, %s)",
                (roll_no, full_name, email, klass["class_id"])
            )
            conn.commit()
            flash("Student added!")
        except Exception as e:
            conn.rollback()
            flash(f"Error adding student: {e}")

        conn.close()
        return redirect(url_for("students"))

    cur.execute("SELECT roll_no, full_name, email FROM students ORDER BY roll_no")
    rows = cur.fetchall()
    conn.close()
    return render_template("students.html", students=rows, klass=klass)


# ----------------------------
# CREATE ATTENDANCE SESSION
# ----------------------------
@app.route("/create-session", methods=["GET", "POST"])
def create_session():
    conn = get_conn()
    if not conn:
        flash("Database connection failed!")
        return redirect(url_for('home'))
    cur = conn.cursor()

    cur.execute("""
        SELECT cs.class_subject_id, s.subject_code, s.subject_name, t.teacher_name
        FROM class_subjects cs
        JOIN subjects s ON s.subject_id = cs.subject_id
        JOIN teachers t ON t.teacher_id = cs.teacher_id
        ORDER BY s.subject_code
    """)
    class_subjects = cur.fetchall()

    if request.method == "POST":
        class_subject_id = request.form.get("class_subject_id")
        session_date = request.form.get("session_date")
        start_time = request.form.get("start_time", "").strip() or None

        if not class_subject_id or not session_date:
            flash("Please select subject and date.")
            conn.close()
            return redirect(url_for("create_session"))

        try:
            cur.execute(
                "INSERT INTO attendance_sessions (class_subject_id, session_date, start_time) VALUES (%s, %s, %s)",
                (int(class_subject_id), session_date, start_time)
            )
            conn.commit()
            flash("Session created!")
        except Exception as e:
            conn.rollback()
            flash(f"Error creating session: {e}")

        conn.close()
        return redirect(url_for("create_session"))

    cur.execute("""
        SELECT ses.session_id, ses.session_date, ses.start_time, s.subject_name
        FROM attendance_sessions ses
        JOIN class_subjects cs ON cs.class_subject_id = ses.class_subject_id
        JOIN subjects s ON s.subject_id = cs.subject_id
        ORDER BY ses.session_id DESC
        LIMIT 10
    """)
    recent = cur.fetchall()

    conn.close()
    return render_template("create_session.html", class_subjects=class_subjects, recent=recent)


# ----------------------------
# MARK ATTENDANCE
# ----------------------------
@app.route("/mark-attendance", methods=["GET", "POST"])
def mark_attendance():
    conn = get_conn()
    if not conn:
        flash("Database connection failed!")
        return redirect(url_for('home'))
    cur = conn.cursor()

    cur.execute("""
        SELECT ses.session_id,
               s.subject_name,
               ses.session_date,
               ses.start_time
        FROM attendance_sessions ses
        JOIN class_subjects cs ON cs.class_subject_id = ses.class_subject_id
        JOIN subjects s ON s.subject_id = cs.subject_id
        ORDER BY ses.session_id DESC
        LIMIT 30
    """)
    session_rows = cur.fetchall()

    sessions = []
    for row in session_rows:
        label = f"{row['subject_name']} | {row['session_date']}"
        if row["start_time"]:
            label += f" {row['start_time']}"
        sessions.append({
            "session_id": row["session_id"],
            "label": label
        })

    if request.method == "POST":
        session_id = int(request.form["session_id"])

        cur.execute("SELECT student_id, roll_no, full_name FROM students ORDER BY roll_no")
        students = cur.fetchall()

        try:
            cur.execute("DELETE FROM attendance WHERE session_id = %s", (session_id,))

            present_ids = set(request.form.getlist("present"))

            for st in students:
                status = "P" if str(st["student_id"]) in present_ids else "A"
                cur.execute(
                    "INSERT INTO attendance (session_id, student_id, status) VALUES (%s, %s, %s)",
                    (session_id, st["student_id"], status)
                )

            conn.commit()
            flash("Attendance saved!")
        except Exception as e:
            conn.rollback()
            flash(f"Error saving attendance: {e}")

        conn.close()
        return redirect(url_for("mark_attendance") + f"?session_id={session_id}")

    selected_session_id = request.args.get("session_id", type=int)
    roster = []
    session_label = None
    already_marked = set()

    if selected_session_id:
        for s in sessions:
            if s["session_id"] == selected_session_id:
                session_label = s["label"]
                break

        cur.execute("SELECT student_id, roll_no, full_name FROM students ORDER BY roll_no")
        roster = cur.fetchall()

        cur.execute("SELECT student_id FROM attendance WHERE session_id = %s AND status = 'P'", (selected_session_id,))
        already_marked = {row["student_id"] for row in cur.fetchall()}

    conn.close()
    return render_template(
        "mark_attendance.html",
        sessions=sessions,
        selected_session_id=selected_session_id,
        session_label=session_label,
        roster=roster,
        already_marked=already_marked
    )


# ----------------------------
# GRADES
# ----------------------------
@app.route("/grades", methods=["GET", "POST"])
def grades():
    conn = get_conn()
    if not conn:
        flash("Database connection failed!")
        return redirect(url_for('home'))
    cur = conn.cursor()

    # Load subjects for the dropdown
    cur.execute("SELECT subject_id, subject_code, subject_name FROM subjects ORDER BY subject_code")
    subjects = cur.fetchall()

    if request.method == "POST":
        subject_id = int(request.form["subject_id"])

        cur.execute("SELECT student_id FROM students ORDER BY roll_no")
        students = cur.fetchall()

        try:
            # First, delete old grades for this subject
            cur.execute("DELETE FROM grades WHERE subject_id = %s", (subject_id,))

            for st in students:
                st_id = st["student_id"]
                mark_val = request.form.get(f"marks_{st_id}")
                grade_val = request.form.get(f"grade_{st_id}")
                
                # Check if input has something. If both are empty, we leave it deleted.
                if (mark_val and mark_val.strip() != "") or (grade_val and grade_val.strip() != ""):
                    # Convert to float if it exists
                    m = float(mark_val) if mark_val and mark_val.strip() else None
                    g = grade_val.strip() if grade_val and grade_val.strip() else None
                    
                    cur.execute(
                        "INSERT INTO grades (student_id, subject_id, marks, grade) VALUES (%s, %s, %s, %s)",
                        (st_id, subject_id, m, g)
                    )

            conn.commit()
            flash("Grades saved successfully!")
        except Exception as e:
            conn.rollback()
            flash(f"Error saving grades: {e}")

        conn.close()
        return redirect(url_for('grades') + f"?subject_id={subject_id}")

    # Handling GET
    selected_subject_id = request.args.get("subject_id", type=int)
    roster = []
    subject_label = None

    if selected_subject_id:
        # Get subject name for label
        chosen_subject = next((s for s in subjects if s["subject_id"] == selected_subject_id), None)
        if chosen_subject:
            subject_label = f"Entering Grades for: {chosen_subject['subject_code']} - {chosen_subject['subject_name']}"
        
        # Get students with existing grades populated
        cur.execute("""
            SELECT s.student_id, s.roll_no, s.full_name, g.marks, g.grade
            FROM students s
            LEFT JOIN grades g ON s.student_id = g.student_id AND g.subject_id = %s
            ORDER BY s.roll_no
        """, (selected_subject_id,))
        roster = cur.fetchall()

    conn.close()
    return render_template(
        "grades.html",
        subjects=subjects,
        selected_subject_id=selected_subject_id,
        roster=roster,
        subject_label=subject_label
    )


# ----------------------------
# DEFAULTERS REPORT
# ----------------------------
@app.route("/defaulters", methods=["GET"])
def defaulters():
    subject_id = request.args.get("subject_id", type=int)
    conn = get_conn()
    if not conn:
        flash("Database connection failed!")
        return redirect(url_for('home'))
    cur = conn.cursor()

    cur.execute("SELECT subject_id, subject_code, subject_name FROM subjects ORDER BY subject_code")
    subjects = cur.fetchall()

    results = []
    chosen_subject = None

    if subject_id:
        chosen_subject = next((s for s in subjects if s["subject_id"] == subject_id), None)

        cur.execute("""
            SELECT st.roll_no,
                   st.full_name,
                   ROUND(
                       100.0 * SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*),
                       2
                   ) AS attendance_percent
            FROM attendance a
            JOIN attendance_sessions ses ON ses.session_id = a.session_id
            JOIN class_subjects cs ON cs.class_subject_id = ses.class_subject_id
            JOIN students st ON st.student_id = a.student_id
            WHERE cs.subject_id = %s
            GROUP BY st.student_id, st.roll_no, st.full_name
            HAVING attendance_percent < 75
            ORDER BY attendance_percent ASC
        """, (subject_id,))
        results = cur.fetchall()

    conn.close()

    return render_template(
        "report_defaulters.html",
        subjects=subjects,
        results=results,
        chosen_subject=chosen_subject
    )


if __name__ == "__main__":
    app.run(debug=True)