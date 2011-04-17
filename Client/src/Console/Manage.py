import Networking.Client
import Objects.Zone
#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Video
import Video.PyGame
import Video.FPS
import Video.Rendering
import Events.Handle
import Maps.Tiled
import Camera.Manage
import Player.MainPlayer
import Dialog.Popup
import Dialog.Global

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
Console_Surface = None
Console_Background_Surface = None
Console_Data_Surfaces = []
Console_Input_Prompt_Surface = None
Console_Input_Text = None
Console_Input_Text_Surface = []
Console_Font = None

Console_XPOS = None
Console_YPOS = None
Console_Focused = None


#     ________________________
# ___/ Function Declarations  \_________________________________________________
def Init():
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Input_Prompt_Surface
    global Console_Input_Text
    global Console_Input_Text_Surface
    global Console_Font
    global Console_XPOS
    global Console_YPOS
    global Console_Focused

    Console_Data_Surfaces = []

    Console_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 10)
    
    #Load Console Background Surface
    Console_Background_Surface = pygame.image.load("data/images/Console_Background.png")

    Console_Surface = pygame.Surface((Console_Background_Surface.get_width(), Console_Background_Surface.get_height()), SRCALPHA)

    Console_Input_Prompt_Surface = Console_Font.render(">", False, (255,255,255))
    Console_Input_Text = ""
    Console_Input_Text_Surface = []

    Console_XPOS = Video.PyGame.Screen_Width - Console_Background_Surface.get_width()
    Console_YPOS = Video.PyGame.Screen_Height - Console_Background_Surface.get_height()
    Console_Focused = False

#Updates Console Surfaces With Current Data
def Update():
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Input_Prompt_Surface
    global Console_Input_Text
    global Console_Input_Text_Surface
    global Console_Font
    global Console_XPOS
    global Console_YPOS
    global Console_Focused

    #Make sure the game window is focused
    if pygame.mouse.get_focused() == True:
        #Get mouse x,y
        x, y = pygame.mouse.get_pos()

        #Get mouse buttons
        b1, b2, b3 = pygame.mouse.get_pressed()

        #Mouse Click (Button1)
        if b1 == True:
            #Check X,Y
            if x >= Console_XPOS and y >= Console_YPOS:
                #Focus Console for event input
                Console_Focused = True
                #Change key input speed(good speed for typing)
                pygame.key.set_repeat(200,200)
            else:
                #UnFocus / Keep Unfocued
                Console_Focused = False
                #Change key input speed(default for player movement)
                pygame.key.set_repeat(1,1)

    #Clear Console_Surface
    Console_Surface.fill((0,0,0, 150))

    Console_Input_Text_Surface = []

    #Reverse Console_Data_Surfaces
    #tmp = Console_Data_Surfaces
    #tmp.reverse()
    tmp = []

    for i in range(len(Console_Data_Surfaces), 0, -1):
        tmp.append(Console_Data_Surfaces[i-1])
    
    #Loop through recent Console Data
    for i in range(0, len(tmp)):
        #Only render recent 13 elements
        if i < 13:
            #Render so most recent element is lowest, while older elements are higher
            Console_Surface.blit(tmp[i], (0, (Console_Background_Surface.get_height()-28)-(i * 14)))
        else:
            #Render nothing else, break from loop
            break

    #Render Console Input Prompt
    Console_Surface.blit(Console_Input_Prompt_Surface, (0, Console_Background_Surface.get_height()-14))

    #Render Input Data To Memory
    char_index = 0
    for char in Console_Input_Text:
        #25 chars only
        if char_index < 36:
            InputWrite(char, (255,255,255))
        char_index += 1

    #Check if there is any console input data to render
    if len(Console_Input_Text_Surface) > 0:
        for i in range(0, len(Console_Input_Text_Surface)):
            Console_Surface.blit(Console_Input_Text_Surface[i], (14+(i*6), Console_Background_Surface.get_height()-14))

#Renders Console
def Render():
    global Console_Surface
    global Console_XPOS
    global Console_YPOS

    #Update Console XPOS, YPOS -- To be safe (Incase fullscreen or resize of screen)
    Console_XPOS = Video.PyGame.Screen_Width - Console_Background_Surface.get_width()
    Console_YPOS = Video.PyGame.Screen_Height - Console_Background_Surface.get_height()
    
    Video.PyGame.Screen.blit(Console_Surface, (Console_XPOS, Console_YPOS))


#Adds Line of Text
def Write(string, color):
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Font

    #Surface array for each charater in "string"
    Char_Surface = []

    #Create a surface for each character
    for i in range(0, len(string)):
        Char_Surface.append(Console_Font.render(str(string[i]), False, color))

    #Render Message To Console Accordingly
    count = 0
    tmpSurface = pygame.Surface((Console_Background_Surface.get_width(), 14), SRCALPHA)

    #Go through each character
    for i in range(0, len(Char_Surface)):
        #39 char per line max
        if count <= 39:
            #Blit Surface Character
            tmpSurface.blit(Char_Surface[i], (count*6,0))

            #Increase count
            count += 1
        else:
            #Blit Surface Character
            tmpSurface.blit(Char_Surface[i], (count*6,0))
            
            #Create new Data element
            Console_Data_Surfaces.append(tmpSurface)

            #Reset char count
            count = 0

            #Reset tmpSurface
            tmpSurface = pygame.Surface((Console_Background_Surface.get_width(), 14), SRCALPHA)
            
    #Create new Data element
    Console_Data_Surfaces.append(tmpSurface)

#Adds Line of Text (Chat Message)
def ChatMessage(string, color):
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Font

    #Create new string with message data, and player name data
    tmpStr = str("[" + str(Player.MainPlayer.Player_Name) + "]:" + str(string))

    #Surface array for each charater in "string"
    Char_Surface = []

    #Create a surface for each character
    for i in range(0, len(tmpStr)):
        Char_Surface.append(Console_Font.render(str(tmpStr[i]), False, color))

    #Render Message To Console Accordingly
    count = 0
    tmpSurface = pygame.Surface((Console_Background_Surface.get_width(), 14), SRCALPHA)

    #Go through each character
    for i in range(0, len(Char_Surface)):
        #36 char per line max
        if count <= 36:
            #Blit Surface Character
            tmpSurface.blit(Char_Surface[i], (count*6,0))

            #Increase count
            count += 1
        else:
            #Blit Surface Character
            tmpSurface.blit(Char_Surface[i], (count*6,0))

            #Create new Data element
            Console_Data_Surfaces.append(tmpSurface)

            #Reset char count
            count = 0

            #Reset tmpSurface
            tmpSurface = pygame.Surface((Console_Background_Surface.get_width(), 14), SRCALPHA)

    #Create new Data element
    Console_Data_Surfaces.append(tmpSurface)

    #Send to server
    Networking.Client.SendData(str("cht_msg:" + str(string)) + ":")

#Writes Text To Console Input Area
def InputWrite(char, color):
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Font
    global Console_Input_Text_Surface

    Console_Input_Text_Surface.append(pygame.Surface((Console_Background_Surface.get_width(), 14), SRCALPHA))
    Console_Input_Text_Surface[len(Console_Input_Text_Surface)-1] = Console_Font.render(str(char), False, color)


#Handles Input To Console
def InputHandle():
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Input_Prompt_Surface
    global Console_Input_Text
    global Console_Input_Text_Surface
    global Console_Font
    global Console_XPOS
    global Console_YPOS
    global Console_Focused

    #Set Local Variables
    Input = Console_Input_Text

    #Reset Other Variables
    Console_Input_Text = ""
    Console_Input_Text_Surface = []

    #Was the input a slash command?
    if Input[0:1] == "/":
        #Extract command data
        Command_Data = Input[1:len(Input)]

        #Extract command and parameter(s)
        SpaceLoc = Command_Data.find(" ")
        Command = Command_Data[0:SpaceLoc]
        Parameters = Command_Data[SpaceLoc+1:len(Command_Data)]

        #Write(str("COMMAND: " + Command + " PARA: " + Parameters), (0,255,0))

        #Commands
        if Command == "get":
            if Parameters == "zone":
                Write(str(Objects.Zone.Last_Triggered_Zone_Name),(130,250,123))
            elif Parameters == "cords":
                Write(str("Your current cords: " + str(Player.MainPlayer.XPOS) + "," + str(Player.MainPlayer.YPOS)), (250,130,128))
            elif Parameters == "name":
                Write(str("Current Player Name: " + str(Player.MainPlayer.Player_Name)), (255,0,0))
            else:
                Write("zone - Gets current zone info", (255,134,0))
                Write("cords - Gets current player (x,y)", (255,134,0))
                Write("name - Gets local player name", (255,134,0))
    else:
        #Echo back to the console
        ChatMessage(str(Input), (61,255,255))


#Handles Events when console is focued
def EventHandle(event):
    global Console_Surface
    global Console_Background_Surface
    global Console_Data_Surfaces
    global Console_Input_Prompt_Surface
    global Console_Input_Text
    global Console_Input_Text_Surface
    global Console_Font
    global Console_XPOS
    global Console_YPOS
    global Console_Focused
    
    #Keydown Events
    if event.type == KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            Console_Input_Text = Console_Input_Text[0:len(Console_Input_Text)-1]
        elif event.key == pygame.K_RETURN:
            InputHandle()
        elif int(event.key) > -1 and int(event.key) < 256:
            Console_Input_Text += chr(event.key)
