import pyodbc as py

def connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-4HC9J5AE\\SQLEXPRESS;"  # double backslash for Windows
        "DATABASE=ETl_pipeline;"
        "Trusted_Connection=yes;"
    )
    return py.connect(conn_str)