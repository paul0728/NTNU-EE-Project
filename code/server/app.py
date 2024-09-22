from flask import Flask, render_template, url_for, request, redirect
import sqlite3,os,os.path


app = Flask(__name__)#__name__代表目前執行的模組。如果當成主程式來執行,會是"main"
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
path=os.path.dirname(os.path.realpath(__file__))
con = sqlite3.connect(path+"/test.db",check_same_thread = False) 
#con = sqlite3.connect(r"/app/test.db",check_same_thread = False) 

@app.route('/', methods=['GET','POST'])#函式的裝飾(Decorator):已函式為基礎,提供附加的功能
def home():
	print('start')
	flag='0'
	if request.method == 'POST':
		if 'send' in request.form:
			if request.form['send']=="搜尋":
				flag = '1'
	print(flag)
	data1=[]
	image_path=[]
	image_html=[]
	cursor = con.cursor()
	cursor. execute("SELECT id,name,length FROM projects")
	#cursor. execute("select * from projects1")
	data = cursor.fetchall() #data from database."../picture.jpg"
	cursor.execute("SELECT file FROM projects")
	file1=cursor.fetchall()
	for i in file1:
		image_path.append(os.path.basename(i[0]))
	#image_path1=os.listdir(path+"\\static")
	for i in image_path:
		image_html.append("<img src="+"/static/"+i+">")	
	for i,j in zip(data,image_html):
		i = i[:1] + (j,) + i[1:3]
		data1.append(list(i))
	#print(data1)
	return render_template("display.html", value=data1, flag=flag)





if __name__ == "__main__":#如果以主程式執行
    app.run(host='0.0.0.0',port=8088,debug=False)#立刻啟動伺服器



