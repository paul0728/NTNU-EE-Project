from flask import Flask, render_template, url_for, request, redirect
import sqlite3


app = Flask(__name__)#__name__代表目前執行的模組。如果當成主程式來執行,會是"main"
con = sqlite3.connect(r"D:\projectv2\server\test.db",check_same_thread = False) 
#con = sqlite3.connect(r"/app/test.db",check_same_thread = False) 

@app.route('/', methods=['POST', 'GET'])#函式的裝飾(Decorator):已函式為基礎,提供附加的功能
def home():
	cursor = con.cursor()
	cursor. execute("select * from projects")
	#cursor. execute("select * from projects1")
	data = cursor. fetchall() #data from database.
	return render_template("display1.html", value=data)

if __name__ == "__main__":#如果以主程式執行
    app.run(debug=False)#立刻啟動伺服器



