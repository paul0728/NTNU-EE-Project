import csv
import pandas as pd 
col_list = ['id','name','length']
df = pd.read_csv("fishinfo_total.csv", usecols=col_list)
df.to_csv('fishinfo_total.csv')
print(df)