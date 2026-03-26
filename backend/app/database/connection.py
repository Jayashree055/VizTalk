# import sqlite3
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "marketing.db")

# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


import sqlite3
import os

def get_db_connection():
    # Always go to project root
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

    DB_PATH = os.path.join(ROOT_DIR, "marketing.db")

    print("DB PATH:", DB_PATH)
    print("DB EXISTS:", os.path.exists(DB_PATH))

    return sqlite3.connect(DB_PATH)