import sys
import csv
import socket
import tqdm
import os
import pandas as pd 
import progressbar
import numpy as np
import cv2


if __name__ =="__main__":
    #numpy.set_printoptions(threshold=numpy.inf)
    df = pd.read_json("D:\\desktop\\project_9_24\\client"+"\\"+"demo.json")
    arraystr = df['images'].to_list()[0]
    #listed = arraystr.split(",")
    array = np.fromstring(arraystr, dtype=int,sep = ",")
    size = df['size'].to_list()[0]
    print(size.split("x"))
    x,y,c = size.split("x")
    image=np.reshape(array,(int(y),int(x),int(c)))
    cv2.imwrite('D:/desktop/project_9_24/client/color_img.jpg', image)
    image = cv2.imread('D:/desktop/project_9_24/client/color_img.jpg')
    cv2.imshow( "image",image)
    cv2.waitKey()
