import math
import Player.MainPlayer
import time
import Networking.Client
#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import os.path
import random

#PyOnline
import Camera.Manage
import Video.PyGame
import Video.FPS
import Maps.Tiled
import Console.Manage

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
Sprites = []
Max_Frame_Up = None
Min_Frame_Up = None
Max_Frame_Down = None
Min_Frame_Down = None
Max_Frame_Left = None
Min_Frame_Left = None
Max_Frame_Right = None
Min_Frame_Right = None
Current_Frame = None
XPOS = None
YPOS = None
Move_Speed = None
Moving_Right = None
Moving_Left = None
Moving_Up = None
Moving_Down = None
Can_Move_Up = None
Can_Move_Down = None
Can_Move_Left = None
Can_Move_Right = None

Player_Name = None
SpriteSheet_File = None
SpriteMap_File = None


#     ________________________
# ___/ Function Declarations  \_________________________________________________
#Init Player Stuff
def Init():
    #Setup Variables
    global Sprites
    global Max_Frame_Up
    global Min_Frame_Up
    global Max_Frame_Down
    global Min_Frame_Down
    global Max_Frame_Left
    global Min_Frame_Left
    global Max_Frame_Right
    global Min_Frame_Right
    global Current_Frame
    global XPOS
    global YPOS
    global Move_Speed
    global Moving_Right
    global Moving_Left
    global Moving_Up
    global Moving_Down
    global Can_Move_Up
    global Can_Move_Down
    global Can_Move_Left
    global Can_Move_Right
    global Player_Name
    global SpriteSheet_File
    global SpriteMap_File

    Sprite = []
    Max_Frame_Up = 0
    Min_Frame_Up = -1
    Max_Frame_Down = 0
    Min_Frame_Down = -1
    Max_Frame_Left = 0
    Min_Frame_Left = -1
    Max_Frame_Right = 0
    Min_Frame_Right = -1
    Current_Frame = 0
    #Only Set X,Y if not already set by a Spawn_Point map object
    if XPOS == None and YPOS == None:
        XPOS = 300
        YPOS = 300
    Move_Speed = 6
    Moving_Right = False
    Moving_Left = False
    Moving_Up = False
    Moving_Down = False
    Can_Move_Up = True
    Can_Move_Down = True
    Can_Move_Left = True
    Can_Move_Right = True

    #Load Sprite
    tmpSprite = None
    if os.path.exists(str(SpriteSheet_File)):
        tmpSprite = pygame.image.load(str(SpriteSheet_File))
    else:
        print "\nSprite Sheet File: \"", str(SpriteSheet_File), "\" not found!\n"

    #Make sure the Sprite Map File exists
    if os.path.exists(str(SpriteMap_File)):
        #Open sprite map and load data
        FILE = open(str(SpriteMap_File), 'r')
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
                    if Min_Frame_Down == -1:
                        Min_Frame_Down = count
                    #Update Max_Frame
                    Max_Frame_Down += 1
                if Direction == "UP":
                    #Do we need to set Min_Frame?
                    if Min_Frame_Up == -1:
                        Min_Frame_Up = count
                    #Update Max_Frame
                    Max_Frame_Up += 1

                if Direction == "LEFT":
                    #Do we need to set Min_Frame?
                    if Min_Frame_Left == -1:
                        Min_Frame_Left = count
                    #Update Max_Frame
                    Max_Frame_Left += 1
                    
                if Direction == "RIGHT":
                    #Do we need to set Min_Frame?
                    if Min_Frame_Right == -1:
                        Min_Frame_Right = count
                    #Update Max_Frame
                    Max_Frame_Right += 1

                #Append sprite from sprite sheet
                Sprites.append(tmpSprite.subsurface((int(OffX), int(OffY), int(Width), int(Height))))

                #Increase loop count
                count += 1
        #Fix Max_Fame Value
        Max_Frame_Down += Min_Frame_Down
        Max_Frame_Up += Min_Frame_Up
        Max_Frame_Left += Min_Frame_Left
        Max_Frame_Right += Min_Frame_Right

        #Take Max_Frame down one to respect the "starting from zero" system
        Max_Frame_Down -= 1
        Max_Frame_Up -= 1
        Max_Frame_Left -= 1
        Max_Frame_Right -= 1

        #Debug output -- Frame info
        #print "DOWN - MIN: ", Min_Frame_Down, " MAX: ", Max_Frame_Down
        #print "RIGHT - MIN: ", Min_Frame_Right, " MAX: ", Max_Frame_Right
        #print "LEFT - MIN: ", Min_Frame_Left, " MAX: ", Max_Frame_Left
        #print "UP - MIN: ", Min_Frame_Up, " MAX: ", Max_Frame_Up

        #Set Player_Name
        #Player_Name = "Player"

        #Append random numbers to Player_Name
        #Seed = 0
        #while Seed == 0:
        #    Seed = random.randint(0, 1000)
        #Numbers = 0
        #while Numbers == 0:
        #    Numbers = random.randrange(0,1000, int(Seed))

        #Player_Name = str(str(Player_Name) + str(Numbers))

        #Send current frame to server
        Networking.Client.SendData(Current_Frame)

        Console.Manage.Write(str("You are now playing as: " + str(Player_Name)), (255,255,0))

    else:
        print "\nSprite Map File: \"", str(SpriteMap_File), "\" not found!\n"
                
        
def Render():
    #Setup Variables
    global Sprites
    global Max_Frame_Up
    global Min_Frame_Up
    global Max_Frame_Down
    global Min_Frame_Down
    global Max_Frame_Left
    global Min_Frame_Left
    global Max_Frame_Right
    global Min_Frame_Right
    global Current_Frame
    global XPOS
    global YPOS
    global Move_Speed
    global Moving_Right
    global Moving_Left
    global Moving_Up
    global Moving_Down

    Video.PyGame.Screen.blit(Sprites[Current_Frame], (XPOS - Camera.Manage.CamX, YPOS - Camera.Manage.CamY))

#Handles Animation Frames
def Animation_Thread():
    #Setup Variables
    global Sprites
    global Max_Frame_Up
    global Min_Frame_Up
    global Max_Frame_Down
    global Min_Frame_Down
    global Max_Frame_Left
    global Min_Frame_Left
    global Max_Frame_Right
    global Min_Frame_Right
    global Current_Frame
    global XPOS
    global YPOS
    global Move_Speed
    global Moving_Right
    global Moving_Left
    global Moving_Up
    global Moving_Down

    while True:
        #Moving Right
        if Moving_Right == True:
            #Keep within Frames Min_Frame-Max_Frame
            if Current_Frame >= Min_Frame_Right and Current_Frame < Max_Frame_Right:
                Current_Frame += 1
            elif Current_Frame > Max_Frame_Right:
                Current_Frame -= 1
            else:
                Current_Frame = Min_Frame_Right

        #Moving Left
        if Moving_Left == True:
            #Keep within Frames Min_Frame-Max_Frame
            if Current_Frame >= Min_Frame_Left and Current_Frame < Max_Frame_Left:
                Current_Frame += 1
            elif Current_Frame > Max_Frame_Left:
                Current_Frame -= 1
            else:
                Current_Frame = Min_Frame_Left

        #Moving Down
        if Moving_Down == True:
            #Keep within Frames Min_Frame-Max_Frame
            if Current_Frame >= Min_Frame_Down and Current_Frame < Max_Frame_Down:
                Current_Frame += 1
            elif Current_Frame > Max_Frame_Down:
                Current_Frame -= 1
            else:
                Current_Frame = Min_Frame_Down

        #Moving Up
        if Moving_Up == True:
            #Keep within Frames Min_Frame-Max_Frame
            if Current_Frame >= Min_Frame_Up and Current_Frame < Max_Frame_Up:
                Current_Frame += 1
            elif Current_Frame > Max_Frame_Up:
                Current_Frame -= 1
            else:
                Current_Frame = Min_Frame_Up

        #Keep FPS Regulated
        Video.FPS.Tick()
        Video.FPS.Tick()

#Handles Player Animation, without threading
def Animate():
    #Setup Variables
    global Sprites
    global Max_Frame_Up
    global Min_Frame_Up
    global Max_Frame_Down
    global Min_Frame_Down
    global Max_Frame_Left
    global Min_Frame_Left
    global Max_Frame_Right
    global Min_Frame_Right
    global Current_Frame
    global XPOS
    global YPOS
    global Move_Speed
    global Moving_Right
    global Moving_Left
    global Moving_Up
    global Moving_Down

    #Moving Right
    if Moving_Right == True:
        #Keep within Frames Min_Frame-Max_Frame
        if Current_Frame >= Min_Frame_Right and Current_Frame < Max_Frame_Right:
            Current_Frame += 1
        elif Current_Frame > Max_Frame_Right:
            Current_Frame -= 1
        else:
            Current_Frame = Min_Frame_Right

    #Moving Left
    if Moving_Left == True:
        #Keep within Frames Min_Frame-Max_Frame
        if Current_Frame >= Min_Frame_Left and Current_Frame < Max_Frame_Left:
            Current_Frame += 1
        elif Current_Frame > Max_Frame_Left:
            Current_Frame -= 1
        else:
            Current_Frame = Min_Frame_Left

    #Moving Down
    if Moving_Down == True:
        #Keep within Frames Min_Frame-Max_Frame
        if Current_Frame >= Min_Frame_Down and Current_Frame < Max_Frame_Down:
            Current_Frame += 1
        elif Current_Frame > Max_Frame_Down:
            Current_Frame -= 1
        else:
            Current_Frame = Min_Frame_Down

    #Moving Up
    if Moving_Up == True:
        #Keep within Frames Min_Frame-Max_Frame
        if Current_Frame >= Min_Frame_Up and Current_Frame < Max_Frame_Up:
            Current_Frame += 1
        elif Current_Frame > Max_Frame_Up:
            Current_Frame -= 1
        else:
            Current_Frame = Min_Frame_Up


#Sends out movement update when player x,y changes (Threaded)
def Movement_Monitor_Thread():
    global Sprites
    global Max_Frame_Up
    global Min_Frame_Up
    global Max_Frame_Down
    global Min_Frame_Down
    global Max_Frame_Left
    global Min_Frame_Left
    global Max_Frame_Right
    global Min_Frame_Right
    global Current_Frame
    global XPOS
    global YPOS
    global Move_Speed
    global Moving_Right
    global Moving_Left
    global Moving_Up
    global Moving_Down

    tmpX = XPOS
    tmpY = YPOS
    count = 0
    while True:
        #Check for possible speed hacks
        #NOTE: THIS HAS NOT BEEN TESTED, JUST A THEORY
        #NOTE: Client side implementation of anti-hack system may not be the best idea
        #      could possibly be edited / disabled - Use server side check as well!
        Sensitivity = 2
        MSpeed = Player.MainPlayer.Move_Speed * int(Sensitivity)
        #Positive X Direction
        if math.fabs(int(XPOS)) > math.fabs(int(int(tmpX) + int(MSpeed))):
            #If the last recorded xpos is greater than that of the max next possible xpos, then speed hack should be inplace locally
            #The max next possible xpos would be the last reorded xpos, plus the player movementspeed
            # Example: Current X = 50, Movespeed = 5 -- The next time the player moves in the positive direction, the xpos SHOULD be 55
            Console.Manage.Write("[POSSIBLE SPEED HACK DETECTED]", (255, 153, 255))

        #Negitive X Direction
        elif math.fabs(int(XPOS)) < math.fabs(int(int(tmpX) - int(MSpeed))):
            Console.Manage.Write("[POSSIBLE SPEED HACK DETECTED]", (255, 153, 255))

        #Positive Y Direction
        if math.fabs(int(YPOS)) > math.fabs(int(int(tmpY) + int(MSpeed))):
            Console.Manage.Write("[POSSIBLE SPEED HACK DETECTED]", (255, 153, 255))

        #Negitive Y Direction
        elif math.fabs(int(YPOS)) < math.fabs(int(int(tmpY) - int(MSpeed))):
            Console.Manage.Write("[POSSIBLE SPEED HACK DETECTED]", (255, 153, 255))
                
        #Check if we are connected to server
        if Networking.Client.isConnected:
            #Check for change
            if tmpX != XPOS or tmpY != YPOS or count == 0:
                #Send out movement update and update local variables
                Networking.Client.SendData(str("mov_plr:" + str(XPOS)+ ":" + str(YPOS) + ":") + str(Current_Frame) + ":")
                tmpX = XPOS
                tmpY = YPOS

            #Update Count
            count += 1

            #Prevent server flood
            Video.FPS.Tick()
        else:
            #Delay server online checking just a tad
            time.sleep(0.2)