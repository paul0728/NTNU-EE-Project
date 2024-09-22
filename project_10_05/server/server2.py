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

        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)

        filesize =  int(filesize)

        filepath = os.path.dirname(__file__)+filename
        print(filepath)

        with open(filepath ,'wb') as f:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break 
            f.write(bytes_read)
        #把資料寫入database
        con = sqlite3.connect(r"D:\project\project10_05\server\test.db",check_same_thread = False) # change to 'sqlite:///your_filename.db'        
        df = pd.read_csv(filepath)
        df.to_sql('projects', con, if_exists='append', index=False)

        #save2database(filepath) # save data to total


        os.remove(filepath) # delete file 

            


'''def save2database(filename):  # move recived data to database
    col_list =  ['id','name','length']

    # open recieved file as dataframe 
    received = pd.read_csv(filename, usecols=col_list)

    # open old file as dataframe
    basename = "data.csv"
    DatabasePath = os.path.dirname(__file__) + "/" + basename
    
    if os.path.isfile(DatabasePath):
        database = pd.read_csv(DatabasePath, usecols=col_list)
    else:
        database = pd.DataFrame(columns=col_list)

    # write to csv 
    new = pd.concat([ database ,received] , axis = 0 , ignore_index=True) # concatenate old and new dataframe
    new.to_csv( DatabasePath , index=False )
    '''
def main():
    path=os.path.dirname(os.path.realpath(__file__))
    receive( path )

if __name__ == "__main__":
    main()


