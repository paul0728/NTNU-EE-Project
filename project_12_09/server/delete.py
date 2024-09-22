import sqlite3,shutil,os
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("DELETE FROM projects")
conn.commit()
path="/home/paul/server/static/receive"
shutil.rmtree(path) 
os.mkdir(path)
