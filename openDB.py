import sqlite3

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе данных:", tables)

conn.close()
