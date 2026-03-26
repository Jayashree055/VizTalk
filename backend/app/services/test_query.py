from app.database.connection import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

query = "SELECT Campaign_Type, SUM(Revenue) as total FROM campaigns GROUP BY Campaign_Type"

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

conn.close()