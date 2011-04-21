#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import sys
import os.path
import gc
import thread
import md5

#Simple PyGame GUI
import SPG.gui
import SPG.defaultStyle

#PyOnline
import Video
import Video.PyGame
import Video.FPS
import Video.Rendering
import Events.Handle
import Maps.Tiled
import Collision.Manage
import Camera.Manage
import Player.MainPlayer
import Dialog.Popup
import Dialog.Global
import Objects.Zone
import Console.Manage
import Networking.Client
import Maps.Tiled
import NPC.Manage
import Game

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
Username_Input = "" #Keeps track of what is entered into the Username textbox
Password_Input = "" #Keeps track of what is entered into the Password textbox

#Controls rather or not the Login window should still be running
RUN_LOGIN_WINDOW = True

#SPG Desktop for gui widgets
Desktop = None

#Status label for the login window
StatusLbl = None

#Background for Login Window
Background = None

#     _______________________
# ___/ Function Declarations \__________________________________________________
#Loads the Login screen for authentication
def Run():
    global Username_Input
    global Password_Input
    global RUN_LOGIN_WINDOW
    global Desktop
    global StatusLbl
    global Background

    #Enable Python GC
    gc.enable()

    #Init Video
    Video.PyGame.InitVideo()

    #Setup Video
    Video.PyGame.SetVideo(800, 640, False)

    #Init FPS System
    Video.FPS.Init()

    #Update Window Caption To Current Ver
    pygame.display.set_caption(str("PyOnline - " + str(Networking.Client.CLIENT_VER)))
    
    #Load Background
    if os.path.exists("data/images/Login_Background.png"):
        Background = pygame.image.load("data/images/Login_Background.png")

    #Setup SPG(Simple Pygame GUI)
    Desktop = SPG.gui.Desktop()
    SPG.defaultStyle.init(SPG.gui)

    #Setup Login Window Elements
    LoginWin_Caption = str("PyOnline Login - Ver: " + str(Networking.Client.CLIENT_VER))
    LoginWin = SPG.gui.Window(position = (100, 100), size = (300,200), text = LoginWin_Caption, closeable = False, parent = Desktop)
    UsernameLbl = SPG.gui.Label(position = (24,58), text = "Username:", parent = LoginWin)
    UsernameTxt = SPG.gui.TextBox(position = (100, 56), parent = LoginWin)
    PasswordLbl = SPG.gui.Label(position = (24,88), text = "Password:", parent = LoginWin)
    PasswordTxt = SPG.gui.TextBox(position = (100, 86), parent = LoginWin)
    LoginBtn = SPG.gui.Button(position = (100, 130), text = "Login!", parent = LoginWin)
    StatusLbl = SPG.gui.Label(position = (100,150), text = " ", parent = LoginWin)

    #Setup Login Button Events
    LoginBtn.onClick = LoginBtn_OnClick

    #Keeps track of the length of text in the textboxes
    Username_TextLen = 0
    Password_TextLen = 0

    #Login Loop
    while RUN_LOGIN_WINDOW == True:
        #Clear Screen
        Video.PyGame.Screen.fill((0,0,0))

        #Update Desktop for SPG
        Desktop.update()

        #Event Handling
        if RUN_LOGIN_WINDOW == True:
            for event in SPG.gui.setEvents():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        #Disconnect from game server
                        if Networking.Client.isConnected:
                            Networking.Client.DisConnect()
                            
                        #Stop PyGame
                        pygame.quit()

                        #Exit Completly
                        sys.exit(0)
                        
                    if event.key == K_BACKSLASH:
                        #Toggle Fullscreen
                        if Video.PyGame.Screen_Fullscreen == False:
                            Video.PyGame.SetVideo(800, 640, True)
                        else:
                            Video.PyGame.SetVideo(800, 640, False)

        #Check for Changed Text In Username Text Box
        if Username_TextLen != len(UsernameTxt.text):
            #Handle any changes to text
            UsernameHandle(UsernameTxt)
            Username_TextLen = len(UsernameTxt.text)

        #Check for Changed Text In Password Text Box
        if Password_TextLen < len(PasswordTxt.text):
            #If new text is added, handle it
            PasswordHandle(PasswordTxt)
            Password_TextLen = len(PasswordTxt.text)

        elif Password_TextLen > len(PasswordTxt.text):
            #If text is removed, update Password_Input
            Password_Input = Password_Input[0:len(Password_Input)-1]
            Password_TextLen = len(PasswordTxt.text)
            
        #Render Background
        if Background != None: #Make sure background image was loaded
            Video.PyGame.Screen.blit(Background, (0,0))

        #Render Desktop for SPG
        Desktop.draw()

        #Update Display
        pygame.display.flip()

        #FPS Regulation
        Video.FPS.Tick()

        #Python Garbage Collection
        gc.collect()

    #Reset all SPG elements
    LoginWin_Caption = None
    LoginWin = None
    UsernameLbl = None
    UsernameTxt = None
    PasswordLbl = None
    PasswordTxt = None
    LoginBtn =  None

    #Update SPG Desktop
    Desktop.update()
    Desktop.draw()
    Desktop = None

#Handles input into the Username Text Box
def UsernameHandle(widget):
    global Username_Input

    #Keep track of username input in textbox
    Username_Input = widget.text

#Handles input into the Password Text Box
def PasswordHandle(widget):
    global Password_Input

    #Get the last char the user typed (most recent one)
    LastChar = widget.text[len(widget.text)-1]

    #Get full password, unmasked
    Text = str(str(Password_Input) + str(LastChar))

    #Save the currently typed password, unmasked
    Password_Input = Text

    #Remask the password text
    PasswordMask(widget)


#Masks out the text in the password feild
def PasswordMask(widget):
    Mask = ""

    #Generate '*' for each character in the text box
    for i in range(0, len(widget.text)):
        Mask += "*"

    widget.text = str(Mask)

#Called with the LoginBtn is Clicked
def LoginBtn_OnClick(widget):
    global Username_Input
    global Password_Input
    global RUN_LOGIN_WINDOW
    global Desktop
    global StatusLbl

    #Only Continue If Text Boxs Have Data
    if len(Username_Input) > 0 and len(Password_Input) > 0:
        #Set Username and Password for client
        Networking.Client.USERNAME = Username_Input
        #Networking.Client.PASSWORD = Password_Input
        Networking.Client.PASSWORD = str(md5.md5(Password_Input).hexdigest()) #MD5 the password

        #Attempt to Connect
        if Networking.Client.Init() == True:
            #Update Status
            StatusLbl.text = "Attempting to Login..."
            Desktop.update()
            Desktop.draw()
            pygame.display.flip()

            Networking.Client.Connect()

        else:
           print "Check the data/Server.conf file, does not exist?"
           StatusLbl.text = "Could not find Server.conf!"
           Desktop.update()
           Desktop.draw()
           pygame.display.flip()

        #Check if we are connected
        if Networking.Client.isConnected == True:
            #Update Status
            StatusLbl.text = "Loading Game..."
            Desktop.update()
            Desktop.draw()
            pygame.display.flip()

            #Stop the Login Window Process
            RUN_LOGIN_WINDOW = False

            #Double check that we are connected before starting the game
            if Networking.Client.isConnected == True:
                #Run Game
                Game.Run()

        else:
            Networking.Client.USERNAME = None
            Networking.Client.PASSWORD = None
            Desktop.update()
            Desktop.draw()
            pygame.display.flip()
    else:
        StatusLbl.text = "Enter a Username/Password!"
        Desktop.update()
        Desktop.draw()
        pygame.display.flip()