import sys
import cv2
import math
import numpy as np
import csv
import os
import pandas as pd
import imutils
from imutils import contours

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

#///test///
#   foo           -> test code
#//////////
# ============================================================#

# +++++++++++++++++ functions ++++++++++++++++++

# calculate length #$$
def get_length(imagepath , distance):

    # --------  get the best contour ---------
    image = cv2.imread(imagepath)
    clone = image.copy()
    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur( gray ,(7,7) , 0 )
    edged = cv2.Canny (blur , 00 , 100 )
    #edged = auto_canny(blur)
    edged = cv2.dilate(edged , None , iterations = 1 )
    edged = cv2.erode(edged , None , iterations = 1 )

    cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)
    #print (cnts)
    #s =  sorted(cnts, key = getrectsize ,reverse=False)
    #print(s)
    '''for c in cnts:
        box = cv2.minAreaRect(c)
        box1 = np.int0(cv2.boxPoints (box))
        cv2.drawContours(clone, [box1], -1, (0, 255, 0), 2)
        #print(box[1][0]*box[1][1])'''
    #print(s)
    if (len(cnts)>0):
        cont=max(cnts,key= getrectsize)
        box = cv2.minAreaRect(cont)
        distances = [box[1][0],box[1][1]]
        #print(box[1][0]*box[1][1])
        box1 = np.int0(cv2.boxPoints (box))
        #cv2.drawContours(clone, [box1], -1, (0, 255, 0), 2)
        #print (box)
        distances.sort(reverse = True)
        D = distances[0]
    else:
        D = 0 

    #cv2.imshow("image", clone)
    #cv2.waitKey(0)
    
    # -------- get distance per pixel  ---------
    x = 2 * (distance/image.shape[1]) * math.tan(26.75 * math.pi / 180)
    #print(D)

    d = D*x

    return d

def auto_canny(image, sigma = 0.9):
    v = np.median(image)
    lower = int(max(0 , (1. - sigma)* v) )
    upper = int( min( 255 ,( 1 + sigma )*v))
    edged =  cv2.Canny (image,lower,upper)
    return edged

# save to csv 
def save(lengths,csvfile):
    col_list =   ['file','id','name','length']
    df = pd.read_csv(csvfile, usecols=col_list)
    df['length'] = lengths
    df.to_csv(csvfile,index = False)

# get files form csv 
def getfiles(csvfile):
    col_list =  ['file']
    df = pd.read_csv(csvfile, usecols=col_list)
    dflist = df['file'].values.tolist()
    return dflist

# 
def getminarea(th2 ):
    # get new contours 
    (cnts , _ ) = cv2.findContours( th2.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE ) 

    # sort by area
    s = sorted(cnts,key=cv2.contourArea)

    # get new box of the bigget contour 
    box = cv2.minAreaRect(s[-1]) 

    return box 

# get box size 
def getrectsize(contour):
    box = cv2.minAreaRect(contour)
    area = box[1][1]* box[1][0]
    return area

# ++++++++++++++++ main program ++++++++++++++++

def Main():
    csvfile = sys.argv[1]
    distance = sys.argv[2]
    # get files 
    files =  getfiles(csvfile)

    # set saver
    lengths = []

    # calculate 
    for fil in files:
        length = get_length(fil,int(distance))
        lengths.append(length)
    
    # save data
    save(lengths,csvfile )
    
if __name__ =="__main__":
    Main()