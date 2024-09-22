import sqlite3
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("SELECT * FROM projects")
rows = c.fetchall()
for row in rows:
	print(row)
conn.commit()