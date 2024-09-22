from torchvision.transforms import ToTensor
#from modeltorch  import cnn
from modeltorch2 import cnn2


import sys
import csv
import torch
import cv2
import os
import pandas as pd 
import numpy
from PIL import Image

# ==========================legend============================#
# &&              -> to be changed
# $$              -> not finished
# <!>             -> urgent
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

# predict name (cnn)
def get_name(img_path,model,class_list):
    # get image
    image = cv2.imread(img_path)
    #image =cut(image)
    
    # resize 
    image = resize( image,400,400 )
    cv2.imshow("image",image)
    cv2.waitKey(0)

    # change brg to rgb
    #image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #numpy array to pil image
    item = Image.fromarray(image)
    #item.show()
    item = ToTensor()(image)
    item = item.unsqueeze(0)
    
    #print(item )

    pred =  model(item)
    print(pred)
    print(pred.max() )
    if pred.max() > 0.80:
        correct = pred.argmax(dim=1)
        return class_list[correct.item()]
    else:
        return "None"




def cut(image):
    height, width,_ = image.shape
    gray =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray,(7,7),0)
    #edged = auto_canny(blur)
    edged = cv2.Canny (blur , 0 , 100 )
    edged = cv2.dilate(edged , None , iterations = 1 )
    edged = cv2.erode(edged , None , iterations = 1 )

    # find countours 
    (cnts , _ ) = cv2.findContours( edged, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE ) 

    # sort by area 
    clone = image.copy()

    #s = sorted(cnts,key=cv2.contourArea)
    #clone = cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)
    #cv2.imshow("image",clone)
    #cv2.waitKey(0)

    if (len(cnts)>0):
        cont=max(cnts,key= getrectsize)
        box = cv2.minAreaRect(cont)
        width = int(box[1][0])
        height = int(box[1][1])
        #print(box)
        box1 = numpy.int0(cv2.boxPoints (box))
        #print(box1)
        #cv2.drawContours(clone, [box1], -1, (0, 255, 0), 2)
        
        #cv2.imshow("image",clone)
        
        src_pts = box1.astype("float32")
        dst_pts = numpy.array([[0, height-1],[0, 0],[width-1, 0],[width-1, height-1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(image, M, (width, height))
        #cv2.imshow("image",warped)
        #cv2.waitKey(0)
        return warped
    else:
        return image

def auto_canny(image, sigma = 0.9):
    v = numpy.median(image)
    lower = int(max(0 , (1. - sigma)* v) )
    upper = int( min( 255 ,( 1 + sigma )*v))
    edged =  cv2.Canny (image,lower,upper)
    return edged

def getrectsize(contour):
    box = cv2.minAreaRect(contour)
    area = box[1][1]* box[1][0]
    return area

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

# change size to  400**2  and file blanks
def resize( image, newimagex = 400 , newimagey= 400 ): 
    # get image size 
    y,x,_ = image.shape

    # create new image

    # get images ratios
    imageratio = x/(y*1.)
    newimageratio = newimagex/(newimagey*1.)

    # if image is too big
    if x > newimagex or y > newimagey :
        # create new image 
        newimage = numpy.zeros((newimagey,newimagex,3), numpy.uint8)
        if newimageratio > imageratio:
            #print("vertical")
            newx=int(newimagey*imageratio)
            image= cv2.resize(image,(newx,newimagey))
            bs = int((newimagex-newx)/2 ) #blackspce
            bs2 = newx+bs
            newimage[  :,bs :bs2] = image

        else :
            #print("horizontal")
            newy = int(newimagex/imageratio)
            image = cv2.resize(image,(newimagex,newy))
            bs = int((newimagey-newy)/2) #blackspce
            bs2 = newy+bs
            newimage[bs:bs2,:] = image
        im = newimage 

  
    # if image is to small 
    else:
        if newimageratio > imageratio:
            #print("vertical")
            newimage = numpy.zeros((y,int(y*newimageratio),3), numpy.uint8)
            bs = int(round((y*newimageratio-x)/2)) #blackspce
            bs2 = x+bs
            newimage[:, bs  : bs2] =  image

        else :
            #print("horizontal")
            newimage = numpy.zeros((int(x/newimageratio),x,3), numpy.uint8)
            bs = int(round((int(x/newimageratio)-y)/2)) #blackspce
            bs2 = y+bs
            newimage[bs : bs2 ,:]=image 

        im = newimage
        im  = cv2.resize(im,(newimagex,newimagey))
        
    return im

# ++++++++++++++ main program ++++++++++++++++++ 

def Main():
    csvfile = sys.argv[1]
    path = os.path.dirname(csvfile)

    # get files 
    files =  getfiles(csvfile)
    
    
    # load model 
    weigthfile = 'best_weight_cnn2_2.pt'
    model = torch.load( f"{path}/{weigthfile}" ,map_location =  'cpu')
    # model = model.to("cpu") 
    model.eval()
    # get classes
    classes = get_class(f"{path}/classes.txt")

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