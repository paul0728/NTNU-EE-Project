import sys
import cv2
import math
import numpy as np
import csv
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

# calculate length #$$
def get_length(imagepath):

    # get gray numpy image
    image = cv2.imread( imagepath )
    image = cv2.resize( image ,( 1024 , 720 ))
    gray  = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    O = gray * 1.
    O[O > 255] = 255
    O = np.round( O )
    O = O.astype( np.uint8 )


    # image processing 
    blur = cv2.GaussianBlur( O , ( 5 , 5 ) , 0)
    _ , th2 = cv2.threshold( blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU )
    """th2 = 255 - th2"""


    # find countours 
    (cnts , _ ) = cv2.findContours( th2.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE ) 

    
    # length proportions
    distance = 117 #(cm)
    x = 2 * distance * math.tan(26.75 * math.pi / 180)
    y = 2 * distance * math.tan(20.75 * math.pi / 180) # useless 

    #objects = []
    boxes = []

    """
    max_area = 700000
    min_area = 10000
    """

    # sort by area 
    s = sorted(cnts,key=cv2.contourArea)

    # filter by area
    '''filteredcnt = [i for i in s if cv2.contourArea(i) > min_area and cv2.contourArea(i) < max_area ] '''

    # min area of the biggest area
    box = cv2.minAreaRect(s[-1]) 

    # ////////////////////// test //////////////////////
    # if background color is incorrect 
    if box[1][1] >= 1024*0.99  and box[1][0]>=  720*0.99 and box[2]==-90:

        # invert color 
        th2 = 255 - th2

        # get new contours 
        (cnts , _ ) = cv2.findContours( th2.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE ) 

        # sort by area
        s = sorted(cnts,key=cv2.contourArea)

        # get new box of the bigget contour 
        box = cv2.minAreaRect(s[-1]) 
    # //////////////////////////////////////////////////

    """# ////////////////////// test //////////////////////
    clone = image.copy()
    for i in s:
        box2= cv2.minAreaRect(i) 
        box1 = np.int0(cv2.boxPoints (box2))
        cv2.drawContours(clone, [box1], -1, (0, 255, 0), 2)
    # //////////////////////////////////////////////////"""
    
    """# ////////////////////// test //////////////////////
    cv2.imshow("image",clone)
    cv2.waitKey(0)
    # //////////////////////////////////////////////////"""
    
    # biggest side
    if box[1][0] > box[1][1] :
        boxes.append( box[1][0] )
        length = (x / 1024) * box[1][0] 
    else:
        boxes.append( box[1][1] )
        length = (x / 1024) * box[1][1]


    return length

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

# ++++++++++++++++ main program ++++++++++++++++

def Main():
    csvfile = sys.argv[1]
    # get files 
    files =  getfiles(csvfile)

    # set saver
    lengths = []

    # calculate 
    for fil in files:
        length = get_length(fil)
        lengths.append(length)
    
    # save data
    save(lengths,csvfile )
    
if __name__ =="__main__":
    Main()