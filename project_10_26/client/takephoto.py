from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os
import cv2
import time
import PIL.Image, PIL.ImageTk
# import picamera

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

class takeW(Frame):
    def __init__(self, parent,filename, totalname ):
        Frame.__init__(self, parent)
        self.parent = parent
        # not resizable

        # __________________ data __________________
        # file dir
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        # selectec dir
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.filename = filename 
        self.totalname = totalname

        # __________________ image __________________
        self.vid = cameraview(0)

        # __________________ frames __________________

        self.frame = Frame(self,bg="red")
        self.frame.pack(side = LEFT,fill = Y,expand = 0,anchor="w")

        self.imageframe = Frame(self,bg="blue")
        self.imageframe.pack(side = RIGHT,fill= BOTH, expand = 1 ,anchor="e")

        # __________________ gatgets __________________

        # --------------- button, labels and entry -------------

        # text file name 
        self.textname =Label(self.frame,width=25, height=2,text="imput file name",relief=RIDGE, bg="gray")
        self.textname.pack(side = TOP,fill = X)

        # get file name     
        self.nametext = Entry(self.frame , text="file name" ) 
        self.nametext.pack(side = TOP,fill = X)

        # select dir text
        self.dirtextname =Label(self.frame ,width=25, height=2,text="select directory",relief=RIDGE, bg="gray")
        self.dirtextname.pack(side = TOP,fill = X)
        
        # open dirctory explorer button
        self.directbutton = Button( self.frame ,width=25, height=2,text = "select directory" , command = self.select )
        self.directbutton.pack(side = TOP,fill = X)

        # take photo button
        self.savebutton  = Button( self.frame ,width=25, height=2 ,text = "save image", command =  self.save )
        self.savebutton.pack(side = BOTTOM,fill = X)
        
        # get file name     
        self.taketext = Label(self.frame , text="TAKE!" ) 
        self.taketext.pack(side = BOTTOM,fill = X)

        # ---------------- image --------------------
        
        # show image from camera     
        self.canvas = Canvas(self.imageframe,bg = "gray")
        self.canvas.pack(side = RIGHT, fill = BOTH ,expand = 1)

        self.update()

    # +++++++++++++++ button ++++++++++++++++++

    def save(self):
        filename = self.nametext.get()
        if filename != "" :
            
            # get file path 
            path = self.directory + "/" + filename + ".png"
            print(path)

            #take photo from picamara
            image = self.take()

            if os.path.isfile(path):
                # if exist ask if realy want to overwrite 
                MsgBox = messagebox.askquestion ('warning','file already exist \ndo you want to overwrite?',icon = 'warning')
                if MsgBox == 'yes':
                    cv2.imwrite(path,image)
                    # save info to csv
                    self.savetocsv(self.current_dir,path)
                else:
                    print("no")
            
            else:
                # else messege box "save "file name""
                cv2.imwrite(path,image)
                # save info to csv
                self.savetocsv(self.current_dir,path)
            
            self.parent.changetogrid()

        else:
            messagebox.showinfo("warning", "no name")
        
    
    # select save image directory
    def select(self):
        directores = askdirectory()
        print(directores)
        self.directory = directores
        self.directbutton.pack_forget()
        self.directbutton = Button( self.frame ,width=25, height=2,text = os.path.basename(directores) , command = self.select )
        self.directbutton.pack(side = TOP,fill = X)

    # +++++++++++++++ functionals +++++++++++++++++

    # save path to csv and add index
    def savetocsv(self,dirpath,imagepath):
        j = self.getindex()
        csvpath = dirpath+"/"+self.filename
        col_list = ['file','id','name','length']

        if os.path.isfile(csvpath):
            olddf = pd.read_csv(csvpath, usecols=col_list)
        else:
            olddf = pd.DataFrame(columns=col_list)

        adddf = pd.DataFrame( columns = col_list ) # create new dataframe  
        adddf['file'] = [imagepath]
        newdf = pd.concat( [olddf,adddf] , axis = 0 , ignore_index = True ) # concatenate old and new dataframe
        newdf["id"] = [(i+j) for i in range(newdf.index[-1]+1)] 
        newdf.to_csv( csvpath , index=False ) # save to csv

    # save image from pi camera 
    def take(self):
        _ ,frame = self.vid.get_frame()
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        return image
    
    # get last index from total csv
    def getindex(self):
        if os.path.isfile(self.totalname ):
            col_list =  ['id']
            df = pd.read_csv(self.totalname, usecols=col_list)
            if df.empty:
                return 1
            else:
                return(df.iloc[-1].values[0]+1)
        return 1

    # get image from camera
    def update(self):
        ret,frame = self.vid.get_frame()

        if ret :
            self.photo = PIL.ImageTk.PhotoImage( master =self.canvas,image = PIL.Image.fromarray(frame) )
            self.canvas.create_image(0,0 , image = self.photo, anchor = NW)

        self.after( 15 ,self.update)


    def __del__(self):
        del self.vid



class cameraview():
    def __init__(self,video_source = 0  ):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError()
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        if self.vid.isOpened():
            ret,frame =self.vid.read()
            if ret:
                return (ret,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else : 
                return (ret,None)
        else:
            return (ret,None)

    def __del__(self ):
        if self.vid.isOpened():

            self.vid.release()
            
#os.chdir(os.path.dirname(os.path.realpath(__file__)))
#dire = os.path.dirname(os.path.realpath(__file__))
#window = takeW(None,dire,"None","None") 
#window.mainloop()