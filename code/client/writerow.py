import csv

fn = 'fishinfo.csv'
with open(fn, 'a', newline = '') as csvFile:    # 開啟csv檔案
    csvWriter = csv.writer(csvFile)             # 建立Writer物件   
    csvWriter.writerow(['Name', 'Age', 'City'])
    csvWriter.writerow([ , , ])
    csvWriter.writerow(['James', '40', 'Chicago'])


