import os
from tkinter import *
from takephoto import takeW

if __name__ =="__main__":
    dire = os.path.dirname(os.path.realpath(__file__))
    window = Tk()
    frame = takeW(window, "fishinfo.csv","fishinfo_total.csv")
    frame.pack(fill =BOTH, expand = True)

    window.mainloop()