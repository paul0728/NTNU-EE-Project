import sys
import csv
import socket
import tqdm
import os
import pandas as pd 
import progressbar

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

# ++++++++++++++++++ functions +++++++++++++++++++++++

#$$
def send(path):
    # prepere data
    filename = 'demo.csv'
    sendedfile = path+"\\"+filename # real path

    col_list = ['id','name','length']
    df = pd.read_csv(path+"\\fishinfo.csv", usecols=col_list,index_col=0)
    df.to_csv(sendedfile)

    filesize = os.path.getsize(sendedfile)

    # start socket
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096

    host = "127.0.0.1"
    port = 8088

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")


    # send data
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    with open(sendedfile, "rb" ) as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    os.remove(sendedfile)# delete file 
    s.close()


# ++++++++++++++++++  main program ++++++++++++++

def Main():
    path = sys.argv[1]
    #path=os.path.dirname(os.path.realpath(__file__))
    send(path)

if __name__ =="__main__":
    Main()

