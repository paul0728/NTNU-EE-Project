from flask import Flask, render_template, url_for, request, redirect
from subprocess import call
import pandas as pd 
import numpy as np
import sqlite3

app = Flask(__name__)#__name__代表目前執行的模組。如果當成主程式來執行,會是"main"
con = sqlite3.connect(r"D:\project\project10_05\server\test.db",check_same_thread = False) 
#con = sqlite3.connect(r"/app/test.db",check_same_thread = False) 

@app.route('/', methods=['POST', 'GET'])#函式的裝飾(Decorator):已函式為基礎,提供附加的功能
def home():
	data1=[]
	cursor = con.cursor()
	cursor.execute("select * from projects")
	#cursor. execute("select * from projects1")
	data = cursor. fetchall() #data from database.
	con.commit()
	len1=len(data)
	'''fdata=zip(data1,range(len1))
	if request.method == 'POST':  
		delete=request.form.get("delete")
		cursor.execute("DELETE FROM projects WHERE id=(?)",(int(delete),))
		print(int(delete))
		return render_template("display1.html", value=fdata,rows=len1)'''
	if(data):
		for (row,i) in zip(data,range(len1)):
			row1=list(row)
			row1[0]=i+1
			data1.append(row1)
		df = pd.DataFrame(np.array(data1),columns=['id', 'name', 'length'])
		df.to_sql('projects', con, if_exists='replace',index=False)
		return render_template("display1.html", value=data1,rows=len1)
	else:
		return render_template("display1.html", value=data,rows=len1)
if __name__ == "__main__":#如果以主程式執行
    app.run(debug=False)#立刻啟動伺服器



