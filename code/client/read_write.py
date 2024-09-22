import csv
import sys

#本次有int(sys.argv[1])張圖
n=int(sys.argv[1])
#之前有count張圖
count=int(sys.argv.pop())
#n=3
rows=[]
T=[]
T1=[]
fn = 'fishinfo.csv'
ft = 'fishinfo_total.csv'
#資料對齊
with open(fn) as csvFile:               # 開啟csv檔案
    csvReader = csv.reader(csvFile)     # 讀檔案建立Reader物件csvReader
    for row in csvReader:               # 用迴圈列出csvReader物件內容
        rows.append(row)
        print("Row %s = " % csvReader.line_num, row)

    
with open(fn,'w',newline='') as csvFile:
    csvWriter=csv.writer(csvFile)
    for i in range(n):
        T.append([rows[i][0],rows[i][1],rows[i+n][2],rows[i][3],''])
        T1.append([rows[i][0],str(int(rows[i][1])+count),rows[i+n][2],rows[i][3],''])
    csvWriter.writerow(['file','id','name','length','delete'])
    for i in T:
        csvWriter.writerow(i)
    

with open(ft,'a',newline='') as csvFile: # 開啟csv檔案
    csvWriter=csv.writer(csvFile)     # 讀檔案建立Reader物件csvReader
    if count==0:
        csvWriter.writerow(['file','id','name','length','delete'])
    for i in T1:
        csvWriter.writerow(i)







    






