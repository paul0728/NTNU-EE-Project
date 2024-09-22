from torchvision.transforms import ToTensor
from modeltorch  import cnn

import sys
import csv
import torch
import cv2
import os
import pandas as pd

# ==========================legend============================#
# &&              -> to be changed
# $$              -> not finished
# <!>             -> urgent
# +++ foo +++     -> segment
# === foo ===     -> in class segment
# ___ foo ___     -> functions mayor segment
# --- foo ---     -> functions minor segment
# foo             -> mini description
# """foo"""       -> modified code
# ============================================================#

# +++++++++++++++++ functions ++++++++++++++++++

# predict name (cnn)
def get_name(img_path,model,class_list):
    image = cv2.imread(r'%s'%(img_path))
    image = cv2.resize(image, (400,400))   
    item = ToTensor()(image)
    item = item.unsqueeze(0)
    pred =  model(item)
    correct = pred.argmax(dim=1)
    return class_list[correct.item()]


# get classes list 
def get_class(class_path):
    class_list=[]
    with open(class_path ,'r') as file:
        for i in file :
            i= i.strip("\n")  
            class_list.append(i)
    return class_list

# save names to csv  
def save(names,csvfile):
    col_list =   ['file','id','name','length']
    df = pd.read_csv(csvfile, usecols=col_list)
    df['name'] = names 
    df.to_csv(csvfile,index= False)

# get files from  csv  
def getfiles(csvfile):
    col_list =  ['file']
    df = pd.read_csv(csvfile, usecols=col_list)
    dflist = df['file'].values.tolist()
    return dflist

# ++++++++++++++ main program ++++++++++++++++++ 

def Main():
    csvfile = sys.argv[1]
    path = os.path.dirname(csvfile)

    # get files 
    files =  getfiles(csvfile)
    
    
    # load model 
    weigthfile = 'best_weight.pt'
    model = torch.load( path +"/"+ weigthfile)
    model = model.to("cpu") 
    model.eval()

    # get classes
    classes = get_class( "classes.txt")

    # set saver
    names = []

    # calculate 
    for fil in files:
        class_name = get_name(fil,model,classes)
        names.append(class_name)

    # save data
    save(names,csvfile)
        
if __name__ =="__main__":
    Main()