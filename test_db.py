from database import get_connection
conn=get_connection()
cursor=conn.cursor()
cursor.execute("show tables")
print(cursor.fetchall())