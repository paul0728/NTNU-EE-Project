import os
import sys
import cv2
import pandas as pd
import numpy as np 


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

def order(path):
    """print(path)"""
    infilename = "demo.json" #input filename
    outfilename = "demo.csv" #output filename

    photodir = "{}/photo".format(path) # directory where the photo will be saved

    # see if the dir exist,if not generate a new one
    if not  os.path.isdir(photodir):
        os.mkdir(photodir) 
    

    intotalpath = "{}/{}".format(path ,infilename )
    outtotalpath = "{}/{}".format(path , outfilename)

    """col_list = ["file","name",'length','image','size']"""
    dfin = pd.read_json(intotalpath )
    
    # save useful sata to csv 
    dfout = pd.DataFrame()
    dfout['lenght']= dfin['length']
    dfout['name'] = dfin['name']
    dfout['file'] = ["{}/{}".format(photodir,i) for i in dfin['file'].to_list()]

   
    size = len (dfin['size'].to_list())

    for i in range(size):
        savephoto(dfout['file'].to_list()[i], dfin['image'].to_list()[i], dfin['size'].to_list()[i])

    """ print(dfout)"""
    dfout.to_csv(outtotalpath)


def savephoto(path ,imagestr , sizestr):
    x,y,c = sizestr.split("x")
    array = np.fromstring(imagestr, dtype=int,sep = ",")
    image = np.reshape(array,(int(y),int(x),int(c)))
    cv2.imwrite(path, image)


def main():
    path = sys.argv[1]
    #path = "D:/desktop/project_9_24/server"
    order(path )


if __name__ == "__main__":
    main()
