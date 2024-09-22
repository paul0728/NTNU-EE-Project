from flask import Flask, render_template, url_for, request, redirect
import sqlite3,os,os.path


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
path=os.path.dirname(os.path.realpath(__file__))
con = sqlite3.connect(path+"/test.db",check_same_thread = False) 

@app.route('/', methods=['POST', 'GET'])
def home():
  
  value = None

  if request.method == 'POST':
    value = []
    # on 'search' button click.
    fish_type = request.form.get('fish_type')
    fish_len = request.form.get('fish_len')

    
    if fish_len=="0-9":
      lower=0
      upper=9
    elif fish_len=="10-19":
      lower=10
      upper=19
    elif fish_len=="20-29":
      lower=20
      upper=29
    elif fish_len=="30-39":
      lower=30
      upper=39
    elif fish_len=="40-49":
      lower=40
      upper=49
    elif fish_len=="50-59":
      lower=50
      upper=59
    elif fish_len=="≥60":
      lower=60
      upper=10000
    elif fish_len=="":
      lower = 0
      upper = 10000
    else:
      lower = 10000
      upper = 0


    cursor = con.cursor()
    if fish_type=="":
      cursor.execute('''
      SELECT
        id,
        file,
        name,
        length
      FROM
        projects
      WHERE
        length >= '{}' AND length <= '{}';'''.format(lower, upper))

    else:
      cursor.execute('''
      SELECT
        id,
        file,
        name,
        length
      FROM
        projects
      WHERE
        name = '{}' AND (length >= '{}' AND length <= '{}');'''.format(fish_type, lower, upper))
    filters = cursor.fetchall()
    filters = [list(f) for f in filters]

    for ix, row in enumerate(filters):
      row[0] = ix+1
      row[1] = "<img src=" + "/static/receive/" + os.path.basename(row[1]) + ">"
      value.append(row)

  return render_template("display1.html", value=value)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8088,debug=True)



