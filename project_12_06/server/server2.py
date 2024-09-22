import socket
import os
import sqlite3
import pandas as pd
import progressbar
import time

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

def receive(path):
    # socket 
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8088

    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    s = socket.socket()

    s.bind((SERVER_HOST, SERVER_PORT))
    
    # recive data 
    while True:
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        
        client_socket, address = s.accept() 
        print(f"[+] {address} is connected.")
        
        received = client_socket.recv(BUFFER_SIZE).decode()
        print (received)

        # get filename and filesize 
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)

        filesize =  int(filesize)

        # generate the path where the buffer file will be saved  
        filepath = f"{path}/{filename}"
        """print(filepath)"""

        # recive the path form the internet 
        with open(filepath ,'wb') as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break 
                f.write(bytes_read)
        

        os.system(f"python {path}/order.py {path}") #save image from json and generate a csv with only the path 
        os.remove(filepath) # delete file 
        #把資料寫入database
        con = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"\\test.db",check_same_thread = False) # change to 'sqlite:///your_filename.db' 
        header_list = ["id", "name", "length","file"]       
        df = pd.read_csv(f"{path}/demo.csv", usecols=header_list)
        print(df)
        df.to_sql('projects', con, if_exists='append', index=False)


def main():
    path=os.path.dirname(os.path.realpath(__file__))
    receive( path )

if __name__ == "__main__":
    main()


