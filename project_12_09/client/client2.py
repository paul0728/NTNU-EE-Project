import sys
import csv
import socket
import tqdm
import os
import pandas as pd 
import progressbar
import numpy
import cv2
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

# ++++++++++++++++++ functions +++++++++++++++++++++++

# send data to socket
def send(filepath):
    # prepere data
    path = os.path.dirname(filepath)
    csvpath =  os.path.basename(filepath)
    '''filename = "demo.json"
    sendedfile = path+"\\"+filename # real path

    col_list = ['file','name','length']

    #get the dataframe
    df = pd.read_csv(filepath, usecols=col_list)

    # save image in the dataframe
    df = image2dataframe(df)

    # get only the basename of the image
    df['file'] = [os.path.basename(i) for i in df['file'].to_list()]  

    df.to_json(sendedfile)
    #df.to_json( path+"\\"+"demo.json")

    filesize = os.path.getsize(sendedfile)

    # start socket
    SEPARATOR = "<SEPARATOR>"'''
    BUFFER_SIZE = 4096

    host = "140.122.79.53"
    port = 8086

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")

    try:
        s.connect((host, port))
        print("[+] Connected.")
        connected = True
    except:
        connected = False


    if connected :
        # prepere data
        filename = "demo.json"
        sendedfile = path+"\\"+filename # real path

        col_list = ['id','file','name','length']

        #get the dataframe
        df = pd.read_csv(filepath, usecols=col_list)

        # save image in the dataframe
        df = image2dataframe(df)

        # get only the basename of the image
        df['file'] = [os.path.basename(i) for i in df['file'].to_list()]  

        df.to_json(sendedfile)
        #df.to_json( path+"\\"+"demo.json")

        filesize = os.path.getsize(sendedfile)

        # start socket
        SEPARATOR = "<SEPARATOR>"
        # send data
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        with open(sendedfile, "rb" ) as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)

        os.remove(filepath)
        os.remove(sendedfile)# delete file 
        s.close()

    else:
        print("not connected")
        unsentpath = f"{path}/fishinfo_unsent.csv"
        if os.path.isfile(unsentpath):
            olddf = pd.read_csv(unsentpath)
        else:
            olddf = pd.DataFrame()

        if csvpath != "fishinfo_unsent.csv":
            newdf = pd.read_csv(filepath)
            os.remove(filepath)
        else:
            newdf = pd.DataFrame()
        
        olddf = olddf.append(newdf, ignore_index=True)
        olddf.to_csv(unsentpath,index=False)


# convert image to string and then sve it to the dataframe 
def image2dataframe(df):
    images = []
    sizes = []
    for i in df['file'].to_list():
        # read image 
        image = cv2.imread(i)

        # resize to max size
        resized = resize(image)

        # get the new image size
        hight,width,channels =  resized.shape
 
        # flatten the image 
        flattened = resized.flatten()

        # convert to string 
        stringimage = numpy.array2string(flattened, precision=2, separator=',', suppress_small=True)

        # strip all unecesary chars form the string
        striped=stringimage.replace("\n","")
        striped=striped.replace(" ","")
        striped=striped.replace("]","")
        striped=striped.replace("[","")

        # append the string to the dataframe 
        images.append(striped)
        
        # convert the image size to string 
        sizestring= "{}x{}x{}".format(width, hight,channels)

        # save the image size in dataframe
        sizes.append(sizestring)

    df["image"] = images
    df['size'] = sizes 

    return df

# resize if is too big to reduce data 
def resize(image, maxwidth = 100, maxhight = 100):
    #get image size 
    y,x,_=  image.shape

    # image ratio 
    ratio = x/y

    maxratio = maxwidth / maxhight

    # is vertival 
    if ratio > maxratio:
        # if is too big
        if x > maxwidth:
            image = cv2.resize(image,(maxwidth,int(maxwidth/ratio)))

    # is horizontal 
    else:
        # if is too big
        if y > maxhight:
            image = cv2.resize(image,(int(ratio*maxhight),maxhight))

    return image 
# ++++++++++++++++++  main program ++++++++++++++

def Main():
    filepath = sys.argv[1]
    numpy.set_printoptions(threshold=numpy.inf)
    #path=os.path.dirname(os.path.realpath(__file__))
    send(filepath)

if __name__ =="__main__":
    Main()

