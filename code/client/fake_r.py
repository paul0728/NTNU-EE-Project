import csv
import string
import random
import sys
n=int(sys.argv[1])
k=random.randint(1, 5)
l=[]
def id_generator(size=k, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


for i in range(n):
    l.append(id_generator())

fn = 'fishinfo.csv'
with open(fn, 'a', newline = '') as csvFile:    # 開啟csv檔案
    csvWriter = csv.writer(csvFile)             # 建立Writer物件   
    for i in l:
        csvWriter.writerow(['', '', i, '', ''])
