#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import os.path
import time
import socket

#PyOnline
import Crypto.Data
import Login
import Player.MainPlayer
import Networking.Client
import Camera.Manage
import Video.PyGame
import Video.FPS
import Console.Manage

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
#Our Current Client Version
CLIENT_VER = None

#Game server connection info
SERVER_IP = None
SERVER_PORT = None

#Username and password from login screen (for authentication)
USERNAME = None
PASSWORD = None

#Network socket for us to the server
Client_Socket = None

#Keeps track of rather or not we are connected to the game server
isConnected = False

#Holds all messages that need to be displayed from the server (at login)
SERVER_MESSAGES = []

#Other player information
OTHER_PLAYERS = {}

#     _____________________
# ___/ Class Declaration   \____________________________________________________
#Class is used for all other players connected to the server
class OtherPlayer:
    #Player information
    Name = None #Player name
    SpriteSheet = None #Player spritesheet location
    SpriteMap = None #Player spritemap location

    #Player animation stuff
    Sprites = [] #Player sprites (frame by frame)
    Current_Frame = None #Player's current frame (animation)
    Max_Frame_Up = None
    Min_Frame_Up = None
    Max_Frame_Down = None
    Min_Frame_Down = None
    Max_Frame_Left = None
    Min_Frame_Left = None
    Max_Frame_Right = None
    Min_Frame_Right = None

    #Player movement / Animation
    CurrentX = None #Player x pos
    CurrentY = None #Player y pos
    Moving_Right = None
    Moving_Left = None
    Moving_Up = None
    Moving_Down = None

    def __init__(self, PlayerName, PlayerSpriteSheet, PlayerSpriteMap, PlayerX,\
        PlayerY, PlayerCurrentFrame):
            #Set Player Information
            self.Name = PlayerName
            self.SpriteSheet = PlayerSpriteSheet
            self.SpriteMap = PlayerSpriteMap
            self.CurrentX = int(PlayerX)
            self.CurrentY = int(PlayerY)
            self.Current_Frame = int(PlayerCurrentFrame)

            #Load player sprite information
            #TODO: Check to make sure spritesheet and spritemap files exist
            self.Sprites = []
            self.Max_Frame_Up = 0
            self.Min_Frame_Up = -1
            self.Max_Frame_Down = 0
            self.Min_Frame_Down = -1
            self.Max_Frame_Left = 0
            self.Min_Frame_Left = -1
            self.Max_Frame_Right = 0
            self.Min_Frame_Right = -1
            self.Current_Frame = 0
            self.Moving_Right = False
            self.Moving_Left = False
            self.Moving_Up = False
            self.Moving_Down = False
            self.Can_Move_Up = True
            self.Can_Move_Down = True
            self.Can_Move_Left = True
            self.Can_Move_Right = True

            #Load Sprite
            tmpSprite = pygame.image.load(str(self.SpriteSheet))

            #Open sprite map and load data
            FILE = open(str(self.SpriteMap), 'r')
            DATA = FILE.readlines()
            FILE.close()

            #Go through each line and pull important data
            count = 0 #Count ignores comments
            for line in DATA:
                Data_Line = str(line).strip()

                #Ignore comments
                if Data_Line[0:1] != "#":
                    #Direction
                    Sep_Loc = Data_Line.find(";")
                    Direction = Data_Line[0:Sep_Loc]
                    Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                    #OffSet X
                    Sep_Loc = Data_Line.find(";")
                    OffX = Data_Line[0:Sep_Loc]
                    Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                    #OffSet Y
                    Sep_Loc = Data_Line.find(";")
                    OffY = Data_Line[0:Sep_Loc]
                    Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                    #Width
                    Sep_Loc = Data_Line.find(";")
                    Width = Data_Line[0:Sep_Loc]
                    Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                    #Height
                    Height = Data_Line[0:Sep_Loc]

                    #Update animation frame information
                    if Direction == "DOWN":
                        #Do we need to set Min_Frame?
                        if self.Min_Frame_Down == -1:
                            self.Min_Frame_Down = count
                        #Update Max_Frame
                        self.Max_Frame_Down += 1
                    if Direction == "UP":
                        #Do we need to set Min_Frame?
                        if self.Min_Frame_Up == -1:
                            self.Min_Frame_Up = count
                        #Update Max_Frame
                        self.Max_Frame_Up += 1

                    if Direction == "LEFT":
                        #Do we need to set Min_Frame?
                        if self.Min_Frame_Left == -1:
                            self.Min_Frame_Left = count
                        #Update Max_Frame
                        self.Max_Frame_Left += 1

                    if Direction == "RIGHT":
                        #Do we need to set Min_Frame?
                        if self.Min_Frame_Right == -1:
                            self.Min_Frame_Right = count
                        #Update Max_Frame
                        self.Max_Frame_Right += 1

                    #Append sprite from sprite sheet
                    self.Sprites.append(tmpSprite.subsurface((int(OffX), int(OffY), int(Width), int(Height))))

                    #Increase loop count
                    count += 1

            #Fix Max_Fame Value
            self.Max_Frame_Down += self.Min_Frame_Down
            self.Max_Frame_Up += self.Min_Frame_Up
            self.Max_Frame_Left += self.Min_Frame_Left
            self.Max_Frame_Right += self.Min_Frame_Right

            #Take Max_Frame down one to respect the "starting from zero" system
            self.Max_Frame_Down -= 1
            self.Max_Frame_Up -= 1
            self.Max_Frame_Left -= 1
            self.Max_Frame_Right -= 1

    #Renders player information to screen
    def Render(self):
        #Render to screen
        Video.PyGame.Screen.blit(self.Sprites[self.Current_Frame], (int(self.CurrentX)-Camera.Manage.CamX, int(self.CurrentY)-Camera.Manage.CamY))



#     ________________________
# ___/ Function Declaration   \_________________________________________________
#Reads Server configuration file (data/Server.config)
def Init():
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected
    global USERNAME
    global PASSWORD

    #Make sure the server config exists
    if os.path.exists("data/Server.conf") == True:
        #Open Server config file
        file = open("data/Server.conf")

        #Loop through the file, reading line by line
        lineCount = 0 #Keeps track of what line number we are reading
        while 1:
            #Read line
            line = file.readline()

            #Server IP
            if lineCount == 1:
                SERVER_IP = str(line).strip()

            #Server Port
            elif lineCount == 3:
                SERVER_PORT = int(str(line).strip())

            #Make sure there is line data
            if not line:
                #If not, close the file
                break
            else:
                #If there is, read the next line
                lineCount += 1

        #Close Server.config file
        file.close()

        #Return true, meaning that the file was found, and read
        return True

    else:
        #Return false, meaning that the file was NOT found
        return False

#Connects to the game server and authenticates our client
def Connect():
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected
    global USERNAME
    global PASSWORD
    global SERVER_MESSAGES
    global CLIENT_VER

    #Setup Client Socket
    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Attempt to connect
    try:
        #Connect
        Client_Socket.connect((SERVER_IP, SERVER_PORT))

        #Update connection status
        isConnected = True
    except:
        #Guess the server is offline :/
        Login.StatusLbl.text = "Server is OFFLINE!" #Update login window status

        #Update connection status
        isConnected = False

        #Close socket, to be safe
        Client_Socket.close()

        #Stop Connection process
        return

    #Attempt Authentication
    try:
        #Send Server our Client ver
        try:
            Networking.Client.SendData(CLIENT_VER)
            time.sleep(0.2) #Pause, don't want to flood the server
        except:
            #Update login window status
            Login.StatusLbl.text = "Login FAILED! [0]"

            #Update connection status
            isConnected = False

            #Close socket, just to be safe
            Client_Socket.close()

            #Stop Connection process
            return

        #Send Server our login info
        try:
            Networking.Client.SendData(USERNAME)
            time.sleep(0.02) #Prevent server flood
            Networking.Client.SendData(PASSWORD)
            time.sleep(0.02) #Prevent server flood
        except:
            #Update login window status
            Login.StatusLbl.text = "Login FAILED! [1]"

            #Update connection status
            isConnected = False

            #Close socket, just to be safe
            Client_Socket.close()

            #Stop Connection process
            return

        #Get sprite info back from Server
        try:
            Player.MainPlayer.SpriteSheet_File = str(Networking.Client.ReadData())
            Player.MainPlayer.SpriteMap_File = str(Networking.Client.ReadData())
        except:
            #Update login window status
            Login.StatusLbl.text = "Login FAILED! [2]"

            #Update connection status
            isConnected = False

            #Close socket, just to be safe
            Client_Socket.close()

            #Stop Connection process
            return

        #Get player name from server
        try:
            Player.MainPlayer.Player_Name = str(Networking.Client.ReadData())
        except:
            #Update login window status
            Login.StatusLbl.text = "Login FAILED! [3]"

            #Update connection status
            isConnected = False

            #Close socket, just to be safe
            Client_Socket.close()

            #Stop Connection process
            return

        #Get player x,y from server
        try:
            Player.MainPlayer.XPOS = int(Networking.Client.ReadData())
            Player.MainPlayer.YPOS = int(Networking.Client.ReadData())
        except:
            #Update login window status
            Login.StatusLbl.text = "Login FAILED! [4]"

            #Update connection status
            isConnected = False

            #Close socket, just to be safe
            Client_Socket.close()

            #Stop Connection process
            return

        #Get server messages from the server
        try:
            Num = int(Networking.Client.ReadData())
            for i in range(0, int(Num)):
                SERVER_MESSAGES.append(str(Networking.Client.ReadData()))
        except:
            SERVER_MESSAGES.append(str("[ERROR GETTING SERVER MESSAGES!]"))
            
        #Get previous client data from the server
        try:
            Num = int(Networking.Client.ReadData())
            for i in range(0, int(Num)):
                data = Networking.Client.ReadData()
                
                #Get information for new connection
                tmpData = str(data)
                Data = []
                while len(tmpData) > 1:
                    Sep_Loc = tmpData.find(":")

                    TmpData = tmpData[0:Sep_Loc]
                    Data.append(TmpData[0:Sep_Loc])

                    tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                #Data should be formatted as follows
                #[0] - rnd_new ; [1] name ; [2] sheet ; [3] map [4] x ; [5] y ; [6] frame
                OTHER_PLAYERS[str(Data[1])] = OtherPlayer(str(Data[1]), str(Data[2]),\
                str(Data[3]), int(Data[4]), int(Data[5]), int(Data[6]))
                
                #print "[DEBUG]: Got previous client data for \"", str(Data[1]), "\"!"
        
        except:
            pass

    except Exception, e:
        #Output exception
        print "Login FAILED! - \"", str(e), "\""

        #Update login window status
        Login.StatusLbl.text = "Login FAILED!"

        #Update connection status
        isConnected = False

        #Close socket, just to be safe
        Client_Socket.close()

        #Stop Connection process
        return

#Disconnects us from the game server
def DisConnect():
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected

    #Attempt disconnection process
    try:
        #Send command to disconnect
        Networking.Client.SendData(str("dis_conn"))

        #Close socket
        Client_Socket.close()
    except:
        pass

    #Update connection status
    isConnected = False

#Sends data to the game server
def SendData(data):
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected

    #Make sure we are connected before sending anything
    if isConnected == True:
        #Attempt to send data
        try:
            #TODO: Add encryption here
            Enc_Data = Crypto.Data.Encrypt(data)
            
            #Send data
            Client_Socket.send(str(Enc_Data))
        except:
            pass

#Reads data from the game server
def ReadData():
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected

    #Holds data recieved from server
    data = None

    #Make sure we are connected before attempting to recieve any data
    if isConnected == True:
        #Attempt to read data
        try:
            #Get data
            data = Client_Socket.recv(4096)

            #TODO: Add decryption of data here
            data = Crypto.Data.Decrypt(data)

        except:
            #Since there was an issue reading data, set data to "None"
            data = None

    #Return whatever data we were able to read
    return data

#Handles Connection Data while connected to game server
def Connection_Loop():
    global SERVER_IP
    global SERVER_PORT
    global Client_Socket
    global isConnected
    global OTHER_PLAYERS

    #Send data before entering connection loop
    #Send the server our starting animation frame
    #Networking.Client.SendData(Player.MainPlayer.Current_Frame)
    #time.sleep(0.02) #Prevent server flood

    #Connection Loop (Only loop while we are connected)
    while isConnected == True:
        #Attempt to read data, catching any issues
        try:
            #Read data from server
            data = Networking.Client.ReadData()

            #Strip character we don't need
            data = str(data.strip())

            #Server Ping?
            if data == "PING?":
                #Pong!
                Networking.Client.SendData("PONG!")

            #New Client Connection
            elif data[0:8] == "new_conn":
                #Get information for new connection
                tmpData = str(data)
                Data = []
                while len(tmpData) > 1:
                    Sep_Loc = tmpData.find(":")

                    TmpData = tmpData[0:Sep_Loc]
                    Data.append(TmpData[0:Sep_Loc])

                    tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                #Data should be formatted as follows
                #[0] - new_conn ; [1] name ; [2] sheet ; [3] map [4] x ; [5] y ; [6] frame
                OTHER_PLAYERS[str(Data[1])] = OtherPlayer(str(Data[1]), str(Data[2]),\
                str(Data[3]), int(Data[4]), int(Data[5]), int(Data[6]))
                

            #Client Update (Movement)
            elif data[0:10] == "update_plr":
                #Get information for updated client
                tmpData = str(data)
                Data = []
                while len(tmpData) > 1:
                    Sep_Loc = tmpData.find(":")

                    TmpData = tmpData[0:Sep_Loc]
                    Data.append(TmpData[0:Sep_Loc])

                    tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                #Data should be formatted as follows
                #[0] - update_plr ; [1] name ; [2] x ; [3] y ; [4] frame
                OTHER_PLAYERS[str(Data[1])].CurrentX = int(Data[2])
                OTHER_PLAYERS[str(Data[1])].CurrentY = int(Data[3])
                OTHER_PLAYERS[str(Data[1])].Current_Frame = int(Data[4])

            #Server Client Removal
            elif data[0:6] == "rm_plr":
                #Get information for removed client
                tmpData = str(data)
                Data = []
                while len(tmpData) > 1:
                    Sep_Loc = tmpData.find(":")

                    TmpData = tmpData[0:Sep_Loc]
                    Data.append(TmpData[0:Sep_Loc])

                    tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                #Data should be formatted as follows
                #[0] - rm_plr ; [1] name

                #Remove player
                del OTHER_PLAYERS[str(Data[1])]

            elif data[0:7] == "cht_msg":
                #Get information for removed client
                tmpData = str(data)
                Data = []
                while len(tmpData) > 1:
                    Sep_Loc = tmpData.find(":")

                    TmpData = tmpData[0:Sep_Loc]
                    Data.append(TmpData[0:Sep_Loc])

                    tmpData = tmpData[Sep_Loc+1:len(tmpData)]

                #Data should be formatted as follows
                #[0] - cht_msg ; [1] name ; [2] message

                #Add message to console
                Console.Manage.Write(str("[" + Data[1] + "]:" + Data[2]), (255,255,255))
                

        except Exception, e:
            #print "[Client Connection Loop]: Exception caught: \"", str(e), "\""
            pass