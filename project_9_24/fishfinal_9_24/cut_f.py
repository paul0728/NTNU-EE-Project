import glob, os,os.path
import numpy
import random
#一個class一個folder
# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#current_dir = os.path.dirname("")


#判斷是'/'還是'\'
if '/' in current_dir:
	flag=0
elif '\\'in current_dir :
	flag=1 
#flag_1=0
# Percentage of images to be used for the test set
#x %
percentage_test = 20;

# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')  
file_test = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  


files =os.listdir(current_dir)



for f in files:
	# 產生檔案的絕對路徑
	fullpath = os.path.join(current_dir, f)
	# 判斷 fullpath 是檔案還是目錄
	if os.path.isfile(fullpath):
		pass
	elif os.path.isdir(fullpath):
		#判斷附檔名種類
		#if flag_1==0:
		for name in os.listdir(fullpath):
			if name.endswith(".txt"):
				pass
			else:
				ext=os.path.splitext(name)[1]
				#flag_1=1
				break
		
		
		ext_1="*"+ext
		listtitle=[]
		for pathAndFilename in glob.iglob(os.path.join(fullpath, ext_1)):
			print (os.path.basename(pathAndFilename))
			title, ext = os.path.splitext(os.path.basename(pathAndFilename))
			listtitle.append(title)
		random.shuffle(listtitle)

		for title in listtitle:
			if counter == index_test:
				counter = 1
				if flag==0:
					file_test.write(fullpath + '/'+ title + ext + "\n")
				else:
					file_test.write(fullpath + '\\'+ title + ext + "\n")
			else:
				if flag==0:
					file_train.write(fullpath +'/'+ title + ext + "\n")
				else:
					file_train.write(fullpath + '\\'+ title + ext + "\n")
				counter = counter + 1
file_test.close()
file_train.close()