import sqlite3


def get_conn():
    con = sqlite3.connect("college_attendance.db")
    con.row_factory = sqlite3.Row
    return con