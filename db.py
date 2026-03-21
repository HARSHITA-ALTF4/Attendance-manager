# import mysql.connector

# def get_conn():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="nandini@2006",
#         database="college_attendance"
#     )


import sqlite3

def get_conn():
    con = sqlite3.connect("college_attendance.db")
    con.row_factory = sqlite3.Row
    return con

# import os
# import mysql.connector

# def get_conn():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME"),
#         port=int(os.getenv("DB_PORT", "3306"))
#     )

# import sqlite3

# def get_conn():
#     con = sqlite3.connect("college_attendance.db")
#     con.row_factory = sqlite3.Row
#     return con