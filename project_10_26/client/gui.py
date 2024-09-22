from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, askopenfiles
from tkinter.simpledialog import askstring
from PIL import ImageTk, Image
import sys, os, csv
import cv2
import numpy

import pandas as pd

from takephoto import takeW

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

# ++++++++++++++++ gui +++++++++++++++++++++


class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = Canvas(
            self, borderwidth=0, background="#ffffff"
        )  # place canvas on self
        self.viewPort = Frame(
            self.canvas, background="#ffffff"
        )  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )  # place a scrollbar on self
        self.canvas.configure(
            yscrollcommand=self.vsb.set
        )  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(
            side="left", fill="both", expand=True
        )  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window(
            (4, 4),
            window=self.viewPort,
            anchor="nw",  # add view port frame to canvas
            tags="self.viewPort",
        )

        self.viewPort.bind(
            "<Configure>", self.onFrameConfigure
        )  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind(
            "<Configure>", self.onCanvasConfigure
        )  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(
            None
        )  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


class TotalFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # ________________ data path ________________
        self.pth = os.path.dirname(os.path.realpath(__file__))
        self.totalfilename = "fishinfo_total.csv"
        self.totalcsv = self.pth + "/" + self.totalfilename

        # ________________ pages ________________
        self.CurrentPage = 1
        self.pagesize = 15
        self.total_pages = self.getpages()

        # ________________ gui ________________

        # -------------- data frame ----------------------
        self.data = []
        self.datagrid = ScrollFrame(self)
        self.datagrid.pack(fill=BOTH, expand=1)

        # -------------- draw grid -----------------------
        self.display()

        # -------------- buttons frame -------------------
        self.pagebuttonsframe = Frame(self)
        self.pagebuttonsframe.pack(side=BOTTOM)

        self.button1 = Button(self.pagebuttonsframe, text="<<", command=self.button1action)
        self.button1.grid(column=0, row=0, sticky=W + E + N + S)

        self.button2 = Button(self.pagebuttonsframe, text="<", command=self.button2action)
        self.button2.grid(column=2, row=0, sticky=W + E + N + S)

        self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
        self.label1.grid(column=3, row=0, sticky=W + E + N + S)

        self.label2 = Label(self.pagebuttonsframe, text="/")
        self.label2.grid(column=4, row=0, sticky=W + E + N + S)

        self.label3 = Label(self.pagebuttonsframe, text=str(self.total_pages))
        self.label3.grid(column=5, row=0, sticky=W + E + N + S)

        self.button3 = Button(self.pagebuttonsframe, text=">", command=self.button3action)
        self.button3.grid(column=6, row=0, sticky=W + E + N + S)

        self.button4 = Button(self.pagebuttonsframe, text=">>", command=self.button4action)
        self.button4.grid(column=7, row=0, sticky=W + E + N + S)

    # ============== buttons =============
    def button1action(self): # go to  first page 
        if self.CurrentPage > 1:
            self.CurrentPage = 1
            # update current page label  
            self.label1.destroy()
            self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
            self.label1.grid(column=3, row=0, sticky=W + E + N + S)
            # update grid frame
            self.display()

    def button2action(self): # go to previus page
        if self.CurrentPage > 1:
            self.CurrentPage -= 1
            # update current page label  
            self.label1.destroy()
            self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
            self.label1.grid(column=3, row=0, sticky=W + E + N + S)
            # update grid frame
            self.display()

    def button3action(self): # go to next page
        if self.CurrentPage < self.total_pages:
            self.CurrentPage += 1
            # update current page label    
            self.label1.destroy()
            self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
            self.label1.grid(column=3, row=0, sticky=W + E + N + S)
            # update grid frame
            self.display()

    def button4action(self): # go to last page
        if self.CurrentPage < self.total_pages:
            self.CurrentPage = self.total_pages
            # update current page label  
            self.label1.destroy()
            self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
            self.label1.grid(column=3, row=0, sticky=W + E + N + S)
            # update grid frame
            self.display()

    def delete(self, number, pages): # delete row from total csv
        MsgBox = messagebox.askquestion ('warning','do you want to delete?',icon = 'warning')
        if MsgBox == 'yes':
            total = (pages - 1) * self.pagesize + number

            # get data from csv
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.totalcsv, usecols=col_list)

            # delete row 
            df.drop(labels=None,axis= 0, index= total-1,inplace= True)

            # save to csv
            df.to_csv(self.totalcsv,index= False)

            # redisplay
            self.total_pages = self.getpages()
            if self.total_pages <= self.CurrentPage:  
                self.CurrentPage = self.total_pages

            self.label1.destroy()
            self.label1 = Label(self.pagebuttonsframe, text=str(self.CurrentPage))
            self.label1.grid(column=3, row=0, sticky=W + E + N + S)
            self.label3.destroy()
            self.label3 = Label(self.pagebuttonsframe, text=str(self.total_pages))
            self.label3.grid(column=5, row=0, sticky=W + E + N + S)

            self.display()

    def show(self, path): # show image in new window
        imageW(None, path)

    # ============= functions =============

    def getpages(self): # get number of pages 
        if os.path.isfile(self.totalcsv):
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.totalcsv, usecols=col_list)
            if df.empty:
                return 1
            else:
                total = df.index[-1]+1
                npages = int((total ) / self.pagesize)
                if (total ) % self.pagesize != 0:
                    npages += 1
                return npages
        return 1

    def get_data(self): # get data for current page from total csv
        if os.path.isfile(self.totalcsv):
            initialpos = (self.CurrentPage - 1) * self.pagesize
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.totalcsv, usecols=col_list)
            dflist=df[initialpos : initialpos + self.pagesize].values.tolist()
            self.data = dflist
        else:
            self.data = []

    def getname(self, path):  # get file name form path
        name = path.split("/")[-1]
        return name

    # =========== gui ===========

    def display(self): # display grid of data 
        # data
        self.data = []
        self.get_data()
        # frame ----------------------
        self.datagrid.destroy()
        self.datagrid = ScrollFrame(self)
        self.datagrid.pack(fill=BOTH, expand=1)
        # draw grid -----------------------
        index = ["file", "id", "name", "length(cm)", "delete"]
        k = 0
        for i in index:
            Label(
                self.datagrid.viewPort,
                width=25,
                height=2,
                text=i,
                relief=RIDGE,
                bg="gray",
            ).grid(row=0, column=k)
            k += 1
        r = 1
        for row in self.data:
            c = 0
            for col in row:
                if c == 0:
                    Button(
                        self.datagrid.viewPort,
                        width=25,
                        height=2,
                        text=self.getname(col),
                        relief=RIDGE,
                        command=Callback(self.show, col),
                    ).grid(row=r, column=c)
                else:
                    Label(
                        self.datagrid.viewPort,
                        width=25,
                        height=2,
                        text=col,
                        relief=RIDGE,
                    ).grid(row=r, column=c)
                c += 1
            Button(
                self.datagrid.viewPort,
                width=25,
                height=2,
                text="delete",
                relief=RIDGE,
                command=Callback2(self.delete, r, self.CurrentPage),
            ).grid(row=r, column=c)
            r += 1


class SessionFrame(Frame):

    def __init__(self, parent,distance):
        Frame.__init__(self, parent)
        self.parent = parent
        self.distance = distance 

        # ________________ csv file path ________________
        self.pth = os.path.dirname(os.path.realpath(__file__))
        self.filename = "fishinfo.csv"
        self.totalfilename = "fishinfo_total.csv"
        self.csvpth = self.pth + "/" + self.filename
        self.totalcsv = self.pth + "/" + self.totalfilename

        # ________________ data ________________
        self.data = []

        # ________________ gui ________________
        self.frame =  Frame(self, background="#ffffff")
        self.frame.pack(fill = BOTH,expand =1)
        self.showgrid()
        """
        # -------------- top button -----------------------
        self.frame1 = Frame(self.frame , background="#ffffff")
        self.frame1.pack(side=TOP)

        self.button1 = Button(self.frame1, text="calculate name and length", command=self.calculate)
        self.button1.grid(column=1, row=0)

        self.photobutton = Button(self.frame1, text="take photo", command=self.take)
        self.photobutton.grid(column=0, row=0)

        # -------------- display grid -----------------------
        self.datagrid = ScrollFrame(self.frame)
        self.datagrid.pack(fill=BOTH, expand=1)
        self.display()

        # -------------- bottom  button -----------------------
        self.frame2 = Frame(self.frame, background="#ffffff")
        self.frame2.pack(side=BOTTOM)
        self.button2 = Button(self.frame2, text="save and send", command=self.saveandsend)
        self.button2.pack(side=BOTTOM)
        
        # -------------- camera -----------------------
        """
    # =========== buttons ============
    def saveandsend(self): # execute function save and send after button is pushed, show warning if data is not filled 
        filled = self.filled()
        if filled == True:
            self.save()
            self.send()
            self.display()
        else:
            messagebox.showinfo("warning", "data no filled")

    def take(self):# take photo with raspberry gpio
        self.frame.destroy()
        self.frame = takeW(self,self.filename ,self.totalfilename)
        self.frame.pack(fill = BOTH,expand =1)

    def delete(self, number): # delete row from session csv
        MsgBox = messagebox.askquestion ('warning','do you want to delete?',icon = 'warning')
        if MsgBox == 'yes':
            # get index
            j = self.getindex()
            new_id=[]

            # get data from csv
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.csvpth, usecols=col_list)

            # delete row 
            df.drop(labels = None,axis = 0, index = number - 1, inplace = True)
            df = df.reset_index(drop=True) # reset index

            # new id 
            if df.empty:
                new_id=[]
            else:
                new_id = [(j+i) for i in range(df.index[-1]+1)]

            # replace old id for new id 
            df["id"]=new_id

            # save to csv
            df.to_csv(self.csvpth,index=False)

            # redisplay
            self.display()

    def show(self, path): # show image in new window 
        imageW(None, path)

    def calculate(self): # calculate name and length after button is push, if no data show warning 
        if os.path.isfile(self.csvpth):
            try:
                os.system(f"python {self.pth}/minarea_3.py {self.csvpth} {self.distance}")# + self.csvpth)
                os.system(f"python {self.pth}/detect.py {self.csvpth}")#+ self.csvpth)
            except:
                messagebox.showinfo("warning", "no file selected")
        else:
            messagebox.showinfo("warning", "no file selected")
        self.display()

    # =========== functions ============

    def get_data(self): # get data from session csv
        if os.path.isfile(self.csvpth) == False:
            self.data = []
        else:
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.csvpth, usecols=col_list)
            dflist=df.values.tolist()
            self.data = dflist
   
    def getname(self, path): # get file name form path 
        name = path.split("/")[-1]
        return name

    def getindex(self): # get the last id from total csv
        if os.path.isfile(self.totalcsv):
            col_list =  ['id']
            df = pd.read_csv(self.totalcsv, usecols=col_list)
            if df.empty:
                return 1
            return(df.iloc[-1].values[0]+1)
        return 1

    def save(self): # save data do total csv
        col_list=['file','id','name','length']
        if not  os.path.isfile(self.totalcsv):
            dftotal = pd.DataFrame(columns=col_list)
        else:
            dftotal =  pd.read_csv(self.totalcsv, usecols = col_list)

        dftemp = pd.read_csv(self.csvpth, usecols = col_list)
        dftotal = pd.concat( [dftotal,dftemp] ,axis = 0,ignore_index = True)
        dftotal.to_csv(self.totalcsv,index= False)

    def send(self): # send data to server
        os.system("python client2.py " + self.csvpth)

    def filled(self): # detect if data are filled
        if os.path.isfile(self.csvpth):
            with open(self.csvpth, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    i = row
                if i[2] == "":
                    return False
                else:
                    return True
        else:
            return False

    def name(self, string): # convert string to "" if is nan, else return  string or number
        if self.isNaN(string):
            return ""
        return string

    def isNaN(self,string): # detect if string is NaN
        return string != string
        
    # =========== gui ============
    def showgrid(self):
         # -------------- top button -----------------------
        self.frame1 = Frame(self.frame , background="#ffffff")
        self.frame1.pack(side=TOP)

        self.button1 = Button(self.frame1, text="calculate name and length", command=self.calculate)
        self.button1.grid(column=1, row=0)

        self.photobutton = Button(self.frame1, text="take photo", command=self.take)
        self.photobutton.grid(column=0, row=0)

        # -------------- display grid -----------------------
        self.datagrid = ScrollFrame(self.frame)
        self.datagrid.pack(fill=BOTH, expand=1)
        self.display()

        # -------------- bottom  button -----------------------
        self.frame2 = Frame(self.frame, background="#ffffff")
        self.frame2.pack(side=BOTTOM)
        self.button2 = Button(self.frame2, text="save and send", command=self.saveandsend)
        self.button2.pack(side=BOTTOM)

    def display(self):
        # data
        self.data = []
        self.get_data()
        # frame ----------------------
        self.datagrid.destroy()
        self.datagrid = ScrollFrame(self.frame)
        self.datagrid.pack(fill=BOTH, expand=1)
        # draw grid -----------------------
        index = ["file", "id", "name", "length(cm)", "delete"]
        k = 0
        for i in index:
            Label(
                self.datagrid.viewPort,
                width=25,
                height=2,
                text=i,
                relief=RIDGE,
                bg="gray",
            ).grid(row=0, column=k)
            k += 1
        r = 1
        for row in self.data:
            c = 0
            for col in row:
                if c == 0:
                    Button(
                        self.datagrid.viewPort,
                        width=25,
                        height=2,
                        text=self.getname(col),
                        relief=RIDGE,
                        command=Callback(self.show, col),
                    ).grid(row=r, column=c)
                else:
                    Label(
                        self.datagrid.viewPort,
                        width=25,
                        height=2,
                        text=self.name(col),
                        relief=RIDGE,
                    ).grid(row=r, column=c)
                c += 1
            Button(
                self.datagrid.viewPort,
                width=25,
                height=2,
                text="delete",
                relief=RIDGE,
                command=Callback(self.delete, r),
            ).grid(row=r, column=c)
            r += 1

    def changetogrid(self):
        self.frame.destroy()
        self.frame = Frame(self, background="#ffffff")
        self.frame.pack(fill = BOTH,expand =1)
        self.showgrid()


class UnsentFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # ________________ csv file path ________________
        self.pth = os.path.dirname(os.path.realpath(__file__))
        self.unsentcsv = "fishinfo_unsent.csv"
        self.unsentpath = f"{self.pth}/{self.unsentcsv}"

        self.data = []

        # ________________ gui ________________
        # -------------- grid -----------------------
        self.frame1 = Frame(self)
        self.display()

        # -------------- send button  -----------------------
        self.frame2 = Frame(self, background="#ffffff")
        self.frame2.pack(side=BOTTOM)
        self.button2 = Button(self.frame2, text="send", command=self.send)
        self.button2.pack(side=BOTTOM)

    # =========== buttons ===========
    def send(self):
        if os.path.isfile(self.unsentpath):
            os.system("python client2.py " + self.unsentpath)
        self.display()

    def delete(self, number): # delete row from session csv
        MsgBox = messagebox.askquestion ('warning','do you want to delete?',icon = 'warning')
        if MsgBox == 'yes':

            # get data from csv
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.unsentpath, usecols=col_list)

            # delete row 
            df.drop(labels = None,axis = 0, index = number - 1, inplace = True)
            df = df.reset_index(drop=True) # reset index

            # save to csv
            df.to_csv(self.unsentpath,index=False)

            # redisplay
            self.display()

    def show(self, path): # show image in new window
        imageW(None, path)

    # =========== functionals ===========
    def get_data(self): # get data from session csv
        if os.path.isfile(self.unsentpath) == False:
            self.data = []
        else:
            col_list =  ['file','id','name','length']
            df = pd.read_csv(self.unsentpath, usecols=col_list)
            dflist=df.values.tolist()
            self.data = dflist

    def name(self, string): # convert string to "" if is nan, else return  string or number
        if self.isNaN(string):
            return ""
        return string

    def isNaN(self,string): # detect if string is NaN
        return string != string

    def getname(self, path): # get file name form path 
        name = path.split("/")[-1]
        return name

    # ============== gui ==============
    def display(self):
        # data
        self.data = []
        self.get_data()
        # frame ----------------------
        self.frame1.destroy()
        self.frame1 = ScrollFrame(self)
        self.frame1.pack(fill=BOTH, expand=1)
        # draw grid -----------------------
        index = ["file", "id", "name", "length(cm)", "delete"]
        k = 0
        for i in index:
            Label(
                self.frame1.viewPort,
                width=25,
                height=2,
                text=i,
                relief=RIDGE,
                bg="gray",
            ).grid(row=0, column=k)
            k += 1
        r = 1
        for row in self.data:
            c = 0
            for col in row:
                if c == 0:
                    Button(
                        self.frame1.viewPort,
                        width=25,
                        height=2,
                        text=self.getname(col),
                        relief=RIDGE,
                        command=Callback(self.show, col),
                    ).grid(row=r, column=c)
                else:
                    Label(
                        self.frame1.viewPort,
                        width=25,
                        height=2,
                        text=self.name(col),
                        relief=RIDGE,
                    ).grid(row=r, column=c)
                c += 1
            Button(
                self.frame1.viewPort,
                width=25,
                height=2,
                text="delete",
                relief=RIDGE,
                command=Callback(self.delete, r),
            ).grid(row=r, column=c)
            r += 1


class MainW(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title("fish classifier")
        self.geometry("940x600")

        # ________________ data ________________

        self.distance = 117

        # ________________ csv file path ________________
        self.pth = os.path.dirname(os.path.realpath(__file__))
        self.filename = "fishinfo.csv"
        self.totalfilename = "fishinfo_total.csv"
        self.csvpth = self.pth + "/" + self.filename
        self.totalcsv = self.pth + "/" + self.totalfilename

        # ________________ gui ________________
        # -------------- menu frame --------------
        self.menu = Menu(self)
        self.config(menu=self.menu)

        # -------------- file --------------
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)

        # new
        self.filemenu.add_command(label="New session", command=self.new)

        # add
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Add to session", command=self.add)

        # exit
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command = self.destroy)

        # -------------- view --------------
        self.viewmenu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "view", menu = self.viewmenu)

        self.viewmenu.add_command(label = "Total", command = self.viewtotal)
        self.viewmenu.add_command(label = "Session", command = self.viewsession)
        self.viewmenu.add_command(label = "Unsent", command  =  self.viewunsent  )

        # -------------- set --------------

        self.setmenu = Menu(self.menu ,tearoff = 0)
        self.menu.add_cascade(label = "set", menu = self.setmenu)

        self.setmenu.add_command(label = "set distace", command = self.setdistace)

        # -------------- help --------------
        self.helpmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About", command=self.about)

        # ___________ frame _____________

        self.viewframe = SessionFrame(self,self.distance)
        self.viewframe.pack(fill=BOTH, expand=1)

    # =========== buttons ===========
    def about(self): # open a message box
        messagebox.showinfo("info", "this is for help")

    def viewtotal(self): # show TotalFrame frame
        self.viewframe.destroy()
        del self.viewframe
        self.viewframe = TotalFrame(self)
        self.viewframe.pack(fill=BOTH, expand=1)

    def viewsession(self): # show SessionFrame frame
        self.viewframe.destroy()
        del self.viewframe
        self.viewframe = SessionFrame(self,self.distance)
        self.viewframe.pack(fill=BOTH, expand=1)

    def viewunsent(self): # show UnsentFrame frame 
        self.viewframe.destroy()
        del self.viewframe
        self.viewframe = UnsentFrame(self)
        self.viewframe.pack(fill=BOTH, expand=1)

    def add(self): # add files to csv 
        newfiles = askopenfilenames(
            parent=self,
            title="選擇檔案",
            filetypes=(("all files", "*.*"),("jpg files", "*.jpg"),("png files", "*.png")))
        if not len(newfiles) == False: # oly if newfile is not empty
            j = self.getindex()
            col_list = ['file','id','name','length']

            if os.path.isfile(self.csvpth): # if file exist, get dataframe
                olddf = pd.read_csv(self.csvpth, usecols=col_list)
            else :  #if file dont exist, create dataframe
                olddf = pd.DataFrame(columns=col_list)

            adddf = pd.DataFrame(columns=col_list) # create new dataframe  
            adddf['file'] = newfiles  
            newdf = pd.concat( [olddf,adddf] ,axis = 0,ignore_index=True) # concatenate old and new dataframe
            newdf["id"] = [(i+j) for i in range(newdf.index[-1]+1)]  # get new id 
            newdf.to_csv(self.csvpth,index=False) # save to csv
        self.viewsession()

    def new(self): # create new csv file and add data to csv
        newfiles = askopenfilenames(
            parent=self,
            title="選擇檔案",
            filetypes=(("all files", "*.*"),("jpg files", "*.jpg"),("png files", "*.png")))
        if not len(newfiles) == False: # oly if newfile is not empty
            j = self.getindex()

            if os.path.isfile(self.csvpth): # delete old file if exist 
                os.remove(self.csvpth)

            col_list = ['file','id','name','length']
            df = pd.DataFrame(columns=col_list) # create new data frame  
            df['file'] = newfiles 
            df["id"] = [(i+j) for i in range(len(newfiles))] 
            df.to_csv(self.csvpth,index=False)

        self.viewsession()

    def setdistace(self): # set distance between the camera and the objec (default = 117 cm )
        string = askstring('distance', f'set the distance between the table and the camera in cm (default = 117 cm)\nexample: 117\ncurrent value = {self.distance}\nif distance equal 0, distance will be set to default')
        if string == "" or string == "0":
            self.distance = 117
        else:
            try:
                self.distance = int(string)
            except:
                messagebox.showinfo("warning", "input must only contain numbers")
        self.viewsession()
                
    # =========== functions ============

    def getindex(self): # get last id from total csv
        if os.path.isfile(self.totalcsv):
            col_list =  ['id']
            df = pd.read_csv(self.totalcsv, usecols=col_list)
            if df.empty:
                return 1
            else:
                return(df.iloc[-1].values[0]+1)
        return 1

    # ============== gui ==============


class imageW(Tk):
    def __init__(self, parent, filepath):
        Tk.__init__(self, parent)

        self.parent = parent
        self.title(filepath)
        img = Image.open(filepath)
        maxwidth , maxheight =1024 ,720
        img = self.resize(maxwidth , maxheight , img)
        self.tkimage = ImageTk.PhotoImage(img, master=self)
        Label(self, image=self.tkimage).place(x=0, y=0, relwidth=1, relheight=1)
        x,y=img.size
        self.geometry(f"{x}x{y}")

    # resize if is too big to fit in the screem
    def resize(self,maxwidth,maxheight,image):
        width , height = image.size
        ratio = width/height
        if ratio > 1:
            if width > maxwidth :
                image = image.resize((maxwidth,int(maxwidth/ratio )))
        else :
            if height > maxheight :
                image = image.resize((int(ratio*maxheight),maxheight ))
        return image



# ++++++++++++++++ funtionals ++++++++++++++++


class Callback:
    def __init__(self, func, arg1):
        self.func = func
        self.arg1 = arg1

    def __call__(self):
        self.func(self.arg1)


class Callback2:
    def __init__(self, func, arg1, arg2):
        self.func = func
        self.arg1 = arg1
        self.arg2 = arg2

    def __call__(self):
        self.func(self.arg1, self.arg2)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app = MainW(None)
    app.mainloop()