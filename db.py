import os
import sqlite3


def get_conn():
    db_path = os.path.join(os.path.dirname(__file__), "college_attendance.db")
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con