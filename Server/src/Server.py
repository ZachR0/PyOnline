#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline Server
import MySQL
import Accounts.Character
import Authentication.Authenticate
import Crypto.Data

#System
import SocketServer
import time
import thread

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
SERVER = None
HOST = '' #Listen on all interfaces
PORT = 1337
SERVER_HOST = (HOST, PORT)
CONNECTED_CLIENTS = {} #Holds list of all connected clients CONNECTED_CLIENT[name] format

#Holds an array of all server messages that need to be displayed
#Sent upon user connection
SERVER_MESSAGES = []


#     _____________________
# ___/ Class Declarations  \____________________________________________________
#Client Class
class Client:
    Socket = None
    Name = None
    SpriteSheet = None
    SpriteMap = None
    CurrentX = None
    CurrentY = None
    CurrentFrame = None

    def __init__(self, ClientSocket, PlayerName, PlayerSpriteSheet, PlayerSpriteMap,\
        PlayerCurrentX, PlayerCurrentY, PlayerCurrentFrame):
            #Set variables
            self.Socket = ClientSocket
            self.Name = PlayerName
            self.SpriteSheet = PlayerSpriteSheet
            self.SpriteMap = PlayerSpriteMap
            self.CurrentX = PlayerCurrentX
            self.CurrentY = PlayerCurrentY
            self.CurrentFrame = PlayerCurrentFrame


#Socket Handler Class
class RequestHandler(SocketServer.BaseRequestHandler):
    #Current Client Info
    Client_Username = ""
    Client_Name = ""
    Client_SpriteSheet = None
    Client_SpriteMap = None
    Client_CurrentX = None
    Client_CurrentY = None
    Client_CurrentFrame = None
    Client_Char_ID = None

    #Called first upon new connection
    def setup(self):
        global SERVER
        global HOST
        global PORT
        global SERVER_HOST
        global CONNECTED_CLIENTS
        global SERVER_MESSAGES

        #Inform console of new connection
        print "[!] A New Connection From \'", self.client_address, "\'!"
        print "[", self.client_address, "] Starting Client Authentication..."

        #Authenticate Client
        Auth_Status, Auth_Message = Authentication.Authenticate.Begin(self.request)

        #Check Authentication Status
        if Auth_Status == True:
            #Set Client_Name
            self.Client_Username = Auth_Message

            #Client should be identified
            print "[", self.client_address, "] Identified as \"",\
                str(Auth_Message), "\""
        else:
            #Client was not able to authenticate it's connection
            print "[", self.client_address, "] Authentication FAILED! \"",\
                str(Auth_Message), "\""


            #Close connection
            self.request.close()

            #Stop connection process of remote client
            return

        #Make sure the client is authenticated before continueing
        if Auth_Status == True:
            #Start to load character data, and get the client's char info
            print "[", self.Client_Username, "] Starting Inital Character Setup..."
            CharID, CharName, CharX, CharY,\
            CharSpriteSheet, CharSpriteMap\
            = Accounts.Character.Initial_Setup(Auth_Status, self.request, self.Client_Username)

            #Make sure we were able to get the client's char info
            if CharID != "NaN" and CharName != "NaN" and CharX != "NaN" and\
               CharY != "NaN" and CharSpriteSheet != "NaN" and CharSpriteMap != "NaN":
                #Set Client's Character ID
                self.Client_Char_ID = CharID

                #Set Client's Character Name
                self.Client_Name = CharName

                #Set Client's X,Y
                self.Client_CurrentX = CharX
                self.Client_CurrentY = CharY

                #Set Client's Sprite Infomation
                self.Client_SpriteSheet = CharSpriteSheet
                self.Client_SpriteMap = CharSpriteMap
                
            else:
                print "[", self.Client_Username, "] FAILED during Character Setup!"
                print "\t - Disconnecting..."
                self.request.close()

                #Stop connection process of remote client
                return


        #Make sure the client is authenticated before continueing
        if Auth_Status == True:
            #Send server messages to client
            print "[", self.Client_Username, "] Sending Server Messages..."

            self.request.send(Crypto.Data.Encrypt(str(len(SERVER_MESSAGES)))) #Send length of server messages

            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)

            for i in range(0, len(SERVER_MESSAGES)):
                self.request.send(Crypto.Data.Encrypt(str(SERVER_MESSAGES[i])))
                time.sleep(0.02) #Delay sending (prevent flood / allow processing time)

            #At this point, the client should have the player loaded locally
            #print "[", self.Client_Username, "] Requesting Initial Animation Frame..."

            ##Get character's inital animation frame
            #data = self.request.recv(4096)
            #data = str(data.strip())
            #self.Client_CurrentFrame = Crypto.Data.Decrypt(data)
            #time.sleep(0.02)
            self.Client_CurrentFrame = 0 #Default Frame is Zero
            
            #Send all of the previous client data to our new guest ^.^ (Make introductions xD)
            print "[", self.Client_Username, "] Is Beginning Introductions..."
            self.request.send(Crypto.Data.Encrypt(str(len(CONNECTED_CLIENTS)))) #Send length of current clients
            for client in CONNECTED_CLIENTS:
                #print "[DEBUG]: Sending client \"", str(client), "\" to \"", str(self.Client_Name), "\"!"
                try:
                    #Prepare data
                    Connection_Data = str("rnd_new:" + str(CONNECTED_CLIENTS[client].Name)+\
                    ":" + str(CONNECTED_CLIENTS[client].SpriteSheet) + ":" + str(CONNECTED_CLIENTS[client].SpriteMap)+\
                    ":" + str(CONNECTED_CLIENTS[client].CurrentX) + ":" + str(CONNECTED_CLIENTS[client].CurrentY) + ":"+\
                    str(self.Client_CurrentFrame) + ":")

                    #Encrypt Data
                    Connection_Data = Crypto.Data.Encrypt(Connection_Data)

                    #Send
                    self.request.send(str(Connection_Data))

                    time.sleep(0.2) #Delay sending (prevent flood / allow processing time)
                except:
                    pass

            #Update Current Client List
            CONNECTED_CLIENTS[self.Client_Name] = Client(self.request, self.Client_Name,\
                                self.Client_SpriteSheet, self.Client_SpriteMap, self.Client_CurrentX,\
                                self.Client_CurrentY, self.Client_CurrentFrame)
            print "[", self.Client_Username, "] Was Added To The Client List!"

            #Let all of the other players' clients know that we have a new guest ^.^
            print "[!] Informing All Previous Clients Of \'", self.Client_Name, "\'s\' Connection..."
            for client in CONNECTED_CLIENTS:
                try:
                    if client != self.Client_Name:
                        #Prepare data
                        Connection_Data = str("new_conn:" + str(self.Client_Name)+\
                        ":" + str(self.Client_SpriteSheet) + ":" + str(self.Client_SpriteMap)+\
                        ":" + str(self.Client_CurrentX) + ":" + str(self.Client_CurrentY) + ":"+\
                        str(self.Client_CurrentFrame) + ":")

                        #Encrypt Data
                        Connection_Data = Crypto.Data.Encrypt(Connection_Data)

                        #Send
                        CONNECTED_CLIENTS[client].Socket.send(str(Connection_Data))

                        time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
                except:
                    pass

            #Client should be connected and good to go! :D
            print "[", self.Client_Username, "] Entered the PyOnline World! ^.^"
            
        else:
            #Close connection
            self.request.close()

            #Stop connection process of remote client
            return

    #Connection handle
    def handle(self):
        global SERVER
        global HOST
        global PORT
        global SERVER_HOST
        global CONNECTED_CLIENTS
        global SERVER_MESSAGES

        #Start Ping/Pong Thread
        thread.start_new_thread(Ping_Pong_Thread, ())

        #Connection Loop
        while True:
            #Catch any issues while recieving data from client
            try:
                #Get client data
                data = self.request.recv(4096)
                data = str(data.strip())

                #Hard Core debug?
                #print "[", self.Client_Name, "]: ", data

                #Decrypt data
                data = Crypto.Data.Decrypt(data)

                #Client Ping/Pong Response
                if data == "PONG!":
                    #Ignore(for now)?
                    pass

                #Client Disconnection Request
                elif data == "dis_conn":
                    self.finish()
                    break

                #Client Movement Notification
                elif data[0:7] == "mov_plr":
                    tmpData = str(data)
                    Data = []

                    #Get parameters from command
                    while len(tmpData) > 1:
                        Sep_Loc = tmpData.find(":")

                        TmpData = tmpData[0:Sep_Loc]
                        Data.append(TmpData[0:Sep_Loc])

                        tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                    #Data should be formatted as follows
                    #[0] - mov_plr ; [1] x ; [2] y ; [3] frame

                    #Update client list
                    CONNECTED_CLIENTS[str(self.Client_Name)].CurrentX = Data[1]
                    CONNECTED_CLIENTS[str(self.Client_Name)].CurrentY = Data[2]
                    CONNECTED_CLIENTS[str(self.Client_Name)].CurrentFrame = Data[3]
                    self.Client_CurrentX = Data[1]
                    self.Client_CurrentY = Data[2]
                    self.Client_CurrentFrame = Data[3]

                    #Send update out
                    for client in CONNECTED_CLIENTS:
                        try:
                            #Send to everyone but ourself
                            if client != self.Client_Name:
                                #Prepare Data
                                Connection_Data = str("update_plr:" + str(self.Client_Name)+\
                                ":" + str(self.Client_CurrentX) + ":" + str(self.Client_CurrentY) + ":"+\
                                str(self.Client_CurrentFrame) + ":")

                                #Encrypt Data
                                Connection_Data = Crypto.Data.Encrypt(Connection_Data)

                                #Send
                                CONNECTED_CLIENTS[str(client)].Socket.send(str(Connection_Data))

                                time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
                        except:
                            pass

                #Client Chat Message
                elif data[0:7] == "cht_msg":
                    tmpData = str(data)
                    Data = []

                    #Get parameters from command
                    while len(tmpData) > 1:
                        Sep_Loc = tmpData.find(":")

                        TmpData = tmpData[0:Sep_Loc]
                        Data.append(TmpData[0:Sep_Loc])

                        tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                    #Data should be formatted as follows
                    #[0] - cht_msg ; [1] message

                    #Send message out
                    for client in CONNECTED_CLIENTS:
                        try:
                            #Send to everyone but ourself
                            if client != self.Client_Name:
                                #Prepare Data
                                Connection_Data = str("cht_msg:" + str(self.Client_Name)+\
                                ":" + str(Data[1]) +  ":")

                                #Encrypt Data
                                Connection_Data = Crypto.Data.Encrypt(Connection_Data)

                                #Send
                                CONNECTED_CLIENTS[str(client)].Socket.send(str(Connection_Data))

                                time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
                        except:
                            pass

            except:
                #Do nothing (for now?)
                pass
    
    #Called upon connection ending
    def finish(self):
        global SERVER
        global HOST
        global PORT
        global SERVER_HOST
        global CONNECTED_CLIENTS
        global SERVER_MESSAGES

        try:
            #Update Client's character LastXPos and LastYPos in MySQL database
            MySQL.SetCharacterXPOS(self.Client_Char_ID, CONNECTED_CLIENTS[str(self.Client_Name)].CurrentX)
            MySQL.SetCharacterYPOS(self.Client_Char_ID, CONNECTED_CLIENTS[str(self.Client_Name)].CurrentY)

            #Disconnect client
            CONNECTED_CLIENTS[str(self.Client_Name)].Socket.close()
            del CONNECTED_CLIENTS[str(self.Client_Name)]
            print "[", str(self.Client_Name), "] Disconnected!"

            #Inform other clients of disconnection
            for client in CONNECTED_CLIENTS:
                try:
                    print "[!] Telling the other clients to say Good Bye to \'", self.Client_Name, "\'..."

                    #Prepare Data
                    Command = str("rm_plr:" + str(self.Client_Name) + ":")

                    #Encrypt Data
                    Command = Crypto.Data.Encrypt(Command)

                    #Send
                    CONNECTED_CLIENTS[str(client)].Socket.send(Command)

                    time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
                except:
                    pass
        except:
            pass

        #Close Client Socket
        self.request.close()

#Started in a seperate thread to keep connection alive for all clients
def Ping_Pong_Thread():
    global SERVER
    global HOST
    global PORT
    global SERVER_HOST
    global CONNECTED_CLIENTS

    #Wait for a moment before starting PingPong thread
    time.sleep(1)

    while True:
        #Connection Alive?
        for client in CONNECTED_CLIENTS:
            try:
                CONNECTED_CLIENTS[client].Socket.send("PING?")
            except:
                try:
                    CONNECTED_CLIENTS[client].Socket.close()
                    del CONNECTED_CLIENTS[str(self.Client_Name)]
                except:
                    pass
                break

        #Delay PingPong
        time.sleep(60)


#Starts the Server
def Start():
    global SERVER
    global HOST
    global PORT
    global SERVER_HOST
    global CONNECTED_CLIENTS
    global SERVER_MESSAGES

    #Output a welcome message
    print "- PyOnline Game Server"

    #Get server messages from the SQL database
    print "- Getting Server Messages..."
    SERVER_MESSAGES = MySQL.GetServerMessages()

    #Setup and start the server
    print "- Starting Server..."
    SERVER = SocketServer.ThreadingTCPServer(SERVER_HOST, RequestHandler)
    SERVER.serve_forever()

#Start Server
Start()