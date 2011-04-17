import Crypto.Data
#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline Server
import MySQL

#System
import SocketServer
import time
import thread

def Begin(client_socket):
    Auth_Status = False
    Auth_Message = "NaN"
    
    #Get the version of the client's game client
    data = client_socket.recv(4096)
    data = str(data.strip()) #Strip formatting crap
    data.replace(' ', '')

    #Decrypt data to get Client Version
    ClientVer = Crypto.Data.Decrypt(data)
    
    #Check if the ClientVer is supported
    if ClientVer != "DEV-ALPHA 2.1.1":
        Auth_Status = False
        Auth_Message = str(str("Incorrect Client Version! - ") + str(data))
    else:
        #Get the account username and password from client
        data = client_socket.recv(4096)
        data = str(data.strip()) #Strip formatting crap
        data.replace(' ', '')
        Username = Crypto.Data.Decrypt(data)

        data = client_socket.recv(4096)
        data = str(data.strip()) #Strip formatting crap
        data.replace(' ', '')
        Password = Crypto.Data.Decrypt(data)

        #Check Username and Password against the MySQL database
        if str(Password) == str(MySQL.GetPassword(Username)):
            Auth_Status = True
            Auth_Message = str(Username)

        else:
            Auth_Status = False
            Auth_Message = "Incorrect Username/Password!"
    

    #Return Authentication Status and Authentication Message
    return Auth_Status, Auth_Message